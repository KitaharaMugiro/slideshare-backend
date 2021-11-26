import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

user_pool_id = os.getenv("USER_POOL_ID")
source_mail = os.getenv("SOURCE_MAIL")
htmls = {"ConfirmationForSubscribing": "ConfirmationForSubscribing.html"}
# SESでメールを送信するためのハンドラ
def send_email(USER_NAME, TYPE, TITLE, DATE, URL):
    # cognitoからユーザー情報を取得
    client = boto3.client("cognito-idp")
    response = client.admin_get_user(UserPoolId=user_pool_id, Username=USER_NAME)

    attributes = response.pop("UserAttributes")
    print(attributes)
    email = None
    for attribute in attributes:
        if attribute["Name"] == "email":
            email = attribute["Value"]
            break
    print(email)
    if email is None:
        raise Exception("Email is not registered")

    # HTMLを構成
    filename = htmls[TYPE]
    filepath = os.path.join("html", filename)
    with open(filepath) as f:
        html_body = f.read()
    if TYPE == "ConfirmationForSubscribing":
        html_body = html_body.replace("$TITLE", TITLE)
        html_body = html_body.replace("$DATE", DATE)
        html_body = html_body.replace("$URL", URL)
    print(html_body)

    # メールタイトル
    subject = None
    if TYPE == "ConfirmationForSubscribing":
        subject = f"【PresenShare】" + TITLE + "にご参加ありがとうございます"

    ses_client = boto3.client("ses")
    # メールを送信する
    ses_client.send_email(
        Source=source_mail,
        Destination={
            "ToAddresses": [
                email,
            ]
        },
        Message={
            "Subject": {"Data": subject, "Charset": "UTF-8"},
            "Body": {
                "Text": {"Data": html_body, "Charset": "UTF-8"},
                "Html": {"Data": html_body, "Charset": "UTF-8"},
            },
        },
    )
