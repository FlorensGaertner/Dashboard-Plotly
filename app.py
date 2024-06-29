import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load your data
data_file = 'energy_efficiency_data.csv'
df = pd.read_csv(data_file)

# Calculate Total_Load and drop Heating_Load, Cooling_Load columns if they exist
if 'Heating_Load' in df.columns and 'Cooling_Load' in df.columns:
    df['Total_Load'] = df['Heating_Load'] + df['Cooling_Load']
    df_for_scatter = df.copy()  # Make a copy for scatter plot and table
    df_for_scatter.drop(['Heating_Load', 'Cooling_Load', 'Wall_Area', 'Roof_Area'], axis=1, inplace=True)
else:
    df_for_scatter = df.drop(['Wall_Area', 'Roof_Area'], axis=1)

# Calculate mean Total_Load per Relative_Compactness, Glazing_Area, and Overall_Height
mean_total_load_per_rc_ga = df_for_scatter.groupby(['Relative_Compactness', 'Glazing_Area', 'Overall_Height'])['Total_Load'].mean().reset_index()
mean_total_load_per_rc_ga['Total_Load'] = mean_total_load_per_rc_ga['Total_Load'].round(1)  # Round to 1 decimal place
mean_total_load_per_rc_ga['Total_Load'] = mean_total_load_per_rc_ga['Total_Load'].apply(lambda x: f'{x:.1f}' if x.is_integer() else f'{x}')

# Set option to disable deprecation warning for st.pyplot()
st.set_option('deprecation.showPyplotGlobalUse', False)

# Define Streamlit app layout
st.title("Energy Efficiency Dashboard")

# Heatmap for correlation matrix
st.header("Correlation Matrix of Energy Efficiency Factors")

# Calculate correlation matrix
correlation_matrix = df.corr()

# Create figure for heatmap
fig_heatmap = go.Figure(data=go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.columns,
    colorscale='Portland',
    zmin=-1, zmax=1
))
fig_heatmap.update_layout(title="Correlation Heatmap")

# Display heatmap
st.plotly_chart(fig_heatmap)

# Select Relative Compactness
st.header("Select Relative Compactness")
selected_compactness = st.selectbox("Choose Relative Compactness", sorted(df['Relative_Compactness'].unique()))

# Filter data based on selected compactness
filtered_df_3_5 = mean_total_load_per_rc_ga[(mean_total_load_per_rc_ga['Relative_Compactness'] == selected_compactness) &
                                            (mean_total_load_per_rc_ga['Overall_Height'] == 3.5)]
filtered_df_7 = mean_total_load_per_rc_ga[(mean_total_load_per_rc_ga['Relative_Compactness'] == selected_compactness) &
                                          (mean_total_load_per_rc_ga['Overall_Height'] == 7)]

# Check if filtered data is empty for both heights
if filtered_df_3_5.empty and filtered_df_7.empty:
    st.error(f"No data available for Relative Compactness: {selected_compactness}")
else:
    # Create subplot figure
    fig = make_subplots(rows=1, cols=1)

    # Add trace for Room Height 3.5 if data exists
    if not filtered_df_3_5.empty:
        filtered_df_3_5['Total_Load'] = pd.to_numeric(filtered_df_3_5['Total_Load'], errors='coerce')
        fig.add_trace(go.Scatter(
            x=filtered_df_3_5['Glazing_Area'],
            y=filtered_df_3_5['Total_Load'],
            mode='markers',
            marker=dict(color=filtered_df_3_5['Total_Load'], colorscale='Portland', showscale=True,
                        colorbar=dict(title="Total Load", tickvals=[0, 50, 100])),
            name='Room Height 3.5',
            hoverinfo='text',
            text=[f'Relative Compactness: {row.Relative_Compactness}<br>Glazing Area: {row.Glazing_Area}<br>Total Load: {row.Total_Load}<br>Room Height: {row.Overall_Height}' for _, row in filtered_df_3_5.iterrows()]
        ))

    # Add trace for Room Height 7 if data exists
    if not filtered_df_7.empty:
        filtered_df_7['Total_Load'] = pd.to_numeric(filtered_df_7['Total_Load'], errors='coerce')
        fig.add_trace(go.Scatter(
            x=filtered_df_7['Glazing_Area'],
            y=filtered_df_7['Total_Load'],
            mode='markers',
            marker=dict(color=filtered_df_7['Total_Load'], colorscale='Portland', showscale=True,
                        colorbar=dict(title="Total Load", tickvals=[0, 50, 100])),
            name='Room Height 7',
            hoverinfo='text',
            text=[f'Relative Compactness: {row.Relative_Compactness}<br>Glazing Area: {row.Glazing_Area}<br>Total Load: {row.Total_Load}<br>Room Height: {row.Overall_Height}' for _, row in filtered_df_7.iterrows()]
        ))

    # Update layout
    fig.update_layout(
        title=f'Mean Total Load per Glazing Area ({selected_compactness})',
        xaxis_title='Glazing Area',
        yaxis_title='Total Load',
        yaxis=dict(range=[0, 100]),  # Fix the range of y-axis from 0 to 100
        legend_title_text='Room Height'
    )

    # Display plotly figure
    st.plotly_chart(fig)

# Display message if no data is available for Room Height 3.5
if filtered_df_3_5.empty:
    st.warning(f"No Data for Room Height 3.5 for the Relative Compactness of {selected_compactness}")

# Display message if no data is available for Room Height 7
if filtered_df_7.empty:
    st.warning(f"No Data for Room Height 7 for the Relative Compactness of {selected_compactness}")
