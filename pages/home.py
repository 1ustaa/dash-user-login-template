import dash
import dash_mantine_components as dmc

dash.register_page(__name__, path="/")


def layout():
    page = dmc.Container(
        dmc.Grid(
            dmc.GridCol(
                style={"textAlign": "center"},
                children=[
                    dmc.Text(children="Главная страница",
                             fw="700",
                             size="xl"),
                    dmc.Text(children="Контент главной страницы",
                             size="md")
                ]
            )
        )
    )
    return page
