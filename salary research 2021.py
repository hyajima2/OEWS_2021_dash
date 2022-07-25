# data manipulation
import pandas as pd
import numpy as np

# plotly 
import plotly.express as px
import plotly.graph_objects as go

# dashboards
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc #for dashboard theme
from datetime import date


# read excel file
# estimated run time = 2.21s
data = pd.read_excel('OEWS_2021_Cross_Industry_Only.xlsx')

# cleaning
data['A_MEDIAN'] = [i if type(i) == int else np.nan for i in data["A_MEDIAN"]]
data['TOT_EMP'] = [i if type(i) == int else np.nan for i in data["TOT_EMP"]]
data = data.rename(columns = {'A_MEDIAN':'Annual Median Income', 'TOT_EMP':'Total Employment'})


# list of all indicators
state_dict = {
    "U.S.": "US",
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}

occupation_list = ['All Occupations'] + sorted([x for x in data.OCC_TITLE.unique() if x != 'All Occupations'])
state_list = state_dict.keys()

# app
app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
server = app.server


app.layout = html.Div([
    html.H1('Median Salary/Employment Dashboard in 2021 from OEWS'),
    html.A(children = 'Data Source: OEWS', href = 'https://www.bls.gov/oes/tables.htm', target="_blank"),
    html.Br(),
    html.Br(),
    # Options
    html.Div([
        html.Div(children = [
            html.Label('Select Location'),
            html.Br(),
            dcc.Dropdown(
                id = 'state_list',
                value = 'U.S.',
                options = [{'label': i, 'value': i} for i in state_list]
                ),
            ], style = {'width': '45%', 'height':'100px', 'display': 'inline-block', 'text-align':'left'}
        ),
        html.Div(children = [
            html.Label('Select Occupation'),
            html.Br(),
            dcc.Dropdown(
                id='occupation_list',
                value = 'All Occupations',
                options = [{'label': i, 'value': i} for i in occupation_list]
                ),
            ], style = {'width': '45%', 'height':'100px', 'display': 'inline-block', 'text-align':'left'}
        ),
    ], style={'width': '100%', "display":"inline-block", 'text-align':'center'}),
    
    #Graphs
    dcc.Tabs([
            #tab1 (salary)
            dcc.Tab(label = 'Median Salary', children = [
                html.Div([
                    html.Div([
                        html.Div([
                            # salary_number
                            dcc.Loading(dcc.Graph(id='salary_number'
                                )),
                            ], style={'width': '45%', "display":"inline-block", 'text-align':'left'}
                        ),
                        html.Div([
                            # salary_histogram
                            dcc.Loading(dcc.Graph(id='salary_histogram'
                                )),
                            ], style={'width': '45%', "display":"inline-block", 'text-align':'left'}
                        ),
                    ], style={'width': '100%', "display":"inline-block", 'text-align':'center'}
                    ),
                
                    html.Div([
                        html.Div([
                            # salary_table
                            dcc.Loading(dcc.Graph(id='salary_table'
                                )),
                            ], style={'width': '45%', "display":"inline-block", 'text-align':'left'}
                        ),
                        html.Div([
                            # salary_map
                            dcc.Loading(dcc.Graph(id='salary_map'
                                )),
                            ], style={'width': '45%', "display":"inline-block", 'text-align':'left'}
                        ),
                    ], style={'width': '100%', "display":"inline-block", 'text-align':'center'}
                    )
                ]),
            ]),


            #tab2 (employment)
            dcc.Tab(label = '# of Employment', children = [
                html.Div([
                    html.Div([
                        html.Div([
                            # employment_histogram
                            dcc.Loading(dcc.Graph(id='employment_number'
                                )),
                            ], style={'width': '45%', "display":"inline-block", 'text-align':'left'}
                        ),
                        html.Div([
                            # employment_histogram
                            dcc.Loading(dcc.Graph(id='employment_histogram'
                                )),
                            ], style={'width': '45%', "display":"inline-block", 'text-align':'left'}
                        ),
                    ], style={'width': '100%', "display":"inline-block", 'text-align':'center'}
                    ),
                
                    html.Div([
                        html.Div([
                            # employment_table
                            dcc.Loading(dcc.Graph(id='employment_table'
                                )),
                            ], style={'width': '45%', "display":"inline-block", 'text-align':'left'}
                        ),
                        html.Div([
                            # employment_map
                            dcc.Loading(dcc.Graph(id='employment_map'
                                )),
                            ], style={'width': '45%', "display":"inline-block", 'text-align':'left'}
                        ),
                    ], style={'width': '100%', "display":"inline-block", 'text-align':'center'}
                    )
                ]),
            ]),
        ])
])



