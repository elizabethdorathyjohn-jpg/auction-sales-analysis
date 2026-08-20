from pathlib import Path

import pandas as pd


# --------------------------------------------------
# 1. FILE PATHS
# --------------------------------------------------

input_path = Path("../data/raw/auction_data.csv")
output_path = Path("../data/cleaned/auction_cleaned_anonymised.csv")
category_summary_path = Path("../data/cleaned/category_summary.csv")


# --------------------------------------------------
# 2. LOAD THE DATASET
# --------------------------------------------------

df = pd.read_csv(input_path)

print("Original dataset shape:", df.shape)


# --------------------------------------------------
# 3. STANDARDISE COLUMN NAMES
# --------------------------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace("%", "pct", regex=False)
    .str.replace(r"\s+", "_", regex=True)
)

print("\nCleaned column names:")
print(df.columns.tolist())


# --------------------------------------------------
# 4. REMOVE THE EMPTY EXPORTED COLUMN
# --------------------------------------------------

df = df.drop(columns=["unnamed:_17"], errors="ignore")


# --------------------------------------------------
# 5. CLEAN TEXT COLUMNS
# --------------------------------------------------

text_cols = df.select_dtypes(include=["object", "string"]).columns

for col in text_cols:
    df[col] = df[col].apply(
        lambda value: value.strip()
        if isinstance(value, str)
        else value
    )

df[text_cols] = df[text_cols].replace(r"^\s*$", pd.NA, regex=True)


# --------------------------------------------------
# 6. CHECK DATA QUALITY
# --------------------------------------------------

print("\nMissing values before cleaning:")
print(df.isna().sum())

duplicate_count = df.duplicated().sum()

print("\nNumber of exact duplicate rows:")
print(duplicate_count)


# --------------------------------------------------
# 7. REMOVE EXACT DUPLICATES
# --------------------------------------------------

df = df.drop_duplicates().reset_index(drop=True)

print("\nDataset shape after removing duplicates:", df.shape)


# --------------------------------------------------
# 8. CHECK IMPORTANT NUMERIC COLUMNS
# --------------------------------------------------

