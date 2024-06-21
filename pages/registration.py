import dash
import dash_mantine_components as dmc
from dash import callback, Input, Output, State, dcc
from database.model import User, session

dash.register_page(__name__)


def layout():
    page = [
        dcc.Location(id="reload_page",
                     refresh=True),
        dmc.Container(
            dmc.Grid(
                dmc.GridCol(
                    style={"textAlign": "center"},
                    children=[
                        dmc.Text(children="Регистрация",
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
                    style={"borderColor": "green"},
                    label="Логин",
                    id="login_field",
                    w="300",
                    rightSectionWidth="30px"
                ),
                dmc.PasswordInput(label="Пароль",
                                  id="password_field",
                                  w="300"),
                dmc.PasswordInput(label="Подтвердите пароль",
                                  id="check_password_filed",
                                  w="300",
                                  ),
                dmc.Space(h="20"),
                dmc.Alert(id="register_alert_message",
                          hide=True,
                          color="orange"),
                dmc.Space(h="20"),
                dmc.Button(color="green",
                           id="registration_button",
                           children="Зарегистрироваться",
                           n_clicks=0),
            ]
        )
    ]
    return page


@callback(
    Output("reload_page", "href"),
    Output("register_alert_message", "hide"),
    Output("register_alert_message", "children"),
    Input("registration_button", "n_clicks"),
    State("login_field", "value"),
    State("password_field", "value"),
    State("check_password_filed", "value")
)
def registration_user(n_clicks, login, password, check_password):
    if n_clicks:
        if not login or not password or not check_password:
            return None, False, "Все поля должны быть заполнены"
        duplicate = session.query(User).filter_by(login=login).first()
        if not duplicate:
            if password == check_password:
                user = User(login=login)
                user.generate_password_hash(password)
                session.add(user)
                session.commit()
                return None, False, "Пользователь зарегистрирован!"
            else:
                return None, False, "Пароли не совпадают!"
        else:
            return None, False, "Пользователь с таким именем уже сужествует!"
    return None, True, ""
