import pandas as pd
import taipy.gui.builder as tgb
from taipy.gui import Gui, state

# Load dataset
file_path = "Data.csv"
df = pd.read_csv(file_path)

# Convert Timestamp to datetime and extract year
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
df = df.dropna(subset=["PM2.5", "state"])
available_state = sorted(df["state"].dropna().unique().tolist())
selected_state='Maharashtra'

# Function to get top 10 states by PM2.5 for a given year
def get_graph(s):
    filtered_df = df[df["state"] == s]
    filtered_df["Timestamp"] = pd.to_datetime(filtered_df["Timestamp"], errors="coerce")
    chart_values=filtered_df.groupby("Timestamp")["PM2.5"].mean().reset_index()
    
    # Return empty DataFrame if no data
    return (
        chart_values
    )


chart_data = get_graph(selected_state)
layout = {"yaxis": {"title": "PM2.5 Levels"}, "title": f"PM2.5 Level in {selected_state}","xaxis": {"title": "Years"}}

# Function to update data when selector changes
def update_data(state):
    state.selected_state = state.selected_state  # Ensure it's an integer
    state.chart_data = get_graph(state.selected_state)
    state.layout = {"yaxis": {"title": "PM2.5 Levels"}, "title": f"PM2.5 Level in {state.selected_state}","xaxis": {"title": "Years"}}

with tgb.Page() as page:
    tgb.text("Select State:")
    tgb.selector(value="{selected_state}", lov=available_state, on_change=update_data,dropdown=True, 
    label="State")
    tgb.chart(data="{chart_data}",mode='lines', x="Timestamp", y="PM2.5", layout="{layout}")

gui = Gui(page)
gui.run(title="PM2.5 Dashboard",port="auto")
