import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import Dash, _dash_renderer, dcc, callback, Input, Output, State, clientside_callback

_dash_renderer._set_react_version("18.2.0")

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
                                                                 children=[dmc.ActionIcon(
                                                                     children=DashIconify(icon="clarity:settings-line",
                                                                                          width=20,
                                                                                          ),
                                                                     id="registration_page",
                                                                     n_clicks=0
                                                                 )]
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
    Input("registration_page", "n_clicks")
)
def redirect_registration(n_cliks):
    if n_cliks > 0:
        return "/registration"


if __name__ == "__main__":
    app.run(debug=True)
