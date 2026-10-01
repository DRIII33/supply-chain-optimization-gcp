"""
Filename: scripts/statistical_analysis.py
Description: Pulls transformed BigQuery views, executes advanced statistical analysis
             (ANOVA, Chi-Square, OLS Regression), and outputs diagnostic matrices.
Author: Portfolio project author
Target Environment: Google Colab / Python 3.10+ / GCP Free Tier (2026)
"""

import sys
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from google.cloud import bigquery

# Project Configuration
PROJECT_ID = "driiiportfolio"
DATASET_ID = "supply_chain_optimization"

def fetch_bq_data(query: str, project_id: str) -> pd.DataFrame:
    """Executes SQL query against BigQuery and returns a Pandas DataFrame."""
    client = bigquery.Client(project=project_id)
    try:
        df = client.query(query).to_dataframe()
        print(f"[INFO] Successfully queried {len(df)} records from BigQuery.")
        return df
    except Exception as e:
        print(f"[ERROR] BigQuery query execution failed: {e}")
        sys.exit(1)

def run_anova_warehouse_lead_times(df_logs: pd.DataFrame):
    """Performs One-Way ANOVA across distinct warehouse locations on actual lead times."""
    print("\n" + "="*80)
    print("1. STATISTICAL EVALUATION: ONE-WAY ANOVA (Warehouse Lead Time Variance)")
    print("="*80)

    # Group lead times by warehouse
    groups = [group["actual_lead_time_days"].values for _, group in df_logs.groupby("warehouse_id")]

    f_stat, p_val = stats.f_oneway(*groups)

    print(f"Calculated F-Statistic: {f_stat:.4f}")
    print(f"Calculated P-Value:     {p_val:.4e}")

    if p_val < 0.05:
        print("[CONCLUSION] Reject Null Hypothesis (H0). Statistically significant differences exist")
        print("             in mean actual lead times across distribution centers (p < 0.05).")
    else:
        print("[CONCLUSION] Fail to Reject H0. No statistically significant difference in lead times")
        print("             detected across distribution centers.")

def run_chi_square_stockouts(df_logs: pd.DataFrame):
    """Executes Chi-Square Test of Independence between Warehouse and Stock Status."""
    print("\n" + "="*80)
    print("2. STATISTICAL EVALUATION: CHI-SQUARE TEST OF INDEPENDENCE (Stockout Risk)")
    print("="*80)

    contingency_table = pd.crosstab(df_logs["warehouse_id"], df_logs["stock_status"])
    print("Contingency Table (Warehouse vs Stock Status):")
    print(contingency_table)

    chi2, p_val, dof, expected = stats.chi2_contingency(contingency_table)

    print(f"\nChi-Square Statistic: {chi2:.4f}")
    print(f"Degrees of Freedom:  {dof}")
    print(f"Calculated P-Value:   {p_val:.4e}")

    if p_val < 0.05:
        print("[CONCLUSION] Reject H0. Stockout frequency is dependent on warehouse location (p < 0.05).")
    else:
        print("[CONCLUSION] Fail to Reject H0. Stockout status is independent of warehouse location.")

def run_ols_lead_time_regression(df_logs: pd.DataFrame):
    """Fits an Ordinary Least Squares (OLS) regression model to predict lead time delays."""
    print("\n" + "="*80)
    print("3. PREDICTIVE EVALUATION: OLS MULTIPLE REGRESSION MODEL")
    print("="*80)

    # Feature engineering for regression
    df_logs["lead_delay"] = df_logs["actual_lead_time_days"] - df_logs["planned_lead_time_days"]

    model = ols('lead_delay ~ C(carrier) + C(warehouse_id) + planned_lead_time_days', data=df_logs).fit()

    print(model.summary())

def main():
    # Query logs data directly from sanitized BigQuery table
    logs_query = f"""
        SELECT
            warehouse_id,
            carrier,
            planned_lead_time_days,
            actual_lead_time_days,
            stock_status
        FROM `{PROJECT_ID}.{DATASET_ID}.stg_warehouse_logs`
        ORDER BY log_id
    """

    df_logs = fetch_bq_data(logs_query, PROJECT_ID)

    # Run statistical engines
    run_anova_warehouse_lead_times(df_logs)
    run_chi_square_stockouts(df_logs)
    run_ols_lead_time_regression(df_logs)

if __name__ == "__main__":
    main()
