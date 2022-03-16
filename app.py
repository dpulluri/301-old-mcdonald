import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import pandas as pd

########### Define your variables ######

tabtitle = 'Old McDonald'
sourceurl = 'https://plot.ly/python/choropleth-maps/'
githublink = 'https://github.com/austinlasseter/agriculture-exports-map'
# here's the list of possible columns to choose from.
list_of_columns =['GENERAL ACUTE CARE', 'CRITICAL ACCESS', 'LONG TERM CARE', 'PSYCHIATRIC','MILITARY']
#list_of_columns =['TYPE', 'STATUS', 'TRAUMA', 'HELIPAD']


########## Set up the chart

import pandas as pd
df = pd.read_csv('assets/Hospitals.csv')

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle
########### Set up the layout

app.layout = html.Div(children=[
    html.H1('Hospitals, by State'),
    html.Div([
        html.Div([
                html.H6('Select the type of hospital for analysis:'),
                dcc.Dropdown(
                    id='options-drop',
                    options=[{'label': i, 'value': i} for i in list_of_columns],
                    value='PSYCHIATRIC'
                ),
        ], className='two columns'),
        html.Div([dcc.Graph(id='figure-1'),
            ], className='ten columns'),
    ], className='twelve columns'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)


# make a function that can intake any varname and produce a map.
@app.callback(Output('figure-1', 'figure'),
             [Input('options-drop', 'value')])
def make_figure(varname):
    mygraphtitle = f'Hospitals of {varname}'
    mycolorscale = 'Blues' # Note: The error message will list possible color scales.
    mycolorbartitle = "Count"

    data=go.Choropleth(
        locations=df['STATE'], # Spatial coordinates
        locationmode = 'USA-states', # set of locations match entries in `locations`
        z = df[df["TYPE"] == varname]["STATE"].value_counts(normalize=True), # Data to be color-coded
        colorscale = mycolorscale,
        colorbar_title = mycolorbartitle,
    )
    fig = go.Figure(data)
    fig.update_layout(
        title_text = mygraphtitle,
        geo_scope='usa',
        width=1200,
        height=800
    )
    return fig


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)