numeric_columns = [
    "reserve",
    "estimate_minimum",
    "estimate_maximum",
    "hammer_price",
    "buyers_premium_pct",
    "vendors_commission_pct",
    "vendors_commission_vat_pct",
    "buyers_premium_vat_pct",
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")


# --------------------------------------------------
# 9. CREATE SOLD STATUS
# --------------------------------------------------

df["sold"] = df["hammer_price"].fillna(0) > 0

df["sale_status"] = df["sold"].map(
    {
        True: "Sold",
        False: "Not Sold",
    }
)


# --------------------------------------------------
# 10. CREATE PRICE-PERFORMANCE CATEGORY
# --------------------------------------------------

def price_performance(row):
    if not row["sold"]:
        return "Not Sold"

    if (
        pd.isna(row["estimate_minimum"])
        or pd.isna(row["estimate_maximum"])
    ):
        return "Estimate Unavailable"

    if row["hammer_price"] < row["estimate_minimum"]:
        return "Below Estimate"

    if row["hammer_price"] > row["estimate_maximum"]:
        return "Above Estimate"

    return "Within Estimate"


df["price_performance"] = df.apply(
    price_performance,
    axis=1,
)


# --------------------------------------------------
# 11. CHECK WHETHER LOTS SOLD BELOW RESERVE
# --------------------------------------------------

df["sold_below_reserve"] = (
    df["sold"]
    & df["reserve"].notna()
    & (df["hammer_price"] < df["reserve"])
)


# --------------------------------------------------
# 12. CALCULATE BUYER PREMIUM REVENUE
# --------------------------------------------------

df["buyer_premium_revenue"] = 0.0

sold_mask = df["sold"]

df.loc[sold_mask, "buyer_premium_revenue"] = (
    df.loc[sold_mask, "hammer_price"]
    * df.loc[sold_mask, "buyers_premium_pct"].fillna(0)
    / 100
)


# --------------------------------------------------
# 13. CALCULATE BUYER PREMIUM VAT
# --------------------------------------------------

df["buyer_premium_vat"] = 0.0

if "buyers_premium_vat_pct" in df.columns:
    df.loc[sold_mask, "buyer_premium_vat"] = (
        df.loc[sold_mask, "buyer_premium_revenue"]
        * df.loc[sold_mask, "buyers_premium_vat_pct"].fillna(0)
        / 100
    )


# --------------------------------------------------
# 14. CALCULATE VENDOR COMMISSION
# --------------------------------------------------

df["vendor_commission_revenue"] = 0.0

if "vendors_commission_pct" in df.columns:
    df.loc[sold_mask, "vendor_commission_revenue"] = (
        df.loc[sold_mask, "hammer_price"]
        * df.loc[sold_mask, "vendors_commission_pct"].fillna(0)
        / 100
    )


# --------------------------------------------------
# 15. CALCULATE COMMISSION VAT
# --------------------------------------------------

df["vendor_commission_vat"] = 0.0

if "vendors_commission_vat_pct" in df.columns:
    df.loc[sold_mask, "vendor_commission_vat"] = (
        df.loc[sold_mask, "vendor_commission_revenue"]
        * df.loc[sold_mask, "vendors_commission_vat_pct"].fillna(0)
        / 100
    )


# --------------------------------------------------
# 16. CREATE CATEGORY SUMMARY
# --------------------------------------------------

category_summary = (
    df.groupby(
        "category_descriptions",
        dropna=False,
    )
    .agg(
        total_lots=("lotno", "count"),
        sold_lots=("sold", "sum"),
        total_hammer_revenue=("hammer_price", "sum"),
        average_hammer_price=("hammer_price", "mean"),
        median_hammer_price=("hammer_price", "median"),
        buyer_premium_revenue=(
            "buyer_premium_revenue",
            "sum",
        ),
        vendor_commission_revenue=(
            "vendor_commission_revenue",
            "sum",
        ),
        lots_below_reserve=(
            "sold_below_reserve",
            "sum",
        ),
    )
    .reset_index()
)


category_summary["sales_rate_pct"] = (
    category_summary["sold_lots"]
    / category_summary["total_lots"]
    * 100
)


category_summary[
    [
        "total_hammer_revenue",
        "average_hammer_price",
        "median_hammer_price",
        "buyer_premium_revenue",
        "vendor_commission_revenue",
        "sales_rate_pct",
    ]
] = category_summary[
    [
        "total_hammer_revenue",
        "average_hammer_price",
        "median_hammer_price",
        "buyer_premium_revenue",
        "vendor_commission_revenue",
        "sales_rate_pct",
    ]
].round(2)


category_summary = category_summary.sort_values(
    by="total_hammer_revenue",
    ascending=False,
).reset_index(drop=True)


# --------------------------------------------------
# 17. CREATE ANONYMISED VENDOR IDs
# --------------------------------------------------

vendor_values = (
    df["vendor_no"]
    .dropna()
    .astype(str)
    .unique()
)

unique_vendors = sorted(vendor_values)

vendor_map = {
    vendor: f"V{i + 1:03d}"
    for i, vendor in enumerate(unique_vendors)
}

df["vendor_id"] = (
    df["vendor_no"]
    .astype("string")
    .map(vendor_map)
)


# --------------------------------------------------
# 18. CREATE GENERIC LOT IDs
# --------------------------------------------------

df["public_lot_id"] = [
    f"L{i + 1:04d}"
    for i in range(len(df))
]


# --------------------------------------------------
# 19. CREATE THE PUBLIC ANONYMISED DATASET
# --------------------------------------------------

sensitive_columns = [
    "buyer_name",
    "vendor_name",
    "buyer_paddle",
    "vendor_no",
    "description",
    "lotno",
]

anonymised = df.drop(
    columns=sensitive_columns,
    errors="ignore",
).copy()


# --------------------------------------------------
# 20. SAVE THE CLEANED FILES
# --------------------------------------------------

output_path.parent.mkdir(
    parents=True,
    exist_ok=True,
)

category_summary_path.parent.mkdir(
    parents=True,
    exist_ok=True,
)

anonymised.to_csv(
    output_path,
    index=False,
)

category_summary.to_csv(
    category_summary_path,
    index=False,
)


# --------------------------------------------------
# 21. DISPLAY FINAL CHECKS
# --------------------------------------------------

print("\nFinal private dataset shape:")
print(df.shape)

print("\nFinal anonymised dataset shape:")
print(anonymised.shape)

print("\nSale status counts:")
print(df["sale_status"].value_counts(dropna=False))

print("\nPrice-performance counts:")
print(df["price_performance"].value_counts(dropna=False))

print("\nNumber of lots sold below reserve:")
print(df["sold_below_reserve"].sum())

print("\nCategory summary preview:")
print(category_summary.head(10))

print("\nFiles saved successfully:")
print(f"Anonymised dataset: {output_path}")
print(f"Category summary: {category_summary_path}")
