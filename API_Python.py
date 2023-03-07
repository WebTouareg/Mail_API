import smtplib
import imaplib
import email


"""
This module defines the EmailAPI class, which provides methods for sending and fetching emails using the SMTP and IMAP protocols.

Classes:
- EmailAPI: A class that allows users to send emails and fetch emails from their email account using the SMTP and IMAP protocols.

Usage:
1. To use the EmailAPI class, first create an instance by passing in the server address, port number, username, and password.
2. Use the send_email method to send an email with an optional attachment.
3. Use the fetch_emails method to retrieve emails from the inbox with optional search criteria.

Example:
    email_api = EmailAPI('smtp.gmail.com', 587, 'example@gmail.com', 'password')
    email_api.send_email('recipient@example.com', 'Hello', 'Hello World!')
    emails = email_api.fetch_emails('FROM "sender@example.com"')

Note to me: 587 is a port number used for secure email transmission. It supports 
encrypted connections using TLS (Transport Layer Security) or SSL (Secure Sockets Layer).
"""


class EmailAPI:
    def __init__(self, server, port, username, password):
        self.server = server
        self.port = port
        self.username = username
        self.password = password

    def send_email(self, recipient, subject, body, attachments=None):
        self._validate_input(recipient, subject, body)

        message = email.message.EmailMessage()
        message['Subject'] = subject
        message['From'] = self.username
        message['To'] = recipient
        message.set_content(body)

        if attachments:
            for attachment in attachments:
                self._add_attachment(message, attachment)

        self._send_email(message)

    def fetch_emails(self, search_criteria='ALL'):
        with self._get_imap_server() as server:
            server.select('inbox')

            result, data = server.search(None, search_criteria)
            ids = data[0].split()

            emails = []
            for id in ids:
                raw_email = self._fetch_email_body(server, id)
                email_message = email.message_from_bytes(raw_email)
                emails.append(email_message)

            return emails

    def _validate_input(self, recipient, subject, body):
        if not recipient or not isinstance(recipient, str):
            raise ValueError("Invalid recipient email address")
        if not subject or not isinstance(subject, str):
            raise ValueError("Invalid email subject")
        if not body or not isinstance(body, str):
            raise ValueError("Invalid email body")

    def _add_attachment(self, message, attachment):
        try:
            with open(attachment, 'rb') as file:
                data = file.read()
            message.add_attachment(data, maintype='application', subtype='octet-stream', filename=attachment)
        except FileNotFoundError:
            raise ValueError("Attachment file not found: {}".format(attachment))
        except Exception as e:
            raise Exception("Error adding attachment {}: {}".format(attachment, e))

    def _send_email(self, message):
        with smtplib.SMTP(self.server, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(message)

    def _get_imap_server(self):
        try:
            server = imaplib.IMAP4_SSL(self.server)
            server.login(self.username, self.password)
            return server
        except imaplib.IMAP4.error as e:
            raise Exception("Error connecting to email server: {}".format(e))
        except Exception as e:
            raise Exception("Error connecting to email server: {}".format(e))

    def _fetch_email_body(self, server, email_id):
        result, data = server.fetch(email_id, '(RFC822)')
        return data[0][1]
