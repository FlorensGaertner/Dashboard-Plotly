import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load your data
df = pd.read_csv('energy_efficiency_data.csv')

# Compute Total Load
df['Total_Load'] = df['Heating_Load'] + df['Cooling_Load']

# Map numeric orientations to cardinal directions
orientation_map = {
    2: 'North',
    3: 'East',
    4: 'South',
    5: 'West'
}
df['Cardinal_Orientation'] = df['Orientation'].map(orientation_map)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Building Energy Efficiency Dashboard"),

    # Dropdown to select feature
    dcc.Dropdown(
        id='feature-dropdown',
        options=[
            {'label': 'Relative Compactness', 'value': 'Relative_Compactness'},
            {'label': 'Surface Area', 'value': 'Surface_Area'},
            {'label': 'Glazing Area', 'value': 'Glazing_Area'},
            {'label': 'Overall Height', 'value': 'Overall_Height'}
        ],
        value='Relative_Compactness'
    ),

    # Graph for total load vs selected feature
    dcc.Graph(id='total-load-graph'),

    # Correlation heatmap
    dcc.Graph(id='correlation-heatmap', figure=px.imshow(df[['Relative_Compactness', 'Surface_Area', 'Glazing_Area', 'Overall_Height', 'Total_Load']].corr(), 
                                                         title="Correlation Matrix of Energy Efficiency Factors",
                                                         color_continuous_scale='aggrnyl',
                                                         zmin=-1, zmax=1))
])

# Define the callback to update the graph
@app.callback(
    Output('total-load-graph', 'figure'),
    [Input('feature-dropdown', 'value')]
)
def update_graph(selected_feature):
    fig = px.scatter(df, x=selected_feature, y='Total_Load', color='Cardinal_Orientation',
                     title=f'Total Load vs {selected_feature} with Orientation',
                     labels={selected_feature: selected_feature, 'Total_Load': 'Total Load'})
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
