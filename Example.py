from EmailManager import EmailManager

def change_password_amino(email):
    email_manager = EmailManager(email)

    if email_manager.request_verification_code():
        verification_url = email_manager.read_first_url_from_inbox()
        print(f"Verification URL {verification_url}")

        new_password = input("Enter the new password : " )
        verification_code = input("Enter the verification code : ")

        if email_manager.change_password(new_password, verification_code):
            print("Password change successful")
        else:
            print("Failed to change password")

if __name__ == "__main__":
    email = 'Email'
    change_password_amino(email)
