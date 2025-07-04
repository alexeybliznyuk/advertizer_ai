import os
import sys
from functools import cached_property
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError

project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(project_directory)
print(project_directory)

if os.path.exists(f"{project_directory}/.env"):
    sender_service_env = f"{project_directory}/global/services/sender-service.env"
else:
    sender_service_env = "/app/settings/sender-service.env"


class Settings(BaseSettings):
    # Database settings
    SENDER_DB_HOST: str = "localhost"
    SENDER_DB_PORT: int = 5432
    SENDER_DB_NAME: str = "sender_db"
    SENDER_DB_USER: str = "sender_user"
    SENDER_DB_PASS: str = "sender_password"
    
    # Service settings
    SENDER_SERVICE_PORT: int = 8007
    
    # Email settings (if needed for sending functionality)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASS: str = ""
    
    # DeepSeek AI settings
    COURSE_STRUCTURE_AI_API_KEY: str 
    COURSE_STRUCTURE_AI_REQUESTS_URL: str 

    model_config = SettingsConfigDict(env_file=sender_service_env)


settings = Settings() 