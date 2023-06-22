#%%
from datetime import datetime 

import geopandas as gpd 

import STARTHER
import lastnedvegnett  
import skrivdataframe
import nvdbgeotricks 

def tellfelt( feltoversikt ):
    felt = feltoversikt.split(',')
    count = 0
    for etfelt in felt:
        if 'O' in etfelt or 'H' in etfelt or 'V' in etfelt or 'S' in etfelt:
            pass
        else:
            count += 1
    return count


if __name__ == '__main__': 
    t0 = datetime.now()

    mittfilter = lastnedvegnett.filtersjekk(  )
    mittfilter['vegsystemreferanse'] = 'Fv'

    # myGdf = lastnedvegnett.vegnetthelelandet( mittfilter=mittfilter )
    # myGdf.to_file( '../resultater/vegnettFV.gpkg', layer='norge', driver='GPKG')
    myGdf  = gpd.read_file( '../resultater/vegnettFV.gpkg', layer='norge')

    # Kjørefelt og feltlengde
    myGdf['antallFelt'] = myGdf['feltoversikt'].apply( tellfelt )
    myGdf['feltlengde'] = myGdf['lengde'] * myGdf['antallFelt']

    # Lagrer 2023-fylkesnummer for verifisering mot fjorårets leveranse
    minAgg = myGdf.groupby( ['fylke'] ).agg( {'lengde' : 'sum', 'feltlengde' : 'sum' } ).reset_index()

    minAgg['Lengde vegnett (km)'] = minAgg['lengde'] / 1000
    minAgg['Lengde vegnett (km)'] = minAgg['Lengde vegnett (km)'].astype(int)
    minAgg['Feltlengde (km)']     = minAgg['feltlengde'] / 1000
    minAgg['Feltlengde (km)']     = minAgg['Feltlengde (km)'].astype(int)
    minAgg.drop( columns=['lengde', 'feltlengde'], inplace=True )

    skrivdataframe.skrivdf2xlsx( minAgg, '../resultater/verifiserVeglengder.xlsx')

    # Repeter analysen, men nå med 2024-fylkesnummer
    myGdf = lastnedvegnett.fylker2024( myGdf )
    minAgg = myGdf.groupby( ['fylke'] ).agg( {'lengde' : 'sum', 'feltlengde' : 'sum' } ).reset_index()
    minAgg['Lengde vegnett (km)'] = minAgg['lengde'] / 1000
    minAgg['Lengde vegnett (km)'] = minAgg['Lengde vegnett (km)'].astype(int)
    minAgg['Feltlengde (km)']     = minAgg['feltlengde'] / 1000
    minAgg['Feltlengde (km)']     = minAgg['Feltlengde (km)'].astype(int)
    minAgg.drop( columns=['lengde', 'feltlengde'], inplace=True )

    skrivdataframe.skrivdf2xlsx( minAgg, '../resultater/veglengerFVJuni2023.xlsx')

