from flask import Flask, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GITHUB_USERNAME = "nima-samii"

@app.route("/projects")
def get_projects():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?sort=updated"
    headers = {
        "Accept": "application/vnd.github.mercy-preview+json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        filtered = [
            {
                "name": repo["name"],
                "description": repo["description"],
                "topics": repo.get("topics", []),
                "language": repo.get("language", "Code"),
                "html_url": repo["html_url"]
            }
            for repo in data if repo.get("description")
        ]
        return jsonify(filtered)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Portfolio API is running"

if __name__ == "__main__":
    app.run(debug=True)