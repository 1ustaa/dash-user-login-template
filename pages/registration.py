import dash
import dash_mantine_components as dmc

dash.register_page(__name__)


def layout():
    page = dmc.Container(
        dmc.Grid(
            dmc.GridCol(
                style={"textAlign": "center"},
                children=[
                    dmc.Text(children="Регистрация",
                             fw="700",
                             size="xl"),
                    dmc.Text(children="",
                             size="md")
                ]
            )
        )
    )
    return page
