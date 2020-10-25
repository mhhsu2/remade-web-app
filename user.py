from flask_login import LoginManager, UserMixin

login_manager = LoginManager()

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(user_id):
    if user_id not in users:
        return

    user = User()
    user.id = user_id
    print(user.id)
    return user

def request_loader(request):
    user_id = request.form.get('user_id')
    if user_id not in users:
        return

    user = User()
    user.id = user_id

    user.is_authenticated = request.form['password'] == users[user_id]['password']

    return user

users = {'Me': {'password': 'myself'}}

