import gspread
from oauth2client.service_account import ServiceAccountCredentials

def update_google_sheet(email):
    """ Update Google Sheet when email is opened """
    try:
        SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        CREDS_FILE = "ytscript.json"
        SPREADSHEET_ID = "1a5dLnc8gSCod5Uj_YsdRVYE6fOuDjeJx-F-Hfxd5O8Y"

        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SPREADSHEET_ID).sheet1
        data = sheet.get_all_records()

        for i, row in enumerate(data):
            if row["Email"] == email and row["Open Status"] != "Opened":
                sheet.update_cell(i + 2, 6, "Opened")  # Column 6 = Open Status
                break

    except Exception as e:
        print(f"❌ Google Sheets error: {e}")

@app.route('/track')
def track_email():
    email = request.args.get('email')
    update_google_sheet(email)

    return send_file("pixel.png", mimetype='image/png')
