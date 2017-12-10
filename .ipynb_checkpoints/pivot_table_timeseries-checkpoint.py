"""
Vertrekt van de tijdreeksen van de features van het teamleader ecosysteem.
Input:
    - Feature 
    - Specifiek bedrijf in het teamleader ecosysteem
Output:

    - Boxplot voor het bedrijf en de feature
"""

import sys

if sys.argv[1] == '-h':
    print("<pivot_table.py -feature -firm(s) >")
    quit()
    
# Hier komt het gedeelte waar we de argumenten vanuit de command line zullen parsen.

path = sys.argv[2] # pad waar figure opgeslagen wordt
top_x = float(sys.argv[1])  # 1. Vraag op hoeveel bedrijven samengenomen moeten worden
feature = sys.argv[3]


import pandas as pd
import numpy as np
import pickle  
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate


# De pivot tables zijn een verzameling dataframes. Per feature is er een dataframe gemaakt, deze bevat waarden voor de feature voor een volledig ecosysteem over verschillende tijdstippen.

pivot_tables = pickle.load(open('pivot_tables.p', 'rb'))

# Features die per dataframe beschreven zijn:
"""
        ['employees', 'revenue', 'datascouts score', 'social_score',
       'traction_score', 'business_size_score', 'seo_score',
       'median_load_time', 'median_load_time_percentile',
       'incoming_links_count', 'alexa_rank', 'alexa_rank_change',
       'reach_alexa_rank_change', 'reach_per_million',
       'reach_per_million_change_percentile', 'page_views_per_user',
       'page_views_per_user_change_percentile', 'page_views_per_million',
       'page_views_per_million_change_percentile', 'page_views_alexa_rank',
       'page_views_alexa_rank_change', 'rank', 'top_rank', 'domain_rating',
       'backlinks_count', 'referring_domains_count', 'referring_ips_count',
       'referring_class_c_count', 'referring_pages_count', 'checkins_count',
       'likes_count', 'talking_about_count', 'listed_count', 'tweet_count',
       'favourites_count']
"""

# Hier komt het gedeelte waar we zullen bepalen welke feature we wensen te onderzoeken, deze zal via de command line aangedreven worden
# Uit de pivottable zullen we één enkele dataframe voor deze feature halen.

df = pivot_tables[feature]

# We nemen de eerste week als de basis waarop we de grootste, kleinste en mediaan bedrijven zullen bepalen

basis = df.iloc[0, :]
basis = basis.dropna().sort_values(ascending=False) # sorteer de basis van hoog naar laag en verwijderen bedrijven met missing values. 
num_firms = len(basis)

# Hier komt het gedeelte waar we het gewenst aantal bedrijven met de hoogste feature waarden zullen zoeken.

top_firms = basis.head(round(top_x*num_firms))
print("Timeseries for top 5% firms on feature {} \n".format(feature))
top_firms = df.loc[:, top_firms.index]
print(top_firms)


# Hier komt het gedeelt waar we de mediaanwaarde van de feature zullen zoeken.

middle_firms = basis.iloc[round(0.475*num_firms):round(0.525*num_firms)] # Series hebben enkel een indexer nodig voor de rows
print("Timeseries for middle 5% firms on feature {} \n".format(feature))
middle_firms = df.loc[:, middle_firms.index]
print(middle_firms)
# Hier komt het gedeelte waar we het gewenst aantal bedrijven met de laagste feature waarden zullen zoeken.

bottom_firms = basis.tail(round(top_x*num_firms))
print("Timeseries for bottom 5% firms on feature {} \n".format(feature))
bottom_firms = df.loc[:, bottom_firms.index]
print(bottom_firms)
   
# Hier komt de functionaliteit die ervoor zorgt dat we tijdreeksen kunnen plotten

top_firms_mean = top_firms.mean(axis=1)
bottom_firms_mean = bottom_firms.mean(axis=1)
middle_firms_mean = middle_firms.mean(axis=1)

if True:
    import matplotlib
    plt.rcParams.update(plt.rcParamsDefault)
    plt.style.use('bmh')
    # Plot size to 14" x 7"
    matplotlib.rc('figure', figsize = (14, 7))
    # Font size to 14
    matplotlib.rc('font', size = 11)
    # Do not display top and right frame lines
    matplotlib.rc('axes.spines', top = False, right = False)
    # Remove grid lines
    matplotlib.rc('axes', grid = False)
    # Set backgound color to white
    matplotlib.rc('axes', facecolor = 'white')
    
    ax, fig = plt.subplots()
    fig.set_title('Time dependent range plot of feature {}'.format(feature))
    fig.set_ylabel(feature)
    # top firms
    plt.plot(top_firms_mean.index, top_firms_mean.values, label='Top Firms')
    plt.fill_between(top_firms_mean.index, top_firms.min(axis=1), top_firms.max(axis=1), color='#449DC7', alpha=.3, label='range top')
    
    # middle firms
    plt.plot(middle_firms_mean.index, middle_firms_mean.values, label='Middle Firms')
    plt.fill_between(middle_firms_mean.index, middle_firms.min(axis=1), middle_firms.max(axis=1), color='#B51F38', alpha=.3, label='range middle')
    
    # bottom firms
    plt.plot(bottom_firms_mean.index, bottom_firms_mean.values, label='Bottom Firms')
    plt.fill_between(bottom_firms_mean.index, bottom_firms.min(axis=1), bottom_firms.max(axis=1), color='#8D7FB3', alpha=.3, label='range bottom')
    _ = plt.xticks(rotation=45)
    plt.legend(loc='best')
    plt.savefig(path+'/'+feature+'.png')
    
    
    
    
# Hier komt de functionaliteit die ervoor zorgt dat we de gemiddelde waarden over de tijd heen kunnen plotten als een histogram voor alle bedrijven.
# Daarvoor moeten we uitrekenen welke de gemiddelde waarde van ieder bedrijf is voor de gegeven feature.


