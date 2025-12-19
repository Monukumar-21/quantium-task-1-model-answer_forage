import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px


df = pd.read_csv("sales.csv")

df['date'] = pd.to_datetime(df['date'])

daily_sales = df.groupby('date')['sales'].sum().reset_index()

fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={"date": "Date", "sales": "Total Sales"}
)

import datetime


fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={"date": "Date", "sales": "Total Sales"}
)


fig.add_shape(
    type="line",
    x0=datetime.datetime(2021, 1, 15),
    x1=datetime.datetime(2021, 1, 15),
    y0=daily_sales['sales'].min(),
    y1=daily_sales['sales'].max(),
    line=dict(color="red", width=2, dash="dash")
)

fig.add_annotation(
    x=datetime.datetime(2021, 1, 15),
    y=daily_sales['sales'].max(),
    text="Price Increase",
    showarrow=True,
    arrowhead=1
)


app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1("Soul Foods Sales Visualiser", style={'textAlign': 'center'}),
    dcc.Graph(id="sales-line-chart", figure=fig)
])

if __name__ == "__main__":
    app.run_server(debug=True)