from flask import Flask, request, render_template
import imaplib
import email
from bs4 import BeautifulSoup
import re

# Gmail IMAP settings
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993

# Your Gmail credentials
GMAIL_USERNAME = 'harounjiha@gmail.com'
GMAIL_PASSWORD = 'gxpd uxdo bnim rtnd'  # Create an App Password for your Gmail account

# Initialize Flask app
app = Flask(__name__)

# Function to check for new emails, verify the email, and return the link
def check_emails_and_send_info(user_email):
    try:
        # Connect to Gmail
        imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        imap.login(GMAIL_USERNAME, GMAIL_PASSWORD)
        imap.select('inbox')

        # Search for the latest unread email
        status, email_ids = imap.search(None, 'UNSEEN', 'ALL')

        if status == 'OK':
            email_ids = email_ids[0].split()
            if email_ids:
                # Fetch the latest email (use email_ids[-1])
                latest_email_id = email_ids[-1]
                status, email_data = imap.fetch(latest_email_id, '(RFC822)')

                if status == 'OK':
                    raw_email = email_data[0][1]

                    # Parse the email
                    msg = email.message_from_bytes(raw_email)

                    # Initialize variables to store the link and email address
                    link = None
                    email_address = None

                    # Iterate through message parts
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        if "attachment" not in content_disposition:
                            if content_type == "text/plain" or content_type == "text/html":
                                charset = part.get_content_charset()
                                if charset is None:
                                    charset = 'utf-8'
                                try:
                                    email_content = part.get_payload(decode=True).decode(charset, errors="ignore")

                                    # Use regular expressions to find the link and email address
                                    link_match = re.search(r'https://accounts\.epicgames\.com/resetPassword\?code=[^\s]+', email_content)
                                    email_match = re.search(r'(\S+@\S+\.mozmail\.com)', email_content)

                                    if link_match:
                                        link = link_match.group(0)
                                    if email_match:
                                        email_address = email_match.group(1)

                                    # If both link and email address are found, break the loop
                                    if link and email_address:
                                        break
                                except AttributeError:
                                    pass

                    # Verify if the user's entered email matches the retrieved email
                    if email_address and user_email == email_address:
                        return link if link else None

                # Logout from Gmail
                imap.logout()

    except Exception as e:
        pass

    return None

# Route for the root URL
@app.route("/")
def index():
    return render_template("index.html", link=None)

# Route for handling the form submission and email verification
@app.route("/verify_email", methods=["POST"])
def verify_email():
    user_email = request.form["email"]
    link = check_emails_and_send_info(user_email)
    return render_template("index.html", link=link)

if __name__ == "__main__":
    app.run(debug=True, port=8080)

