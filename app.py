import dash
from dash import html, dcc, Dash, Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from pages.charts import generate_product_sunburst, generate_feature_bars
from pages.pipeline import run_pipeline

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

tab1 = html.Div(children=[
    dbc.Row([
        dbc.Col(generate_product_sunburst(), width=5, className="dashboard-chart"),
        dbc.Col(generate_feature_bars(), width=5, className="dashboard-chart")
    ], justify='around', className="dashboard-row"),
])
tab2 = html.Div([
    dcc.Textarea(
        id='review-input',
        placeholder='write a review',
        style={'width': '100%', 'height': 100},
    ),
    dbc.Button("Generate review sentiment", id="generate_label"),
    html.Div(id='classification-output', className="output-area"),
    html.Div(html.Img(
    src='/assets/classification_report.png',
    className="sentiment-image"
    ))
], className="model-page")

@dash.callback(Output('classification-output', 'children'), 
    [
        Input('review-input', 'value'), Input('generate_label', 'n_clicks')
    ]
)
def update_output(input_review, button_clicks):
    if button_clicks is None:
        raise PreventUpdate
    else:
        if len(input_review) > 1:
            output_label = run_pipeline(input_review=input_review)
            output_component = html.Div(
                html.H5(
                "The review written was "+output_label
                ), className="positive-sentiment-label" if output_label=='Positive' else "negative-sentiment-label"
            )
            return output_component
        else:
            return f"Please enter a review in the text box"
    

title_row = html.Div(children=[
    html.Div(html.H3(children="Sentiment analysis for product reviews")),
    html.Div(html.Img(
    src='/assets/sentiment.png',
    className="sentiment-image"
    ))
], className="title-row")

tab_row = html.Div(children=[
    dcc.Tabs(id="tabs-for-graph", value='Dashboard', children=[
        dcc.Tab(label='Dashboard', children=[tab1], value='Dashboard'),
        dcc.Tab(label='Model', children=[tab2], value='Model'),
    ])
])

app.layout = html.Div(children=[
    title_row,
    tab_row
])

if __name__ == "__main__":
    app.run_server(debug=True, port=8070)