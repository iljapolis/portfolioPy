from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
import requests
import smtplib
from email.mime.text import MIMEText


load_dotenv()

app = Flask(__name__)

# Replace with your secret key from Google reCAPTCHA
RECAPTCHA_SECRET_KEY = '6Lf-6WoqAAAAAE15SbGfuKPCeGJM13Ex9mPgquvU'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    # Verify reCAPTCHA
    recaptcha_response = request.form['g-recaptcha-response']
    data = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()

    # Check if reCAPTCHA was successful
    if result['success']:
        # Process form data if reCAPTCHA was successful
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        try:
            sender_email = 'iljapolis.225@gmail.com'
            receiver_email = os.getenv("EMAIL_ADDRESS")
            password = os.getenv("GMAIL_APP_PASSWORD")

            msg = MIMEText(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")
            msg['Subject'] = f"New message from {name}"
            msg['From'] = sender_email
            msg['To'] = receiver_email

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.send_message(msg)

            return redirect(url_for('home', success=True))
        except Exception as e:
            print(f"Error: {e}")
            return redirect(url_for('home', success=False))
    else:
        # If reCAPTCHA failed, redirect back with an error
        return redirect(url_for('home', success=False, recaptcha_failed=True))

if __name__ == '__main__':
    app.run(debug=True)
