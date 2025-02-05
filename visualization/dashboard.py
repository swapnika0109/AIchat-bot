import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

class Dashboard:
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.setup_layout()

    def setup_layout(self):
        """Set up dashboard layout"""
        self.app.layout = html.Div([
            html.H1("Customer Support Analytics"),
            
            dcc.Tabs([
                dcc.Tab(label='Conversation Overview', children=[
                    dcc.Graph(id='daily-conversations'),
                    dcc.Graph(id='topic-distribution')
                ]),
                
                dcc.Tab(label='User Segments', children=[
                    dcc.Graph(id='user-segments'),
                    dcc.Graph(id='segment-characteristics')
                ]),
                
                dcc.Tab(label='Performance Metrics', children=[
                    dcc.Graph(id='response-times'),
                    dcc.Graph(id='satisfaction-scores')
                ])
            ])
        ])

    def update_conversation_metrics(self, data: pd.DataFrame):
        """Update conversation metrics"""
        # Create daily conversation trend
        daily_trend = px.line(
            data.groupby('date')['conversation_id'].count().reset_index(),
            x='date',
            y='conversation_id',
            title='Daily Conversations'
        )
        return daily_trend

    def run_server(self, debug=True):
        """Run the dashboard server"""
        self.app.run_server(debug=debug) 