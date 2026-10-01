CREATE OR REPLACE MODEL `driiiportfolio.supply_chain_optimization.mdl_delay_classifier`
OPTIONS(model_type='LOGISTIC_REG',input_label_cols=['is_delayed'],data_split_method='RANDOM',data_split_eval_fraction=0.25,auto_class_weights=FALSE) AS
SELECT IF(lead_time_variance_days>0,1,0) is_delayed,carrier,warehouse_id,planned_lead_time_days,EXTRACT(DAYOFWEEK FROM dispatch_timestamp) dispatch_dow
FROM `driiiportfolio.supply_chain_optimization.stg_warehouse_logs`;
