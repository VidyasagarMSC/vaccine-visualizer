import streamlit as st
import pandas as pd
import altair as alt


from urllib.error import URLError

@st.cache
def get_vaccination_data():
    COVID_INDIA_URL = "https://api.covid19india.org/csv/latest/vaccine_doses_statewise.csv"
    df = pd.read_csv(COVID_INDIA_URL)
    df.columns.name = "date"
    new_cols = dict(zip(df.columns[1:], [pd.to_datetime(x,format="%d/%m/%Y").date() for x in df.columns[1:]]))
    df_formatted = df.rename(columns= new_cols, inplace=False)
    return df_formatted.set_index("State")

try:
   
    df = get_vaccination_data()
    states = st.multiselect(
        "Choose states", list(df.index), ["Andhra Pradesh", "Goa"]
    )
    
    if not states:
        st.error("Please select at least one state.")
    else:
        data = df.loc[states]
        #data /= 1000.0
        st.write("### Vaccinations", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["date"]).rename(
            columns={"date": "date", "value": "Total Individuals Vaccinated"}
        )
        chart = (
            alt.Chart(data)
            .mark_line()
            .encode(
                x="date:T",
                y=alt.Y("Total Individuals Vaccinated:Q", stack=None),
                color="State:N",
                strokeDash='State',
                tooltip = [alt.Tooltip('State:N'),
                           alt.Tooltip('date:T'),
                           alt.Tooltip('Total Individuals Vaccinated:Q')
                          ]
            ).interactive()
        )
    st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
    """
        % e.reason
    )