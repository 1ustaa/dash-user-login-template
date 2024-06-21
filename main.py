import dash
import os
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import Dash, dcc, callback, Input, Output, html
from database.model import User, session
from flask import Flask

from flask_login import LoginManager, current_user, logout_user

os.environ['REACT_VERSION'] = '18.2.0'

stylesheets = [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
]
server = Flask(__name__)
app = Dash(external_stylesheets=stylesheets,
           use_pages=True,
           server=server,
           suppress_callback_exceptions=True)

server.config.update(
    SECRET_KEY="verysecretkey=)"
)

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"


@login_manager.user_loader
def load_user(user_id):
    return session.get(User, int(user_id))


app.layout = dmc.MantineProvider(forceColorScheme="dark",
                                 children=[
                                     dcc.Location(id="redirect",
                                                  refresh=True),
                                     dmc.Container(
                                         dmc.Grid([
                                             dmc.GridCol(
                                                 children=dmc.AppShell(
                                                     children=[
                                                         dmc.AppShellNavbar(
                                                             dmc.GridCol(
                                                                 style={"textAlign": "center"},
                                                                 children=[dmc.Space(h=20),
                                                                           dcc.Link(
                                                                               href="/",
                                                                               children=dmc.ActionIcon(
                                                                                   color="green",
                                                                                   children=DashIconify(
                                                                                       icon="carbon:home",
                                                                                       width=20,
                                                                                   ),
                                                                                   id="home_page",
                                                                                   n_clicks=0
                                                                               )),
                                                                           html.Div(id="user_table_button"),
                                                                           dmc.Space(h=20),
                                                                           dcc.Link(
                                                                               href="/registration",
                                                                               children=dmc.ActionIcon(
                                                                                   color="green",
                                                                                   children=DashIconify(
                                                                                       icon="material-symbols:app-registration-outline-rounded",
                                                                                       width=20,
                                                                                   ),
                                                                                   id="registration_page",
                                                                                   n_clicks=0
                                                                               )),
                                                                           dmc.Space(h=20),
                                                                           html.Div(
                                                                               id="login_logout_button",

                                                                           )

                                                                           ]
                                                             )
                                                         ),
                                                     ]
                                                 )),
                                             dmc.GridCol(children=dash.page_container)
                                         ])
                                     )
                                 ])


@callback(
    Output("login_logout_button", "children"),
    Input("redirect", "pathname")
)
def update_button(pathname):
    if not current_user.is_authenticated:
        return dcc.Link(
            href="/login",
            children=dmc.ActionIcon(
                color="green",
                children=DashIconify(
                    icon="material-symbols:login",
                    width=20,
                ),
                id="login_page",
                n_clicks=0
            ))
    else:
        return dmc.ActionIcon(
            color="red",
            children=DashIconify(
                icon="material-symbols:login",
                width=20,
            ),
            id="logout_button",
            n_clicks=0
        )


@callback(
    Output("redirect", "href"),
    Input("logout_button", "n_clicks")
)
def user_logout(n_clicks):
    if n_clicks:
        logout_user()
        return "/"


@callback(
    Output("user_table_button", "children"),
    Input("redirect", "pathname")
)
def hide_button(pathname):
    if current_user.is_authenticated and current_user.is_admin():
        return [dmc.Space(h=20),
                dcc.Link(
                    href="/user-table",
                    children=dmc.ActionIcon(
                        color="green",
                        children=DashIconify(
                            icon="clarity:administrator-line",
                            width=20,
                        ),
                        id="registration_page",
                        n_clicks=0
                    ))]
    else:
        return None


if __name__ == "__main__":
    app.run_server(debug=True)
