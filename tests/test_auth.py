from app.services import Authentication


def test_signin_signup():
    auth = Authentication()
    signin = auth.signIN("9279212496", "Sahu@2020")
    signup = auth.user_signUp("Mr Adipal Singhania", "9709988944", "Singh@2020", "Hydrabad")
    manager_signup = auth.manager_signUP("Rahul Kaur", "7549364545", "Sahu@2020", 750247, 14554)

    assert signin.mobile_no == "9279212496"
    assert signup.mobile_no == "9709988944"
    assert manager_signup.mobile_no == "7549364545"
    



