from taipy.gui import Gui, state
import taipy.gui.builder as tgb
import pandas as pd
import taipy as tp

data = pd.read_csv("Data.csv")
state1_list = sorted(data["state"].dropna().unique().tolist())
state1 = "Gujarat"

state2_list = sorted(data["state"].dropna().unique().tolist())
state2 = "Maharashtra"


def yearly_average_pm25(state1: str, state2: str) -> pd.DataFrame:
    df=data.copy()
    print(state1,state2)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

    df_filtered = df[(df["Timestamp"].dt.year >= 2019) & (df["Timestamp"].dt.year <= 2024)]

    df_filtered = df_filtered[df_filtered["state"].isin([state1, state2])]

    yearly_avg_pm25 = df_filtered.groupby([df_filtered["Timestamp"].dt.year, "state"])["PM2.5"].mean().unstack()
    yearly_avg_pm25.reset_index(inplace=True)
    yearly_avg_pm25.columns = ["Year", state1, state2]
    print(yearly_avg_pm25)
    return yearly_avg_pm25


chart_data = yearly_average_pm25(state1,state2)
layout = {
  "yaxis": {"title": "PM2.5 Levels"},
    "title": f"Comparision Between {state1} & {state2}"
  }

def update_values(state):
    state.state1 = state.state1
    state.state2 = state.state2
    print(state.state1,state.state2)
    state.chart_data = yearly_average_pm25(
        state.state1,
        state.state2
    )
    state.layout={
  "yaxis":{"title": "PM2.5 Levels"},
    "title": f"Comparision Between {state.state1} & {state.state2}"
  }
    


with tgb.Page() as page:
    with tgb.part(class_name="container"):
        tgb.text("# Compare PM2.5 Levels of Two States", mode="md")
        with tgb.part(class_name="card"):
            with tgb.layout(columns="1 1 1"):
                with tgb.part():
                    tgb.text("Select **State 1**", mode="md")
                    tgb.selector(value="{state1}",
                                 lov=state1_list,
                                 dropdown=True
                                 )  
                with tgb.part():
                    tgb.text("Select **State 2**", mode="md")
                    tgb.selector(
                        value="{state2}",
                        lov=state2_list,
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
        mode='lines' , 
        x='Year', 
        y__1="{state1}",
        y__2="{state2}" ,
        color__1='blue',
        color__2='red',
        layout="{layout}"
)

Gui(page=page).run(title="Comparision", dark_mode=True, debug=True,port="auto")
