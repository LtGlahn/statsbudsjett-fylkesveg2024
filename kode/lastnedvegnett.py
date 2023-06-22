"""
Div kjekke funksjoner for nedlasting av data til KOSTRA-rapportering
"""
from copy import deepcopy
import pdb 

import pandas as pd
import geopandas as gpd 
from shapely import wkt 

import STARTHER 
import nvdbgeotricks  
import nvdbapiv3 
import skrivdataframe

def fylker2024( myDataFrame, fylker2024='nyFylkesinndeling.csv'):
    """
    Oversetter 2023-kommunenummer til fylkesnummer gyldige i 2024

    ARGUMENTS
        myDataFrame - Dataframe eller GeoDataFrame. Må ha kolonnene kommune og fylke

    KEYWORDS
        fylke2024 - string, filnavn for CSV-fil med kolonnene Kommune2023 og Fylkesnummer2024

    RETURNS
        modifisert myDataFrame, som har fått nye kolonner fylke2023, fylkesnavn2024 og Fylkesnummer2024  
        kolonnen fylke er nå med 2024-fylkesnumrene 
    """

    mydf = myDataFrame.copy() # for å unngå sideeffekter
    mydf['fylke2023'] = mydf['fylke']

    fylker = pd.read_csv( fylker2024, sep=';')

    nyDf = pd.merge( mydf, fylker, how='inner', left_on='kommune', right_on='Kommune2023' )
    assert len(nyDf) == len( mydf), 'Feil i kobling 2024-kommunenummer vs 2023-fylker'

    nyDf['fylke'] = nyDf['Fylkesnummer2024']
    nyDf.drop( columns=['Kommune2023', 'KommuneNavn'], inplace=True )

    return nyDf 


def vegnetthelelandet( mittfilter={} ):
    mittfilter = filtersjekk( mittfilter )

    
    myDf = pd.DataFrame( nvdbapiv3.nvdbVegnett( filter=mittfilter ).to_records() )
    myDf['geometry'] = myDf['geometri'].apply( wkt.loads )

    myGdf = gpd.GeoDataFrame( myDf, geometry='geometry', crs=5973 )
    return myGdf


def rapport01_gdf2excel( mygdf, filnavn='vegnettkostra.xlsx', sheet_prefiks='', metadata=None ): 
    """
    Lager excel-oppsummering av lengde vegnett per fylke, kommune og vegkategori
    """

    # Konverterer lengde til km
    mygdf = deepcopy( mygdf ) 
    mygdf['lengde'] = mygdf['lengde'] / 1000 

    # Finner kryssystem 
    mygdf['kryss'] = mygdf['vegsystemreferanse'].apply( lambda x : harViKryssSystem( x ) )
    kryss = mygdf[ mygdf['kryss']]

    # t1 = mygdf.groupby( [ 'fylke' ]).agg({ 'lengde' : 'sum' }).reset_index()
    t2  = mygdf.groupby( [ 'fylke', 'vegkategori' ]).agg({ 'lengde' : 'sum' }).reset_index()
    t2x = kryss.groupby( [ 'fylke', 'vegkategori' ]).agg({ 'lengde' : 'sum' }).reset_index()
    t3  = mygdf.groupby( [ 'fylke', 'kommune' ]).agg({ 'lengde' : 'sum' }).reset_index()
    t4  = mygdf.groupby( [ 'fylke', 'kommune', 'vegkategori' ]).agg({ 'lengde' : 'sum' }).reset_index()

    t2 = skrivdataframe.fylkesnr2fylkesnavn( t2 )
    t2_transponert = skrivdataframe.transponerFylkePerVegkategori( t2 )
    t2_transponert['Riksveg (E+R)'] = t2_transponert['E'] + t2_transponert['R']
    t2_transponert = t2_transponert[['fylke', 'Riksveg (E+R)', 'E', 'R', 'F', 'K', 'P', 'S' ]]

    t2x = skrivdataframe.fylkesnr2fylkesnavn( t2x )
    t2x_transponert = skrivdataframe.transponerFylkePerVegkategori( t2x )
    t2x_transponert['Riksveg (E+R)'] = t2x_transponert['E'] + t2x_transponert['R']
    t2x_transponert = t2x_transponert[['fylke', 'Riksveg (E+R)', 'E', 'R', 'F', 'K', 'P' ]]

    t4_transponert = skrivdataframe.transponerKommunePerVegkategori( t4 )

    # # Skal ha med formattering fra xlsxwriter, men ikke tilgjengelig akkurat nu... 
    # t2.to_excel( filnavn, sheet_name=sheet_prefiks + 'Fylke per vegkategori' )
    # t3.to_excel( filnavn, sheet_name=sheet_prefiks +'per kommune')
    # t4.to_excel( filnavn, sheet_name=' per kommune og vegkategori')

    navneliste = [  sheet_prefiks+'Tabell fylker',                  # t2_transponert
                    sheet_prefiks+'Lengde kryssystem',              # t2x_transponert
                    sheet_prefiks+'Tabell kommuner',                # t4_transponert
                    sheet_prefiks+'radvis per fylke og vegkat',     # t2
                    sheet_prefiks+'radvis per kommune',             # t3 
                    sheet_prefiks+'radvis per kommune og vegkat'  ] # t4 

    skrivdataframe.skrivdf2xlsx([t2_transponert, t2x_transponert, t4_transponert, t2, t3, t4], filnavn=filnavn, sheet_name=navneliste, metadata=metadata )

