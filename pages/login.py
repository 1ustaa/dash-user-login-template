import dash
import dash_mantine_components as dmc
from dash import callback, Input, Output, State, dcc
from database.model import User, session
from flask_login import login_user


dash.register_page(__name__)


def layout():
    page = [
        dcc.Location(id="login_redirect", refresh=True),
        dmc.Container(
            dmc.Grid(
                dmc.GridCol(style={"textAlign": "center"},
                            children=[
                                dmc.Text(children="Авторизация",
                                         fw="700",
                                         size="xl",
                                         ),
                            ]
                            )
            )
        ),
        dmc.Container(
            style={"textAlign": "center",
                   "display": "flex",
                   "flexDirection": "column",
                   "alignItems": "center"},
            children=[
                dmc.Space(h="20"),
                dmc.TextInput(
                    label="Логин",
                    id="auth_login_field",
                    w="300",
                    rightSectionWidth="30px"
                ),
                dmc.PasswordInput(label="Пароль",
                                  id="auth_password_field",
                                  w="300"),
                dmc.Space(h="20"),
                dmc.Alert(id="login_alert_message",
                          hide=True,
                          color="orange"),
                dmc.Space(h="20"),
                dmc.Button(color="green",
                           id="login_button",
                           children="Войти",
                           n_clicks=0)
            ]
        )
    ]
    return page


@callback(
    Output("login_redirect", "href"),
    Output("login_alert_message", "hide"),
    Output("login_alert_message", "children"),
    Input("login_button", "n_clicks"),
    State("auth_login_field", "value"),
    State("auth_password_field", "value")
)
def user_login(n_clicks, login, password):
    if n_clicks:
        if not login or not password:
            return None, False, "Все поля должны быть заполнены!"
        user = session.query(User).filter_by(login=login).first()
        if user and user.check_password_hash(password):
            login_user(user)
            return "/", True, None
        else:
            return None, False, "Неправильный логин или пароль!"
    return None, True, ""
