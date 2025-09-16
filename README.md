readme_content = """# GCP Dashboard (Flask + GCP APIs)

A simple Flask-based dashboard to interact with **Google Cloud Platform (GCP)** services like:

- ✅ List Compute Engine Instances
- ✅ List GCS Buckets
- ✅ List Projects
- ✅ Health Check API

---

## 📂 Project Structure
gcp_dashboard/
│── app.py # Main Flask application
│── templates/
│ └── index.html # Frontend (basic dashboard)
│── .env # Environment variables (GCP creds path)
│── requirements.txt # Dependencies

yaml
Always show details

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd gcp_dashboard
2. Create a virtual environment
bash
Always show details


python3 -m venv venv
source venv/bin/activate
3. Install dependencies
bash
Always show details


pip install -r requirements.txt
4. Setup Google Cloud Credentials
Create a Service Account in GCP Console

Assign roles:

Viewer (for projects)

Compute Viewer (for instances)

Storage Admin or Storage Viewer (for buckets)

Download JSON key file.

5. Configure .env
Create .env file in project root:

env
Always show details


GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/your/service-account.json
PORT=8080
🚀 Run the App
bash
Always show details


python3 app.py
App will start at:
👉 http://127.0.0.1:8080

📡 API Endpoints
1. Health Check
bash
Always show details


GET /api/health
Response:

json
Always show details


{"status": "ok"}
2. List Projects
bash
Always show details


GET /api/projects
Response:

json
Always show details


[
  {"projectId": "my-project-123", "name": "My Test Project", "state": "ACTIVE"},
  {"projectId": "analytics-001", "name": "Analytics Project", "state": "ACTIVE"}
]
3. List Instances
bash
Always show details


GET /api/instances?project=<PROJECT_ID>
Response:

json
Always show details


[
  {"name": "instance-1", "zone": "us-central1-a", "status": "RUNNING"},
  {"name": "instance-2", "zone": "us-central1-b", "status": "TERMINATED"}
]
4. List Buckets
bash
Always show details


GET /api/buckets?project=<PROJECT_ID>
Response:

json
Always show details


[
  {"name": "my-bucket-1", "location": "US", "storageClass": "STANDARD"},
  {"name": "backup-bucket", "location": "EU", "storageClass": "NEARLINE"}
]
🛠 Troubleshooting
403 Permission Error → Make sure required APIs are enabled:

Cloud Resource Manager API

Compute Engine API

Cloud Storage API

Invalid Credentials → Check .env path matches your JSON file.

📌 Requirements
Put this inside requirements.txt:

nginx
Always show details


Flask
python-dotenv
google-auth
google-auth-oauthlib
google-api-python-client
google-cloud-storage
