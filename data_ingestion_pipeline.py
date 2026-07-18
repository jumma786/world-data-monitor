import os
import json
import hashlib
import logging
import datetime
import requests
import pandas as pd
import kagglehub

# Establish tracking directories
BASE_DATA_DIR = "./data_warehouse"
LOG_DIR = "./logs"
REPORT_DIR = "./reports"

for folder in [BASE_DATA_DIR, LOG_DIR, REPORT_DIR]:
    os.makedirs(folder, exist_ok=True)

# Standardized structural execution logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "pipeline_execution.log")),
        logging.StreamHandler()
    ]
)


class DataPipelineMonitor:
    def __init__(self):
        self.execution_summary = {
            "execution_time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "successful_downloads": [],
            "failed_downloads": [],
            "skipped_no_changes": []
        }

    def get_content_hash(self, content: bytes) -> str:
        """Generates SHA-256 file hashes to verify if contents have updated."""
        return hashlib.sha256(content).hexdigest()

    def save_file_with_versioning(self, repository: str, dataset_name: str, content: bytes, file_ext: str = "csv") -> None:
        """Saves dynamic version snapshots alongside an un-versioned entrypoint for data engines."""
        repo_path = os.path.join(BASE_DATA_DIR, repository, dataset_name)
        os.makedirs(repo_path, exist_ok=True)

        new_hash = self.get_content_hash(content)
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")

        # Verify deduplication constraints
        duplicate_found = False
        for existing_file in os.listdir(repo_path):
            if new_hash in existing_file and existing_file.endswith(file_ext):
                duplicate_found = True
                break

        if duplicate_found:
            logging.info(f"[{repository}] Data asset '{dataset_name}' shows no changes. Skipping.")
            self.execution_summary["skipped_no_changes"].append({"repository": repository, "dataset": dataset_name})
            return

        # Write unique storage entry
        filename = f"v_{timestamp}_{new_hash}.{file_ext}"
        full_path = os.path.join(repo_path, filename)
        with open(full_path, "wb") as f:
            f.write(content)

        # Update stable point-of-entry pointer file
        latest_path = os.path.join(repo_path, f"latest.{file_ext}")
        with open(latest_path, "wb") as f:
            f.write(content)

        logging.info(f"[{repository}] Stored structural version: {filename}")
        self.execution_summary["successful_downloads"].append({
            "repository": repository, "dataset": dataset_name, "file": filename
        })

    def track_failure(self, repository: str, dataset_name: str, error_msg: str):
        logging.error(f"[{repository}] Ingestion error at '{dataset_name}': {error_msg}")
        self.execution_summary["failed_downloads"].append({
            "repository": repository, "dataset": dataset_name, "error": error_msg,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        })

    def ingest_world_bank(self, indicator_code: str, dataset_alias: str):
        url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator_code}?format=json&per_page=15000"
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            if len(data) < 2 or not data[1]:
                raise ValueError("Payload structural processing mismatch.")
            records = [{
                "country_id": item["country"]["id"], "country_value": item["country"]["value"],
                "date": item["date"], "value": item["value"],
                "indicator_id": item["indicator"]["id"], "indicator_value": item["indicator"]["value"]
            } for item in data[1]]
            df = pd.DataFrame(records)
            self.save_file_with_versioning("world_bank", dataset_alias, df.to_csv(index=False).encode('utf-8'))
        except Exception as e:
            self.track_failure("world_bank", dataset_alias, str(e))

    def ingest_who_gho(self, indicator_code: str, dataset_alias: str):
        url = f"https://ghoapi.azureedge.net/api/{indicator_code}"
        try:
            response = requests.get(url, timeout=45)
            response.raise_for_status()
            payload = response.json()
            if "value" not in payload or not payload["value"]:
                raise ValueError("OData payload stream empty.")
            df = pd.DataFrame(payload["value"])
            self.save_file_with_versioning("who_gho", dataset_alias, df.to_csv(index=False).encode('utf-8'))
        except Exception as e:
            self.track_failure("who_gho", dataset_alias, str(e))

    def ingest_kaggle_dataset(self, dataset_handle: str, target_file: str, dataset_alias: str):
        try:
            downloaded_dir = kagglehub.dataset_download(dataset_handle)
            file_path = os.path.join(downloaded_dir, target_file)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Target dataset component '{target_file}' missing from download directory.")
            with open(file_path, "rb") as f:
                content_bytes = f.read()
            ext = target_file.split('.')[-1] if '.' in target_file else 'csv'
            self.save_file_with_versioning("kaggle", dataset_alias, content_bytes, ext)
        except Exception as e:
            self.track_failure("kaggle", dataset_alias, str(e))

    def export_summary_report(self):
        report_filename = f"report_{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
        with open(os.path.join(REPORT_DIR, report_filename), "w") as f:
            json.dump(self.execution_summary, f, indent=4)


if __name__ == "__main__":
    pipeline = DataPipelineMonitor()
    # Ingestion Jobs
    pipeline.ingest_world_bank("NY.GDP.MKTP.CD", "gdp_current_usd")
    pipeline.ingest_world_bank("SP.POP.TOTL", "total_population")
    pipeline.ingest_who_gho("WHOSIS_000001", "life_expectancy")
    pipeline.ingest_who_gho("MDG_0000000001", "infant_mortality")
    pipeline.ingest_kaggle_dataset("neuromusic/avocado-prices", "avocado.csv", "avocado_prices")
    # Finish Tracking
    pipeline.export_summary_report()
