import dash
import os
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import Dash, dcc, callback, Input, Output

os.environ['REACT_VERSION'] = '18.2.0'

stylesheets = [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
]

app = Dash(external_stylesheets=stylesheets, use_pages=True)

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
                                                                           dmc.ActionIcon(
                                                                               color="green",
                                                                               children=DashIconify(
                                                                                   icon="carbon:home",
                                                                                   width=20,
                                                                               ),
                                                                               id="home_page",
                                                                               n_clicks=0
                                                                           ),
                                                                           dmc.Space(h=20),
                                                                           dmc.ActionIcon(
                                                                               color="green",
                                                                               children=DashIconify(
                                                                                   icon="clarity:settings-line",
                                                                                   width=20,
                                                                               ),
                                                                               id="registration_page",
                                                                               n_clicks=0
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
    Output("redirect", "href"),
    Input("home_page", "n_clicks"),
    Input("registration_page", "n_clicks")

)
def redirect_registration(home, registration):
    if home:
        return "/"
    elif registration:
        return "/registration"


if __name__ == "__main__":
    app.run_server(debug=True)
