# Looker Studio Control Tower — Dashboard User Guide

**Dashboard state:** Final specification aligned to the completed dashboard corrections.

## Page 1 — Executive Control Tower

Six executive scorecards summarize:

- **Fulfillment Rate:** 52.1%
- **Avg Lead-Time Variance:** +0.87 days
- **Stockout Incidents:** 247
- **Low-Stock Warnings:** 444
- **Gross Transaction Value:** $44,350,562.38
- **Total Shipments:** 2,500

The warehouse risk map uses city as the geographic dimension, stockout incidents for bubble size, and average lead-time variance for color. The category trend uses daily transaction value by inventory category.

## Page 2 — Shipment Performance & Risk

The carrier scatter/bubble chart compares average planned versus actual lead time, with bubble size representing delay rate and carrier used as the color dimension.

The SKU Stockout Risk Table contains shipment count, stockout incidents, stockout rate, and average lead-time variance. It is sorted **primarily by Stockout Rate descending and secondarily by Stockout Incidents descending**.

## Final controls and source configuration

- Shipment source: `vw_shipment_detail`
- Inventory source: `vw_inventory_daily`
- Default date range: Jan 1, 2026 – Jun 30, 2026
- Controls: `warehouse_id`, `carrier`, date range

The data is synthetic and descriptive; differences are not causal findings.
