import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from application.email_template import EmailTemplate

class EmailNotifier:
    def __init__(self):
        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env.local'))
        self.api_key = os.getenv("SENDGRID_API_KEY")
        self.sender_email = os.getenv("SENDER_EMAIL")

    def send_email(self, recipient_email: str, report_rows: list[dict | dict[str, str]]):
        html_body = EmailTemplate.build(report_rows)
        message = Mail(
            from_email=self.sender_email,
            to_emails=recipient_email,
            subject="TEST: Alerta de caída significativa en ETFs y acciones",
            html_content=html_body
        )
        try:
            # send_grid_client = SendGridAPIClient(self.api_key)
            # response = send_grid_client.send(message)
            # print(f"✅ Email enviado con estado {response.status_code}")
            with open("preview_email.html", "w", encoding="utf-8") as f:
                f.write(html_body)
            print("Previsualización guardada en preview_email.html")
        except Exception as e:
            print(f"❌ Error al enviar correo: {e}")