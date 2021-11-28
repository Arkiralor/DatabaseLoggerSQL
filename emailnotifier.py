import os
import smtplib

from dotenv import load_dotenv

load_dotenv()

class EmailNotifier():
    def __init__(self):
        self.mail_server = os.environ.get('mail_server')
        self.server_port = int(os.environ.get('server_port'))

        self.server = smtplib.SMTP_SSL(self.mail_server, self.server_port)

        self.serveruid = os.environ.get('username')
        self.server_app_password = os.environ.get('password')
        self.app_name = os.environ.get('email_app_name')

    def mail_notifier(self, msg: str):

        message = msg

        try:
            self.server.login(self.serveruid, self.server_app_password)

            self.server.sendmail(
                os.environ.get('sender_email'),
                os.environ.get('recipient_email'),
                message
            )

            self.server.quit()

            # print({'email': True})
            # return {'email': True}
        except Exception as e:
            print({'Error': f'{e}; Could not send email.'})

            self.server.quit()

            # print({'email': False, 'error': str(e)})
            # return {'email': False, 'error': str(e)}
