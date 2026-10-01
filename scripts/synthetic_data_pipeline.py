import os
import uuid
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError

# Configuration Parameters
PROJECT_ID = "driiiportfolio"
DATASET_ID = "supply_chain_optimization"
LOCATION = "US"
NUM_WAREHOUSES = 5
NUM_PRODUCTS = 20
NUM_TRANSACTIONS = 1500
NUM_LOGS = 2500

def initialize_bigquery_client(project_id: str) -> bigquery.Client:
    """Initializes and returns a Google BigQuery Client instance."""
    try:
        client = bigquery.Client(project=project_id)
        print(f"[INFO] BigQuery client initialized successfully for project: {project_id}")
        return client
    except Exception as e:
        print(f"[ERROR] Failed to initialize BigQuery client: {e}")
        raise e

def create_bigquery_dataset(client: bigquery.Client, dataset_id: str, location: str) -> str:
    """Creates the target BigQuery dataset if it does not already exist."""
    dataset_ref = bigquery.DatasetReference(client.project, dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = location
    try:
        dataset = client.create_dataset(dataset, exists_ok=True)
        full_dataset_id = f"{client.project}.{dataset.dataset_id}"
        print(f"[INFO] Dataset {full_dataset_id} verified/created in location {location}.")
        return full_dataset_id
    except GoogleAPIError as e:
        print(f"[ERROR] Failed to create dataset {dataset_id}: {e}")
        raise e

def generate_synthetic_data():
    """Generates synthetic relational dataframes modeling supply chain operations."""
    print("[INFO] Starting synthetic enterprise dataset generation...")
    np.random.seed(42)
    random.seed(42)

    # 1. Warehouses Entity
    warehouses_data = []
    cities = ["Seattle", "Dallas", "Chicago", "Atlanta", "New York"]
    states = ["WA", "TX", "IL", "GA", "NY"]
    for i in range(NUM_WAREHOUSES):
        warehouses_data.append({
            "warehouse_id": f"WH-{100 + i}",
            "warehouse_name": f"Regional Distribution Center {cities[i]}",
            "city": cities[i],
            "state": states[i],
            "capacity_units": int(np.random.choice([50000, 75000, 100000, 150000])),
            "operating_cost_daily": round(float(np.random.uniform(2500.0, 6000.0)), 2)
        })
    df_warehouses = pd.DataFrame(warehouses_data)

    # 2. Inventory Transactions Entity
    categories = ["Electronics", "Apparel", "Home & Kitchen", "Automotive"]
    products = [f"SKU-{2000 + i}" for i in range(NUM_PRODUCTS)]

    transactions_data = []
    start_date = datetime(2026, 1, 1)

    for _ in range(NUM_TRANSACTIONS):
        tx_date = start_date + timedelta(
            days=random.randint(0, 180),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        tx_type = np.random.choice(["RESTOCK", "OUTBOUND", "ADJUSTMENT"], p=[0.35, 0.55, 0.10])
        qty = int(np.random.randint(5, 500)) if tx_type != "ADJUSTMENT" else int(np.random.randint(-20, 20))

        transactions_data.append({
            "transaction_id": str(uuid.uuid4()),
            "warehouse_id": f"WH-{100 + random.randint(0, NUM_WAREHOUSES - 1)}",
            "sku": random.choice(products),
            "category": random.choice(categories),
            "transaction_type": tx_type,
            "quantity": qty,
            "unit_cost": round(float(np.random.uniform(10.0, 250.0)), 2),
            "transaction_timestamp": tx_date.strftime("%Y-%m-%d %H:%M:%S")
        })
    df_transactions = pd.DataFrame(transactions_data)

    # 3. Warehouse Logistics & Fulfillment Logs Entity
    logs_data = []
    carriers = ["FedEx Freight", "UPS Supply Chain", "DHL Express", "JB Hunt"]
    stock_statuses = ["IN_STOCK", "LOW_STOCK", "STOCKOUT"]

    for _ in range(NUM_LOGS):
        dispatch_time = start_date + timedelta(
            days=random.randint(0, 180),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        planned_lead_days = random.randint(2, 7)
        # Delay is intentionally independent of carrier and warehouse.
        actual_lead_days = planned_lead_days + int(np.random.choice([0, 1, 2, 3, 5], p=[0.5, 0.25, 0.15, 0.07, 0.03]))
        delivery_time = dispatch_time + timedelta(days=actual_lead_days)

        logs_data.append({
            "log_id": f"LOG-{uuid.uuid4().hex[:8].upper()}",
            "warehouse_id": f"WH-{100 + random.randint(0, NUM_WAREHOUSES - 1)}",
            "sku": random.choice(products),
            "carrier": random.choice(carriers),
            "planned_lead_time_days": planned_lead_days,
            "actual_lead_time_days": actual_lead_days,
            "stock_status": np.random.choice(stock_statuses, p=[0.70, 0.20, 0.10]),
            "dispatch_timestamp": dispatch_time.strftime("%Y-%m-%d %H:%M:%S"),
            "delivery_timestamp": delivery_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    df_logs = pd.DataFrame(logs_data)

    print("[INFO] Synthetic data generation complete.")
    return df_warehouses, df_transactions, df_logs

def save_and_load_to_bigquery(client: bigquery.Client, dataset_id: str, tables_dict: dict):
    """Saves DataFrames to local CSV files and loads them into BigQuery tables."""
    os.makedirs("data_export", exist_ok=True)

    for table_name, df in tables_dict.items():
        csv_path = os.path.join("data_export", f"{table_name}.csv")
        df.to_csv(csv_path, index=False)
        print(f"[INFO] Saved local CSV: {csv_path} ({len(df)} rows)")

        table_ref = client.dataset(dataset_id).table(table_name)
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
        )

        with open(csv_path, "rb") as source_file:
            load_job = client.load_table_from_file(
                source_file,
                table_ref,
                job_config=job_config
            )

        print(f"[INFO] Starting BigQuery load job for table: {table_name}...")
        load_job.result()  # Wait for job execution to complete

        destination_table = client.get_table(table_ref)
        print(f"[SUCCESS] Loaded {destination_table.num_rows} rows into {PROJECT_ID}.{dataset_id}.{table_name}")

def main():
    try:
        from google.colab import auth
        auth.authenticate_user()
    except ImportError:
        print("[INFO] Non-Colab execution: using existing Google Application Default Credentials.")
    client = initialize_bigquery_client(PROJECT_ID)
    create_bigquery_dataset(client, DATASET_ID, LOCATION)

    df_warehouses, df_transactions, df_logs = generate_synthetic_data()

    tables_to_upload = {
        "dim_warehouses": df_warehouses,
        "fact_inventory_transactions": df_transactions,
        "fact_warehouse_logs": df_logs
    }

    save_and_load_to_bigquery(client, DATASET_ID, tables_to_upload)
    print("\n[COMPLETE] Phase 2 Data Ingestion Pipeline executed successfully.")

if __name__ == "__main__":
    main()
