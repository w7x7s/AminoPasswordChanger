import secmail
import os
from hmac import new
import requests
import re
from base64 import b64decode, b64encode
from hashlib import sha1
import json
from typing import Union


class EmailManager(secmail.SecMail):
    PREFIX = bytes.fromhex("19")
    SIG_KEY = bytes.fromhex("DFA5ED192DDA6E88A12FE12130DC6206B1251E44")
    DEVICE_KEY = bytes.fromhex("E7309ECC0953C6FA60005B2765F99DBBC965C8E9")

    def __init__(self, email):
        self.email = email
        # super().__init__(email)
        self.api = "https://service.aminoapps.com/api/v1"
        self.headers = {
            "NDCDEVICEID": None,
            "Accept-Language": "en-US",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": None,
            "Host": "service.narvii.com",
            "Accept-Encoding": "gzip",
            "Connection": "Upgrade"
        }

    def generate_device_id(self, data: bytes = None) -> str:
        if isinstance(data, str):
            data = bytes(data, 'utf-8')
        identifier = self.PREFIX + (data or os.urandom(20))
        mac = new(self.DEVICE_KEY, identifier, sha1)
        device_id = f"{identifier.hex()}{mac.hexdigest()}".upper()
        self.headers.update({"NDCDEVICEID": device_id})
        return device_id

    def generate_signature(self, data: Union[str, bytes]) -> str:
        data = data if isinstance(data, bytes) else data.encode("utf-8")
        signature = b64encode(self.PREFIX + new(self.SIG_KEY, data, sha1).digest()).decode("utf-8")
        self.generate_device_id()
        self.headers.update({"NDC-MSG-SIG": signature})
        return signature

    def read_first_url_from_inbox(self) -> str:
        for _ in range(5):
            messages = self.get_messages(email=self.email)
            if messages.id:
                message_id = messages.id[0]
                html = self.read_message(email=self.email, id=message_id).htmlBody
                urls = re.findall(
                    'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                    html
                )
                return urls[0] if urls else ''
            else:
                print(f"No messages found in the inbox for email: {self.email}")

    def request_verification_code(self, reset_password: bool = True) -> bool:
        data = {
            "identity": self.email,
            "type": 1,
            "deviceID": self.generate_device_id()
        }

        if reset_password:
            data["level"] = 2
            data["purpose"] = "reset-password"

        data = json.dumps(data)
        self.generate_signature(data=data)
        response = requests.post(
            f"{self.api}/g/s/auth/request-security-validation",
            headers=self.headers,
            data=data
        )

        if response.status_code == 200:
            return True
        else:
            print(response.text)
            return False

    def change_password(self, password: str, code: str) -> bool:
        data = json.dumps({
            "updateSecret": f"0 {password}",
            "emailValidationContext": {
                "data": {
                    "code": code
                },
                "type": 1,
                "identity": self.email,
                "level": 2,
                "deviceID": self.generate_device_id()
            },
            "phoneNumberValidationContext": None,
            "deviceID": self.generate_device_id()
        })
        self.generate_signature(data=data)

        response = requests.post(
            f"{self.api}/g/s/auth/reset-password",
            headers=self.headers,
            data=data
        )

        if response.status_code == 200:
            return True
        else:
            print(response.text)
            return False
