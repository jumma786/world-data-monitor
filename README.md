# Automated Global Data Ingestion Pipeline (ETL)

An end-to-end, production-grade cloud data engineering pipeline that automates the extraction, transformation, deduplication, and loading (ETL) of global development and socioeconomic metrics. Running completely serverless, the pipeline ensures downstream analytics applications always have access to a clean, stable, and self-updating data warehouse.

---

## 🚀 Key Features & Architecture

- **Automated Multi-Source Extraction:** Uses Python to programmatically extract data streams from live REST APIs (World Bank, WHO Global Health Observatory) and third-party dataset providers via the Kaggle ecosystem.
- **Serverless Automation (Orchestration):** Managed via **GitHub Actions** on a daily cron schedule (`0 0 * * *`), eliminating the need for dedicated on-premise infrastructure or manual script execution.
- **Change-Data-Capture (CDC) via Hashing:** Implements structural data integrity verification using **MD5 cryptographic checksums**. If upstream data hasn't updated, the system halts storage writes to save resources. If variations are detected, it dynamically writes an immutable historical snapshot.
- **Stable Machine Learning & BI Endpoints:** Maintains a decoupled storage layer where data assets are mirrored into unique historical tracking versions alongside a permanent `latest.csv` pointer. This ensures connected Power BI, Tableau, or Excel dashboards never break when updates occur.
- **Secured Authentication Vault:** Implements production-level secret management by dynamically mapping encrypted GitHub Actions repository secrets into execution environment variables (`KAGGLE_USERNAME`, `KAGGLE_KEY`).

---

## 🛠️ Tech Stack & Tools

- **Language:** Python 3.10
- **Libraries:** Pandas (Data Transformation), Requests (API Ingestion), Kagglehub (Data Ingestion), Loggers & Hashlib (System Monitoring & Fingerprinting)
- **CI/CD & Orchestration:** GitHub Actions Workflow Engine
- **Storage Layer:** Git-based Data Lakehouse (`./data_warehouse`)

---

## 📁 Repository Directory Structure

```text
├── .github/workflows/
│   └── data_pipeline.yml          # GitHub Actions serverless cron configuration
├── data_warehouse/                # Automated Local Storage Layer
│   ├── kaggle/
│   │   └── avocado_prices/        # Deduplicated avocado retail logs
│   ├── who_gho/
│   │   ├── infant_mortality/      # Global infant mortality tracking matrices
│   │   └── life_expectancy/       # Global life expectancy index records
│   └── world_bank/
│       ├── gdp_current_usd/       # Worldwide GDP (Current USD)
│       └── total_population/      # Global population registries
├── logs/
│   └── pipeline_execution.log     # Detailed system event logging files
├── reports/
│   └── report_[timestamp].json    # Structured JSON pipeline run diagnostic receipts
├── data_ingestion_pipeline.py     # Main Python ETL engine
└── README.md                      # Project documentation (You are here)


## 📊 Automated Ingestion Targets

| Source | Dataset ID | Method | Core Metric |
| :--- | :--- | :--- | :--- |
| **World Bank** | `gdp_current_usd` | REST API | Gross Domestic Product |
| **World Bank** | `total_population` | REST API | Total Population |
| **WHO GHO** | `life_expectancy` | OData | Life Expectancy at Birth |
| **WHO GHO** | `infant_mortality` | OData | Infant Mortality Rate |
| **Kaggle** | `avocado_prices` | Kaggle API | Retail Vol & Pricing |

---

## 🔄 How the Automation Loop Executes

1. **Trigger:** The GitHub Actions workflow wakes up automatically every single day at midnight UTC.
2. **Infrastructure Standup:** A serverless Linux runtime container initializes, configures Python 3.10, and upgrades dependencies (`pandas`, `requests`, `kagglehub`).
3. **Secure Authentication:** The virtual environment safely maps repository secrets to verify data extraction access points.
4. **ETL Execution:** The Python pipeline extracts raw JSON objects, cleans anomalies into uniform schema data frames, and computes MD5 values.
5. **Data Mirroring & Version Control:** Fresh updates are committed back onto the master branch automatically by an authorized execution bot (`github-actions[bot]`).

---

## 🔌 Connecting This Live Feed to Downstream Tools

Because this pipeline outputs static, stable file paths (`latest.csv`), you can hook these assets directly into popular Business Intelligence tools for real-time reporting:

### For Microsoft Excel / Power Query

1. Navigate to the desired data asset directory in this repository (e.g., `data_warehouse/world_bank/gdp_current_usd/latest.csv`).
2. Click the **Raw** view button on GitHub and copy the complete URL string.
3. Open Excel, navigate to the **Data** ribbon, and select **From Web**.
4. Paste the raw URL string, then click **Load**.
5. *To get updates, simply open your spreadsheet and click **Data** -> **Refresh All**.*

### For Power BI / Tableau

- Select **Get Data** -> **Web Input Source**, provide the secure GitHub raw asset URL link, and set a daily schedule refresh cadence matching the midnight execution routine.


