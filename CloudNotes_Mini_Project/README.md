# CloudNotes — Cloud Computing Mini Project

A polished, responsive campus notice board built with Python Flask, HTML, CSS, and JavaScript. This version is designed to run locally at **zero cost**, without an AWS account, credit card, Docker, paid API, or external database.

## Features

- Publish campus notices with a title, message, and category.
- View notices in a responsive card-based interface.
- Search notices and filter by category.
- Sort notices newest-first or oldest-first.
- Delete notices.
- Store notices in `notices.json`, so they remain after the app restarts.
- Validate empty/oversized inputs.
- Health endpoint (`/health`) and JSON endpoint (`/api/notices`).
- Friendly 404 page and eight automated tests.
- Responsive layout for desktop and mobile.

## Requirements

- Python 3.10 or newer
- VS Code (recommended) or any code editor
- Internet is only needed once to install Flask; after installation, the app itself runs locally.

## Run on Windows

1. Extract `CloudNotes_Mini_Project.zip`.
2. Open the extracted `CloudNotes_Mini_Project` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Check Python:

   ```powershell
   py --version
   ```

   If `py` is not recognized, try `python --version`. If neither works, install Python from https://www.python.org/downloads/ and select **Add Python to PATH** during setup.

5. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

   If you used `python` in step 4, use `python -m venv .venv`.

6. Activate it in PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run this for the current terminal only, then activate again:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

7. Install Flask:

   ```powershell
   python -m pip install -r requirements.txt
   ```

8. Start the app:

   ```powershell
   python app.py
   ```

9. Open **http://127.0.0.1:5000** in your browser.

Keep the terminal open while you use the app. Press `Ctrl+C` in the terminal to stop it.

## Test the project

In a second terminal with the virtual environment activated:

```powershell
python -m unittest discover -s tests -v
```

Eight tests cover the home page, health endpoint, adding a notice, invalid inputs, 404 handling, JSON API, and deleting a notice.

## Project structure

```text
CloudNotes_Mini_Project/
├── app.py                 # Flask routes, validation, JSON persistence
├── requirements.txt       # Python dependency
├── notices.json           # Local notice storage (starts empty)
├── templates/
│   ├── index.html         # Main notice board
│   └── 404.html           # Not-found page
├── static/
│   ├── style.css          # Responsive visual design
│   └── app.js             # Search, filters, sorting, modal interactions
└── tests/
    └── test_app.py        # Automated tests
```

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Display the notice board |
| POST | `/add` | Validate and save a notice |
| POST | `/delete/<notice_id>` | Delete a notice |
| GET | `/health` | Return a simple health status |
| GET | `/api/notices` | Return stored notices as JSON |

## How it relates to Cloud Computing

This local version demonstrates the application layer and basic persistence. The original project guide describes a cloud deployment using AWS EC2, Docker, Amazon S3, IAM, Security Groups, CloudWatch, and SNS. Those cloud services are **not configured by this local ZIP**.

If your instructor requires actual AWS evidence, ask whether the college provides an AWS lab account or approved credits before proceeding. Do not claim an AWS deployment, S3 persistence, CloudWatch metrics/logs, or SNS alerts until you have actually configured and tested them.

## Cost and privacy

- The application code has no paid services or paid APIs.
- No AWS account or credit card is needed to run locally.
- Flask and Python are free to use.
- Installing Flask requires internet access once.
- Notices are stored in the local `notices.json` file on your computer.
- The built-in Flask development server is intended for local demonstration, not public production hosting.

## Suggested demo

1. Open the home page and show the responsive notice board.
2. Publish a notice under the Academic or Events category.
3. Search for part of the notice title.
4. Filter by category and change the sort order.
5. Refresh the page and show that the notice remains saved.
6. Open `/health` and `/api/notices`.
7. Run the automated tests.
8. Take screenshots of the real results for your report.
