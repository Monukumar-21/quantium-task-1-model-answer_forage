import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import datetime

# Load sales data
df = pd.read_csv("sales.csv")
df['date'] = pd.to_datetime(df['date'])

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div(
    style={
        "backgroundColor": "#f9f9f9",
        "fontFamily": "Arial, sans-serif",
        "padding": "20px"
    },
    children=[
        html.H1(
            "Soul Foods Sales Visualiser",
            style={
                "textAlign": "center",
                "color": "#2c3e50",
                "marginBottom": "30px"
            }
        ),

        # Radio buttons for region selection
        html.Div(
            style={"textAlign": "center", "marginBottom": "20px"},
            children=[
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    labelStyle={"display": "inline-block", "margin": "10px", "fontSize": "18px"},
                    inputStyle={"marginRight": "5px"}
                )
            ]
        ),

        # Line chart
        dcc.Graph(id="sales-line-chart", style={"border": "2px solid #2c3e50", "borderRadius": "10px"})
    ]
)

# Callback to update chart based on region filter
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered = df.groupby("date")["sales"].sum().reset_index()
    else:
        filtered = df[df["region"] == selected_region].groupby("date")["sales"].sum().reset_index()

    fig = px.line(
        filtered,
        x="date",
        y="sales",
        title=f"Pink Morsel Sales Over Time ({selected_region.capitalize()})",
        labels={"date": "Date", "sales": "Total Sales"},
        template="plotly_white"
    )

    # Add vertical line for price increase
    fig.add_shape(
        type="line",
        x0=datetime.datetime(2021, 1, 15),
        x1=datetime.datetime(2021, 1, 15),
        y0=filtered["sales"].min(),
        y1=filtered["sales"].max(),
        line=dict(color="red", width=2, dash="dash")
    )

    fig.add_annotation(
        x=datetime.datetime(2021, 1, 15),
        y=filtered["sales"].max(),
        text="Price Increase",
        showarrow=True,
        arrowhead=1,
        font=dict(color="red")
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)