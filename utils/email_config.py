from dataclasses import dataclass
import os

@dataclass
class EmailConfig:
  servidor_smtp: str
  porta_smtp: int
  email_remetente: str | None
  senha_app: str | None

def email_config() -> EmailConfig:
   return EmailConfig(
      servidor_smtp = os.getenv('SMTP_SERVER'),
      porta_smtp = int(os.getenv('SMTP_PORT')),
      email_remetente = os.getenv('EMAIL_USER'),
      senha_app = os.getenv('EMAIL_PASSWORD')
   )