from datetime import datetime 

import geopandas as gpd 

import STARTHER
import lastnedvegnett  
import skrivdataframe
import nvdbgeotricks
import nvdbapiv3

t0 = datetime.now()

mittfilter = {  # 'tidspunkt'              : '2021-12-16', 
                'trafikantgruppe'       : 'G', 
                'detaljniva'            : 'VT,VTKB',
                'adskiltelop'           : 'med,nei',
                'vegsystemreferanse'    : 'Fv',
                'veglenketype'          : 'hoved', 
                'typeveg'               : 'kanalisertVeg,enkelBilveg,rampe,rundkjøring,gangOgSykkelveg,sykkelveg,gangveg,gatetun'
                }

sok = nvdbapiv3.nvdbVegnett( )
sok.filter( mittfilter )
myGdf = nvdbgeotricks.nvdbsok2GDF( sok )
myGdf.to_file( '../resultater/vegnettFV.gpkg', layer='gangsykkelveg', driver='GPKG')

statistikk = myGdf.groupby( ['fylke'] ).agg( { 'lengde' : 'sum' } ).reset_index()
statistikk['lengde'] = statistikk['lengde'] / 1000
statistikk.rename( columns={ 'lengde' : 'G/S-veglengde (km)'}, inplace=True )
skrivdataframe.skrivdf2xlsx( statistikk, '../resultater/verifiserSykkelveg.xlsx' )

# 2024-fylker
myGdf = lastnedvegnett.fylker2024( myGdf )
statistikk = myGdf.groupby( ['fylke'] ).agg( { 'lengde' : 'sum' } ).reset_index()
statistikk['lengde'] = statistikk['lengde'] / 1000
statistikk.rename( columns={ 'lengde' : 'G/S-veglengde (km)'}, inplace=True )
skrivdataframe.skrivdf2xlsx( statistikk, '../resultater/sykkelveg.xlsx' )

