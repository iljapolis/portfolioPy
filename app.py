from flask import Flask, render_template, request
from flask import redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    try:
        # Email Configuration
        sender_email = 'ilja.polis225@gmail.com'
        receiver_email = 'ilja.polis225@gmail.com'  # This could be the same as the sender
        password = 'mgio tpaj hjjg nmke'  # Use an app password if using Gmail

        # Create the email content
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"New Message from {name}"

        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the Gmail server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        return redirect(url_for('home', success=True))

    except Exception as e:
        print(f"Error: {e}")
        return redirect(url_for('home', success=False))

if __name__ == '__main__':
    app.run(debug=True)