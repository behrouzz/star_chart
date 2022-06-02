# https://dash.plotly.com/dash-core-components/datepickersingle

from datetime import date
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

app = Dash(__name__)
app.layout = html.Div([
    dcc.DatePickerSingle(
        id='my-date-picker-single',
        min_date_allowed=date(2020, 1, 1),
        max_date_allowed=date(2030, 12, 31),
        #initial_visible_month=date(2017, 8, 5),
        date=date.today(),
        display_format='DD/MM/YYYY'
    ),
    html.Div(id='output-container-date-picker-single')
])


@app.callback(
    Output('output-container-date-picker-single', 'children'),
    Input('my-date-picker-single', 'date'))
def update_output(date_value):
    string_prefix = 'You have selected: '
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')
        return string_prefix + date_string


if __name__ == '__main__':
    app.run_server(debug=True)
