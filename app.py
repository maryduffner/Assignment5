# %% [markdown]
# ### Assignment #4: Basic UI
# 
# DS4003 | Spring 2024
# 
# Objective: Practice buidling basic UI components in Dash. 
# 
# Task: Build an app that contains the following components user the gapminder dataset: `gdp_pcap.csv`. [Info](https://www.gapminder.org/gdp-per-capita/)
# 
# UI Components:
# A dropdown menu that allows the user to select `country`
# -   The dropdown should allow the user to select multiple countries
# -   The options should populate from the dataset (not be hard-coded)
# A slider that allows the user to select `year`
# -   The slider should allow the user to select a range of years
# -   The range should be from the minimum year in the dataset to the maximum year in the dataset
# A graph that displays the `gdpPercap` for the selected countries over the selected years
# -   The graph should display the gdpPercap for each country as a line
# -   Each country should have a unique color
# -   Graph DOES NOT need to interact with dropdown or slider
# -   The graph should have a title and axis labels in reader friendly format  
# 
# Layout:  
# - Use a stylesheet
# - There should be a title at the top of the page
# - There should be a description of the data and app below the title (3-5 sentences)
# - The dropdown and slider should be side by side above the graph and take up the full width of the page
# - The graph should be below the dropdown and slider and take up the full width of the page
# 
# Submission: 
# - There should be only one app in your submitted work
# - Comment your code
# - Submit the html file of the notebook save as `DS4003_A4_LastName.html`
# 
# 
# **For help you may use the web resources and pandas documentation. No co-pilot or ChatGPT.**

# %%
# import dependencies

from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px

# %%
# reading in the data
df = pd.read_csv("gdp_pcap.csv")

# previewing the data
df.head()

# %%
# cleaning the data to make 3 columns in order to convert the wide df to a long df 
df_long = pd.melt(df, id_vars ='country', var_name ='year', value_name = 'gdp per capita')

df_long.head()

# %%
# looking at the types of data we have...all objects (maybe we want to change these to numerical)
df_long.info()

# %%
# we want the year to be an int to be able to use it in the slider 
df_long['year'] = df_long['year'].astype(int)

# here we are converting the gdp per capita values (ex: 10k --> 10000) as ints to then use in the graph
df_long['gdp per capita'] = df_long['gdp per capita'].replace({"k":"*1e3"}, regex=True).map(pd.eval).astype(int)

df_long.info()

# %%
# build a line chart
fig = px.line(df_long, 
                      x = 'year', 
                      y = 'gdp per capita', 
                      color = 'country', # each line is a country
                      title = 'GDP Per Capita Over Time')
# display the chart
fig.show()

# %%
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # load the CSS stylesheet

app = Dash(__name__, external_stylesheets=stylesheets) # initialize the app

# %%
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Mary Duffner Assignment 5', className="app-header--title") # creating the title of the page 
        ]
    ),
    html.Div(
        children=html.Div([
            html.H1('Description'), # header for our overview below
            html.Div('''
                This dashboard is an interactive interface
                     allowing users to look at specific countries' gdp
                     per capita within a range of time. We utilize a dataset
                     called gdp_pcap.csv which includes gdp per 
                     capita data with dates ranging from 1800 - 2100. We needed to
                     manipulate this dataframe in order to create 3 working columns
                     to use including: country (stayed the same), year, and
                     gdp per capita. We allow users to select multiple countries 
                     and a range of dates to then show visually what the gdp per 
                     capita looks like over time with a line graph. 
            ''')
        ])
    ),
    html.Div(children = [
        html.H2(children = 'Select Countries'),
        dcc.Dropdown(
            df_long.country.unique(), # this targets the country column
            id = 'country-column',
            placeholder =  'select a column',
            multi = True, # this allows us to select multiple
            value = 'USA' # want a default value so that we have something on the graph (user can change this)
            )
    ], style = {'display': 'inline-block', 'width': '50%'}), # we use this in order to have the dropdown take up half the page
    # we want the slider to be next to the dropdown taking up the other half of the page
    html.Div([
        html.H2(children = 'Select Year Range'),
        dcc.RangeSlider(
            min = df_long['year'].min(), # pulling the minimum year
            max = df_long['year'].max(), # pulling the maximum year
            marks = {year: {'label': str(year), 'style': {'writingMode': 'vertical-rl'}} 
                     for year in range(df_long['year'].min(), df_long['year'].max() + 1, 10)}, 
            step = 1,
            value = [df_long['year'].min(), df_long['year'].max()], 
            id = 'year-slider',
            tooltip = {'always_visible': True}
    )
    ], style = {'display': 'inline-block', 'width': '50%'}), # this is making the slider in line with the dropdown to take up rest of page
    html.Div(
        dcc.Graph(
        id='GDP per Capita',
        figure = fig, # bringing in the graph we built above to visualize the countries' gdp per capita over time
        style = {'marginTop' : '50px'} # I did this to push up the slider so that the years weren't cut off
    )
    )
])

# define callbacks
@app.callback(
    Output('GDP per Capita', 'figure'), # we want to output the graph
    Input('country-column', 'value'), # one input is the countries from the dropdown
    Input('year-slider', 'value')) # the other input is the year range on the slider
def update_graph(selected_country, selected_year): 
    if not isinstance(selected_country, list): # without this, we get a value error --> ensuring the data from the dropdown is a string
        # so that we can compare columns of different lengths
        selected_country = [selected_country]

    # need to ensure all inputs are within the available options from the data...without this we get an error
    dff = df_long[(df_long['year'] >= selected_year[0]) & (df_long['year'] <= selected_year[1]) &
                   (df_long['country'].isin(selected_country))]

    fig = px.line(dff, # creating my line graph
                    x = 'year', 
                    y = 'gdp per capita', 
                    color = 'country',
                    title = 'GDP Per Capita Over Time',
                    )

    return fig

# run app
if __name__ == '__main__':
    app.run_server(debug=True)
 


