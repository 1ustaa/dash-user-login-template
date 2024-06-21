import dash
import dash_mantine_components as dmc
from dash import callback, Input, Output, State, dcc
from database.model import User, session
from flask_login import current_user

dash.register_page(__name__, path="/user-table")


def generate_table():
    users = session.query(User).all()
    rows = [
        dmc.TableTr(
            [
                dmc.TableTd(user.id),
                dmc.TableTd(user.login),
                dmc.TableTd(user.role),
                dmc.TableTd(
                    dmc.Button(id={"type": "redact-user", "index": user.id}, children="Изменить")
                ),
                dmc.TableTd(
                    dmc.Button(id={"type": "delete-user", "index": user.id}, children="Удалить")
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
                            dmc.Alert(id="admin_alert_message",
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
    Output("admin_alert_message", "hide"),
    Output("admin_alert_message", "children"),
    Output("table-container", "children"),
    Input({"type": "delete-user", "index": dash.dependencies.ALL}, "n_clicks")
)
def delete_user(n_clicks):
    ctx = dash.callback_context
    triggered_id = ctx.triggered_id
    if triggered_id:
        user_id = triggered_id["index"]
        user = session.get(User, int(user_id))
        if user:
            session.delete(user)
            session.commit()
            return True, None, generate_table()

    return True, None, generate_table()