# Functions

# Salary Function

# number function    
@app.callback(
    Output('salary_number', 'figure'),
    Input('state_list', 'value'),
    Input('occupation_list', 'value')
)
def salary_number(state, occupation):
    
    if len(occupation) > len('All Occupations'):
        if ',' in occupation:
            occupation_title = occupation.replace(',', '...?').replace(' and ', '...?')
        else:
            occupation_title = occupation.replace(' ', '...?')
    else: 
        occupation_title = occupation
    if '...?' in occupation_title:
        occupation_title = occupation_title.split('?')[0]
    else: 
        occupation_title = occupation
    title = 'Annual Median Income of {} in {}'.format(occupation_title, state)

    fig1 = go.Figure()
    
    fig1.add_trace(go.Indicator(
        mode = "gauge+number",
        value = int(data.loc[(data.AREA_TITLE == state) & (data.OCC_TITLE == occupation), 'Annual Median Income'].median()),
        number={'font_color':'blue', 'font_size':80, 'prefix': '$'},
        domain = {'row': 0, 'column': 1},
        gauge = {
            'axis': {'range': [data['Annual Median Income'].min(), data['Annual Median Income'].max()], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "blue"},
            }    
    ))
    
    fig1.update_layout(
        template = {'data' : {'indicator': [{
            'title': {'text': title, 'font':{'size':18}},
            }]
         }})
    return fig1


# histogram function
@app.callback(
    Output('salary_histogram', 'figure'),
    Input('state_list', 'value'),
    Input('occupation_list', 'value')
)
def salary_hist(state, occupation):

    if len(occupation) > len('All Occupations'):
        if ',' in occupation:
            occupation_title = occupation.replace(',', '...?').replace(' and ', '...?')
        else:
            occupation_title = occupation.replace(' ', '...?')
    else: 
        occupation_title = occupation
    if '...?' in occupation_title:
        occupation_title = occupation_title.split('?')[0]
    else: 
        occupation_title = occupation

    if state == 'U.S.':
        fig2 = px.histogram(data[(data.AREA_TITLE.isin([x for x in state_list if x != 'U.S.'])) & (data.OCC_TITLE == occupation)], x="Annual Median Income", nbins = 30)
        fig2.update_layout(
            title = dict(
                text='Annual Median Income of {} in {} by State'.format(occupation_title, state),
                font = dict(size = 18),
                ),
            xaxis_title="Annual Median Income ($)"
            )
    elif occupation == 'All Occupations':
        fig2 = px.histogram(data[(data.AREA_TITLE == state) & (data.OCC_TITLE.isin([x for x in occupation_list if x != 'All Occupations']))], x="Annual Median Income", nbins = 30)
        fig2.update_layout(
            title = dict(
                text = 'Annual Median Income of {} in {} by Occupation'.format(occupation_title, state),
                font = dict(size = 18),
                ),
            xaxis_title="Annual Median Income ($)"
        )
    else:
        fig2 = go.Figure()
    
        fig2.add_trace(go.Indicator(
            number = {'font': {'size': 1}
                    },
            value = None
            ))

        fig2.update_layout(
        template = {'data' : {'indicator': [{
            'title': {'text': 'No Histogram', 'font':{'size': 80}}
            }]
        }})
        
    return fig2


