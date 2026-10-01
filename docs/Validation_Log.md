# Validation Log

## 2026-09-30 analytical validation record

The supplied validation record reports 15/15 DQ checks passing; 2,500 shipments; 1,500 inventory transactions; 1,303 on-time/early; 1,197 delayed; 247 stockouts; 444 low-stock; +0.87 average lead variance; $44,350,562.38 gross value; ANOVA F=0.174 p=0.952; Chi-Square 3.342 df=8 p=0.911; OLS R²=0.002 F-test p=0.799; and BigQuery ML ROC AUC=0.527 with the model not promoted.

## Repository corrections already incorporated

1. Client/AGBG wording → fictional self-directed scenario.
2. 12-center scenario vs 5 generated warehouses → explicitly separated.
3. Streaming/real-time claims → batch default; streaming billing-gated.
4. Partitioning → removed from sandbox staging.
5. Dashboard sources → `vw_shipment_detail` and `vw_inventory_daily` added as the primary semantic sources.
6. Mock dashboard values → replaced by the validated values above.
7. Looker COUNTIF formulas → replaced with precomputed 0/1 flags and SUM/COUNT calculations.
8. Last 90 Days → fixed to Jan 1–Jun 30, 2026 for validation.
9. SKU category dimension → removed from the shipment risk table.
10. DQ suite → expanded from 13 to 15 checks, including dashboard-source reconciliation.
11. Streaming sample distribution → aligned to the synthetic generator.
12. Statistical row ordering → deterministic `ORDER BY log_id`.

## Final dashboard corrections — completed

13. Sixth scorecard renamed from **Gross Transaction Value** to **Total Shipments**; metric is `COUNT(log_id)` and acceptance value is **2,500**.
14. Avg Lead-Time Variance presentation finalized as **+0.87 days**.
15. SKU risk table primary sort finalized as **Stockout Rate descending** with **Stockout Incidents descending** as the secondary sort.
16. Executive-facing chart labels finalized so technical fields are not presented as raw `is_stockout`, `lead_time_variance_days`, or `gross_value` labels.
17. Inventory trend Y-axis minimum finalized at **0** to avoid implying a negative value range.

## Local repository QA performed during final handoff audit

- All repository Python scripts parsed successfully.
- All notebook code cells parsed successfully: **0 syntax errors**.
- Synthetic generator logic independently reproduces the headline counts and gross value: **2,500 shipments, 1,500 transactions, 1,303 on-time/early, 247 stockouts, 444 low-stock, +0.8704 days, $44,350,562.38 gross value**.
- Repository documentation was reconciled to the finalized dashboard configuration.
- SQL object inventory contains the intended staging tables, semantic views, 15-check DQ table, and BigQuery ML classifier.

## Evidence boundaries

The repository does not independently connect to or publish the user's live Looker Studio report. The final dashboard corrections above are incorporated as the user-confirmed final dashboard state. BigQuery execution results are represented from the supplied 2026-09-30 validation record; this handoff audit does not claim a new live BigQuery query.

## Remaining operational items

- Push the final repository contents to GitHub.
- Preserve or re-run the BigQuery Sandbox build before its expiration window if the dataset is needed for continued demonstration.
- Billing-gated managed GCP services remain documented but are not represented as executed in the no-billing environment.
