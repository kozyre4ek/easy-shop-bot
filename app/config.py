from pydantic import BaseSettings

from webdriver_manager.chrome import ChromeDriverManager


class Settings(BaseSettings):
    telegram_token: str = "your-telegram-token"
    headers: dict = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    webdriver: str = ChromeDriverManager().install()


settings = Settings()