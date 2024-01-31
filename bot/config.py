from dotenv import load_dotenv
from pydantic.v1 import BaseSettings, SecretStr

load_dotenv()


class AppConfig(BaseSettings):
    """A class that contains data from an environment file"""

    bot_token: SecretStr

    class Config:
        """A class that contains reading data from an environment file"""

        env_file = ".env"
        env_file_encoding = "utf-8"


app_config = AppConfig()
