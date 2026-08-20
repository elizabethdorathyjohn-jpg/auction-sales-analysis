# Auction Sales Performance and Pricing Analysis

A beginner-to-intermediate data analytics portfolio project using a real dataset of 1,264 auction lots, covering Python/pandas data cleaning, SQL analysis, and a four-page Power BI dashboard — with every number independently verified across all three tools.

## Project summary

The dataset records lots offered at auction: item descriptions, categories, reserve prices, price estimates, vendor and buyer details, commission percentages, and final hammer prices. This project cleans the raw export, engineers useful fields (sold status, price performance vs. estimate, fee revenue), and answers business questions on sales performance, pricing accuracy, and vendor performance — reproducing the same headline numbers independently in Python, SQL, and Power BI.

**Headline result:** 13.7% sell-through rate (173 of 1,264 lots), £50,810 total hammer revenue. Jewellery dominates by volume (53% of all lots) but converts poorly (10.3%); smaller categories like Coins/Stamps/Banknotes convert far better (34.3%).

## Repository structure

```
auction-sales-analysis/
├── README.md
├── data/
│   └── cleaned/
│       └── auction_cleaned_anonymised.csv   # only file safe to publish
├── notebooks/
│   └── clean_and_analyse.py                 # full cleaning + analysis pipeline
├── sql/
│   └── auction_queries.sql                  # CREATE TABLE + 9 analysis queries
├── powerbi/
│   └── dashboard_notes.md                   # page-by-page build notes and DAX measures
├── docs/
│   ├── project_insights.md                  # findings, verified across all 3 tools
│   └── career_materials.md
└── project_plan.md
```

> **Note on raw data:** the original export contains buyer names, vendor names, and paddle numbers. Only the cleaned, anonymised dataset — with all identifying columns removed and vendors replaced with anonymous IDs (`V001`, `V002`...) — is published here.

## Tools used

- **Python** (pandas, matplotlib) — data cleaning, field engineering, exploratory analysis, visualisation
- **SQL** (SQLite) - CREATE TABLE, aggregate queries with CASE WHEN, GROUP BY, HAVING
- **Power BI** - four-page interactive dashboard with 13 DAX measures, slicers, and cross-filtering

## Power BI dashboard

Four pages, each with slicers and cross-filtering KPI cards:

1. **Auction Overview** — total/sold/unsold lots, sales rate, top categories by volume
2. **Category Performance** — sales rate and revenue by category, full summary table
3. **Pricing and Estimate Analysis** — scatter of hammer price vs. estimate, price-performance breakdown
4. **Vendor Performance** — anonymised vendor rankings (filtered to vendors with ≥5 lots to avoid small-sample distortion)

## Key data cleaning decisions

- Dropped one entirely empty column and one missing in >99% of rows (`subcategory_1`)
- Treated hammer price of `0` as "unsold" — verified against blank buyer name/paddle fields in all but 2 of 1,264 rows before relying on it; flagged as an inference, not a confirmed source field
- Fixed a bug where averaging `hammer_price` across *all* lots (including unsold £0 rows) produced meaningless category averages — corrected by filtering to sold lots before averaging, applied consistently in Python (`sold_only` filtering), SQL (`AVG(CASE WHEN...)` with no `ELSE`), and DAX (`CALCULATE(AVERAGE(...), sold = TRUE)`)
- Removed all personally identifying columns (buyer name, vendor name, buyer paddle, raw vendor number, free-text description) before any analysis output or export

## Limitations

- Single auction event — findings describe this auction only
- "Unsold = £0 hammer price" is an inferred rule, not a confirmed business rule
- No date field — seasonality/trend questions are out of scope
- Category and vendor rankings below 5 lots are excluded from headline findings due to small-sample distortion

## Completed vs. future work

**Completed:** full Python/pandas cleaning pipeline, 9 verified SQL queries, four-page Power BI dashboard with 13 DAX measures, cross-tool validation of every headline figure.

**Future work:** publish to a live Power BI workspace; extend SQL queries into reusable views; if more auctions become available, add a time dimension for trend analysis.
