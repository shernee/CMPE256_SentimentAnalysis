import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from .charts import generate_product_sunburst, generate_feature_bars
import pandas as pd

dash.register_page(__name__, path="/")

charts = html.Div(children=[
    dbc.Row([
        dbc.Col(generate_product_sunburst(), width=5, className="dashboard-chart"),
        dbc.Col(generate_feature_bars(), width=5, className="dashboard-chart")
    ], justify='around', className="dashboard-row"),
])


layout = html.Div(children=[
    charts
])