# Power BI Dashboard - Build Notes

Built from `data/cleaned/auction_cleaned_anonymised.csv`. No buyer names, vendor names, paddle numbers, or raw vendor numbers loaded — only the anonymised `vendor_id`.

## DAX measures

```dax
Total Lots = COUNTROWS(auction_cleaned_anonymised)

Sold Lots = CALCULATE([Total Lots], auction_cleaned_anonymised[sold] = TRUE)

Unsold Lots = [Total Lots] - [Sold Lots]

Sales Rate % = DIVIDE([Sold Lots], [Total Lots])

Total Hammer Revenue =
    CALCULATE(
        SUM(auction_cleaned_anonymised[hammer_price]),
        auction_cleaned_anonymised[sold] = TRUE
    )

Average Hammer Price =
    CALCULATE(
        AVERAGE(auction_cleaned_anonymised[hammer_price]),
        auction_cleaned_anonymised[sold] = TRUE
    )

Lots Above Estimate =
    CALCULATE(
        [Total Lots],
        auction_cleaned_anonymised[price_performance] = "Above Estimate"
    )

Lots Below Reserve =
    CALCULATE(
        [Total Lots],
        auction_cleaned_anonymised[sold_below_reserve] = TRUE
    )

Total Buyer Premium Revenue = SUM(auction_cleaned_anonymised[buyer_premium_revenue])

Total Vendor Commission Revenue = SUM(auction_cleaned_anonymised[vendor_commission_revenue])
```

**Note:** `Total Buyer Premium Revenue` and `Total Vendor Commission Revenue` can return blank (not 0) for a vendor/category with zero sold lots, since DAX's `SUM()` returns `BLANK` over an empty filtered set. Wrap in `COALESCE(..., 0)` if a consistent 0 display is preferred.

## Page 1 - Auction Overview

- KPI cards: Total Lots, Sold Lots, Unsold Lots, Sales Rate %
- Donut chart: `sale_status` on Legend, `Total Lots` on Values
- Bar chart: `category_descriptions` (Y-axis) vs `Total Lots` (X-axis), sorted descending, Top N filtered by `Total Lots`
- Slicer: `category_descriptions`

## Page 2 - Category Performance

- Bar chart: Sales Rate % by category, filtered to `Total Lots >= 5` to exclude small-sample distortion
- Bar chart: Total Hammer Revenue by category
- Table: category, total lots, sold lots, sales rate %, total hammer revenue, average hammer price
- Slicer: `category_descriptions`

## Page 3 - Pricing and Estimate Analysis

- Scatter chart: `estimate_minimum` (X) vs `hammer_price` (Y), `public_lot_id` in Legend (required to plot one dot per lot rather than a single summed point), page-level filter `sale_status = Sold`
- Stacked bar: `category_descriptions` by `price_performance`, filtered to sold lots
- KPI cards: Lots Above Estimate, Lots Below Reserve
- Slicers: `category_descriptions`, `price_performance`

## Page 4 - Vendor Performance

- Table: `vendor_id`, Total Lots, Sold Lots, Sales Rate %, Total Hammer Revenue — filtered to `Total Lots >= 5`
- Bar chart: Top vendors by Total Hammer Revenue, same filter applied
- KPI cards: Total Buyer Premium Revenue, Total Vendor Commission Revenue
- Slicer: `vendor_id`

**Note:** because this page filters to vendors with ≥5 lots, its totals (1,206 lots / 159 sold / £50,375) are smaller than the full dataset's 1,264 / 173 / £50,810 — by design, not an error.

## Known issues encountered and fixed during build

- Scatter chart initially aggregated all rows into a single summed point — fixed by adding `public_lot_id` to the Legend/Details field, which gives Power BI something unique per row to plot separately
- A page-level `sale_status` filter was reset twice during rebuilds of the scatter visual  moved the filter to page level (rather than visual level) for durability
- Table "Top N" filter was initially ranking by an unrelated field rather than `Total Lots`, silently excluding the largest category (Jewellery) from a "top 10" chart  always verify a Top N filter's "By value" field explicitly
