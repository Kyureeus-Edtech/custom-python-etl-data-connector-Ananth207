# ThreatFox Data Connector

---
- **Student Name:** Ananth Narayanan P
- **Roll Number:** 3122 22 5001 010
- **Dept:** CSE-A
---

## 📋 Overview

This Python script is an ETL (Extract, Transform, Load) pipeline that connects to the **ThreatFox API** by abuse.ch. It extracts recent threat intelligence data, transforms it by adding an ingestion timestamp, and loads it into a specified MongoDB collection.

This project was developed as part of the Software Architecture assignment for SSN CSE, in collaboration with Kyureeus EdTech.

---

## ⚙️ API Details

-   **Provider**: ThreatFox (abuse.ch)
-   **Endpoint Used**: `https://threatfox.abuse.ch/export/json/recent/`
-   **Authentication**: None required for this public endpoint.
-   **Data Format**: JSON

The script fetches indicators of compromise (IOCs) added in the last 7 days.

---

## 🚀 How to Run

### 1. Prerequisites

-   Python 3.8+
-   Access to a MongoDB database (like MongoDB Atlas).

### 2. Setup

1.  **Clone the repository** and navigate into your project folder.

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Credentials**:
    -   Create a file named `.env` in the project root.
    -   Copy the contents from the example below and replace the placeholder with your **actual MongoDB connection string**.

    ```env
    # .env file
    API_URL="[https://threatfox.abuse.ch/export/json/recent/](https://threatfox.abuse.ch/export/json/recent/)"
    MONGO_URI="mongodb+srv://<username>:<password>@<cluster-url>/<db-name>?retryWrites=true&w=majority"
    DB_NAME="threat_intelligence"
    COLLECTION_NAME="threatfox_raw"
    ```

### 3. Execute the Script

Run the ETL pipeline from your terminal:
```bash
python etl_connector.py
```

---

## 🗃️ MongoDB Output

The script will load documents into the `threatfox_raw` collection within the `threat_intelligence` database. Each document will be a threat record from the API, with an added `ingestion_timestamp` field.

**Example Document in MongoDB:**

```json
{
  "_id": "...",
  "ioc_id": "12345",
  "ioc_value": "some-malicious-domain.com",
  "ioc_type": "domain",
  "threat_type": "malware",
  "threat_type_desc": "Represents malware C2 infrastructure.",
  "malware": "SomeMalware",
  "malware_printable": "SomeMalware",
  "malware_alias": null,
  "malware_malpedia": "[https://malpedia.caad.fkie.fraunhofer.de/details/win.some_malware](https://malpedia.caad.fkie.fraunhofer.de/details/win.some_malware)",
  "confidence_level": 100,
  "first_seen_utc": "2025-08-14 00:20:00",
  "last_seen_utc": null,
  "reference": "[https://some-threat-report.com/report](https://some-threat-report.com/report)",
  "reporter": "some_security_researcher",
  "tags": ["C2"],
  "ingestion_timestamp": "2025-08-14T00:30:02.123456Z"
}
```