import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})
#airline_data = airline_data.sample(n=500, random_state=42)
# Create a dash application layout
app = dash.Dash(__name__)

# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add a html.Div and core input text component
# Finally, add graph component.
app.layout = html.Div(children=[html.H1('Airline Performance Dashboard', style={'textAlign':'center', 'color':'#503D36', 'font-size':40}),
                                html.Div(["Input Year", dcc.Input(id='input-year', value='2010', type='number', style={'height':'50px', 'font-size':35})],
                                style={'font-size':40}),
                                html.Br(),
                                html.Br(),
                                html.Div(dcc.Graph(id='line-plot')),
                                html.H1('Total number of flights to the destination state split by reporting air', style={'textAlign':'center', 'color':'#503D36', 'font-size':30}),
                                html.Div(["Input Year", dcc.Input(id='input-year-bar', value='2010', type='number', style={'height':'50px', 'font-size':35})],
                                style={'font-size':35}),
                                html.Br(),
                                html.Br(),
                                html.Div(dcc.Graph(id='bar-plot'))
                                ])
# add callback decorator
@app.callback(Output(component_id='line-plot', component_property='figure'),
               Input(component_id='input-year', component_property='value'))

# Add computation to callback function and return graph
def get_graph(entered_year):
    # Select data based on the entered year
    df =  airline_data[airline_data['Year']==int(entered_year)]
    
    # Group the data by Month and compute the average over arrival delay time.
    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()
    
    # 
    fig = go.Figure(data=go.Scatter(x=line_data['Month'], y=line_data['ArrDelay'], mode='lines', marker=dict(color='green')))
    fig.update_layout(title='Avereage Flight Delay Time vs Month', xaxis_title='Month', yaxis_title='ArrDelay')
    return fig

# add callback decorator
@app.callback(Output(component_id='bar-plot', component_property='figure'),
               Input(component_id='input-year-bar', component_property='value'))

# Add computation to callback function and return graph
def get_graph_bar(entered_year):
    # Select data based on the entered year
    df =  airline_data[airline_data['Year']==int(entered_year)]
    
    # Group the data by Month and compute the average over arrival delay time.
    bar_data = df.groupby('DestState')['Flights'].sum().reset_index()
    # 
    fig = go.Figure(data=go.Bar(x=bar_data['DestState'], y=bar_data['Flights']))
    fig.update_layout(title='Flights to Destination State', xaxis_title='DestState', yaxis_title='Flights')
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
