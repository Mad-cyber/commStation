#utils file creating the permissions for each of the registered users, if cus then cus dashboard etc
def detectUser(user):
    if user.role == 1:
        redirectUrl = 'bussDash'
        return redirectUrl
    elif user.role ==2:
        redirectUrl = 'custDash'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
