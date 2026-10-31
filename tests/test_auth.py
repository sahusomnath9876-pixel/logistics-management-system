from app.services import Authentication


def test_signin_signup():
    auth = Authentication()
    signin = auth.signIN("9279212496", "Sahu@2020")
    signup = auth.user_signUp("Mukesh Thakur", "7856696853", "Mukesh@1212", "Hydrabad")
    manager_signup = auth.manager_signUP("Rahul Yadav", "7549365685", "Rahul@2020", 750245, 14552)
    assert signin.get("success") == True
    assert signup.get("success") == True
    assert manager_signup.get("success") == True



