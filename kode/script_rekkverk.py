import skrivdataframe
import STARTHER
import pandas as pd
import nvdbapiv3
import lastnedvegnett
import nvdbgeotricks 


sok = nvdbapiv3.nvdbFagdata( 5 )
sok.filter( {'vegsystemreferanse' : 'Fv' } )
rekk = nvdbgeotricks.nvdbsok2GDF( sok ) 
rekk.to_file( '../resultater/vegnettFV.gpkg', layer='rekkverk', driver='GPKG')

med_lengde = rekk[ ~rekk['Lengde'].isnull()].copy()
uten_lengde = rekk[ rekk['Lengde'].isnull()].copy()
med_lengde.drop_duplicates( subset='nvdbId', inplace=True )
agg_med_lengde = med_lengde.groupby( 'fylke').agg( {'Lengde' : 'sum' } ).reset_index()
agg_uten_Lengde = uten_lengde.groupby( 'fylke').agg( {'segmentlengde' : 'sum'} ).reset_index()
joined = pd.merge( agg_med_lengde, agg_uten_Lengde, on='fylke', how='inner')
joined['Rekkverk (lm)'] = (joined['Lengde'] + joined['segmentlengde']  )

skrivdataframe.skrivdf2xlsx( joined, '../resultater/verifiserRekkverk.xlsx' )

#-----------------------------------------------------------------------------------------
# 2024-fylker
rekk = lastnedvegnett.fylker2024( rekk )
med_lengde = rekk[ ~rekk['Lengde'].isnull()].copy()
uten_lengde = rekk[ rekk['Lengde'].isnull()].copy()
med_lengde.drop_duplicates( subset='nvdbId', inplace=True )
agg_med_lengde = med_lengde.groupby( 'fylke').agg( {'Lengde' : 'sum' } ).reset_index()
agg_uten_Lengde = uten_lengde.groupby( 'fylke').agg( {'segmentlengde' : 'sum'} ).reset_index()
joined = pd.merge( agg_med_lengde, agg_uten_Lengde, on='fylke', how='inner')
joined['Rekkverk (lm)'] = (joined['Lengde'] + joined['segmentlengde']  )

skrivdataframe.skrivdf2xlsx( joined, '../resultater/rekkverk.xlsx' )
