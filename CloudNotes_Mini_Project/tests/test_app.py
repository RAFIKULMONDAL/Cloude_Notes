import json
import tempfile
import unittest
from pathlib import Path
import app as cloudnotes


class CloudNotesTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        cloudnotes.DATA_FILE = Path(self.temp_dir.name) / "notices.json"
        cloudnotes.app.config["TESTING"] = True
        self.client = cloudnotes.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"CloudNotes", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_add_notice_saves_to_json(self):
        response = self.client.post("/add", data={
            "title": "Library timing",
            "message": "The library closes at 6 PM.",
            "category": "Academic"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Library timing", response.data)
        stored = json.loads(cloudnotes.DATA_FILE.read_text(encoding="utf-8"))
        self.assertEqual(len(stored), 1)
        self.assertEqual(stored[0]["category"], "Academic")

    def test_empty_title_rejected(self):
        response = self.client.post("/add", data={"title": "", "message": "A message"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please enter a title", response.data)
        self.assertEqual(cloudnotes.load_notices(), [])

    def test_empty_message_rejected(self):
        response = self.client.post("/add", data={"title": "A title", "message": ""}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please enter a message", response.data)

    def test_unknown_page_returns_404(self):
        response = self.client.get("/does-not-exist")
        self.assertEqual(response.status_code, 404)

    def test_api_returns_json_list(self):
        response = self.client.get("/api/notices")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_delete_notice(self):
        self.client.post("/add", data={"title": "Temporary", "message": "Remove me", "category": "General"})
        notices = cloudnotes.load_notices()
        response = self.client.post(f"/delete/{notices[0]['id']}", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(cloudnotes.load_notices(), [])


if __name__ == "__main__":
    unittest.main()
