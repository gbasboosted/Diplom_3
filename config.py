import os


BASE_URL = os.getenv(
    "STELLAR_BURGERS_URL", "https://stellarburgers.education-services.ru"
).rstrip("/")
WAIT_TIMEOUT = float(os.getenv("UI_WAIT_TIMEOUT", "20"))
PAGE_LOAD_TIMEOUT = float(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
API_TIMEOUT = float(os.getenv("API_TIMEOUT", "20"))
ORDER_TIMEOUT = float(os.getenv("ORDER_TIMEOUT", "60"))
