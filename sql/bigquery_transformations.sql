-- BigQuery transformations; run after raw tables are loaded.
-- 2026-09-30 dashboard-ready version.

DROP TABLE IF EXISTS `driiiportfolio.supply_chain_optimization.stg_inventory_transactions`;
CREATE TABLE `driiiportfolio.supply_chain_optimization.stg_inventory_transactions`
CLUSTER BY warehouse_id, category AS
SELECT CAST(transaction_id AS STRING) transaction_id, UPPER(TRIM(warehouse_id)) warehouse_id, UPPER(TRIM(sku)) sku,
       INITCAP(TRIM(category)) category, UPPER(TRIM(transaction_type)) transaction_type, CAST(quantity AS INT64) quantity,
       ROUND(CAST(unit_cost AS NUMERIC),2) unit_cost, ROUND(CAST(quantity AS NUMERIC)*CAST(unit_cost AS NUMERIC),2) total_transaction_value,
       SAFE_CAST(transaction_timestamp AS TIMESTAMP) transaction_timestamp
FROM `driiiportfolio.supply_chain_optimization.fact_inventory_transactions` WHERE transaction_id IS NOT NULL;

DROP TABLE IF EXISTS `driiiportfolio.supply_chain_optimization.stg_warehouse_logs`;
CREATE TABLE `driiiportfolio.supply_chain_optimization.stg_warehouse_logs`
CLUSTER BY warehouse_id, carrier AS
SELECT CAST(log_id AS STRING) log_id, UPPER(TRIM(warehouse_id)) warehouse_id, UPPER(TRIM(sku)) sku, TRIM(carrier) carrier,
       CAST(planned_lead_time_days AS INT64) planned_lead_time_days, CAST(actual_lead_time_days AS INT64) actual_lead_time_days,
       CAST(actual_lead_time_days AS INT64)-CAST(planned_lead_time_days AS INT64) lead_time_variance_days,
       UPPER(TRIM(stock_status)) stock_status, SAFE_CAST(dispatch_timestamp AS TIMESTAMP) dispatch_timestamp, SAFE_CAST(delivery_timestamp AS TIMESTAMP) delivery_timestamp
FROM `driiiportfolio.supply_chain_optimization.fact_warehouse_logs` WHERE log_id IS NOT NULL;

CREATE OR REPLACE VIEW `driiiportfolio.supply_chain_optimization.vw_inventory_health` AS
SELECT t.warehouse_id,w.warehouse_name,w.city,w.state,t.category,COUNT(DISTINCT t.transaction_id) total_transactions,
SUM(IF(t.transaction_type='RESTOCK',t.quantity,0)) units_restocked,SUM(IF(t.transaction_type='OUTBOUND',t.quantity,0)) units_dispatched,
SUM(IF(t.transaction_type='ADJUSTMENT',t.quantity,0)) units_adjusted,ROUND(SUM(t.total_transaction_value),2) total_gross_value,ROUND(AVG(t.unit_cost),2) avg_unit_cost
FROM `driiiportfolio.supply_chain_optimization.stg_inventory_transactions` t LEFT JOIN `driiiportfolio.supply_chain_optimization.dim_warehouses` w USING(warehouse_id) GROUP BY 1,2,3,4,5;

CREATE OR REPLACE VIEW `driiiportfolio.supply_chain_optimization.vw_warehouse_performance` AS
SELECT l.warehouse_id,w.warehouse_name,l.carrier,COUNT(*) total_shipments,ROUND(AVG(l.planned_lead_time_days),2) avg_planned_lead_time_days,ROUND(AVG(l.actual_lead_time_days),2) avg_actual_lead_time_days,
ROUND(AVG(l.lead_time_variance_days),2) avg_lead_time_delay_days,COUNTIF(l.lead_time_variance_days>0) delayed_shipment_count,
ROUND(SAFE_DIVIDE(COUNTIF(l.lead_time_variance_days>0),COUNT(l.log_id))*100,2) delay_rate_percentage,COUNTIF(l.stock_status='STOCKOUT') stockout_incidents,
COUNTIF(l.stock_status='LOW_STOCK') low_stock_warnings,ROUND(SAFE_DIVIDE(COUNTIF(l.stock_status='STOCKOUT'),COUNT(l.log_id))*100,2) stockout_rate_percentage
FROM `driiiportfolio.supply_chain_optimization.stg_warehouse_logs` l LEFT JOIN `driiiportfolio.supply_chain_optimization.dim_warehouses` w USING(warehouse_id) GROUP BY 1,2,3;

CREATE OR REPLACE VIEW `driiiportfolio.supply_chain_optimization.vw_shipment_detail` AS
SELECT l.log_id,l.warehouse_id,w.warehouse_name,w.city,w.state,l.sku,l.carrier,l.planned_lead_time_days,l.actual_lead_time_days,l.lead_time_variance_days,l.stock_status,
DATE(l.dispatch_timestamp) dispatch_date,l.dispatch_timestamp,l.delivery_timestamp,IF(l.lead_time_variance_days<=0,1,0) is_on_time,IF(l.lead_time_variance_days>0,1,0) is_delayed,
IF(l.stock_status='STOCKOUT',1,0) is_stockout,IF(l.stock_status='LOW_STOCK',1,0) is_low_stock
FROM `driiiportfolio.supply_chain_optimization.stg_warehouse_logs` l LEFT JOIN `driiiportfolio.supply_chain_optimization.dim_warehouses` w USING(warehouse_id);

CREATE OR REPLACE VIEW `driiiportfolio.supply_chain_optimization.vw_inventory_daily` AS
SELECT DATE(t.transaction_timestamp) transaction_date,t.warehouse_id,w.warehouse_name,w.city,w.state,t.category,t.transaction_type,COUNT(*) transactions,ROUND(SUM(t.total_transaction_value),2) gross_value
FROM `driiiportfolio.supply_chain_optimization.stg_inventory_transactions` t LEFT JOIN `driiiportfolio.supply_chain_optimization.dim_warehouses` w USING(warehouse_id) GROUP BY 1,2,3,4,5,6,7;
