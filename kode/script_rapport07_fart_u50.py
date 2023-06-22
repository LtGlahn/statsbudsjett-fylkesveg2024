from datetime import datetime 

import geopandas as gpd 
import pandas as pd
import numpy as np
from copy import deepcopy

import STARTHER
import lastnedvegnett  
import skrivdataframe
import nvdbapiv3
import nvdbgeotricks

t0 = datetime.now()

#  EnumInSetProvider(105, 2021, 2726, 2728, 11576, 2730, 19885)//TODO: la til 5km/t i listen. Skjekk om det er riktig!
# 
# 
# Eks bygge spørring: egenskap(10278)>=2000 AND egenskap(1313)<=100


egenskapfilter = 'egenskap(2021)=2726 OR egenskap(2021)=2728 OR egenskap(2021)=11576 OR egenskap(2021)=2730 OR egenskap(2021)=19885'


mittfilter = lastnedvegnett.kostraFagdataFilter( mittfilter={} )
mittfilter['vegsystemreferanse'] = 'Fv'
mittfilter['egenskap'] = egenskapfilter
mittfilter['adskiltelop'] = 'med,nei'
mittfilter['sideanlegg'] = 'false'

sok = nvdbapiv3.nvdbFagdata( 105 )
sok.filter( mittfilter )
myGdf = nvdbgeotricks.nvdbsok2GDF( sok ) 
myGdf.to_file( '../resultater/vegnettFV.gpkg', layer='fartU50', driver='GPKG')

myGdf = myGdf[ myGdf['trafikantgruppe'] == 'K']

telling = myGdf.groupby( ['fylke' ]).agg( { 'segmentlengde' : 'sum'} ).astype(int).reset_index()
telling['segmentlengde'] = telling['segmentlengde'] / 1000  
telling.rename( columns={ 'segmentlengde' : 'Veg med fartsgrense 50 km/t eller lavere (km)' }, inplace=True)

skrivdataframe.skrivdf2xlsx( telling, '../resultater/verifiserFartMax50kmt.xlsx' )

tidsbruk = datetime.now() - t0 
print( f"Tidsbruk {tidsbruk} ")

#----------------------------------------------------------------------------
# 2024-fylker

myGdf = lastnedvegnett.fylker2024( myGdf )
telling = myGdf.groupby( ['fylke' ]).agg( { 'segmentlengde' : 'sum'} ).astype(int).reset_index()  
telling['segmentlengde'] = telling['segmentlengde'] / 1000  
telling.rename( columns={ 'segmentlengde' : 'Veg med fartsgrense 50 km/t eller lavere (km)' }, inplace=True)

skrivdataframe.skrivdf2xlsx( telling, '../resultater/fartMax50kmt.xlsx' )
