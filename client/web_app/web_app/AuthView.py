import pynecone as pc

from .State import State
from .client import ClientService


class AuthState(State):
    """The app state."""

    password: str = ""
    confirmPassword: str = ""
    loginInvalid = False
    signup_error = ""
    signupInvalid = False

    def signupInvalidClose(self):
        self.signupInvalid = not self.signupInvalid

    def loginInvalidClose(self):
        self.loginInvalid = not self.loginInvalid

    def set_password(self, password):
        self.password = password

    def set_confirm_password(self, password):
        self.confirmPassword = password

    def login(self):
        print('LOGIN:', self.username, self.password)
        clientService = ClientService()
        response = clientService.authenticate(self.username, self.password)
        if response == 1:
            self.loginInvalid = True
        elif response==0:
            print('redirect')
            return pc.redirect('users')

    def signup(self):
        print('SIGNUP:', self.password, self.username)
        clientService = ClientService()
        if self.confirmPassword != self.password:
            return pc.window_alert('passwords dont match')
        response = clientService.register(self.username, self.password)
        if response == 2:
            self.signup_error = 'username already exists'
            self.signupInvalid = True
        elif response == 1:
            self.signup_error = 'server error'
            self.signupInvalid = True
        elif response==0:
            return pc.redirect('/users')





styles = {
    "login_page": {"padding_top": "10em", "text_align": "top", "position": "relative", "background_image": "bg.svg",
                   "background_size": "100% auto", "width": "100%", "height": "100vh", },
    "login_input": {"shadow": "lg", "padding": "1em", "border_radius": "lg", "background": "white", },

}


def login():
    return pc.box(pc.vstack(pc.center(
        pc.vstack(
            pc.alert_dialog(
                pc.alert_dialog_overlay(
                    pc.alert_dialog_content(
                        pc.alert_dialog_body(
                            "Invalid Credentials"
                        ),
                        pc.alert_dialog_footer(
                            pc.button(
                                "Close",
                                on_click=AuthState.loginInvalidClose,
                            )
                        ),
                    )
                ),
                is_open=AuthState.loginInvalid,
            ),

            pc.input(on_blur=AuthState.set_username, placeholder="Username", width="100%"),
            pc.input(on_blur=AuthState.set_password, placeholder="Password", type_="password", width="100%", ),
            pc.button("Login", on_click=AuthState.login, width="100%"),
            pc.link(pc.button("Sign Up", width="100%"), href="/signup", width="100%"), ),
        style=styles["login_input"], ), ), style=styles["login_page"], )


def signup():
    style_bg = styles["login_page"]
    style_bg['background_image'] = "signup.svg"
    return pc.box(pc.vstack(pc.center(pc.vstack(
        pc.alert_dialog(
            pc.alert_dialog_overlay(
                pc.alert_dialog_content(
                    pc.alert_dialog_body(
                        AuthState.signup_error
                    ),
                    pc.alert_dialog_footer(
                        pc.button(
                            "Close",
                            on_click=AuthState.signupInvalidClose,
                        )
                    ),
                )
            ),
            is_open=AuthState.signupInvalid,
        ),
        pc.input(on_blur=AuthState.set_username, placeholder="Username",
                 width="100%"),
        pc.input(on_blur=AuthState.set_password, placeholder="Password",
                 width="100%", ),
        pc.input(on_blur=AuthState.set_confirm_password,
                 placeholder="Confirm Password", width="100%", ),
        pc.button("Sign Up", on_click=AuthState.signup, width="100%"),
        pc.link(pc.button("Login", width="100%"), href="/", width="100%"),
    ), style=styles["login_input"], ),
    ),
        style=style_bg, )
