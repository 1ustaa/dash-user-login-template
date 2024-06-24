import dash
import dash_mantine_components as dmc
from dash import callback, Input, Output, State, dcc, html
from database.model import User, UserRole, user_role_association, session, get_all_roles
from flask_login import current_user
from dash_iconify import DashIconify

dash.register_page(__name__, path="/user-table")


def generate_table():
    users = session.query(User).all()
    rows = [
        dmc.TableTr(
            [
                dmc.TableTd(id={"type": "tb_user_id", "index": user.id}, children=user.id),
                dmc.TableTd(id={"type": "tb_user_login", "index": user.id}, children=user.login),
                dmc.TableTd(id={"type": "tb_user_role", "index": user.id},
                            style={'whiteSpace': 'pre-wrap', 'wordWrap': 'break-word', 'maxWidth': '300px'},
                            children=user.get_roles_str()),
                dmc.TableTd(dmc.ActionIcon(color="green",
                                           id={"type": "redact-user", "index": user.id},
                                           n_clicks=0,
                                           children=DashIconify(
                                               icon="flowbite:edit-outline",
                                               width=20,
                                           )
                                           )
                            ),
                dmc.TableTd(
                    dmc.ActionIcon(color="red",
                                   id={"type": "delete-user", "index": user.id},
                                   n_clicks=0,
                                   children=DashIconify(
                                       icon="uiw:delete",
                                       width=20,
                                   )
                                   )
                )
            ],
            id=f"delete_user_row_{user.id}"
        )
        for user in users
    ]

    head = dmc.TableThead(
        dmc.TableTr(
            [
                dmc.TableTh("id"),
                dmc.TableTh("Имя"),
                dmc.TableTh("Роль"),
                dmc.TableTh("")
            ]
        )
    )

    body = dmc.TableTbody(rows)

    caption = dmc.TableCaption("Роли пользователей")
    return [head, body, caption]


def layout():
    if current_user.is_authenticated and current_user.is_admin:
        page = [
            dmc.Modal(
                style={"textAlign": "center"},
                id="user_redact_modal",
            ),
            dcc.Location(id="refresh_table", refresh=True),
            dmc.Container(
                dmc.Grid(
                    dmc.GridCol(
                        style={"textAlign": "center"},
                        children=[
                            dmc.Text(children="Таблица пользователей",
                                     fw="700",
                                     size="xl",
                                     ),
                            dmc.Space(h="xl"),
                            dmc.Table(
                                id="table-container",
                                children=generate_table()
                            ),
                            dmc.Alert(id="del_user_alert_msg",
                                      hide=True)
                        ]
                    )
                )
            )
        ]
        return page
    else:
        page = [dmc.Container(
            dmc.Grid(
                dmc.GridCol(
                    style={"textAlign": "center"},
                    children=[
                        dmc.Text(children="Данная страница только для администрации!",
                                 fw="700",
                                 size="xl",
                                 )
                    ]
                )
            )
        )
        ]
        return page


@callback(
    Output("user_redact_modal", "children"),
    Output("user_redact_modal", "opened"),
    Input({"type": "redact-user", "index": dash.dependencies.ALL}, "n_clicks"),
)
def open_redact_user_modal(n_clicks):
    ctx = dash.callback_context
    triggered_id = ctx.triggered_id
    if triggered_id and any(n_clicks):
        user_id = triggered_id["index"]
        user = session.get(User, int(user_id))
        modal_content = html.Div([
            dmc.Text("Редактор пользователя"),
            dmc.TextInput(label="ID", value=user.id, disabled=True, id="red_user_id"),
            dmc.TextInput(label="Логин", value=user.login, id="red_user_login"),
            dmc.MultiSelect(id="red_roles_select",
                            label="Выберите роли",
                            value=user.get_roles(),
                            data=get_all_roles(),
                            w=400
                            ),
            dmc.Space(h="20"),
            dmc.Text("Изменить пароль"),
            dmc.PasswordInput(label="Пароль", id="red_user_password"),
            dmc.PasswordInput(label="Подтвердите пароль", id="red_user_check_password"),
            dmc.Space(h="20"),
            dmc.Alert(id="red_user_alert_msg", hide=True),
            dmc.Space(h="20"),
            dmc.Button("Сохранить", id="save_user_changes", n_clicks=0, color="green")
        ])
        return modal_content, True

    return "", False


@callback(
    Output("del_user_alert_msg", "hide"),
    Output("del_user_alert_msg", "children"),
    Output("table-container", "children"),
    Input({"type": "delete-user", "index": dash.dependencies.ALL}, "n_clicks")
)
def delete_user(n_clicks):
    ctx = dash.callback_context
    triggered_id = ctx.triggered_id
    if triggered_id:
        user_id = triggered_id["index"]
        print(user_id)
        user = session.get(User, int(user_id))
        if user:
            session.delete(user)
            session.commit()
            return True, None, generate_table()

    return True, None, generate_table()


@callback(
    Output("red_user_alert_msg", "hide"),
    Output("red_user_alert_msg", "children"),
    Output("refresh_table", "href"),
    Input("save_user_changes", "n_clicks"),
    State("red_user_id", "value"),
    State("red_user_login", "value"),
    State("red_roles_select", "value"),
    State("red_user_password", "value"),
    State("red_user_check_password", "value"),

)
def confirm_redact_user_modal(n_clicks_redact, user_id, login, roles, password, check_password):
    if n_clicks_redact:
        user = session.get(User, int(user_id))
        assert user, f"Пользователь с айди {user_id} не найден"
        if login and password and check_password != "":
            if password == check_password:
                if user.is_unique(login) or login == user.login:
                    user.login = login
                    user.user_role.clear()
                    for role in roles:
                        user_role = session.query(UserRole).filter_by(role=role).first()
                        user.add_role(user_role)
                    user.generate_password_hash(password)
                    session.commit()
                    return True, "Изменения сохранены!", "/user-table"
                else:
                    return False, "Пользователь с таким именем уже сужествует!", None
            else:
                return False, "Пароли не совпадают!", None
        elif login != "":
            if user.is_unique(login) or login == user.login:
                user.login = login
                user.user_role.clear()
                for role in roles:
                    user_role = session.query(UserRole).filter_by(role=role).first()
                    user.add_role(user_role)
                session.commit()
                return True, "Изменения сохранены!", "/user-table"
            else:
                return False, "Пользователь с таким именем уже сужествует!", None
        else:
            return False, "Логин должен быть заполнен!", None
    return True, "", None
