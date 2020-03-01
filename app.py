import dash
import dash_core_components as dcc
import dash_html_components as html
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
    html.Div(children='Data Analysis using Dash', style={
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
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)