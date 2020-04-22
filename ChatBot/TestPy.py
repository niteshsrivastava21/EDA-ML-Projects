import smtplib
import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(email_addr):
    config = configparser.ConfigParser()
    config.read("config.ini")
    host_name = config["email_params"]["host"]
    port_num = int(config["email_params"]["port"])
    user_name = config["email_params"]["user"]
    password = config["email_params"]["password"]
    subject = config["email_params"]["subject"]
    message_template = open("email_body.html").read()
    # message_template="Dear PERSON_NAME, how are you?"
    msg = MIMEMultipart()  # create a message
    # add in the actual person name to the message template
    message = message_template.replace("PERSON_NAME", "Raju Re")
    msg['Subject'] = subject
    msg['From'] = user_name
    msg['To'] = email_addr
    msg.attach(MIMEText(message, 'html'))
    session = smtplib.SMTP('smtp.mail.yahoo.com', 587)  # use gmail with port
    print(session.ehlo())
    session.starttls()  # enable security
    session.login("getanshu_21feb@yahoo.com", "cqtqcpaoshqyloug")  # login with mail_id and password
    text = msg.as_string()
    session.sendmail("getanshu_21feb@yahoo.com", "niteshsrivastava21@gmail.com", text)
    # session.send_message(text)
    session.quit()
