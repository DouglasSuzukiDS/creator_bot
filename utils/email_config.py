from dataclasses import dataclass
import os

@dataclass
class EmailConfig:
  SMTP_SERVER: str
  SMTP_PORT: int
  EMAIL_USER: str | None
  EMAIL_PASSWORD: str | None
  EMAIL_RECIPIENT: str | None

def email_config() -> EmailConfig:
   return EmailConfig(
      SMTP_SERVER = os.getenv('SMTP_SERVER'),
      SMTP_PORT = int(os.getenv('SMTP_PORT')),
      EMAIL_USER = os.getenv('EMAIL_USER'),
      EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD'),
      EMAIL_RECIPIENT= os.getenv('EMAIL_RECIPIENT')
   )