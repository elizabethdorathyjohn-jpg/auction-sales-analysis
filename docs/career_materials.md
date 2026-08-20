# Career Materials — Auction Sales Performance and Pricing Analysis

## CV bullet points

- Cleaned and analysed a 1,264-row real-world auction dataset using Python and pandas, engineering derived fields (sold status, price-performance vs. estimate, fee revenue) and identifying/fixing a data aggregation bug affecting category-level averages.
- Independently reproduced key findings in SQL (CREATE TABLE, CASE WHEN, GROUP BY, HAVING) against a live SQLite database, verifying every headline figure against the Python analysis.
- Built a four-page interactive Power BI dashboard with 13 custom DAX measures, cross-filtering slicers, and anonymised vendor tracking, covering sales performance, pricing accuracy, and vendor comparisons.
- Applied data anonymisation throughout the pipeline — removing buyer/vendor names and paddle numbers, replacing vendor identifiers with anonymous codes — before any analysis output or dashboard was built.

## LinkedIn project description

> **Auction Sales Performance and Pricing Analysis**
> A self-directed portfolio project analysing 1,264 real auction lots across the full analytics stack — Python, SQL, and Power BI. I cleaned the raw data in pandas, engineered fields to flag sold status and price performance against pre-sale estimates, and answered business questions on sell-through rate, category and vendor performance, and pricing accuracy. I reproduced the same findings independently in SQL and built a four-page Power BI dashboard with custom DAX measures and cross-filtering slicers — cross-checking every headline number across all three tools to make sure they agreed before treating any finding as settled. All personally identifying data was removed before publishing.
> Tools: Python (pandas, matplotlib), SQL (SQLite), Power BI (DAX, data modelling).

## Interview questions and model answers

**1. You mention cross-checking your results across three tools — walk me through an example where that actually caught something.**
Yes — when I first built the category summary table in pandas, I calculated average and median hammer price using `.mean()` and `.median()` directly on the whole dataset. The numbers looked wrong: Jewellery showed a median hammer price of £0, which made no sense for a category worth thousands in total revenue. The bug was that unsold lots (with a hammer price of £0) were being included in the average — since roughly 86% of every category is unsold, the zeros dragged the numbers down to near-meaningless values. I fixed it by filtering to sold lots before calculating the average, and then deliberately checked the same pattern in my SQL query — using `AVG(CASE WHEN sold THEN hammer_price END)` with no `ELSE`, so unsold rows return NULL and get correctly excluded from the average rather than counted as zero — and again in Power BI, using `CALCULATE(AVERAGE(...), sold = TRUE)`. All three now agree.

**2. How did you decide a hammer price of zero meant a lot was unsold?**
I checked it against the data rather than assuming it. Every row with a hammer price of zero also had a blank buyer name and blank paddle number, and vice versa, in all but two of 1,264 rows. That gave me confidence to treat it as a rule, but I documented it clearly as an inference from the data, not a confirmed field from the source system — something I'd want signed off before it was used beyond this project.

**3. Your Vendor Performance page shows smaller totals than your other pages — is that a bug?**
No — that page deliberately filters to vendors with 5 or more lots, the same reasoning I used for a SQL `HAVING COUNT(*) >= 5` clause elsewhere in the project. Without that filter, a vendor with a single lot that happened to sell would show a 100% sales rate, which is a meaningless number driven by sample size rather than genuine performance. I noted this explicitly in my documentation so it doesn't look like a data error to someone reviewing the dashboard.

**4. How did you handle privacy in this project?**
I removed every column that could identify a real person — buyer names, vendor names, and paddle numbers — before any analysis or dashboard was built on top of the data. Vendor performance still needed a way to group by seller, so I replaced the real vendor number with an anonymous ID like V001. I also excluded the free-text lot description from the published file, since auction descriptions can occasionally mention identifying details.

**5. What would you do differently if you were starting this project again?**
I'd set up the "sold lots only" filtering pattern once, early, and apply it consistently from the start, rather than discovering the same bug three separate times in Python, SQL, and DAX. I'd also standardise on page-level filters over visual-level filters in Power BI from the beginning — I lost some time when a visual-level filter kept resetting during rebuilds, which a page-level filter avoided entirely once I switched to it.

## Improvements required before publishing

- [ ] Get explicit permission from the data owner to publish even the anonymised dataset
- [ ] Resolve or document the two rows where hammer price is nonzero but paddle number is blank
- [ ] Add a `COALESCE(..., 0)` wrapper to revenue DAX measures so zero-sale vendors/categories display as 0 rather than blank
- [ ] Publish the Power BI report to a shareable workspace (or export as PDF/screenshots) before linking it from a CV or portfolio site, since a local `.pbix` file isn't viewable by a recruiter without Power BI installed
