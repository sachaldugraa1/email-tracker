import json
import os
import gspread
from flask import Flask, request, send_file
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# 🔹 Google Sheets Access
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
SPREADSHEET_ID = "1a5dLnc8gSCod5Uj_YsdRVYE6fOuDjeJx-F-Hfxd5O8Y"

# ✅ Load Google Credentials from Railway ENV
creds_json = os.getenv("GOOGLE_CREDENTIALS")

if not creds_json:
    raise ValueError("❌ GOOGLE_CREDENTIALS environment variable not found!")

try:
    creds_dict = json.loads(creds_json)  # ✅ JSON Convert Ho Raha Hai
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
    client = gspread.authorize(creds)
    print("✅ Google Credentials Loaded Successfully!")
except json.JSONDecodeError as e:
    raise ValueError(f"❌ Error Loading JSON: {e}")
except Exception as e:
    raise ValueError(f"❌ Google Sheets Authorization Failed: {e}")

def update_google_sheet(email):
    """ Update Google Sheet when email is opened """
    try:
        sheet = client.open_by_key(SPREADSHEET_ID).sheet1
        data = sheet.get_all_records()

        for i, row in enumerate(data):
            if row.get("Email") == email and row.get("Open Status") != "Opened":
                sheet.update_cell(i + 2, 6, "Opened")  # Column 6 = Open Status
                print(f"✅ Updated Open Status for: {email}")
                break
    except Exception as e:
        print(f"❌ Google Sheets error: {e}")

@app.route('/track')
def track_email():
    email = request.args.get('email')
    if not email:
        return "❌ Email parameter is missing", 400
    
    update_google_sheet(email)
    return send_file("pixel.png", mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
