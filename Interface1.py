# Import the liberies
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.figure_factory as ff
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff
import pandas as pd

#Code of the model
import pandas as pd
# Define beer outside the function as global variable because we use It in and outside the function
Beer = pd.read_csv('Bieren1.csv', sep=";")

def calculate_score(Input_beer):
    #Taking the variable beer inside the function
    global Beer    

    #Calculate alcohol category
    Beer["Alcohol percentage"] = Beer["Alcohol percentage"].astype(int)

    def Calculate_alcohol(input):
        beer_dataset = input
            
        if (beer_dataset <= 5):
            return "Low"
        if (beer_dataset >= 8):
            return "High"
        else:
            return "Average"
        
    Beer["Alcohol"] = Beer["Alcohol percentage"].apply(Calculate_alcohol)


    Beer_like = Beer[Beer['Name beer'].str.contains(Input_beer)]
    Beer_like

    #Name brewery
    Great_brewer = Beer_like["Brewery"]
    Great_brewer = Great_brewer.reset_index()
    Great_brewer = Great_brewer["Brewery"]
    Great_brewer = Great_brewer[0]

    #Give score for brewery
    def Good_brewer(input):
        beer_dataset = input
        Name_brewer = Great_brewer
        
        if (beer_dataset == Name_brewer):
            return 1
        else:
            return 0
        
        
    Beer["Score_brewer"] = Beer["Brewery"].apply(Good_brewer)

    #Color beer
    Color_beer = Beer_like["Kleur"]
    Color_beer = Color_beer.reset_index()
    Color_beer = Color_beer["Kleur"]
    Color_beer = Color_beer[0]

    #Give score for beer color
    def Good_color(input):
        beer_dataset = input
        #color_beer = Great_brewer
        
        if (beer_dataset == Color_beer):
            return 1
        else:
            return 0
        
        
    Beer["Score_color"] = Beer["Kleur"].apply(Good_color)

    #Country beer
    Country_beer = Beer_like["land"]
    Country_beer = Country_beer.reset_index()
    Country_beer = Country_beer["land"]
    Country_beer = Country_beer[0]
    Country_beer

    #Give score for beer origin
    def Good_country(input):
        beer_dataset = input
        #color_beer = Great_brewer
        
        if (beer_dataset == Country_beer):
            return 1
        else:
            return 0
        
        
    Beer["Score_country"] = Beer["land"].apply(Good_country)

    Beer[['taste_a','taste_b']] = Beer.Taste.str.split(",",expand=True)

    #taste beer
    taste_beer = Beer_like["Taste"]
    taste_beer = taste_beer.reset_index()
    taste_beer = taste_beer["Taste"]
    taste_beer = taste_beer[0]

    #Give score for beer origin
    def Good_taste(input):
        beer_dataset = input
        #color_beer = Great_brewer
        
        if (beer_dataset in taste_beer):
            return 1
        else:
            return 0
        
    Beer["Score_taste_a"] = Beer["taste_a"].apply(Good_taste)
    Beer["Score_taste_b"] = Beer["taste_b"].apply(Good_taste)

    #type beer
    type_beer = Beer_like["Soort"]
    type_beer = type_beer.reset_index()
    type_beer = type_beer["Soort"]
    type_beer = type_beer[0]

    #Give score for beer type
    def Good_type(input):
        beer_dataset = input
        
        
        if (beer_dataset in type_beer):
            return 1
        else:
            return 0
        
    Beer["type_beer"] = Beer["Soort"].apply(Good_type)

    #type alcohol
    type_alcohol = Beer_like["Alcohol"]
    type_alcohol = type_alcohol.reset_index()
    type_alcohol = type_alcohol["Alcohol"]
    type_alcohol = type_alcohol[0]
    type_alcohol

    def Good_alcohol(input):
        beer_dataset = input
        
        
        if (beer_dataset in type_alcohol):
            return 1
        else:
            return 0
        
    Beer["Score_alchohol"] = Beer["Alcohol"].apply(Good_alcohol)

    Beer["Final_score"] = (Beer["Score_brewer"] + Beer["Score_color"] + Beer["Score_country"] + Beer["Score_taste_a"] + Beer["Score_taste_b"] + Beer["type_beer"] + Beer["Score_alchohol"])/7*100

    Beer = Beer.sort_values(by='Final_score', ascending=False)
    uit = Beer[["Brewery","Name beer","Final_score"]]
    #Output function
    return uit




    #Code to run the Table with restaurants

