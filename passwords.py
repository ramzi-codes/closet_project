from werkzeug.security import(
        generate_password_hash,
        check_password_hash
    )

myPassword = 'ILovePonies7'

hashed_password = generate_password_hash(myPassword)
print(generate_password_hash(myPassword))

#login form
guess = input("Whats your password?")

if check_password_hash(hashed_password, guess):
    print("success! logging you in.")
else:
    print("try again.")