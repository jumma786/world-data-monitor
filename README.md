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


