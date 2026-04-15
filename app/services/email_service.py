import resend
from app.core.config import settings

resend.api_key = settings.RESEND_API_KEY

async def send_reset_email(to_email: str, link: str):
    resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": to_email,
        "subject": "Reset Your Password",
        "html": f"""
        <p>Click below to reset password:</p>
        <a href="{link}">Reset Password</a>
        """
    })