#Define initial table
select_table = Beer
tabel = ff.create_table(select_table, height_constant=20)


#Connection with external style sheet, with style for tables, headers and drop down menu
external_stylesheets = [dbc.themes.COSMO]
app = dash.Dash(external_stylesheets=external_stylesheets)




#Layout app graphs that have to be full screen width are a div on its own, one table left and one right is one div together.

app.layout = html.Div(children=[

#Title and subtitle
html.Div([
    html.H1(children="Find your favorite beer"),
    html.H2(children= "Enter a beer you like!")
    ]),


#Introduction text for the users
html.Div([
    html.Blockquote("In the Netherlands there are a great amount of great breweries, to explore new beers just enter a beer you like, the system would recommend you other beers that are good for you")
]),
dcc.Dropdown(   
    id="selection",
    options=[{"label": "All", "value": "All"},
            {"label": "Texelse bierbrouwerij Overzee IPA", "value": "Overzee IPA"},
            {"label": "Texelse bierbrouwerij Skuumkoppe", "value": "Skuumkoppe"},
            {"label": "Texelse bierbrouwerij Wit", "value": "Wit"},
            {"label": "Texelse bierbrouwerij Tripel", "value": "Tripel"},
            {"label": "Texelse bierbrouwerij Goudkoppe", "value": "Goudkoppe"},
            {"label": "Texelse bierbrouwerij Vuurbaak", "value": "Vuurbaak"},
            {"label": "Texelse bierbrouwerij Springtij", "value": "Springtij"},
            {"label": "Brasserie d'Achouffe Chouffe Houblon", "value": "Chouffe Houblon"},
            {"label": "Brasserie d'Achouffe Chouffe Blanche", "value": "Chouffe Blanche"},
            {"label": "Brasserie d'Achouffe Cherry chouffe", "value": "Cherry chouffe"},
            {"label": "Brasserie d'Achouffe MC Chouffe", "value": "MC Chouffe"},
            {"label": "Brasserie d'Achouffe La Chouffe Blond", "value": "La Chouffe Blond"},
            {"label": "Brasserie d'Achouffe Chouffe Soleil", "value": "Chouffe Soleil"},
            {"label": "Brasserie d'Achouffe N'ice Chouffe", "value": "N'ice Chouffe"},
            {"label": "Scheldebrouwerij n Toeback", "value": "n Toeback"},
            {"label": "Scheldebrouwerij Witheer", "value": "Witheer"},
            {"label": "Scheldebrouwerij Ginnegapper", "value": "Ginnegapper"},
            {"label": "Scheldebrouwerij Krab", "value": "Krab"},
            {"label": "Scheldebrouwerij Oesterstout", "value": "Oesterstout"},
            {"label": "Scheldebrouwerij Hop Euiter", "value": "Hop Euiter"},
            {"label": "Scheldebrouwerij Lamme Goedzak", "value": "Lamme Goedzak"},
            {"label": "Scheldebrouwerij Dulle Griet", "value": "Dulle Griet"},
            {"label": "Scheldebrouwerij Strandgaper", "value": "Strandgaper"},
            {"label": "Scheldebrouwerij Wildebok", "value": "Wildebok"},
            {"label": "TX Brouwerij TX Hopblond", "value": "TX Hopblond"},
            {"label": "TX Brouwerij TX Barrel Aged Bock", "value": "TX Barrel Aged Bock"},
            {"label": "TX Brouwerij TX Goudwit", "value": "TX Goudwit"},
            {"label": "TX Brouwerij TX Donkerblond", "value": "TX Donkerblond"}
            
            ],value='All'),




#the table with the restaurants selected
html.Div([
    html.H3("Recommended beers:"),
    dcc.Graph(
    id='tabel',
    figure=tabel
)],className= "six colomns"),


])

#Interactivity for the dropdown menu. With the callback the data in the graphs will change if you change someting in the dropdown.
#filter on type graph

#Selection on table
@app.callback(    
    Output("tabel", "figure"),    
    [Input("selection", "value")])
def display_table(type_selected):
    if type_selected != "All":
        
        # New dataset is created by running function type_selected
        select_table = calculate_score(type_selected)
        tabel = ff.create_table(select_table, height_constant=20)
    
    
    return tabel
 


#run the app
if __name__ == '__main__':
  app.run_server(debug=False)



