# Looker Studio Build Guide — Enterprise Supply Chain Optimization Control Tower

**Updated:** 2026-09-30  
**Dashboard state:** Final build specification aligned to the completed five dashboard corrections. The live Looker Studio report itself is external to this repository.

## 1. Data sources and report configuration

Connect BigQuery project `driiiportfolio`, dataset `supply_chain_optimization`:

| Report source | BigQuery object | Purpose |
|---|---|---|
| **Shipments** | `vw_shipment_detail` | Fulfillment KPI, risk map, carrier performance, SKU risk |
| **Inventory Daily** | `vw_inventory_daily` | Category-level transaction-value trend |

Use **Owner's Credentials** when appropriate for a portfolio report. Keep the report at the fixed validation period below so acceptance values remain reproducible.

### Date configuration

- Default date range: **Custom — Jan 1, 2026 through Jun 30, 2026**.
- Shipments date-range dimension: `dispatch_date`.
- Inventory Daily date-range dimension: `transaction_date`.
- Do **not** use Last 90 Days for validation.
- Report controls: `warehouse_id`, `carrier`, and date range.
- Enable cross-filtering where useful.

## 2. Page 1 — Executive Control Tower

### Scorecards

| Chart title | Source | Metric / formula | Display / acceptance |
|---|---|---|---:|
| **Fulfillment Rate** | Shipments | `SUM(is_on_time) / COUNT(log_id)` | **52.1%** |
| **Avg Lead-Time Variance** | Shipments | `AVG(lead_time_variance_days)` | **+0.87 days** |
| **Stockout Incidents** | Shipments | `SUM(is_stockout)` | **247** |
| **Low-Stock Warnings** | Shipments | `SUM(is_low_stock)` | **444** |
| **Gross Transaction Value** | Inventory Daily | `SUM(gross_value)` | **$44,350,562.38** |
| **Total Shipments** | Shipments | `COUNT(log_id)` | **2,500** |

**Important:** The sixth scorecard is **Total Shipments**, not Gross Transaction Value. Its value of 2,500 must never be labeled as transaction value.

For the Avg Lead-Time Variance scorecard, retain the underlying metric `AVG(lead_time_variance_days)` and present the executive-facing unit as **days**.

### Warehouse Stockout & Lead-Time Risk Map

- **Chart type:** Google Maps / bubble map.
- **Source:** Shipments.
- **Dimension:** `city`.
- **Bubble size:** `SUM(is_stockout)`.
- **Color:** `AVG(lead_time_variance_days)`.
- **Date range dimension:** `dispatch_date`.
- Executive-facing labels:
  - `Stockout Incidents`
  - `Avg Lead-Time Variance (days)`
- Avoid exposing raw field names such as `is_stockout` or `lead_time_variance_days` in the final presentation.

**Caption:** “Warehouse locations are sized by stockout incidents and colored by average lead-time variance to highlight where inventory availability and fulfillment timing create the greatest operational risk.”

### Inventory Gross Value by Category Over Time

- **Chart type:** time-series / line chart.
- **Source:** Inventory Daily.
- **Dimension:** `transaction_date`.
- **Breakdown:** `category`.
- **Metric:** `SUM(gross_value)`.
- **Sort:** `transaction_date` ascending.
- **Date range dimension:** `transaction_date`.
- **Y-axis title:** `Gross Transaction Value (USD)`.
- **Y-axis minimum:** `0`.
- Executive-facing label: `Gross Transaction Value (USD)` rather than `gross_value`.

**Caption:** “Daily gross transaction value is segmented by inventory category to show how the composition and magnitude of warehouse activity change throughout the reporting period.”

## 3. Page 2 — Shipment Performance & Risk

### Carrier Lead-Time Performance

- **Chart type:** scatter / bubble chart.
- **Source:** Shipments.
- **X-axis:** `AVG(planned_lead_time_days)`.
- **Y-axis:** `AVG(actual_lead_time_days)`.
- **Bubble size:** `SUM(is_delayed) / COUNT(log_id)` (delay rate).
- **Dimensions:** `carrier` and `planned_lead_time_days`.
- **Color:** `carrier`.
- **Sort:** planned lead time ascending, then carrier ascending.
- **X-axis title:** `Avg Planned Lead Time`.
- **Y-axis title:** `Avg Actual Lead Time`.

**Caption:** “Carrier-level bubbles compare planned versus actual lead time, with larger bubbles representing higher delay rates so that slower and less reliable shipment groupings are immediately visible.”

### SKU Stockout Risk Table

- **Chart type:** table.
- **Source:** Shipments.
- **Dimension:** `sku` only.
- **Do not add `category`:** shipment logs do not contain category.
- **Metrics:**
  1. `COUNT(log_id)` → **Shipment Count**
  2. `SUM(is_stockout)` → **Stockout Incidents**
  3. `SUM(is_stockout) / COUNT(log_id)` → **Stockout Rate**
  4. `AVG(lead_time_variance_days)` → **Avg Lead-Time Variance (days)**
- **Primary sort:** **Stockout Rate — descending**.
- **Secondary sort:** **Stockout Incidents — descending**.
- Sort using the underlying/unrounded Stockout Rate calculation, not a display-rounded percentage.

**Important:** The table must not default to Shipment Count descending. That configuration contradicts the intended risk ranking.

**Caption:** “The SKU ranking identifies products with the highest stockout exposure while retaining shipment volume and lead-time variance to distinguish concentrated inventory risk from low-volume anomalies.”

## 4. Calculated fields

Use the precomputed 0/1 flags from `vw_shipment_detail`; do not recreate these as SQL `COUNTIF` expressions in Looker Studio.

| Field | Formula | Type / display |
|---|---|---|
| Fulfillment Rate | `SUM(is_on_time) / COUNT(log_id)` | Percent |
| Delay Rate | `SUM(is_delayed) / COUNT(log_id)` | Percent |
| Stockout Rate | `SUM(is_stockout) / COUNT(log_id)` | Percent |
| Avg Lead-Time Variance | `AVG(lead_time_variance_days)` | Number; display in days |

Recommended executive-facing field names:

- `is_stockout` → **Stockout Incidents**
- `lead_time_variance_days` → **Avg Lead-Time Variance (days)** when used as the displayed aggregate
- `gross_value` → **Gross Transaction Value (USD)**

## 5. Final acceptance values

With no filters other than the fixed Jan 1–Jun 30, 2026 reporting period:

- **Total Shipments:** 2,500
- **On-time / early shipments:** 1,303
- **Delayed shipments:** 1,197
- **Fulfillment Rate:** 52.1%
- **Avg Lead-Time Variance:** +0.87 days
- **Stockout Incidents:** 247
- **Low-Stock Warnings:** 444
- **Inventory Transactions:** 1,500
- **Gross Transaction Value:** $44,350,562.38
- **Data Quality:** 15/15 PASS

Any mismatch should be treated as a source, date-range, aggregation, filter, or chart-configuration issue before publication.
