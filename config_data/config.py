import os
from dotenv import load_dotenv, find_dotenv
if not find_dotenv():
    exit("Переменные окружения не загружены, так как отсутствует файл .env")
else:
    load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}
url = "https://realtor.p.rapidapi.com/properties/list-for-sale"
querystring = {"state_code": "", "city": "", "offset": "0", "limit": "10"}

