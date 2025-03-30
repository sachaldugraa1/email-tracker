from flask import Flask, request, send_file
import datetime

app = Flask(__name__)

@app.route('/track')
def track_email():
    email = request.args.get('email')  # Get recipient email from URL
    with open("tracked_emails.txt", "a") as f:
        f.write(f"{email} - Opened at {datetime.datetime.now()}\n")

    # Return a 1x1 transparent pixel
    return send_file("pixel.png", mimetype='image/png')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
