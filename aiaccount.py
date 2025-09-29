import os
os.system(
    "pip install temp-mails requests beautifulsoup4 lxml websocket-client==1.7.0 --quiet"
)
from temp_mails import Tenminutemail_one
import requests
import json
import zlib
import random
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
def makeaccount():
    mail = Tenminutemail_one()
    print(mail.email)
    url = "https://notegpt.io/user/register"
    payload = f"User%5Bemail%5D={mail.email}&User%5Bpassword%5D=12344321&User%5Bga_cid%5D="
    headers = {
        "accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language":
        "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control":
        "max-age=0",
        "content-type":
        "application/x-www-form-urlencoded",
        "Cookie":
        "sbox-guid=MTc1OTA1MjIzMXwxNHw5MzIyNzIzMTY%3D; _trackUserId=G-1759076265000; _uab_collina=175907627737348317479608; anonymous_user_id=dc868f973263a4eee420f0dea306ed9d; is_first_visit=true; crisp-client%2Fsession%2F02aa9b53-fc37-4ca7-954d-7a99fb3393de=session_86445bd1-49bf-4936-9d51-45a0e468414a; crisp-client%2Fsocket%2F02aa9b53-fc37-4ca7-954d-7a99fb3393de=0; ZFSESSID=hl8uq7otv8issemdi40efpdv92; g_state={\"i_p\":1759083542716,\"i_l\":1}",
        "origin":
        "https://notegpt.io",
        "priority":
        "u=0, i",
        "referer":
        "https://notegpt.io/user/register",
        "upgrade-insecure-requests":
        "1",
        "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0 (Edition Yx GX)"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    data = mail.wait_for_new_email(delay=1.0, timeout=120)
    #print(data)
    if data:  # It returns None if something unexpected happens
        mailm = mail.get_mail_content(data["id"])
        mailm = str(mailm.split("into browser:</p>")[1].split("</p>")[0]).replace(
            "<p>", "0").replace(" ", "")
        mailm = "http" + mailm.split("http")[1]
        #print(mailm)
        response = requests.get(mailm)
        set_cookies = response.cookies

        # Выводим информацию
        # print(f"Статус-код: {response.status_code}")
        # print("-" * 30)
        # print("Куки")

        # Объект 'set_cookies' - это RequestCookieJar, который ведет себя как словарь
        jsready = {}
        if set_cookies:
            for name, value in set_cookies.items():
                # print(f"{name}:{value}")
                jsready[name] = value
        result = "; ".join([f"{key}={value}" for key, value in jsready.items()])
        #print("-" * 30)
        
        # print("Ealabas ready:","EA__"+result+"__LA")
        return result
os.system("python3 -c 'import os;os.system(\"clear\")'")
print("creating 100 generations...")
results = [makeaccount() for _ in range(5)]
idrng = random.randint(1, 999999)
url = "https://sigmapidr.pythonanywhere.com/write/"+idrng
payload = {"text": "EAL_"+"$$$%&".join(results)}
headers = {
    "Content-Type": "application/json",
    "User-Agent": "insomnia/11.6.1"
}
response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)

os.system("python3 -c 'import os;os.system(\"clear\")'")
print("перепиши цифры в еалабас\n"+"V"*30+"\n\n\n",idrng )
