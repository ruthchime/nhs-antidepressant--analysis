
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load data
df = pd.read_csv("BSA_ODP_PCA_REGIONAL_DRUG_SUMMARY.csv")
df["DATE"] = pd.to_datetime(df["YEAR_MONTH"].astype(str), format="%Y%m")
df["COST_PER_ITEM"] = df["COST"] / df["ITEMS"]

# Initialize the Dash app
app = Dash(__name__)
app.title = "NHS Antidepressant Dashboard"

# Layout
app.layout = html.Div(style={'backgroundColor': '#111', 'color': '#fff', 'padding': '20px'}, children=[
    html.H1("NHS Antidepressant Prescribing Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Region:", style={"margin-right": "10px"}),
        dcc.Dropdown(
            id="region-dropdown",
            options=[{"label": r, "value": r} for r in df["REGION_NAME"].unique()],
            value="MIDLANDS",
            style={"width": "300px"}
        )
    ], style={"marginBottom": "20px"}),

    dcc.Graph(id="trend-chart"),
    dcc.Graph(id="top-drugs-chart")
])

# Callbacks
@app.callback(
    [Output("trend-chart", "figure"),
     Output("top-drugs-chart", "figure")],
    [Input("region-dropdown", "value")]
)
def update_charts(region):
    dff = df[df["REGION_NAME"] == region]

    # Trend over time
    trend = dff.groupby("DATE")[["ITEMS", "COST"]].sum().reset_index()
    fig1 = px.line(trend, x="DATE", y=["ITEMS", "COST"],
                   labels={"value": "Total", "DATE": "Date", "variable": "Metric"},
                   title=f"{region} - Monthly Trends", template="plotly_dark")

    # Top 10 drugs by items
    top_drugs = dff.groupby("BNF_CHEMICAL_SUBSTANCE")["ITEMS"].sum().sort_values(ascending=False).head(10)
    fig2 = px.bar(top_drugs[::-1], x=top_drugs[::-1].values, y=top_drugs[::-1].index,
                  title=f"{region} - Top 10 Prescribed Drugs", labels={"x": "Total Items", "y": "Drug"},
                  template="plotly_dark", orientation="h")

    return fig1, fig2

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)


