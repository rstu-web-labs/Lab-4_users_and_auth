import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SendMail:
    def __init__(
        self,
        sender_email="моя почта",
        receiver_email="необходимый легко передать",
        password="не скажу",
        server="smtp.yandex.ru",
        port=587,
    ):
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.password = password
        self.server = server
        self.port = port

    def _connect(self):
        self.smtp = smtplib.SMTP(self.server, self.port)
        self.smtp.starttls()
        self.smtp.login(self.sender_email, self.password)

    def send_confirm(self, message, subject):
        self._connect()

        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = self.receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message))

        self.smtp.sendmail(self.sender_email, self.receiver_email, msg.as_string())
        self.smtp.quit()

    def send_excel(self, file_name, message, subject):
        self._connect()

        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = self.receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message))

        reports_dir = os.path.join(os.getcwd(), "reports")
        file_path = os.path.join(reports_dir, file_name)

        with open(file_path, "rb") as file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file.read())

        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{file_name}"')
        msg.attach(part)

        self.smtp.sendmail(self.sender_email, self.receiver_email, msg.as_string())
        self.smtp.quit()
