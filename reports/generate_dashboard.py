import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from database.fetch_data import fetch_student_data

def generate_dashboard():
    """Create an interactive dashboard to visualize student performance."""
    
    # Fetch Data
    students, records, summaries = fetch_student_data()
    
    # Convert to DataFrame
    df_summary = pd.DataFrame(summaries)

    # Dashboard App
    app = dash.Dash(__name__)

    app.layout = html.Div(children=[
        html.H1("Student Performance Dashboard", style={'textAlign': 'center'}),
        
        # CGPA Distribution
        html.H3("CGPA Distribution"),
        dcc.Graph(
            figure=px.histogram(df_summary, x="cgpa", nbins=10, title="CGPA Distribution")
        ),

        # Semester-wise GPA
        html.H3("Semester-wise GPA Trends"),
        dcc.Graph(
            figure=px.line(df_summary, x="semester", y="gpa", color="registered_no", title="GPA Trend per Student")
        ),
    ])

    print("🌍 Dashboard running at http://127.0.0.1:8050")
    app.run_server(debug=True)

if __name__ == "__main__":
    generate_dashboard()
