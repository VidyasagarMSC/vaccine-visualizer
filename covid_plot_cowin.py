import streamlit as st
import pandas as pd
import altair as alt

from urllib.error import URLError

@st.cache
def get_vaccination_data():
    """
    Data from Covid19India.org

    """
    COVID_INDIA_URL = "http://api.covid19india.org/csv/latest/cowin_vaccine_data_statewise.csv"
    df = pd.read_csv(COVID_INDIA_URL)
    return df

try:
   
    df = get_vaccination_data()
    pivot_table = df.pivot(index = 'State', columns = 'Updated On',values='Total Individuals Vaccinated')
    new_cols = dict(zip(pivot_table.columns, [pd.to_datetime(x,format="%d/%m/%Y").date() for x in pivot_table.columns]))
    df_formatted = pivot_table.rename(columns= new_cols, inplace=False)
    states = st.multiselect(
        "Choose states", list(df_formatted.index), ["Andhra Pradesh", "Goa"]
    )
    
    if not states:
        st.error("Please select at least one state.")
    else:
        data =  df_formatted.loc[states]
        st.write("### Vaccinations", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["Updated On"]).rename(
            columns={"Updated On": "date", "value": "Total Individuals Vaccinated"}
        )
        chart = (
            alt.Chart(data)
            .mark_line()
            .encode(
                x="date:T",
                y=alt.Y("Total Individuals Vaccinated:Q", stack=None),
                color="State:N",
            )
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