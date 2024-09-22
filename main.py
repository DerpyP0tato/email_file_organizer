import imaplib
import os
import email
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from passwrd import passw

# Server to sign into email
host = 'imap.gmail.com'
username = 'max.code.email@gmail.com'
password = passw

mail = imaplib.IMAP4_SSL(host)
mail.login(username, password)
mail.select('inbox')
my_message = []

# Google Authentication
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# path for folder
path = '/Users/maxma/OneDrive/Desktop/Coding/Projects/Emails/Email File Organizer'

filenames = []


# searches all mail
_, search_data = mail.search(None, 'ALL')

# checks every email
for num in search_data[0].split():
    email_data = {}
    # fetch email, dont know what (RFC822) mean
    _, data = mail.fetch(num, '(RFC822)')
    # gets email data
    _, b = data[0]
    email_message = email.message_from_bytes(b)
    for header in ['subject']:
        # Email subject filter
        if str(email_message['Subject']).lower() == 'form':
            # filter emails
            if 'max.code.email@gmail.com' in email_message['From']:
                # gets and filter message content
                for part in email_message.walk():
                    mail_content = ''
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    fileName = part.get_filename()
                    if bool(fileName):
                        filePath = os.path.join(path, fileName)
                        # writes/download file
                        if not os.path.isfile(filePath):
                            fp = open(filePath, 'wb')
                            fp.write(part.get_payload(decode=True))
                            fp.close()
                        subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
                        print('Downloaded "{file}" from email titled "{subject}".'.format(
                                file=fileName,
                                subject=subject
                            ))
                        filenames.append(fileName)

# make a for loop to look through the folder
# uploads files
for upload_file in filenames:
    gfile = drive.CreateFile({'parents': [{'id': 'Nope :)'}]})
    gfile.SetContentFile(upload_file)
    gfile.Upload()
    gfile = None
    print('Uploaded:', upload_file)

# deletes files
for file in filenames:
    print("DELETING:", file)
    os.remove(file)

