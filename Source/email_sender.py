import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(from_address, to_address, subject, body, smtp_server, smtp_port, login, password):
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(login, password)
        server.sendmail(from_address, to_address, msg.as_string())
        server.quit()
        return "Претензия успешно отправлена!"
    except Exception as e:
        return  f"Ошибка: {e}"

print(send_email('XXX@mail.ru', 'XXX@yandex.com',
                 'clims', 'XXX','smtp.mail.ru', 587,
                 'XXX', 'XXX'))
