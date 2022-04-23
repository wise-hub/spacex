# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("../data/spacex_launch_dash.csv")

max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

# Create a dash application
app = dash.Dash(__name__)

unique_sites = spacex_df["Launch Site"].unique().tolist()

launch_sites = []
launch_sites.append({"label": "All Sites", "value": "All Sites"})

for i in unique_sites:
    launch_sites.append({"label": i, "value": i})

print(launch_sites)


# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        # dcc.Dropdown(id='site-dropdown',...)
        dcc.Dropdown(
            id="site-dropdown",
            options=launch_sites,
            placeholder="Select Launch Site",
            searchable=True,
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        # dcc.RangeSlider(id='payload-slider',...)
        dcc.RangeSlider(
            id="payload_slider",
            min=0,
            max=10000,
            step=1000,
            marks={
                0: {"label": "0 kg"},
                1000: {"label": "1000 kg"},
                2000: {"label": "2000 kg"},
                3000: {"label": "3000 kg"},
                4000: {"label": "4000 kg"},
                5000: {"label": "5000 kg"},
                6000: {"label": "6000 kg"},
                7000: {"label": "7000 kg"},
                8000: {"label": "8000 kg"},
                9000: {"label": "9000 kg"},
                10000: {"label": "10000 kg"},
            },
            value=[min_payload, max_payload],
        ),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    [Input(component_id="site-dropdown", component_property="value")],
)
def update_piegraph(site_dropdown):
    if site_dropdown == "All Sites" or site_dropdown == "None":
        all_sites = spacex_df[
            spacex_df["class"] == 1
        ]  # All Success only for all sites.
        fig = px.pie(
            all_sites,
            names="Launch Site",
            title="Total Success Launches by All Sites",
            hole=0.2,
            color_discrete_sequence=px.colors.sequential.RdBu,
        )
    else:
        site_specific = spacex_df.loc[spacex_df["Launch Site"] == site_dropdown]
        fig = px.pie(
            site_specific,
            names="class",
            title="Total Success Launches for Site &#8608; " + site_dropdown,
            hole=0.2,
        )
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload_slider", component_property="value"),
    ],
)
def update_scattergraph(site_dropdown, payload_slider):
    if site_dropdown == "All Sites" or site_dropdown == "None":
        low, high = payload_slider
        all_sites = spacex_df
        inrange = (all_sites["Payload Mass (kg)"] > low) & (
            all_sites["Payload Mass (kg)"] < high
        )
        fig = px.scatter(
            all_sites[inrange],
            x="Payload Mass (kg)",
            y="class",
            title="Correlation Between Payload and Success for All Sites",
            color="Booster Version Category",
            size="Payload Mass (kg)",
            hover_data=["Payload Mass (kg)"],
        )
    else:
        low, high = payload_slider
        site_specific = spacex_df.loc[spacex_df["Launch Site"] == site_dropdown]
        inrange = (site_specific["Payload Mass (kg)"] > low) & (
            site_specific["Payload Mass (kg)"] < high
        )
        fig = px.scatter(
            site_specific[inrange],
            x="Payload Mass (kg)",
            y="class",
            title="Correlation Between Payload and Success for Site &#8608; "
            + site_dropdown,
            color="Booster Version Category",
            size="Payload Mass (kg)",
            hover_data=["Payload Mass (kg)"],
        )
    return fig


# Run the app
if __name__ == "__main__":
    app.run_server()
