from app.services import Authentication


def test_signin_signup():
    auth = Authentication()
    signin = auth.signIN("9279212496", "Sahu@2020")
    signup = auth.user_signUp("Mukesh Tiwari", "7856696854", "Mukesh@1212", "Hydrabad")
    assert signin.get("success") == True
    assert signup.get("success") == True




