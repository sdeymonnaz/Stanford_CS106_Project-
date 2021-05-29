# Load all necessary libraries
import os
import pandas as pd
from matplotlib import pyplot as plt
import geopandas as gpd
import random

# Set the working directory and map size
os.chdir("/Users/SPD/OneDrive/Documentos/Stanford Code in "
         "Place/Stanford_CS106_Project/Stanford_CS106_Project-/Project_map_plotter/")
plt.rcParams["figure.figsize"] = (12, 8)

COUNTRY_DIRECTORY = "countries/"


# These functions activate the user choices to display countries, top and bottom cities
# and play the geo game.

def user_console():
    os.system('clear')
    print("#"*15, " GEO DATA APP ", "#"*15, sep="")
    print("1 - Display world map")
    print("2 - Display selected country")
    print("3 - Display selected city")
    print("4 - Top 10 most populous cities")
    print("5 - Top 10 least populated cities")
    print("6 - Play Geo-Game!")
    print("7 - Exit to close program")
    print()
    menu_selection = input("Type the number of your choice please:")
    print()
    return menu_selection


def validate_country(country_selection):
    if country_selection not in country_names:
        print("Country not found")
        print()
        user_console()


def validate_city(city_selection):
    if city_selection not in cities_names:
        print("City not found")
        print()
        user_console()


def show_country_all():
    ax = world.plot(color='white', edgecolor='black')
    world_cities.plot(ax=ax, color='blue', markersize=1)
    plt.show(block=False)
    

def show_country(country_selection):
    world_cities_sel = world_cities[world_cities.country == country_selection]
    ax = world[world.name == country_selection].plot(color='white', edgecolor='black')
    world_cities_sel.plot(ax=ax, color='blue', markersize=1)
    plt.show(block=False)
    
    
def show_city(country_selection, city_selection):
    validate_country(country_selection)
    validate_city(city_selection)
    world_cities_sel = world_cities[world_cities.country == country_selection]
    world_cities_sel = world_cities_sel[world_cities_sel.city == city_selection]
    ax = world[world.name == country_selection].plot(color='white', edgecolor='black')
    world_cities_sel.plot(ax=ax, color='blue', markersize=6)
    for x, y, text in zip(world_cities_sel.lon, world_cities_sel.lat, world_cities_sel.city):
        plt.text(x, y, text, fontsize=13, color='blue')
    plt.show(block=False)
    

def top_population():
    world_cities_top = world_cities.sort_values(by=['popu'], ascending=False)
    world_cities_top = world_cities_top.head(10)
    ax = world.plot(color='white', edgecolor='black')
    world_cities_top.plot(ax=ax, color='blue', markersize=1)
    for x, y, text in zip(world_cities_top.lon, world_cities_top.lat, world_cities_top.city):
        plt.text(x, y, text, fontsize=8, color='blue', backgroundcolor='#d6cd80', ha='center',
                 stretch='ultra-condensed').set_bbox(dict(facecolor='yellow', alpha=0.5, edgecolor='yellow'))
    plt.show(block=False)


def bottom_population():
    world_cities_top = world_cities.sort_values(by=['popu'], ascending=True)
    world_cities_top = world_cities_top.head(10)
    ax = world.plot(color='white', edgecolor='black')
    world_cities_top.plot(ax=ax, color='blue', markersize=1)
    for x, y, text in zip(world_cities_top.lon, world_cities_top.lat, world_cities_top.city):
        plt.text(x, y, text, fontsize=8, color='blue', backgroundcolor='#746d6f', ha='center',
                 stretch='ultra-condensed').set_bbox(dict(facecolor='yellow', alpha=0.5, edgecolor='yellow'))
    plt.show(block=False)


def play_geo_game():
    names_list = world['name'].to_list()
    random_country_idx = random.randint(0, 177)  
    random_country = names_list[random_country_idx]
    world_game = world[world['name'] == random_country]
    continent = world_game.loc[:, ['continent']].to_string(index=False, header=False)
    show_country(names_list[random_country_idx])
    
    answer = input("Guess country's name: ")        
    if answer.upper() == random_country.upper():
        game_won()
    else:
        print("Incorrect")
        print("First hint: this country is located in", continent, sep="")
        print()
    
    answer = input("Try again, guess the country's name: ")
    if answer.upper() == random_country.upper():
        game_won()
    else:
        print("Incorrect")
        print("Second hint: the first three letters of country's name are: ", random_country[0:3], sep="")
        print()
    
    answer = input("Last chance, enter country's name: ")
    if answer.upper() == random_country.upper():
        game_won()
    else:
        print("Incorrect. The name of country was ", random_country, sep="")
        print("Game over")
        print()


def game_won():
    print("Correct! You won the geo-game")
    print()


# Create a list of country names for the 200 files
country_names = [s.split(".")[0] for s in os.listdir(COUNTRY_DIRECTORY)]

# Create an empty dataframe to stack all data
countries = pd.DataFrame()

# Build a Pandas dataframe with all csv data and add a column with the country name
for name in country_names:
    filename = COUNTRY_DIRECTORY + name + ".csv"
    part = pd.read_csv(filename, skiprows=1, header=None)
    part["country"] = name
    countries = pd.concat([countries, part], axis=0)

# Rename dataframe columns and reset the index column
countries = countries.rename(columns={0: "city", 1: "lat", 2: "lon", 3: "popu"})
countries.reset_index(drop=True, inplace=True)

# Load GeoPandas countries boundaries dataframe.Fix harmonize United States name in both datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world['name'].replace(to_replace='United States of America', value='United States', inplace=True)

# Create a GeoPandas dataframe with the data collected from the 200 csv files
world_cities = gpd.GeoDataFrame(countries, geometry=gpd.points_from_xy(countries.lon, countries.lat))

# Create a list with the 26500 from the CSV files.
cities_names = list(world_cities['city'])


menu_choice = user_console()
while menu_choice != "7":
    if menu_choice == "1":
        show_country_all()
        input("Press enter to continue")
        menu_choice = user_console()

    elif menu_choice == "2":
        country_sel = input("Type the name of the country or leave empty to exit ")
        validate_country(country_sel)
        if country_sel == "":
            break
        else:
            show_country(country_sel)
            input("Press enter to continue")
            menu_choice = user_console()

    elif menu_choice == "3":
        country_sel = input("Type the name of the country or leave empty to exit ")
        if country_sel == "":
            break
        else:
            city_sel = input("Type a city name or 'all' for all cities: ")
            if city_sel == "all":
                show_country(country_sel)
                input("Press enter to continue")
                menu_choice = user_console()
            else:
                show_city(country_sel, city_sel)
                input("Press enter to continue")
                menu_choice = user_console()

    elif menu_choice == "4":
        top_population()
        input("Press enter to continue")
        menu_choice = user_console()

    elif menu_choice == "5":
        bottom_population()
        input("Press enter to continue")
        menu_choice = user_console()

    elif menu_choice == "6":
        play_geo_game()
        input("Press enter to continue")
        menu_choice = user_console()
        
    elif menu_choice == "7":
        exit()
