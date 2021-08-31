import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_table


from app import app
from app import server
from apps import maps, ml_test
from data import loading_stuff

dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/index"),
        dbc.DropdownMenuItem("Maps", href="/maps"),
        dbc.DropdownMenuItem("Machine Learning", href="/ml_test"),
    ],
    nav = True,
    in_navbar = True,
    label = "Explore",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/goldfish.png", height="50px")),
                        dbc.Col(dbc.NavbarBrand("Project Goldfish - Machine Learning for Ames, Iowa", className="mb-1")),
                    ],
                    align="center",
                    no_gutters=False,
                ),
                href="/index",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/maps':
        return maps.layout
    elif pathname == '/singapore':
        return plans.layout
    else:
        return maps.layout

# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)
#
#
# app.layout = dbc.Container([
#     dbc.Row([
#         dbc.Col(html.H1("Machine Learning for Ames Iowa",
#                         className='text-center text-primary, mb-4'),
#                 width=12)
#     ]),
#     dbc.Row([
#         html.Div(id='page-content')
#     ]),
#     dbc.Row([
#         html.Div(id='page-content')
#     ])
# ])
#
#
# #     html.Div([
# #     dcc.Location(id='url', refresh=False),
# #     html.Div(id='page-content')
# # ])
#
#
# @app.callback(Output('page-content', 'children'),
#               Input('url', 'pathname'))
# def display_page(pathname):
#     if pathname == '/apps/app1':
#         return app1.layout
#     elif pathname == '/apps/app2':
#         return app2.layout
#     else:
#         return app1.layout

if __name__ == '__main__':
    app.run_server(debug=True)