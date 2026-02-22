from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('.', path)

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
RECEIVER_EMAIL = "dilfarasheed5@gmail.com"

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        if not all([name, email, message]):
            return jsonify({"status": "error", "message": "Missing fields"}), 400

        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"New Portfolio Message from {name}"

        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
        except smtplib.SMTPAuthenticationError:
            return jsonify({"status": "error", "message": "Email Login Failed. Check your App Password."}), 500
        except Exception as smtp_err:
            return jsonify({"status": "error", "message": f"SMTP Error: {str(smtp_err)}"}), 500

        return jsonify({"status": "success", "message": "Email sent successfully"}), 200

    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({"status": "error", "message": "Backend error occurred."}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
