# Установка всех необходимых пакетов перед импортами
import random
saveid = random.randint(0, 999999)
import os
os.system("pip install temp-mails requests beautifulsoup4 lxml websocket-client==1.7.0 aiohttp --quiet")

# Импорты
import asyncio
import aiohttp
import requests
from concurrent.futures import ThreadPoolExecutor
import json
import zlib
from temp_mails import Tenminutemail_one

def compress(input_string: str) -> str:
    try:
        input_data = input_string.encode('utf-8')
    except UnicodeEncodeError as e:
        print(f"Ошибка кодирования строки: {e}")
        return ""
    try:
        deflated_data = zlib.compress(input_data, level=9, wbits=-15)
    except zlib.error as e:
        print(f"Ошибка при сжатии Deflate: {e}")
        return ""
    hex_output = deflated_data.hex()
    return hex_output

def wait_email(mail):
    return mail.wait_for_new_email(delay=0.5, timeout=60)  # Уменьшен timeout и delay

async def makeaccount(session, proxy=None):
    mail = Tenminutemail_one()
    print(f"Создаём аккаунт с email: {mail.email}")
    url = "https://notegpt.io/user/register"
    payload = f"User%5Bemail%5D={mail.email}&User%5Bpassword%5D=12344321&User%5Bga_cid%5D="
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0 (Edition Yx GX)"
    }

    try:
        async with session.post(url, data=payload, headers=headers, proxy=proxy) as response:
            if response.status != 200:
                print(f"Ошибка {response.status} для {mail.email}")
                return None
            with ThreadPoolExecutor() as executor:
                data = await asyncio.get_event_loop().run_in_executor(executor, wait_email, mail)
            if data:
                mailm = mail.get_mail_content(data["id"])
                mailm = str(mailm.split("into browser:</p>")[1].split("</p>")[0]).replace("<p>", "").replace(" ", "")
                mailm = "http" + mailm.split("http")[1]
                async with session.get(mailm, proxy=proxy) as confirm_response:
                    set_cookies = confirm_response.cookies
                    jsready = {name: value for name, value in set_cookies.items()}
                    result = "; ".join([f"{key}={value}" for key, value in jsready.items()])
                    return result
            return None
    except aiohttp.ClientError as e:
        print(f"Сетевая ошибка для {mail.email}: {e}")
        return None

async def main():
    # Пул прокси (добавьте свои прокси)
    proxies = [
        None,  # Без прокси
        # "http://proxy1:port",
        # "http://proxy2:port",
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [makeaccount(session, proxy=random.choice(proxies)) for _ in range(10)]  # 5 аккаунтов для 100 генераций
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if r is not None]

if __name__ == "__main__":
    os.system("python3 -c 'import os;os.system(\"clear\")'")
    print("creating 200 generations...")  # Оригинальный текст из твоего кода
    results = asyncio.run(main())
    idrng = random.randint(1, 999999)
    url = f"https://sigmapidr.pythonanywhere.com/write/{saveid}"
    payload = {"text": "EAL_" + "$$$%&".join(results)}
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "insomnia/11.6.1"
    }
    response = requests.post(url, json=payload, headers=headers)
    os.system("python3 -c 'import os;os.system(\"clear\")'")
    print(f"перепиши цифры в еалабас\n{'V'*30}\n\n\n{saveid}")
