import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dataframe = pd.read_csv('assets/product_dashboard_data.csv')

sunburst_column_map = {
    'Ratings': {'column': 'overall'},
    'Sentiment': {'column': 'sentiment'}
}

bar_column_map = {
    'Product Category': {'column': 'product'},
    'Ratings': {'column': 'overall'},
    'Sentiment': {'column': 'sentiment'}
}

sentiment_map = {1: 'Positive', 0: 'Negative'}

def generate_product_sunburst():
    dropdown_labels = list(sunburst_column_map.keys())
    return html.Div(children=[
        html.Label('Select one'),
        dcc.Dropdown(dropdown_labels, dropdown_labels[0], id='product-sunburst-dropdown', clearable=False),
        dcc.Graph(id='product-sunburst-graph')
    ])

@dash.callback(Output('product-sunburst-graph', 'figure'), Input('product-sunburst-dropdown', 'value'))
def update_figure(selected_label):
    selected_column = sunburst_column_map[selected_label]['column']

    df_grouped = dataframe.groupby(['product', selected_column]).agg(
        Count=pd.NamedAgg(column=selected_column, aggfunc="count")
    ).reset_index()

    if selected_column == 'sentiment':
        df_grouped['sentiment'] = df_grouped['sentiment'].map(sentiment_map)

    fig = px.sunburst(
        df_grouped,
        path=['product', selected_column],
        values='Count',
        title=f"Division of {selected_label} among product categories",
        width=500, 
        height=500
    )
    fig.update_layout(
        font=dict(
            family="PT Sans Narrow",
            size=11,
            color="RebeccaPurple"
        )
    )

    return fig


def generate_feature_bars():
    dropdown_labels = list(bar_column_map.keys())
    return html.Div(children=[
        html.Label('Select one'),
        dcc.Dropdown(dropdown_labels, dropdown_labels[0], id='feature-bar-dropdown', clearable=False),
        dcc.Graph(id='feature-bar-graph')
    ])

@dash.callback(Output('feature-bar-graph', 'figure'), Input('feature-bar-dropdown', 'value'))
def update_figure(selected_label):
    selected_column = bar_column_map[selected_label]['column']

    df_grouped = dataframe.groupby(
        [selected_column])[['review_length', 'token_count', 'stopword_count', 'punctuation_count', 'lemma_count']]\
            .sum()\
            .unstack()\
            .reset_index()\
            .rename(columns={'level_0': 'Feature', 0: 'Sum'})

    if selected_column == 'sentiment':
        df_grouped['sentiment'] = df_grouped['sentiment'].map(sentiment_map)

    fig = px.bar(
            df_grouped,
            x='Sum',
            y='Feature',
            color=selected_column,
            orientation='h',
            barmode='group',
            title=f"Sum of features for each {selected_label} group",
            width=500, 
            height=500,
            labels={"Sum":"Sum of features", "Feature": "Feature", selected_column: selected_label}
        )
    fig.update_layout(
        font=dict(
            family="PT Sans Narrow",
            size=11,
            color="RebeccaPurple"
        )
    )

    return fig