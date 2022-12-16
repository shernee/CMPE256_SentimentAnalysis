import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from .pipeline import run_pipeline

dash.register_page(__name__, path="/model")


layout = html.Div([
    dcc.Textarea(
        id='review-input',
        value='write a review',
        style={'width': '100%', 'height': 300},
    ),
    dbc.Button("Generate review sentiment", id="generate_label"),
    html.Div(id='classification-output')
])

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
            return f"The review written was {output_label}"
        else:
            return f"Please enter a review in the text box"
    