from allauth.account.views import SignupView, LoginView


class AccountSignupView(SignupView):
    template_name = "users/signup.html"

account_signup_view = AccountSignupView.as_view()


class AccountLoginView(LoginView):
    template_name = "users/login.html"

account_login_view = AccountLoginView.as_view()