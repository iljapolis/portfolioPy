import os
import re
from flask import Flask, request, redirect, url_for, render_template
import smtplib
from email.mime.text import MIMEText
import requests
from dotenv import load_dotenv

# Initialize Flask app and load environment variables
app = Flask(__name__)
load_dotenv()

# Email regex pattern for server-side validation
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    recaptcha_response = request.form['g-recaptcha-response']

    # Server-side email validation
    if not EMAIL_REGEX.match(email):
        return "Invalid email address. Please go back and enter a valid email.", 400

    # Verify reCAPTCHA
    recaptcha_verification = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={'secret': os.getenv('RECAPTCHA_SECRET_KEY'), 'response': recaptcha_response}
    )
    recaptcha_result = recaptcha_verification.json()
    if not recaptcha_result.get('success'):
        return "reCAPTCHA verification failed. Please try again.", 400

    # Process and send email if validation passes
    msg = MIMEText(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")
    msg['Subject'] = f"New message from {name}"
    msg['From'] = os.getenv('EMAIL_ADDRESS')
    msg['To'] = os.getenv('EMAIL_ADDRESS')

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(os.getenv('EMAIL_ADDRESS'), os.getenv('GMAIL_APP_PASSWORD'))
            server.send_message(msg)
        return redirect(url_for('home', success=True))
    except Exception as e:
        print(f"Error: {e}")
        return "There was an error sending your email. Please try again later.", 500

if __name__ == '__main__':
    app.run(debug=True)
