
import secmail
import os 
from hmac import new
import requests
import re
from base64 import b64decode, b64encode
from hashlib import sha1
import json 

# by Emp
# instagram > https://www.instagram.com/w7x7s/
# instagram > https://www.instagram.com/w7x7s/



class SubSM(secmail.SecMail):
        def __init__(self,email):
            self.e=email
            self.api = "https://service.narvii.com/api/v1"
            self.PREFIX = bytes.fromhex("42")
            self.SIG_KEY = bytes.fromhex("F8E7A61AC3F725941E3AC7CAE2D688BE97F30B93")
            self.DEVICE_KEY = bytes.fromhex("02B258C63559D8804321C5D5065AF320358D366F")
            self.headers = {
            "NDCDEVICEID":None,
            "Accept-Language": "en-US",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent":None,
            "Host": "service.narvii.com",
            "Accept-Encoding": "gzip",
            "Connection": "Upgrade"
        }
        @property
        def deviceId(self,data: bytes = None) -> str:
                if isinstance(data, str): data = bytes(data, 'utf-8')
                identifier = self.PREFIX + (data or os.urandom(20))
                mac = new(self.DEVICE_KEY, identifier, sha1)
                deviceId=f"{identifier.hex()}{mac.hexdigest()}".upper()
                self.headers.update({"NDCDEVICEID":deviceId})
                return deviceId
        def signature(self,data) -> dict:
            data = data if isinstance(data, bytes) else data.encode("utf-8")
            signature= b64encode(self.PREFIX + new(self.SIG_KEY, data, sha1).digest()).decode("utf-8")
            self.deviceId
            self.headers.update({"NDC-MSG-SIG":signature})
            return self.headers
            
        def read(self) -> str  :
                of=0
                while of<5:
                    box_len=len(self.get_messages(email=self.e).id)
                    print(f"email ->>>>  {self.e} \nThere are no messages in the box\n" if box_len==0 else "There are messages in the box\n")
                    of+=1
                    while box_len!=0:
                        id=self.get_messages(email=self.e).id
                        html=self.read_message(email=self.e,id=id[0]).htmlBody
                        return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', html)[0]

        def request_verify_code(self, resetPassword: bool = True) -> bool:
                """
                Request an verification code to the targeted email.
                **Parameters**
                    - **email** : Email of the account.
                    - **resetPassword** : If the code should be for Password Reset.
                **Returns**
                    - **Success** : 200 (int)
                    - **Fail** : :meth:`Exceptions <aminofix.lib.util.exceptions>`
                """
                data = {
                    "identity": self.e,
                    "type": 1,
                    "deviceID": self.deviceId
                }

                if resetPassword :
                    data["level"] = 2
                    data["purpose"] = "reset-password"

                data = json.dumps(data)
                response = requests.post(f"{self.api}/g/s/auth/request-security-validation", headers=self.signature(data=data), data=data)
                if response.status_code != 200:
                    print(response.text)
                    return False
                else:
                    return True
        def change_password(self, password: str, code: str) ->  bool:
                """
                Change password of an account.
                Parameters
                    - email : Email of the account.
                    - password : Password of the account.
                    - code : Verification code.
                Returns
                    - Success : 200 (int)
                    - Fail : :meth:Exceptions <aminofix.lib.util.exceptions>
                """

                data = json.dumps({
                    "updateSecret": f"0 {password}",
                    "emailValidationContext": {
                        "data": {
                            "code": code
                        },
                        "type": 1,
                        "identity": self.e,
                        "level": 2,
                        "deviceID": self.deviceId
                    },
                    "phoneNumberValidationContext": None,
                    "deviceID": self.deviceId
                })

                response = requests.post(f"{self.api}/g/s/auth/reset-password", headers=self.signature(data=data), data=data)
                if response.status_code != 200:
                    print(response.text)
                    return False
                else:
                    return True
