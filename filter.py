from taipy.gui import Gui, state
import taipy.gui.builder as tgb
import pandas as pd


data = pd.read_csv("Data.csv")


start_date = pd.to_datetime("2017-01-01")
end_date = pd.to_datetime("2017-12-31")

categories = ["state", "city", "station"]
selected_category = "city"

subcategories = ["PM2.5", "Funding"]
selected_subcategory = "PM2.5"

df = data.copy()
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

def get_chart(s, e, c, sub):
    df2 = data.copy()
    df2["Timestamp"] = pd.to_datetime(df2["Timestamp"])

    filtered_df = df2[(df2["Timestamp"] >= pd.to_datetime(s)) & (df2["Timestamp"] <= pd.to_datetime(e))]

    if c not in filtered_df.columns:
        print(f"Warning: Column '{c}' not found in dataset.")
        return pd.DataFrame(columns=[c, sub])

   
    filtered_df = filtered_df.dropna(subset=[c, sub])

    
    filtered_df[c] = filtered_df[c].astype(str)

   
    chart_df = (
        filtered_df.groupby(c)[sub]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )


    chart_df[c] = chart_df[c].astype(str)

    return chart_df



chart_data = get_chart(start_date, end_date, selected_category, selected_subcategory)

layout = {
    "yaxis": {"title": selected_subcategory},
    "xaxis": {
        "title": selected_category,
        "type": "category",
        "tickmode": "array", 
    },
    "title": f"{selected_category} Vs {selected_subcategory}",
}



def update_values(state):
    state.start_date = state.start_date
    state.end_date = state.end_date
    
    state.selected_category = state.selected_category  
    state.selected_subcategory = state.selected_subcategory  

    
    print(f"Updating Chart - Category: {state.selected_category}, Subcategory: {state.selected_subcategory}")

    state.chart_data = get_chart(
        state.start_date,
        state.end_date,
        state.selected_category,
        state.selected_subcategory
    )

    if state.selected_category in state.chart_data.columns:
        state.chart_data[state.selected_category] = state.chart_data[state.selected_category].astype(str)

    print("Unique X-axis values:", state.chart_data[state.selected_category].unique())

    state.layout = {
        "yaxis": {"title": state.selected_subcategory},
        "xaxis": {
            "title": state.selected_category,
            "type": "category",
            "tickmode": "array",
            "tickvals": list(range(len(state.chart_data[state.selected_category]))),  # Ensures labels are positioned correctly
            "ticktext": state.chart_data[state.selected_category].tolist(),  # Displays correct names
        },
        "title": f"{state.selected_category} Vs {state.selected_subcategory}",
    }

with tgb.Page() as page:
    with tgb.part(class_name="container"):
        tgb.text("# Filter by **Choice**", mode="md")
        with tgb.part(class_name="card"):
            with tgb.layout(columns="1 2 1"):
                with tgb.part():
                    tgb.text("Filter **From**", mode="md")
                    tgb.date("{start_date}")
                    tgb.text("To")
                    tgb.date("{end_date}")  
                with tgb.part():
                    tgb.text("Filter **Category**", mode="md")
                    tgb.selector(
                        value="{selected_category}",
                        lov=categories,
                        dropdown=True,  
                    )
                    tgb.text("Filter **Subcategory**", mode="md")
                    tgb.selector(
                        value="{selected_subcategory}",
                        lov=subcategories,
                        dropdown=True, 
                    )
                with tgb.part(class_name="text-center"):
                    tgb.button(
                        "Apply",
                        class_name="plain apply_button",
                        on_action=update_values
                    )
        tgb.html("br")
        tgb.chart(
        data="{chart_data}",  
        x="{selected_category}",  
        y="{selected_subcategory}",  
        type="bar",
        layout="{layout}"
)
        tgb.html("br")

Gui(page=page).run(title="Filtration", dark_mode=True, debug=True,port="auto")
