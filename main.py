import imaplib
import os
from os import walk
import email
import pydrive
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

'''
https://www.projectpro.io/recipes/upload-files-to-google-drive-using-python
'''

host = 'imap.gmail.com'
username = 'max.code.email@gmail.com'
password = 'MaxwellChan01'

mail = imaplib.IMAP4_SSL(host)
mail.login(username, password)
mail.select('inbox')
my_message = []

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

path = '/Users/maxma/OneDrive/Desktop/Coding/Projects/Emails/Email File Organizer'

_, search_data = mail.search(None, 'ALL')

f = []
filenames = next(walk(path), (None, None, []))[2]

for num in search_data[0].split():
    email_data = {}
    _, data = mail.fetch(num, '(RFC822)')
    _, b = data[0]
    email_message = email.message_from_bytes(b)
    for header in ['subject']:
        if email_message['Subject'] == 'Form' or 'form':
            if 'max.code.email@gmail.com' in email_message['From']:
                for part in email_message.walk():
                    mail_content = ''
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    fileName = part.get_filename()
                    if bool(fileName):
                        filePath = os.path.join(path, fileName)
                        if not os.path.isfile(filePath):
                            if fileName[:3] == '.txt':
                                print('True')
                            else:
                                print('False')
                            #check for file extension
                            #find the folder for that file extension, if the folder doesn't exist, create a folder.
                            #find the path of the folder
                            #write the file to the folder
                            fp = open(filePath, 'wb')
                            fp.write(part.get_payload(decode=True))
                            fp.close()
                        subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
                        print('Downloaded "{file}" from email titled "{subject}".'.format(
                                file=fileName,
                                subject=subject
                                ))
                for upload_file in filenames:
                    gfile = drive.CreateFile({'parents': [{'id': '1Fy6scuzj-WD6ioKx_LFLxZ0itRKSZf1c'}]})
                    gfile.SetContentFile(upload_file)
                    gfile.Upload()
        else:
            print('Something went wrong')
