import pandas as pd
import taipy.gui.builder as tgb
from taipy.gui import Gui, state

# Load dataset
file_path = "Data.csv"
df = pd.read_csv(file_path)

# Convert Timestamp to datetime and extract year
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
df["Year"] = df["Timestamp"].dt.year.astype("Int64")  # Convert to integer

# Ensure PM2.5 values are numeric and drop NaN values
df["PM2.5"] = pd.to_numeric(df["PM2.5"], errors="coerce")
df = df.dropna(subset=["PM2.5", "state", "Year"])  # Ensure no missing values

# Get available years
available_years = [2017,2018,2019,2020,2021,2022,2023,2024]

# Function to get top 10 states by PM2.5 for a given year
def get_top_states(year):
    filtered_df = df[df["Year"] == year]
    if filtered_df.empty:
        return pd.DataFrame({"state": [], "PM2.5": []})  # Return empty DataFrame if no data
    return (
        filtered_df.groupby("state")["PM2.5"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

# Set default values for Taipy State
selected_year = available_years[0] if available_years else None
chart_data = get_top_states(selected_year)
layout = {"yaxis": {"title": "PM2.5 Levels"}, "title": f"Top 10 States with highest PM2.5 Level in {selected_year}"}

# Function to update data when selector changes
def update_data(state, var_name, var_value):
    state.selected_year = int(var_value)  # Ensure it's an integer
    state.chart_data = get_top_states(state.selected_year)
    state.layout = {"yaxis": {"title": "PM2.5 Levels"}, "title": f"Top 10 States with highest PM2.5 Level in {state.selected_year}"}
print(available_years)
# Create UI
with tgb.Page() as page:
    tgb.text("Select a Year:")
    tgb.selector(value="{selected_year}", lov=available_years, on_change=update_data,dropdown=True, 
    label="Year")
    tgb.chart(data="{chart_data}", x="state", y="PM2.5", type="bar", layout="{layout}")

# Run GUI
gui = Gui(page)
gui.run(title="PM2.5 Dashboard",port="auto")
