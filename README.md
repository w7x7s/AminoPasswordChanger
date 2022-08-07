
* This script is used to change the password in amino


* يستخدم هذا السكربت لتغيير كلمة السر  داخل منصة  التواصل الاجتماعي امينو 

```python
email='email'
E=SubSM(email)
if E.request_verify_code():
    print(E.read())
    if E.change_password(password=input('new password > '),code=input("code >")):
        print('done :)')
```
[my account](https://www.instagram.com/w7x7s/) 
