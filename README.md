# ThreatFox ETL Data Connector

- **Student Name:** Ananth Narayanan P
- **Roll Number:** 3122 22 5001 010
- **Dept:** CSE-A
---
## 🚀 Overview

This project provides a robust ETL (Extract, Transform, Load) pipeline written in Python. It securely connects to the authenticated **ThreatFox API** by abuse.ch, extracts recent Indicators of Compromise (IOCs), enriches the data, and loads it into a MongoDB database.

This script was developed to meet the requirements of the SSN College of Engineering's Software Architecture assignment, focusing on secure, reliable, and test-driven development practices.

---

## 🛡️ Error Handling & Robustness

This ETL pipeline is built with resilience in mind and gracefully handles a variety of potential failures.

* **Invalid API Responses**: The script validates the API response at two levels. It first checks for **HTTP errors** (like `401 Unauthorized` for a bad API key or `500 Server Error`). It then inspects the JSON body for **API-specific error messages** (e.g., `query_status: "illegal_query"`), ensuring that only valid data proceeds to the next stage.

* **Connectivity Errors**: The entire network communication process is wrapped in `try...except` blocks. This means the script will not crash from a **failed API connection** (e.g., no internet) or a **failed MongoDB connection** (e.g., incorrect credentials, firewall block, or downed server). It will instead log the error and terminate gracefully.

* **Empty or Malformed Payloads**: The script is designed to handle cases where the API returns a successful status but no data (`"data": []`). Each stage of the pipeline checks if the data it received is valid and non-empty before processing, preventing unexpected errors.

* **Secure Credential Management**: All sensitive information (API keys, database URIs) is loaded securely from a local `.env` file. This file is explicitly listed in `.gitignore` to **prevent accidental commits of secrets** to the repository, following security best practices.

---

## ⚙️ Setup and Execution

Follow these steps to set up and run the ETL pipeline.

### Prerequisites

* Python 3.8+
* Access to a MongoDB database (e.g., MongoDB Atlas)
* A valid **Auth-Key** from the [abuse.ch Authentication Portal](https://bazaar.abuse.ch/user/login/)

### Installation

1.  **Clone the Repository**
    Clone the project to your local machine.

2.  **Create a Virtual Environment**
    It's highly recommended to use a virtual environment to manage dependencies.
    ```bash
    # Create the environment
    python -m venv venv

    # Activate the environment
    # On Windows: venv\Scripts\activate
    # On macOS/Linux: source venv/bin/activate
    ```

3.  **Install Dependencies**
    Install all required Python libraries from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    a. Create a new file named `.env` in the root of the project.

    b. Copy the content from `ENV_TEMPLATE` into your new `.env` file.

    c. Replace the placeholder values with your **actual secrets**.

    **Example `ENV_TEMPLATE` (for reference):**
    ```
    # ThreatFox API Configuration
    API_URL="[https://threatfox-api.abuse.ch/api/v1/](https://threatfox-api.abuse.ch/api/v1/)"
    THREATFOX_API_KEY="your_api_key_goes_here"
    QUERY_DAYS=7

    # MongoDB Configuration
    MONGO_URI="your_mongodb_connection_string"
    DB_NAME="threat_intelligence"
    COLLECTION_NAME="threatfox_raw"
    ```
    ⚠️ **Important**: The `.env` file is your secret store. **NEVER** commit it to Git.

### Running the Script

Execute the main connector script from your terminal.
```bash
python etl_connector.py
```
You will see log messages in the console indicating the progress of the Extract, Transform, and Load stages.

---

## 🗃️ Project Structure

* `etl_connector.py`: The main Python script containing the ETL logic.
* `requirements.txt`: A list of all Python dependencies for the project.
* `README.md`: This documentation file.
* `.gitignore`: Specifies files and directories that Git should ignore (like `.env` and `venv/`).
* `ENV_TEMPLATE`: A safe, committable template listing the required environment variables.
* `.env`: A local, untracked file for storing your secret credentials.