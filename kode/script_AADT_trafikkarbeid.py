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

# sok = nvdbapiv3.nvdbFagdata( 540)
# sok.filter( { 'vegsystemreferanse' : 'Fv'} )
# myGdf = nvdbgeotricks.nvdbsok2GDF( sok ) 
# myGdf = myGdf[ myGdf['adskilte_lop'] != 'Mot']
# myGdf = myGdf[ myGdf['trafikantgruppe'] == 'K']
# myGdf = myGdf[ myGdf['typeVeg'] != 'Gang- og sykkelveg']

# myGdf.to_file( '../resultater/vegnettFV.gpkg', layer='AADT', driver='GPKG')
myGdf = gpd.read_file( '../resultater/vegnettFV.gpkg', layer='AADT')


# telling = myGdf.groupby( ['fylke' ]).agg( { 'segmentlengde' : 'sum'} ).reset_index()  
# skrivdataframe.skrivdf2xlsx( telling, '../kostraleveranse2021/Kostra 12 - Fylkesveg ÅDT over 5000.xlsx', sheet_name='Fv over 5000ÅDT', metadata=filter2)

print( "Tidsbruk:", datetime.now() - t0 )

over1500adt = myGdf[ myGdf['ÅDT, total'] > 1500 ].groupby( 'fylke' ).agg( {  'segmentlengde'  : 'sum' } ).reset_index()
over1500adt.rename( columns={'segmentlengde' : 'Lengde Ådt > 1500 (km)'} , inplace=True)
over1500adt['Lengde Ådt > 1500 (km)'] = over1500adt['Lengde Ådt > 1500 (km)'] / 1000

myGdf['kjoretoyKm'] = myGdf['segmentlengde'] * myGdf['ÅDT, total'] * 365 / 1000
trafikkArb = myGdf.groupby([ 'fylke'] ).agg( {'segmentlengde' : 'sum', 'kjoretoyKm' : 'sum' } ).reset_index()
trafikkArb['Trafikkarbeid (mill kjøretøykm)'] = trafikkArb['kjoretoyKm'] / 1e6
trafikkArb['Lengde veg som har ÅDT-data (km)'] = trafikkArb['segmentlengde'] / 1000
trafikkArb.drop( columns=['segmentlengde', 'kjoretoyKm'], inplace=True )

data = pd.merge( trafikkArb, over1500adt, on='fylke' )
skrivdataframe.skrivdf2xlsx( data, '../resultater/verifiserÅDTanalyse.xlsx' )

#-------------------------------------------------------------------
# Gjentar med 2024 - fylker 

myGdf = lastnedvegnett.fylker2024( myGdf )

over1500adt = myGdf[ myGdf['ÅDT, total'] > 1500 ].groupby( 'fylke' ).agg( {  'segmentlengde'  : 'sum' } ).reset_index()
over1500adt.rename( columns={'segmentlengde' : 'Lengde Ådt > 1500 (km)'} , inplace=True)
over1500adt['Lengde Ådt > 1500 (km)'] = over1500adt['Lengde Ådt > 1500 (km)'] / 1000

# Skal også ha ÅDT > 4000 
over4000adt = myGdf[ myGdf['ÅDT, total'] > 4000 ].groupby( 'fylke' ).agg( {  'segmentlengde'  : 'sum' } ).reset_index()
over4000adt.rename( columns={'segmentlengde' : 'Lengde Ådt > 4000 (km)'} , inplace=True)
over4000adt['Lengde Ådt > 4000 (km)'] = over4000adt['Lengde Ådt > 4000 (km)'] / 1000



myGdf['kjoretoyKm'] = myGdf['segmentlengde'] * myGdf['ÅDT, total'] * 365 / 1000
trafikkArb = myGdf.groupby([ 'fylke'] ).agg( {'segmentlengde' : 'sum', 'kjoretoyKm' : 'sum' } ).reset_index()
trafikkArb['Trafikkarbeid (mill kjøretøykm)'] = trafikkArb['kjoretoyKm'] / 1e6
trafikkArb['Lengde veg som har ÅDT-data (km)'] = trafikkArb['segmentlengde'] / 1000
trafikkArb.drop( columns=['segmentlengde', 'kjoretoyKm'], inplace=True )

data = pd.merge( trafikkArb, over1500adt, on='fylke' )
data = pd.merge( data, over4000adt, on='fylke' )

skrivdataframe.skrivdf2xlsx( data, '../resultater/ÅDTanalyse.xlsx' )
