from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from pathlib import Path
import json
import os
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cloudnotes-local-demo-key")

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "notices.json"
MAX_TITLE = 100
MAX_MESSAGE = 500


def load_notices():
    """Load notices from a local JSON file; create an empty list if needed."""
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_notices(notices):
    """Persist notices locally. This works offline and costs nothing."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(notices, file, indent=2, ensure_ascii=False)


@app.get("/")
def home():
    notices = sorted(load_notices(), key=lambda n: n.get("created_at", ""), reverse=True)
    categories = ["General", "Academic", "Events", "Examination", "Placement", "Sports"]
    return render_template("index.html", notices=notices, categories=categories)


@app.post("/add")
def add_notice():
    title = request.form.get("title", "").strip()
    message = request.form.get("message", "").strip()
    category = request.form.get("category", "General").strip()
    allowed_categories = {"General", "Academic", "Events", "Examination", "Placement", "Sports"}

    if not title or len(title) > MAX_TITLE:
        flash("Please enter a title between 1 and 100 characters.", "error")
        return redirect(url_for("home"))
    if not message or len(message) > MAX_MESSAGE:
        flash("Please enter a message between 1 and 500 characters.", "error")
        return redirect(url_for("home"))
    if category not in allowed_categories:
        category = "General"

    now = datetime.now().astimezone()
    notices = load_notices()
    notices.append({
        "id": uuid.uuid4().hex[:10],
        "title": title,
        "message": message,
        "category": category,
        "created_at": now.isoformat(timespec="minutes"),
        "display_date": now.strftime("%d %b %Y"),
        "display_time": now.strftime("%I:%M %p").lstrip("0")
    })
    save_notices(notices)
    flash("Your notice has been published.", "success")
    return redirect(url_for("home"))


@app.post("/delete/<notice_id>")
def delete_notice(notice_id):
    notices = load_notices()
    remaining = [notice for notice in notices if notice.get("id") != notice_id]
    if len(remaining) == len(notices):
        flash("That notice could not be found.", "error")
    else:
        save_notices(remaining)
        flash("Notice deleted.", "success")
    return redirect(url_for("home"))


@app.get("/health")
def health():
    return jsonify(status="ok", app="CloudNotes")


@app.get("/api/notices")
def api_notices():
    return jsonify(load_notices())


@app.errorhandler(404)
def not_found(_error):
    if request.path.startswith("/api/") or request.path == "/health":
        return jsonify(error="Page not found"), 404
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
