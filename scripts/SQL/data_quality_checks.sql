-- 15-check suite
CREATE OR REPLACE TABLE `driiiportfolio.supply_chain_optimization.dq_check_results` AS
WITH s AS (SELECT * FROM `driiiportfolio.supply_chain_optimization.stg_inventory_transactions`), l AS (SELECT * FROM `driiiportfolio.supply_chain_optimization.stg_warehouse_logs`), d AS (SELECT warehouse_id FROM `driiiportfolio.supply_chain_optimization.dim_warehouses`), checks AS (
SELECT 'completeness','inventory staging row count = source',(SELECT COUNT(*) FROM `driiiportfolio.supply_chain_optimization.fact_inventory_transactions`)-COUNT(*) FROM s
UNION ALL SELECT 'completeness','shipment staging row count = source',(SELECT COUNT(*) FROM `driiiportfolio.supply_chain_optimization.fact_warehouse_logs`)-COUNT(*) FROM l
UNION ALL SELECT 'completeness','null keys',(SELECT COUNTIF(transaction_id IS NULL) FROM s)+(SELECT COUNTIF(log_id IS NULL) FROM l)
UNION ALL SELECT 'uniqueness','duplicate transaction_id',COUNT(*)-COUNT(DISTINCT transaction_id) FROM s
UNION ALL SELECT 'uniqueness','duplicate log_id',COUNT(*)-COUNT(DISTINCT log_id) FROM l
UNION ALL SELECT 'referential integrity','transaction warehouse missing',(SELECT COUNTIF(warehouse_id NOT IN (SELECT warehouse_id FROM d)) FROM s)
UNION ALL SELECT 'referential integrity','shipment warehouse missing',(SELECT COUNTIF(warehouse_id NOT IN (SELECT warehouse_id FROM d)) FROM l)
UNION ALL SELECT 'validity','invalid transaction_type',(SELECT COUNTIF(transaction_type NOT IN ('RESTOCK','OUTBOUND','ADJUSTMENT')) FROM s)
UNION ALL SELECT 'validity','invalid stock_status',(SELECT COUNTIF(stock_status NOT IN ('IN_STOCK','LOW_STOCK','STOCKOUT')) FROM l)
UNION ALL SELECT 'validity','nonpositive unit_cost',(SELECT COUNTIF(unit_cost<=0) FROM s)
UNION ALL SELECT 'consistency','delivery before dispatch',(SELECT COUNTIF(delivery_timestamp<dispatch_timestamp) FROM l)
UNION ALL SELECT 'consistency','lead-time mismatch',(SELECT COUNTIF(TIMESTAMP_DIFF(delivery_timestamp,dispatch_timestamp,DAY)<>actual_lead_time_days) FROM l)
UNION ALL SELECT 'consistency','summary views tie to staging',ABS((SELECT SUM(total_transactions) FROM `driiiportfolio.supply_chain_optimization.vw_inventory_health`)-COUNT(*) FROM s)+ABS((SELECT SUM(total_shipments) FROM `driiiportfolio.supply_chain_optimization.vw_warehouse_performance`)-COUNT(*) FROM l)
UNION ALL SELECT 'completeness','shipment detail rows tie to staging',ABS((SELECT COUNT(*) FROM `driiiportfolio.supply_chain_optimization.vw_shipment_detail`)-COUNT(*) FROM l)
UNION ALL SELECT 'consistency','inventory daily transactions tie to staging',ABS((SELECT SUM(transactions) FROM `driiiportfolio.supply_chain_optimization.vw_inventory_daily`)-COUNT(*) FROM s)
) SELECT CURRENT_TIMESTAMP() run_at,dimension,check_name,failures,IF(failures=0,'PASS','FAIL') status FROM checks;
