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

# OBS! Ved datauttak juni 2023 filtrerte vi ikke for 
# Eier = Fylkeskommune, Stat, Statens vegvesen og (tom)
# Ref vianova-rapport s 32. Dette må rettes opp. 
# Blir noe slikt som 
# rekk['Eier'].fillna( '(tom)', inplace=True )
# rekk = rekk[ (rekk[rekk['Eier'] == 'Fylkeskommune'] ) | 
#              (rekk[rekk['Eier'] == 'Stat, Statens vegvesen'] ) | 
#              (rekk[rekk['Eier'] == '(tom)'] )]

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
