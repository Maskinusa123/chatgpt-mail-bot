import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import openai
from datetime import datetime

# GitHub Secrets
EMAIL_ADDRESS = os.environ['EMAIL_ADDRESS']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
TO_EMAIL = os.environ['TO_EMAIL']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

openai.api_key = OPENAI_API_KEY

# 生成 ChatGPT 内容
prompt = "请用中文概述过去24小时的全球重大新闻，尽量简洁明了，包含标题和来源。"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "你是新闻摘要助手"},
        {"role": "user", "content": prompt}
    ],
    max_tokens=600,
    temperature=0.7
)

news_content = response['choices'][0]['message']['content']

# 邮件发送
subject = f"每日全球新闻摘要 - {datetime.utcnow().strftime('%Y-%m-%d')}"
msg = MIMEMultipart()
msg['From'] = EMAIL_ADDRESS
msg['To'] = TO_EMAIL
msg['Subject'] = subject
msg.attach(MIMEText(news_content, 'plain'))

server = smtplib.SMTP('smtp.office365.com', 587)
server.starttls()
server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
server.send_message(msg)
server.quit()
print("邮件发送成功！")
