import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()

confirmed = pd.read_csv('COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')
deaths = pd.read_csv('COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
recovery = pd.read_csv('COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')

confirmed = confirmed.drop(['Province/State','Lat', 'Long'], axis=1)
deaths = deaths.drop(['Province/State','Lat', 'Long'], axis=1)
recovery = recovery.drop(['Province/State','Lat', 'Long'], axis=1)

confirmed_groupby_country = confirmed.groupby(confirmed['Country/Region']).sum()
deaths_groupby_country = deaths.groupby(deaths['Country/Region']).sum()
recovery_groupby_country = recovery.groupby(recovery['Country/Region']).sum()

aggregate_confirmed = confirmed_groupby_country.sum()
aggregate_deaths = deaths_groupby_country.sum()
aggregate_recovery = recovery_groupby_country.sum()

available_countries = confirmed_groupby_country.index

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Coronavirus Data Analysis',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='Worldwide Statistics', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Graph(
        id='Aggregate Data',
        figure={
            'data': [
                go.Line(
                    x=aggregate_confirmed.index,
                    y=aggregate_confirmed,
                    text='Cases',
                    mode='lines',
                    opacity=0.8,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'blue'}
                    },
                    name='Total Cases'
                ),
            go.Line(
                    x=aggregate_deaths.index,
                    y=aggregate_deaths,
                    text='Deaths',
                    mode='lines',
                    opacity=0.8,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'red'}
                    },
                    name='Total Deaths'
                ),
            go.Line(
                    x=aggregate_recovery.index,
                    y=aggregate_recovery,
                    text='Recovered',
                    mode='lines',
                    opacity=0.8,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'Red'}
                    },
                    name='Total Recovered'
                )
            ],

            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),

    html.Div(children='Country-by-Country Statistics', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': i, 'value': i} for i in available_countries],
            value='US'
        ),
    ],
    style={'width': '10%', 'display': 'inline-block'}),

    dcc.Graph(id='Country by Country Data')
])

@app.callback(
    Output('Country by Country Data', 'figure'),
    [Input('country-dropdown', 'value')])

def update_graph(country_dropdown):
    country_confirmed = confirmed_groupby_country.loc[country_dropdown]
    country_death = deaths_groupby_country.loc[country_dropdown]
    country_recovery = recovery_groupby_country.loc[country_dropdown]

    return {
        'data': [
                go.Line(
                    x=country_confirmed.index,
                    y=country_confirmed,
                    text='Cases',
                    mode='lines',
                    opacity=0.8,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'blue'}
                    },
                    name='Total Cases'
                ),
            go.Line(
                    x=country_death.index,
                    y=country_death,
                    text='Deaths',
                    mode='lines',
                    opacity=0.8,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'red'}
                    },
                    name='Total Deaths'
                ),
            go.Line(
                    x=country_recovery.index,
                    y=country_recovery,
                    text='Recovered',
                    mode='lines',
                    opacity=0.8,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'Red'}
                    },
                    name='Total Recovered'
                )],
        'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']}
        }
}


if __name__ == '__main__':
    app.run_server(debug=True)