# table function
@app.callback(
    Output('salary_table', 'figure'),
    Input('state_list', 'value'),
    Input('occupation_list', 'value')
)
def salary_table(state, occupation):
    if len(occupation) > len('All Occupations'):
        if ',' in occupation:
            occupation_title = occupation.replace(',', '...?').replace(' and ', '...?')
        else:
            occupation_title = occupation.replace(' ', '...?')
    else: 
        occupation_title = occupation
    if '...?' in occupation_title:
        occupation_title = occupation_title.split('?')[0]
    else: 
        occupation_title = occupation

    if state == 'U.S.':
        table = data[(data.AREA_TITLE.isin([x for x in state_list if x != 'U.S.'])) & (data.OCC_TITLE == occupation)].groupby(
            'AREA_TITLE'
        ).agg(
            {'Annual Median Income':'median'
            }
        ).sort_values('Annual Median Income', ascending = False).reset_index().rename(columns = {'AREA_TITLE': 'State'}).head()
        fig3 = go.Figure(data=[go.Table(
            header=dict(values=list(table.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[table.State, table['Annual Median Income']],
                       fill_color='lavender',
                       align='left',
                       format=['', "$,"]),
            )
        ])
        fig3.update_layout(
            title = dict(
                text= 'Top 5 States by Annual Median Income of {}'.format(occupation_title),
                font = dict(size = 18)
                )         
            )

    elif occupation == 'All Occupations':
        table = data[(data.AREA_TITLE == state) & (data.OCC_TITLE.isin([x for x in occupation_list if x != 'All Occupations']))].groupby(
            'OCC_TITLE'
        ).agg(
            {'Annual Median Income':'median'
            }
        ).sort_values('Annual Median Income', ascending = False).reset_index().rename(columns = {'OCC_TITLE': 'State'}).head()
        fig3 = go.Figure(data=[go.Table(
            header=dict(values=list(table.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[table.State, table['Annual Median Income']],
                       fill_color='lavender',
                       align='left',
                       format=['', "$,"]))
        ])
        fig3.update_layout(
            title = dict(
                text='Top 5 Occupations by Annual Median Income of {}'.format(state),
                font = dict(size = 18)
                )         
            )
    else:
        fig3 = go.Figure()
    
        fig3.add_trace(go.Indicator(
            number = {'font': {'size': 1}
                    },
            value = None
            ))

        fig3.update_layout(
        template = {'data' : {'indicator': [{
            'title': {'text': 'No Table', 'font':{'size': 80}}
            }]
        }})
    return fig3



# map function
@app.callback(
    Output('salary_map', 'figure'),
    Input('state_list', 'value'),
    Input('occupation_list', 'value')
)
def salary_map(state, occupation):

    if len(occupation) > len('All Occupations'):
        if ',' in occupation:
            occupation_title = occupation.replace(',', '...?').replace(' and ', '...?')
        else:
            occupation_title = occupation.replace(' ', '...?')
    else: 
        occupation_title = occupation
    if '...?' in occupation_title:
        occupation_title = occupation_title.split('?')[0]
    else: 
        occupation_title = occupation

    map_df = data[(data.AREA_TITLE.isin([x for x in state_list if x != 'US'])) & (data.OCC_TITLE == occupation)].groupby(
                                'AREA_TITLE'
                            ).agg(
                                {'Annual Median Income':'median',
                                }
                            ).reset_index().rename(columns = {'AREA_TITLE': 'State'})
    map_df['state_code'] = [state_dict[i] for i in map_df['State']]
    if state == 'U.S.':
        fig4 = px.choropleth(
                            map_df,
                            locations= 'state_code', 
                            locationmode="USA-states", 
                            scope="usa",
                            color='Annual Median Income',
                            color_continuous_scale="blues"
                            )
        fig4.update_layout(
             title = dict(
                text ='Annual Median Income of {} in U.S.'.format(occupation),
                font = dict(size = 18)
                )         
            )

    else:
        fig4 = go.Figure()
    
        fig4.add_trace(go.Indicator(
            number = {'font': {'size': 1}
                    },
            value = None
            ))

        fig4.update_layout(
        template = {'data' : {'indicator': [{
            'title': {'text': 'No Map', 'font':{'size': 80}}
            }]
        }})
    return fig4







# Employment Functions
# number function    
@app.callback(
    Output('employment_number', 'figure'),
    Input('state_list', 'value'),
    Input('occupation_list', 'value')
)
def employment_number(state, occupation):

    if len(occupation) > len('All Occupations'):
        if ',' in occupation:
            occupation_title = occupation.replace(',', '...?').replace(' and ', '...?')
        else:
            occupation_title = occupation.replace(' ', '...?')
    else: 
        occupation_title = occupation
    if '...?' in occupation_title:
        occupation_title = occupation_title.split('?')[0]
    else: 
        occupation_title = occupation

    fig5 = go.Figure()
    
    fig5.add_trace(go.Indicator(
        mode = "gauge+number",
        value = int(data.loc[(data.AREA_TITLE == state) & (data.OCC_TITLE == occupation), 'Total Employment'].sum()),
        number={'font_color':'red', 'font_size':80},
        domain = {'row': 0, 'column': 1},
        gauge = {
            'axis': {'range': [data['Total Employment'].min(), data['Total Employment'].max()], 'tickwidth': 1},
                'bar': {'color': "red"},
        }
    ))
    
    fig5.update_layout(
        template = {'data' : {'indicator': [{
            'title': {'text': 'Total # of Employment of {} in {}'.format(occupation_title, state), 'font':{'size':18}},
            }]
         }})
    return fig5


# histogram function
@app.callback(
    Output('employment_histogram', 'figure'),
    Input('state_list', 'value'),
    Input('occupation_list', 'value')
)
def employment_hist(state, occupation):

    if len(occupation) > len('All Occupations'):
        if ',' in occupation:
            occupation_title = occupation.replace(',', '...?').replace(' and ', '...?')
        else:
            occupation_title = occupation.replace(' ', '...?')
    else: 
        occupation_title = occupation
    if '...?' in occupation_title:
        occupation_title = occupation_title.split('?')[0]
    else: 
        occupation_title = occupation

    if state == 'U.S.':
        fig6 = px.histogram(data[(data.AREA_TITLE.isin([x for x in state_list if x != 'U.S.'])) & (data.OCC_TITLE == occupation)],
                            x="Total Employment",
                            nbins = 30,
                            color_discrete_sequence=['indianred'])
        fig6.update_layout(plot_bgcolor = "#ffe6e6",
                           title = dict(
                                text='Total # of Employment of {} in {} by State'.format(occupation_title, state),
                                font = dict(size = 18)
                                )                                                   
                        )
    elif occupation == 'All Occupations':
        fig6 = px.histogram(data[(data.AREA_TITLE == state) & (data.OCC_TITLE.isin([x for x in occupation_list if x != 'All Occupations']))], 
                            x="Total Employment", 
                            nbins = 30, 
                            color_discrete_sequence=['indianred'])
        fig6.update_layout(plot_bgcolor = "#ffe6e6",
                             title = dict(
                                text='Total # of Employment of {} in {} by Occupation'.format(occupation_title, state),
                                font = dict(size = 18)
                                )                                                            
                        )
    else:
        fig6 = go.Figure()
    
        fig6.add_trace(go.Indicator(
            number = {'font': {'size': 1}
                    },
            value = None
            ))

        fig6.update_layout(
        template = {'data' : {'indicator': [{
            'title': {'text': 'No Histogram', 'font':{'size': 80}}
            }]
        }})
    return fig6

# table function
@app.callback(
    Output('employment_table', 'figure'),
    Input('state_list', 'value'),
    Input('occupation_list', 'value')
)
def employment_table(state, occupation):

    if len(occupation) > len('All Occupations'):
        if ',' in occupation:
            occupation_title = occupation.replace(',', '...?').replace(' and ', '...?')
        else:
            occupation_title = occupation.replace(' ', '...?')
    else: 
        occupation_title = occupation
    if '...?' in occupation_title:
        occupation_title = occupation_title.split('?')[0]
    else: 
        occupation_title = occupation

    if state == 'U.S.':
        table = data[(data.AREA_TITLE.isin([x for x in state_list if x != 'U.S.'])) & (data.OCC_TITLE == occupation)].groupby(
            'AREA_TITLE'
        ).agg(
            {'Total Employment':'sum'
            }
        ).sort_values('Total Employment', ascending = False).reset_index().rename(columns = {'AREA_TITLE': 'State'}).head()
        fig7 = go.Figure(data=[go.Table(
            header=dict(values=list(table.columns),
                        fill_color='Salmon',
                        align='left'),
            cells=dict(values=[table.State, table['Total Employment']],
                       fill_color='Pink',
                       align='left',
                       format = ["",","]
                       ),
            )
        ])
        fig7.update_layout(
             title = dict(
                        text='Top 5 States by Total # of Employment of {}'.format(occupation_title),
                        font = dict(size = 18)
                        )                  
            )

    elif occupation == 'All Occupations':
        table = data[(data.AREA_TITLE == state) & (data.OCC_TITLE.isin([x for x in occupation_list if x != 'All Occupations']))].groupby(
            'OCC_TITLE'
        ).agg(
            {'Total Employment':'sum'
            }
        ).sort_values('Total Employment', ascending = False).reset_index().rename(columns = {'OCC_TITLE': 'State'}).head()
        fig7 = go.Figure(data=[go.Table(
            header=dict(values=list(table.columns),
                        fill_color='Salmon',
                        align='left'),
            cells=dict(values=[table.State, table['Total Employment']],
                       fill_color='Pink',
                       align='left',
                        format = ["",","]
                      )
            )
        ])
        fig7.update_layout(
            title={
                'text': 'Top 5 Occupations by Total # of Employment of {}'.format(state)
            })
        
    else:
        fig7 = go.Figure()
    
        fig7.add_trace(go.Indicator(
            number = {'font': {'size': 1}
                    },
            value = None
            ))

        fig7.update_layout(
        template = {'data' : {'indicator': [{
            'title': {'text': 'No Table', 'font':{'size': 80}}
            }]
        }})
    return fig7



# map function
@app.callback(
    Output('employment_map', 'figure'),
    Input('state_list', 'value'),
    Input('occupation_list', 'value')
)
def employment_map(state, occupation):

    if len(occupation) > len('All Occupations'):
        if ',' in occupation:
            occupation_title = occupation.replace(',', '...?').replace(' and ', '...?')
        else:
            occupation_title = occupation.replace(' ', '...?')
    else: 
        occupation_title = occupation
    if '...?' in occupation_title:
        occupation_title = occupation_title.split('?')[0]
    else: 
        occupation_title = occupation

    map_df = data[(data.AREA_TITLE.isin([x for x in state_list if x != 'US'])) & (data.OCC_TITLE == occupation)].groupby(
                                'AREA_TITLE'
                            ).agg(
                                {'Total Employment':'sum',
                                }
                            ).reset_index().rename(columns = {'AREA_TITLE': 'State'})
    map_df['state_code'] = [state_dict[i] for i in map_df['State']]
    if state == 'U.S.':
        fig8 = px.choropleth(
                            map_df,
                            locations= 'state_code', 
                            locationmode="USA-states", 
                            scope="usa",
                            color='Total Employment',
                            color_continuous_scale="reds",
                            )
        fig8.update_layout(
                     title = dict(
                        text='Total # of Employment of {} in U.S.'.format(occupation_title),
                        font = dict(size = 18)
                        )                         
                    )
    else:
        fig8 = go.Figure()
    
        fig8.add_trace(go.Indicator(
            number = {'font': {'size': 1}
                    },
            value = None
            ))

        fig8.update_layout(
        template = {'data' : {'indicator': [{
            'title': {'text': 'No Map', 'font':{'size': 80}}
            }]
        }})
    return fig8




if __name__ == '__main__':
        app.run_server(debug=False, port=8899)