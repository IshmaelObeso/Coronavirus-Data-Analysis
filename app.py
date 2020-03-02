import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
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

# calculating daily deltas
confirmed_daily_delta = (confirmed_groupby_country.iloc[:,-1] - confirmed_groupby_country.iloc[:,-2])/confirmed_groupby_country.iloc[:,-2]
deaths_daily_delta = (deaths_groupby_country.iloc[:,-1] - deaths_groupby_country.iloc[:,-2])/deaths_groupby_country.iloc[:,-2]
recovery_daily_delta = (recovery_groupby_country.iloc[:,-1] - recovery_groupby_country.iloc[:,-2])/recovery_groupby_country.iloc[:,-2]

# calculating weekly deltas
confirmed_weekly_delta = (confirmed_groupby_country.iloc[:,-1] - confirmed_groupby_country.iloc[:,-8])/confirmed_groupby_country.iloc[:,-8]
deaths_weekly_delta = (deaths_groupby_country.iloc[:,-1] - deaths_groupby_country.iloc[:,-8])/deaths_groupby_country.iloc[:,-8]
recovery_weekly_delta = (recovery_groupby_country.iloc[:,-1] - recovery_groupby_country.iloc[:,-8])/recovery_groupby_country.iloc[:,-8]

#%%

confirmed_history = pd.concat([confirmed_groupby_country.iloc[:,-8],
                               confirmed_groupby_country.iloc[:,-2],
                               confirmed_groupby_country.iloc[:,-1]],
                              axis=1)
deaths_history = pd.concat([deaths_groupby_country.iloc[:,-8],
                            deaths_groupby_country.iloc[:,-2],
                            deaths_groupby_country.iloc[:,-1]],
                            axis=1)
recovery_history = pd.concat([recovery_groupby_country.iloc[:,-8],
                              recovery_groupby_country.iloc[:,-2],
                              recovery_groupby_country.iloc[:,-1]],
                             axis=1)

# combine deltas and history
confirmed_delta_df = pd.concat([confirmed_history,
                                (confirmed_daily_delta.round(2)*100).astype(str) + '%',
                                (confirmed_weekly_delta.round(2)*100).astype(str) + '%'],
                               axis=1).rename(columns={0: 'Daily Delta', 1: 'Weekly Delta'}).reset_index()
deaths_delta_df = pd.concat([deaths_history,
                             (deaths_daily_delta.round(2)*100).astype(str)+'%',
                             (deaths_weekly_delta.round(2)*100).astype(str)+'%'],
                               axis=1).rename(columns={0: 'Daily Delta', 1: 'Weekly Delta'}).reset_index()
recovery_delta_df = pd.concat([recovery_history,
                               (recovery_daily_delta.round(2)*100).astype(str)+'%',
                               (recovery_weekly_delta.round(2)*100).astype(str)+'%'],
                               axis=1).rename(columns={0: 'Daily Delta', 1: 'Weekly Delta'}).reset_index()

# cleanup
confirmed_delta_df.replace(['inf%'], 'n/a', inplace=True)
deaths_delta_df.replace(['inf%'], 'n/a', inplace=True)
recovery_delta_df.replace(['inf%'], 'n/a', inplace=True)
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
    style={'width': '15%',
           'display': 'inline-block',
           'align-items': 'center',
           'justify-content': 'center'}),

    dcc.Graph(id='Country by Country Data'),
    html.Div(children='Confirmed Cases Deltas', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dash_table.DataTable(
        id='Confirmed Deltas Table',
        columns=[{'name':i, 'id':i} for i in confirmed_delta_df.columns],
        data=confirmed_delta_df.to_dict('rows'),
        style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        }
    ),
    html.Div(children='Deaths Deltas', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dash_table.DataTable(
        id='Deaths Deltas Table',
        columns=[{'name':i, 'id':i} for i in deaths_delta_df.columns],
        data=deaths_delta_df.to_dict('rows'),
        style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        }
    ),
    html.Div(children='Recovery Deltas', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dash_table.DataTable(
        id='Recovery Deltas Table',
        columns=[{'name':i, 'id':i} for i in recovery_delta_df.columns],
        data=recovery_delta_df.to_dict('rows'),
        style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        }
    )
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
                    name='Cases',
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
                    name='Deaths'
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
                    name='Recovered'
                )],
        'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']},
                'title': {
                    'text': f'{country_dropdown}'
                }
        }
}


if __name__ == '__main__':
    app.run_server(debug=True)