# SubSecMail
This script is used to change the password in amino 


Example:






email='email'
E=SubSM(email)
if E.request_verify_code():
print(E.read())
if E.change_password(password=input('new password > '),code=input("code >")):
print('done :)')
