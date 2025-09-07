import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openai import OpenAI

# 从 GitHub Secrets 获取环境变量
EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
TO_EMAIL = os.environ["TO_EMAIL"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# 初始化 OpenAI 客户端
client = OpenAI(api_key=OPENAI_API_KEY)

def get_news():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "请用中文总结过去24小时的全球重大新闻，每条简洁一点。"}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content

def send_email(subject, body, from_email, to_email, password):
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())

if __name__ == "__main__":
    news = get_news()
    send_email("过去24小时全球重大新闻", news, EMAIL_ADDRESS, TO_EMAIL, EMAIL_PASSWORD)
