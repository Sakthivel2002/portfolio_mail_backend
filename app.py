from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://charming-quokka-d15fb8.netlify.app"]}}, supports_credentials=True)

EMAIL_USER = os.getenv('EMAIL_USER', 'sakthins20022002@gmail.com')
EMAIL_PASS = os.getenv('EMAIL_PASS', 'pzwh gmzy wiyt klta') 
TO_EMAIL = os.getenv('TO_EMAIL', 'sakthirollins175@gmail.com')

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Flask backend is running ✅"}), 200


@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject', 'New Contact Form Submission')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    try:
        # Email content
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject

        body = f"""
        You have a new message from your portfolio contact form:

        Name: {name}
        Email: {email}
        Subject: {subject}

        Message:
        {message}
        """

        msg.attach(MIMEText(body, 'plain'))

        # Send email via Gmail SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        return jsonify({'success': True}), 200

    except Exception as e:
        print('Error:', e)
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)




