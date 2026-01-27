# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_site_options = spacex_df['Launch Site'].unique().tolist()
launch_site_options = [{'label': site, 'value':site} for site in launch_site_options]
launch_site_options.insert(0, {'label': 'All Sites', 'value': 'ALL'})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            'SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36','font-size': 40}
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        # dcc.Dropdown(id='site-dropdown',...)
        dcc.Dropdown(id='site-dropdown',
            options=launch_site_options,
            value='ALL',
            placeholder="place holder here",
            searchable=True
            ),
        html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),

        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        html.Div(
            dcc.RangeSlider(
                id='payload-slider', 
                min=min_payload, max=max_payload, step=500,
                marks={0: str(min_payload), 10000: str(max_payload)},
                value=[min_payload, max_payload]
            )
        ),

        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
        ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown',component_property='value'))

def get_pie_chart(entered_site):
    # filtered_df = spacex_df
    if entered_site == 'ALL':
        buffer_data = spacex_df.groupby('Launch Site')['class'].mean().reset_index()
        fig = px.pie(buffer_data, values='class', 
        names='Launch Site', 
        title='Success rate for All Sites')
        return fig
    else:
        buffer_data = spacex_df.loc[
            spacex_df['Launch Site'] == entered_site, 'class'].value_counts().reset_index()
        fig = px.pie(buffer_data, values='count', 
        names='class', 
        title=f'Success rate for {entered_site} Site')
        print(buffer_data)
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run()
