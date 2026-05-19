# 🌍 Automated Global Data Ingestion Pipeline (ETL)

Production-grade serverless ETL pipeline that automates ingestion of global socioeconomic datasets from REST APIs and Kaggle sources using Python and GitHub Actions. The system performs automated extraction, transformation, deduplication, hashing-based CDC validation, and versioned storage for downstream analytics and BI platforms.

---

# 🚀 Project Overview

This project simulates a real-world cloud data engineering workflow where multiple external data sources are continuously monitored, processed, validated, and stored automatically.

The pipeline runs completely serverless using GitHub Actions and updates datasets daily without manual intervention.

The architecture ensures:

- Automated daily ingestion
- Clean and standardized datasets
- Change detection using MD5 hashing
- Historical data versioning
- Stable endpoints for BI dashboards
- Secure secret management
- Automated reporting and logging

---

# 🛠️ Tech Stack

| Category | Tools & Technologies |
|---|---|
| Language | Python 3.10 |
| Data Processing | Pandas |
| API Integration | Requests |
| Dataset Ingestion | Kagglehub |
| Automation | GitHub Actions |
| Scheduling | Cron Jobs |
| Version Control | Git & GitHub |
| Logging | Python Logging |
| Data Validation | Hashlib (MD5) |
| Storage Layer | Git-based Data Lakehouse |

---

# 📊 Automated Data Sources

| Source | Dataset | Method | Metric |
|---|---|---|---|
| World Bank | GDP Current USD | REST API | Economic Growth |
| World Bank | Total Population | REST API | Population Tracking |
| WHO GHO | Life Expectancy | OData API | Healthcare Indicators |
| WHO GHO | Infant Mortality | OData API | Mortality Statistics |
| Kaggle | Avocado Prices | Kaggle API | Retail Pricing Analytics |

---

# ⚙️ Pipeline Architecture

```text
External APIs / Kaggle
        ↓
Python ETL Pipeline
        ↓
Data Cleaning & Transformation
        ↓
MD5 Hash Validation (CDC)
        ↓
Versioned Data Storage
        ↓
latest.csv Stable Endpoints
        ↓
Power BI / Excel / Tableau
```

---

# 🔄 How the Pipeline Works

## 1. Automated Trigger

GitHub Actions automatically triggers the pipeline every day at midnight UTC using cron scheduling.

```yaml
schedule:
  - cron: '0 0 * * *'
```

---

## 2. Data Extraction

The system extracts data from:

- World Bank APIs
- WHO Global Health Observatory APIs
- Kaggle datasets

using Python requests and Kagglehub.

---

## 3. Data Transformation

Raw JSON responses are transformed into clean Pandas DataFrames with standardized schemas.

Operations include:

- Null handling
- Column normalization
- Type conversion
- Data cleaning

---

## 4. Change Data Capture (CDC)

The pipeline computes MD5 hashes for datasets.

If no changes are detected:
- Storage writes are skipped

If changes are detected:
- New historical snapshots are created automatically

This reduces unnecessary storage operations and preserves historical tracking.

---

## 5. Data Versioning

Each dataset maintains:

- Historical snapshots
- Permanent `latest.csv` endpoint

This ensures downstream dashboards never break after updates.

---

# 🔐 Secure Secret Management

Sensitive credentials are stored securely using GitHub Secrets.

Environment variables used:

```env
KAGGLE_USERNAME
KAGGLE_KEY
```

Secrets are dynamically injected during workflow execution.

---

# 📁 Repository Structure

```text
├── .github/workflows/
│   └── data_pipeline.yml
│
├── data_warehouse/
│   ├── kaggle/
│   │   └── avocado_prices/
│   │
│   ├── who_gho/
│   │   ├── infant_mortality/
│   │   └── life_expectancy/
│   │
│   └── world_bank/
│       ├── gdp_current_usd/
│       └── total_population/
│
├── logs/
│   └── pipeline_execution.log
│
├── reports/
│   └── report_[timestamp].json
│
├── data_ingestion_pipeline.py
│
└── README.md
```

---

# 📈 Business Value

This project demonstrates how modern organizations automate data collection pipelines for analytics and reporting systems.

Key benefits include:

- Eliminates manual data collection
- Provides reliable daily updates
- Supports real-time BI reporting
- Reduces duplicate storage writes
- Maintains historical records
- Enables scalable analytics workflows

---

# 📊 BI Tool Integration

The generated `latest.csv` files can be connected directly into:

- Microsoft Excel
- Power BI
- Tableau

using GitHub raw file URLs.

## Example Workflow

### Excel / Power Query

1. Open GitHub raw CSV URL
2. Copy raw file link
3. Excel → Data → From Web
4. Paste URL
5. Refresh anytime for live updates

---

# 🧠 Skills Demonstrated

- ETL Pipeline Development
- Data Engineering
- API Integration
- Workflow Automation
- CI/CD Pipelines
- GitHub Actions
- Change Data Capture (CDC)
- Data Validation
- Logging & Monitoring
- Data Warehousing
- Cloud Automation
- Version Control
- Business Intelligence Integration

---

# 📸 Recommended Screenshots

Add these screenshots to improve portfolio quality:

- GitHub Actions workflow success
- Pipeline execution logs
- Generated CSV outputs
- Folder structure
- Power BI dashboard connection
- Historical snapshot examples

---

# 🎯 Future Improvements

Potential enhancements for future versions:

- Docker containerization
- AWS S3 or Azure Blob storage
- Apache Airflow orchestration
- Data quality monitoring
- Email alert system
- Snowflake or BigQuery integration
- Stream processing support
- Unit & integration testing

---

# 👨‍💻 Author

Developed by Jumma Mohammad  
Aspiring Data Engineer & Data Analyst focused on automation, cloud pipelines, analytics engineering, and business intelligence.

---

# ⭐ Project Highlights

✅ Fully Automated ETL Pipeline  
✅ Serverless Daily Execution  
✅ Multi-Source Data Ingestion  
✅ Production-Style Architecture  
✅ Change Detection with MD5 Hashing  
✅ Historical Data Versioning  
✅ BI Tool Integration Ready  
✅ Real-World Data Engineering Workflow
