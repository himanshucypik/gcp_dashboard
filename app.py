# app.py
from flask import Flask, render_template, jsonify, request
from google.oauth2 import service_account
from googleapiclient import discovery
from google.cloud import storage
import google.auth
import subprocess
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
print("Using credentials:", credentials_path)

app = Flask(__name__)

# Initialize storage client if creds exist
if credentials_path and os.path.exists(credentials_path):
	client = storage.Client.from_service_account_json(credentials_path)
	for bucket in client.list_buckets():
		print(bucket.name)


# Helper: get credentials
def get_credentials():
	key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
	if key_path and os.path.exists(key_path):
		creds = service_account.Credentials.from_service_account_file(
			key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
		)
		return creds
	creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
	return creds


# Root page (frontend)
@app.route("/")
def index():
	return render_template("index.html")


# API: list compute instances
@app.route("/api/instances")
def list_instances():
	project = request.args.get("project")
	if not project:
		return jsonify({"error": "project param required (e.g. ?project=micro-answer-471809 )"}), 400
	creds = get_credentials()
	compute = discovery.build("compute", "v1", credentials=creds, cache_discovery=False)

	instances = []
	req = compute.instances().aggregatedList(project=project)
	while req is not None:
		resp = req.execute()
		items = resp.get("items", {})
		for zone, zone_info in items.items():
			for inst in zone_info.get("instances", []) if zone_info else []:
				instances.append({
					"name": inst.get("name"),
					"id": inst.get("id"),
					"zone": zone.split("/")[-1],
					"machineType": inst.get("machineType", "").split("/")[-1],
					"status": inst.get("status"),
					"internalIP": next((ni["networkIP"] for ni in inst.get("networkInterfaces", []) if ni.get("networkIP")), None),
					"externalIP": next((
						a["natIP"] for ni in inst.get("networkInterfaces", []) for a in ni.get("accessConfigs", []) if a.get("natIP")
					), None),
				})
		req = compute.instances().aggregatedList_next(previous_request=req, previous_response=resp)
	return jsonify(instances)


# API: list buckets
@app.route("/api/buckets")
def list_buckets():
	project = request.args.get("project")
	if not project:
		return jsonify({"error": "project param required (e.g. ?project=my-project-id)"}), 400

	creds = get_credentials()
	client = storage.Client(project=project, credentials=creds)
	buckets = []
	for b in client.list_buckets():
		buckets.append({
			"name": b.name,
			"location": b.location,
			"storageClass": b.storage_class,
			"timeCreated": b.time_created.isoformat() if b.time_created else None
		})
	return jsonify(buckets)


# API: list projects
@app.route("/api/projects")
def list_projects():
	creds = get_credentials()
	crm = discovery.build("cloudresourcemanager", "v1", credentials=creds, cache_discovery=False)
	projects = []
	req = crm.projects().list()
	while req:
		resp = req.execute()
		for p in resp.get("projects", []):
			projects.append({
				"projectId": p.get("projectId"),
				"name": p.get("name"),
				"state": p.get("lifecycleState"),
			})
		req = crm.projects().list_next(previous_request=req, previous_response=resp)
	return jsonify(projects)


# Health check API
@app.route("/api/health", methods=["GET"])
def health_check():
	return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
