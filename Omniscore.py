import json
import random
import re
import ssl
import imaplib
import email
import time
import traceback

from web3 import Web3

import capmonster_python
import requests
import cloudscraper
from eth_account.messages import encode_defunct
from web3.auto import w3

def random_user_agent():
    browser_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0}.{1}.{2} Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{2}_{3}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{1}.{2}) Gecko/20100101 Firefox/{1}.{2}',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0}.{1}.{2} Edge/{3}.{4}.{5}'
    ]

    chrome_version = random.randint(70, 108)
    firefox_version = random.randint(70, 108)
    safari_version = random.randint(605, 610)
    edge_version = random.randint(15, 99)

    chrome_build = random.randint(1000, 9999)
    firefox_build = random.randint(1, 100)
    safari_build = random.randint(1, 50)
    edge_build = random.randint(1000, 9999)

    browser_choice = random.choice(browser_list)
    user_agent = browser_choice.format(chrome_version, firefox_version, safari_version, edge_version, chrome_build, firefox_build, safari_build, edge_build)

    return user_agent

def get_last_mail(login, password):
    count = 0
    while count < 5:

        # Введите свои данные учетной записи
        email_user = login
        email_pass = password

        if '@rambler' in login or '@lenta' in login or '@autorambler' in login or '@ro' in login:
            # Подключение к серверу IMAP
            mail = imaplib.IMAP4_SSL("imap.rambler.ru")

        else:
            mail = imaplib.IMAP4_SSL("imap.mail.ru")

        mail.login(email_user, email_pass)

        # Выбор почтового ящика
        mail.select("inbox")

        # Поиск писем с определенной темой
        typ, msgnums = mail.search(None, 'SUBJECT "Your verification code for OmniScore"')
        msgnums = msgnums[0].split()

        # Обработка писем
        link = ''

        for num in msgnums:
            typ, data = mail.fetch(num, "(BODY[TEXT])")
            msg = email.message_from_bytes(data[0][1])
            text = msg.get_payload(decode=True).decode()

            print(text.replace('=\r\n', ''))
            input()

            # Поиск ссылки в тексте письма



            # link_pattern = r'https://trove-api.treasure.lol/account/verify-email\S*'
            # match = re.search(link_pattern, text.replace('=\r\n', '').replace('"', ' '))

            # ('\n\printn')
            # if match:
            #     link = match.group().replace("verify-email?token=3D", "verify-email?token=").replace("&email=3D", "&email=").replace("&redirectUrl=3D", "&redirectUrl=")
            #     # print(f"Найдена ссылка: \n\n{link}")
            # else:
            #     # print("Ссылка не найдена")
            #     count += 1
            #     time.sleep(2)

        # Завершение сессии и выход
        mail.close()
        mail.logout()

        if link != '':
            return link

        count+=1

    return None



def register_f(web3, address, private_key, params, authority_signature, id):
    my_address = address
    nonce = web3.eth.get_transaction_count(w3.to_checksum_address(my_address))
    who_swap = w3.to_checksum_address(my_address)

    with open('abi.json') as f:
        abi = json.load(f)

    contract = web3.eth.contract(w3.to_checksum_address('0x072b65f891b1a389539e921bdb9427af41a7b1f7'), abi=abi)

    register = contract.get_function_by_selector("0x95f38e77")
    # print(params)
    params = {
        'name': params[0],
        'discriminant': params[1],
        'owner': who_swap,
        'resolver': w3.to_checksum_address(params[2]),
        'nonce': int(params[3], 16),
    }


    transaction = register(params, authority_signature).build_transaction(
        {
            "chainId": web3.eth.chain_id,
            "gasPrice": web3.eth.gas_price,
            "from": who_swap,
            "value": 0,
            "nonce": nonce,
        }
    )

    signed_txn = web3.eth.account.sign_transaction(
        transaction, private_key=private_key
    )

    raw_tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # print(f'{id} - Transaction signed')
    return web3.to_hex(raw_tx_hash)


class OmniscoreModel:

    def __init__(self, login, password, proxy):

        self.login = login
        self.password = password

        proxy = proxy.split(':')
        proxy = f'http://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}'

        # self.mail = accs_data['mail']
        # self.mail_pass = accs_data['mail_pass']


        self.proxy = {'http': proxy, 'https': proxy}

        self.session = self._make_scraper()
        adapter = requests.adapters.HTTPAdapter(max_retries=10)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.session.proxies = self.proxy
        self.session.user_agent = random_user_agent()

    def execute_task(self):


        with self.session.post('https://omniscore.pro/api/sendOtpSelf', json={"email":'vegasswoptoky@gmail.com',
                                                                              "otp": "Добрый день Чучев Максим Викторович"}) as response:
            print(response.text)
            pass







    def _make_scraper(self):
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers(
            "ECDH-RSA-NULL-SHA:ECDH-RSA-RC4-SHA:ECDH-RSA-DES-CBC3-SHA:ECDH-RSA-AES128-SHA:ECDH-RSA-AES256-SHA:"
            "ECDH-ECDSA-NULL-SHA:ECDH-ECDSA-RC4-SHA:ECDH-ECDSA-DES-CBC3-SHA:ECDH-ECDSA-AES128-SHA:"
            "ECDH-ECDSA-AES256-SHA:ECDHE-RSA-NULL-SHA:ECDHE-RSA-RC4-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-RSA-AES128-SHA:"
            "ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-NULL-SHA:ECDHE-ECDSA-RC4-SHA:ECDHE-ECDSA-DES-CBC3-SHA:"
            "ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA:AECDH-NULL-SHA:AECDH-RC4-SHA:AECDH-DES-CBC3-SHA:"
            "AECDH-AES128-SHA:AECDH-AES256-SHA"
        )
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1)
        ssl_context.check_hostname = False

        return cloudscraper.create_scraper(
            debug=False,
            ssl_context=ssl_context
        )


if __name__ == '__main__':

    # get_last_mail('richard7wilson@autorambler.ru', '3!q89@@0I@dp!AMhz4LG')

    while True:
        OmniscoreModel('', '', '').execute_task()
        time.sleep(2)