def rapport01_medsykkel_gdf2excel( mygdf, filnavn='vegnettkostra.xlsx', sheet_prefiks='', metadata=None ): 
    """
    Lager excel-oppsummering av lengde vegnett per fylke, kommune og vegkategori
    """

    # Konverterer lengde til km
    mygdf = deepcopy( mygdf ) 
    mygdf['lengde'] = mygdf['lengde'] / 1000 

    # Finner kryssystem 
    mygdf['kryss'] = mygdf['vegsystemreferanse'].apply( lambda x : harViKryssSystem( x ) )
    kryss = mygdf[ mygdf['kryss']]

    # t1 = mygdf.groupby( [ 'fylke' ]).agg({ 'lengde' : 'sum' }).reset_index()
    t2  = mygdf.groupby( [ 'fylke', 'vegkategori', 'trafikantgruppe'] ).agg({ 'lengde' : 'sum' }).reset_index()
    t2x = kryss.groupby( [ 'fylke', 'vegkategori'] ).agg({ 'lengde' : 'sum' }).reset_index()
    t3  = mygdf.groupby( [ 'fylke', 'kommune', 'trafikantgruppe' ]).agg({ 'lengde' : 'sum' }).reset_index()
    t4  = mygdf.groupby( [ 'fylke', 'kommune', 'vegkategori', 'trafikantgruppe' ]).agg({ 'lengde' : 'sum' }).reset_index()

    t2 = skrivdataframe.fylkesnr2fylkesnavn( t2 )
    t2_transponert = skrivdataframe.transponerFylkePerVegkategori( t2x )
    # t2_transponert['Riksveg (E+R)'] = t2_transponert['E'] + t2_transponert['R']
    # t2_transponert = t2_transponert[['fylke', 'Riksveg (E+R)', 'E', 'R', 'F', 'K', 'P', 'S' ]]

    t2x = skrivdataframe.fylkesnr2fylkesnavn( t2x )
    t2x_transponert = skrivdataframe.transponerFylkePerVegkategori( t2x )
    # t2x_transponert['Riksveg (E+R)'] = t2x_transponert['E'] + t2x_transponert['R']
    # t2x_transponert = t2x_transponert[['fylke', 'Riksveg (E+R)', 'E', 'R', 'F', 'K', 'P' ]]

    t4_transponert = skrivdataframe.transponerKommunePerVegkategori( t4 )

    # # Skal ha med formattering fra xlsxwriter, men ikke tilgjengelig akkurat nu... 
    # t2.to_excel( filnavn, sheet_name=sheet_prefiks + 'Fylke per vegkategori' )
    # t3.to_excel( filnavn, sheet_name=sheet_prefiks +'per kommune')
    # t4.to_excel( filnavn, sheet_name=' per kommune og vegkategori')

    navneliste = [  sheet_prefiks+'Tabell fylker',                  # t2_transponert
                    sheet_prefiks+'Lengde kryssystem',              # t2x_transponert
                    sheet_prefiks+'Tabell kommuner',                # t4_transponert
                    sheet_prefiks+'radvis per fylke og vegkat',     # t2
                    sheet_prefiks+'radvis per kommune',             # t3 
                    sheet_prefiks+'radvis per kommune og vegkat'  ] # t4 

    skrivdataframe.skrivdf2xlsx([t2_transponert, t2x_transponert, t4_transponert, t2, t3, t4], filnavn=filnavn, sheet_name=navneliste, metadata=metadata )




def harViKryssSystem( vegsystemreferanse ): 

    svar = False 
    if 'kryssystem' in vegsystemreferanse: 
        svar = True 

    return svar 


def kostraFagdataFilter( mittfilter={}  ): 
    """
    Returnerer mal for filter for NVDB fagdata til KOSTRA-rapport 
    """

    if not 'vegsystemreferanse' in mittfilter: 
        mittfilter['vegsystemreferanse']       = 'Fv'

    if not 'tidspunkt' in mittfilter: 
        mittfilter['tidspunkt']       = '2021-12-15'

    return mittfilter

def filtersjekk( mittfilter={} ):
    """
    Beriker et filter med vegnett-spesifikke standardverdier for kostra-søk 
    """

    # if not 'kryssystem' in mittfilter.keys():
    #     mittfilter['kryssystem'] = 'false' 

    if not 'sideanlegg' in mittfilter.keys():
        mittfilter['sideanlegg'] = 'false' 


    # Kun kjørende, og kun øverste topologinivå, og ikke adskiltelop=MOT, og ikke konnekteringslenker 
    mittfilter['trafikantgruppe'] = 'K'
    mittfilter['detaljniva']      = 'VT,VTKB'
    mittfilter['adskiltelop']     = 'med,nei' 
    mittfilter['typeveg']         = 'kanalisertVeg,enkelBilveg,rampe,rundkjøring,gatetun' 
    # mittfilter['historisk']       = 'true'
    # mittfilter['tidspunkt']       = '2021-12-16'
    mittfilter['veglenketype']       = 'hoved'

    return mittfilter



