import os
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

# Read in the data
data = pd.read_csv(os.path.join("data","precious_metals_prices_2018_2021.csv"))
data["DateTime"] = pd.to_datetime(data["DateTime"], format="%Y-%m-%d %H:%M:%S")

print(data.head())



app = dash.Dash(__name__)
app.title = "Precious Metal Prices 2018-2021"

fig = px.line(
    data,
    title="Precious Metal Prices 2018-2021",
    x="DateTime",
    y=[i for i in data.columns[1:]],
        color_discrete_map={"Gold": "gold"}
)


#Define layout
app.layout = html.Div(
    id="app-container",
    children=[
        html.Div(
            id="header-area",
            children=[
                html.H1(
                    id="header-title",
                    children="Precious Metal Prices",

                ),
                html.P(
                    id="header-description",
                    children=("The cost of precious metals", html.Br(), "between 2018 and 2021"),
                ),
            ],
        ),
        html.Div(
            id="menu-area",
            children=[
                html.Div(
                    children=[
                        html.Div(
                            className="menu-title",
                            children="Metal"
                        ),
                        dcc.Dropdown(
                            id="metal-filter",
                            className="dropdown",
                            options=[{"label": metal, "value": metal} for metal in data.columns[1:]],
                            clearable=False,
                            value="Gold"
                        ),
                        html.Div( children=[
                            html.Div(
                                className="menu-title",
                                children="Date Range"
                            ),
                            dcc.DatePickerRange(
                                id="date-range",
                               min_date_allowed=data.DateTime.min().date(),
                               max_date_allowed=data.DateTime.max().date(),
                               start_date=data.DateTime.min().date(),
                               end_date=data.DateTime.max().date()
                            )
                        ])
                    ]
                )
            ]
        ),
        html.Div(
            id="graph-container",
            children=dcc.Graph(
                id="price-chart",
                figure=fig,
                config={"displayModeBar": False}
            ),
        ),
    ]
)

@app.callback(
    Output("price-chart", "figure"),
    Input("metal-filter", "value"),
    
    Input("date-range", "start_date"),
    Input("date-range", "end_date")
)
def update_chart_data(selected_metal, start_date, end_date):
    # filtered_data = data[["DateTime", selected_metal]]
    filtered_data = data.loc[(data.DateTime >=start_date) & (data.DateTime <= end_date)]
    filtered_data = filtered_data[["DateTime", selected_metal]]
        
    # Create a plotly plot for use by dcc.Graph().
    fig = px.line(
        filtered_data,
        title="Precious Metal Prices 2018-2021",
        x="DateTime",
        # y=[i for i in data.columns[1:]],
        y=[selected_metal],
        color_discrete_map={"Gold": "gold", 
                            "Platinum": "#123456",
                            "Silver":"#654321",
                                "Palladium":"#234432",
                                "Rhodium":"#876567",
                                "Iridium":"#98ab23",
                                    "Ruthenium":"#721123"}
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Price (USD/oz)",
        font=dict(
            family="Verdana, sans-serif",
            size=18,
            color="white"
        ),
    )
    
    return fig



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))  # Use PORT if available, fallback to 8050 locally
    app.run(host='0.0.0.0', port=port, debug=True)