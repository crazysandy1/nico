from flask import Flask, render_template, request
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import numpy as np

# Initialize Flask app
server = Flask(__name__)

# Initialize Dash app as a component of Flask
dash_app = Dash(__name__, server=server, url_base_pathname='/dash/')

# Generate sample data for visualization
nicotine_steps = np.linspace(0, 10, 11)
cytokine_increase = [10 + 5 * step for step in nicotine_steps]
viability_decrease = [100 - 8 * step for step in nicotine_steps]
oxidative_stress_increase = [20 + 7 * step for step in nicotine_steps]
metabolic_rate_decrease = [80 - 6 * step for step in nicotine_steps]
apoptosis_markers_increase = [10 + 4 * step for step in nicotine_steps]

medicine_steps = np.linspace(0, 10, 11)
cytokine_reduction = [cytokine_increase[-1] - 6 * step for step in medicine_steps]
viability_recovery = [viability_decrease[-1] + 7 * step for step in medicine_steps]
oxidative_stress_reduction = [oxidative_stress_increase[-1] - 6 * step for step in medicine_steps]
metabolic_rate_recovery = [metabolic_rate_decrease[-1] + 5 * step for step in medicine_steps]
apoptosis_markers_reduction = [apoptosis_markers_increase[-1] - 3 * step for step in medicine_steps]

# Dash layout
dash_app.layout = html.Div([
    html.H1("Nicotine Effect on Cell Health", style={"textAlign": "center"}),

    # Sliders
    html.Div([
        html.Label("Nicotine Exposure Level:"),
        dcc.Slider(
            id='nicotine-slider',
            min=0,
            max=10,
            step=1,
            value=0,
            marks={i: str(i) for i in range(11)},
        ),
    ], style={"padding": "20px"}),

    html.Div([
        html.Label("Medicine Response Level:"),
        dcc.Slider(
            id='medicine-slider',
            min=0,
            max=10,
            step=1,
            value=0,
            marks={i: str(i) for i in range(11)},
        ),
    ], style={"padding": "20px"}),

    # Graphs
    dcc.Graph(id='cytokine-levels-graph'),
    dcc.Graph(id='cell-health-graph'),
])

# Dash callbacks for interactivity
@dash_app.callback(
    [
        Output('cytokine-levels-graph', 'figure'),
        Output('cell-health-graph', 'figure')
    ],
    [
        Input('nicotine-slider', 'value'),
        Input('medicine-slider', 'value')
    ]
)
def update_graphs(nicotine_level, medicine_level):
    cytokine = cytokine_increase[nicotine_level] if medicine_level == 0 else cytokine_reduction[medicine_level]
    viability = viability_decrease[nicotine_level] if medicine_level == 0 else viability_recovery[medicine_level]
    oxidative_stress = oxidative_stress_increase[nicotine_level] if medicine_level == 0 else oxidative_stress_reduction[medicine_level]
    metabolic_rate = metabolic_rate_decrease[nicotine_level] if medicine_level == 0 else metabolic_rate_recovery[medicine_level]
    apoptosis_markers = apoptosis_markers_increase[nicotine_level] if medicine_level == 0 else apoptosis_markers_reduction[medicine_level]

    # Cytokine Levels Graph
    cytokine_fig = go.Figure()
    cytokine_fig.add_trace(go.Bar(x=["Cytokine Levels"], y=[cytokine], name="Cytokine Levels"))
    cytokine_fig.update_layout(title="Cytokine Levels (Inflammation Markers)", yaxis_title="Level", xaxis_title="Parameter")

    # Cell Health Graph
    cell_health_fig = go.Figure()
    cell_health_fig.add_trace(go.Bar(x=["Viability"], y=[viability], name="Viability"))
    cell_health_fig.add_trace(go.Bar(x=["Oxidative Stress"], y=[oxidative_stress], name="Oxidative Stress", marker_color='red'))
    cell_health_fig.add_trace(go.Bar(x=["Metabolic Rate"], y=[metabolic_rate], name="Metabolic Rate"))
    cell_health_fig.add_trace(go.Bar(x=["Apoptosis Markers"], y=[apoptosis_markers], name="Apoptosis Markers", marker_color='orange'))
    cell_health_fig.update_layout(
        title="Cell Health Parameters",
        yaxis_title="Level",
        xaxis_title="Parameters",
        barmode="group"
    )

    return cytokine_fig, cell_health_fig

# Flask routes
@server.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    server.run(debug=True)
