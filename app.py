import streamlit as st
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

# Streamlit app layout
st.title("Building Energy Efficiency Dashboard")

# Dropdown to select feature
feature = st.selectbox(
    'Select Feature',
    ['Relative_Compactness', 'Surface_Area', 'Glazing_Area', 'Overall_Height']
)

# Plot for total load vs selected feature
fig = px.scatter(df, x=feature, y='Total_Load', color='Cardinal_Orientation',
                 title=f'Total Load vs {feature} with Orientation',
                 labels={feature: feature, 'Total_Load': 'Total Load'})
st.plotly_chart(fig)

# Correlation heatmap
corr_matrix = df[['Relrative_Compactness', 'Surface_Area', 'Glazing_Area', 'Overall_Height', 'Total_Load']].corr()
heatmap_fig = px.imshow(corr_matrix, 
                        title="Correlation Matrix of Energy Efficiency Factors",
                        color_continuous_scale='aggrnyl',
                        zmin=-1, zmax=1)
st.plotly_chart(heatmap_fig)
