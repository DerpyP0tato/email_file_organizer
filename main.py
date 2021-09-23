import imaplib
import email

host = 'imap.gmail.com'
username = 'max.code.email@gmail.com'
password = 'MaxwellChan01'

mail = imaplib.IMAP4_SSL(host)
mail.login(username, password)
mail.select('inbox')
my_message = []

_, search_data = mail.search(None, 'ALL')

for num in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(num, '(RFC822)')
        # print(data[0])
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        for header in ['subject']:
            if email_message['Subject'] == 'Form' or 'form':
                if 'max.code.email@gmail.com' in email_message['From']:
                    if email_message.is_multipart():
                        mail_content = ''
                        for part in email_message.get_payload():
                            if part.get_content_type() == 'text/plain':
                                mail_content += part.get_payload()
                                print(mail_content)
                    else:
                        mail_content = email_message.get_payload()
                        print(mail_content)
            else:
                print('False')
