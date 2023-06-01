# Change Password Script for Amino / سكربت تغيير كلمة السر في أمينو

This script is used to change the password in Amino.

يستخدم هذا السكربت لتغيير كلمة السر في منصة التواصل الاجتماعي أمينو.

## Usage / الاستخدام

1. Set the email address / قم بتعيين عنوان البريد الإلكتروني:
    ```python
    email = 'email'
    ```

2. Create an instance of the `EmailManager` class / أنشئ كلاس من  `EmailManager`:
    ```python
    E = EmailManager(email)
    ```

3. Request verification code / اطلب رمز التحقق:
    ```python
    if E.request_verification_code():
        print(E.read())
    ```

4. Enter the new password and verification code / أدخل كلمة السر الجديدة ورمز التحقق:
    ```python
    new_password = input('Enter the new password: ')
    verification_code = input('Enter the verification code: ')
    ```

5. Change the password / قم بتغيير كلمة السر:
    ```python
    if E.change_password(new_password, verification_code):
        print('Password change successful')
    else:
        print('Failed to change password')
    ```

## References / المراجع

- [My Instagram Account](https://www.instagram.com/w7x7s/)
