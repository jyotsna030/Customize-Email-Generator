import openai
import sendgrid
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

openai.api_key = OPENAI_API_KEY
sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)

def personalize_email(prompt: str, recipient_name: str, custom_data: dict):
    """
    Generate a personalized email using OpenAI GPT
    """
    input_prompt = prompt.format(name=recipient_name, **custom_data)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=input_prompt,
        max_tokens=150,
    )
    return response["choices"][0]["text"].strip()

def send_emails(dataframe, email_account, subject, prompt):
    """
    Send emails using SendGrid
    """
    statuses = []
    for _, row in dataframe.iterrows():
        recipient = row["email"]
        personalized_body = personalize_email(prompt, row["name"], row.to_dict())
        message = Mail(
            from_email=email_account,
            to_emails=recipient,
            subject=subject,
            plain_text_content=personalized_body,
        )
        try:
            response = sg.send(message)
            statuses.append({"email": recipient, "status": response.status_code})
        except Exception as e:
            statuses.append({"email": recipient, "status": str(e)})
    return statuses
