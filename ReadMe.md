# EmailAPI

EmailAPI is a Python module that provides a simple and easy-to-use interface for sending and fetching emails using the SMTP and IMAP protocols. It allows users to send emails and fetch emails from their email account with just a few lines of code.

## Features

- Send emails with an optional attachment
- Fetch emails from the inbox with optional search criteria
- Supports encrypted connections using TLS or SSL



## Usage

1. To use the EmailAPI class, first create an instance by passing in the server address, port number, username, and password.

```python
from EmailAPI import EmailAPI

email_api = EmailAPI('smtp.gmail.com', 587, 'example@gmail.com', 'password')

email_api.send_email('recipient@example.com', 'Hello', 'Hello World!', attachments=['file1.txt', 'file2.txt'])

emails = email_api.fetch_emails('FROM "sender@example.com"')


Note: You may need to adjust the import statement and module name based on your actual module name and file structure.

