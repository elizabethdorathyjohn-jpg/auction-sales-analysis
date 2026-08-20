# Project Insights — Auction Sales Performance and Pricing Analysis

Every figure below was independently verified across three tools - Python/pandas, SQL, and Power BI  and matched exactly in all three before being included here.

## Headline numbers

- **1,264 lots** offered, **173 sold (13.7% sell-through rate)**
- **£50,810** total hammer revenue, averaging **£293.70** per sold lot
- **£10,162** in buyer premium revenue, **£317.35** in vendor commission revenue
- **10 lots (5.8% of sold lots)** sold below their reserve price
- **98 of 173 sold lots (57%)** sold below their pre-sale estimate; only 15 sold above it

## Finding 1: Volume and conversion are two separate stories

Jewellery makes up 671 of 1,264 lots (53% of the entire auction) and generates the most total revenue (£18,445)  but converts poorly, selling at only a 10.3% rate. By contrast, Coins/Stamps/Banknotes (70 lots) converts at 34.3%, and Silver/Gold and Writing Pens/Stationery outperform Jewellery on sales rate despite far smaller volume. A category leading on revenue is not the same as a category performing well  a distinction worth stating explicitly rather than assuming revenue alone tells the story.

## Finding 2: Pre-sale estimates skewed optimistic

Among sold lots, 57% sold below their estimated range and only 9% sold above it. Separately, unsold lots had noticeably higher average estimates (£503–£610) than sold lots (£289–£357) - suggesting estimates may have been set too high for pricier items specifically, though this dataset alone can't confirm cause and effect.

## Finding 3: Vendor revenue is driven by volume, not performance

The top-revenue vendor (V008, £11,375) achieves this through having the most lots (139), not through a strong sales rate (12.2%). Vendors V060 and V025 both convert at 27–28%, more than double V008's rate, on a fraction of the lots  a genuinely different kind of "good vendor" that a revenue-only ranking would miss.

## Finding 4: Small sample sizes distort simple rankings

Several categories and vendors show 100% or 0% sales rates purely from having 1–2 lots total. Every ranking in this project that could be affected by this (category sales rate, vendor performance) was filtered to a minimum of 5 lots before drawing conclusions the same principle applied consistently in the SQL `HAVING` clauses and the Power BI table/chart filters.

## Limitations

- Single auction event - findings describe this auction only, not the auction house's performance generally
- The "unsold = hammer price of 0" rule is inferred from the data (verified against blank buyer/paddle fields in all but 2 of 1,264 rows), not a confirmed field from the source system
- No date field - seasonality or trend-over-time questions are out of scope
- Vendor and category comparisons below 5 lots are excluded from ranked findings due to small-sample distortion
