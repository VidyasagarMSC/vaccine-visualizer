## Covid vaccinations state-wise Visualization 

:construction: Work in progress

> Inspirated by Streamlit DataFrame demo

Data source: [covid19india/api](https://github.com/covid19india/api)

### Tools

- [Streamlit](https://streamlit.io) 
   ```sh
   pip install streamlit
   ```
- [Pandas](https://pandas.pydata.org)
- [Altair](https://altair-viz.github.io/)

### Run 

```sh
streamlit run covid_plot_statewise.py
```

### Data profiling

If you :heart: to see the data

```sh
pip install pandas-profiling
```

and then 

```sh
jupyter notebook
```
--> Open `covid_plot.ipynb`