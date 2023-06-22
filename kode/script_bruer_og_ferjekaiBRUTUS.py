"""
Leser regneark med BRUTUS-data, gir dem nye fylkesnummer og aggregerer ihht oppskrift
"""

from copy import deepcopy
import pdb 

import pandas as pd

import STARTHER 
import nvdbgeotricks  
import skrivdataframe
import lastnedvegnett

if __name__ == '__main__': 

    bruer = pd.read_excel( '../resultater/160623 grunnlagsdata bruer.xlsx' , sheet_name='Export Worksheet') # Kommer ny fil
    # bruer = pd.read_excel( '../junk/150623 grunnlagsdata bruer.xlsx')
    ferjekai = pd.read_excel( '../resultater/140623 grunnlagsdata ferjekaier.xlsx',         sheet_name='Export Worksheet')
    # ferjekai_v2 = pd.read_excel( '../resultater/150623 grunnlagsdata ferjekaier v2.xlsx',   sheet_name='Export Worksheet')

    ferjekai.drop(         columns=['KOMMUNE', 'FYLKE'], inplace=True )
    # ferjekai_v2.drop(      columns=['KOMMUNE', 'FYLKE'], inplace=True )
    bruer.drop(            columns=['KOMMUNE', 'FYLKE'], inplace=True )
    ferjekai.rename(       columns={'KOMMUNENR' : 'kommune' }, inplace=True)
    # ferjekai_v2.rename(    columns={'KOMMUNENR' : 'kommune' }, inplace=True)
    bruer.rename(          columns={'KOMMUNENR' : 'kommune'}, inplace=True)
    bruer['fylke']       = bruer['kommune'].apply(       lambda x : int( str(x)[:-2] ) )
    ferjekai['fylke']    = ferjekai['kommune'].apply(    lambda x : int( str(x)[:-2] ) )
    # ferjekai_v2['fylke'] = ferjekai_v2['kommune'].apply( lambda x : int( str(x)[:-2] ) )

    # bruer = lastnedvegnett.fylker2024(      bruer )
    # ferjekai = lastnedvegnett.fylker2024(   ferjekai )

    staalbru    = bruer[ bruer['MATERIALE'] == 'Stål']
    ikke_staal  = bruer[ bruer['MATERIALE'] != 'Stål']

#----------------------------------------------------------------------
    # For sammenligning med 2023-data

    # Ekstra sjekk - de tallene Sølvi ga 14.6.2023, med den samme (?) filtreringen som i fjor?
    # bruer_v0 = pd.read_excel(    '../junk/140623 grunnlagsdata bruer.xlsx')
    # ferjekai_v0 = pd.read_excel( '../junk/140623 grunnlagsdata ferjekaier.xlsx',         sheet_name='Export Worksheet')
    # bruer_v0[   'fylke']    = bruer_v0[   'KOMMUNENR'].apply(    lambda x : int( str(x)[:-2] ) )
    # ferjekai_v0['fylke']    = ferjekai_v0['KOMMUNENR'].apply(    lambda x : int( str(x)[:-2] ) )
        
    # staalbru_v0    = bruer_v0[ bruer_v0['MATERIALE'] == 'Stål']
    # ikke_staal_v0  = bruer_v0[ bruer_v0['MATERIALE'] != 'Stål']

    # Aggregering bruer, to versjoner 
    # lengde_staal_v0     = staalbru_v0.groupby(   'fylke').agg( {'LENGDE' : 'sum'}).reset_index()
    lengde_staal        = staalbru.groupby(      'fylke').agg( {'LENGDE' : 'sum'}).reset_index()
    # lengde_ikkestaal_v0 = ikke_staal_v0.groupby( 'fylke').agg( {'LENGDE' : 'sum'}).reset_index()
    lengde_ikkestaal    = ikke_staal.groupby(    'fylke').agg( {'LENGDE' : 'sum'}).reset_index()

    # Aggregering ferjekai, tre versjoner 
    # antall_ferjekai_v0 = ferjekai_v0.groupby( 'fylke').agg( { 'BYGGVERKSNUMMER' : 'count' } ).reset_index()
    antall_ferjekai    = ferjekai.groupby(    'fylke').agg( { 'BYGGVERKSNUMMER' : 'count' } ).reset_index()
    # antall_ferjekai_v2 = ferjekai_v2.groupby( 'fylke').agg( { 'BYGGVERKSNUMMER' : 'count' } ).reset_index()

    # Døper om på ting
    # lengde_ikkestaal_v0.rename( columns={'LENGDE' : 'Lengde bru ikke stål V0'}, inplace=True )
    lengde_ikkestaal.rename(    columns={'LENGDE' : 'Lengde bruer av andre materialtyper enn stål (m)'}, inplace=True )
    # lengde_staal_v0.rename(     columns={'LENGDE' : 'Lengde stålbru V0'}, inplace=True )
    lengde_staal.rename(        columns={'LENGDE' : 'Lengde bruer av stål (m)'}, inplace=True )

    # antall_ferjekai_v0.rename( columns={'BYGGVERKSNUMMER' : 'Ferjekaibrutillegg V0'},    inplace=True )
    antall_ferjekai.rename(    columns={'BYGGVERKSNUMMER' : 'Ferjekaibruer og tilleggskaier (antall)'},    inplace=True )
    # antall_ferjekai_v2.rename( columns={'BYGGVERKSNUMMER' : 'Ferjekaibruer og tilleggskaier (antall) V2'}, inplace=True )



    # myDfList = [ lengde_staal_v0, lengde_staal,  lengde_ikkestaal_v0, lengde_ikkestaal, antall_ferjekai_v0, antall_ferjekai, antall_ferjekai_v2 ]
    # myDfList = [ lengde_staal_v0, lengde_staal,  lengde_ikkestaal_v0, lengde_ikkestaal, antall_ferjekai ]
    myDfList = [ lengde_staal, lengde_ikkestaal, antall_ferjekai ]
    myDfList = [ df.set_index( 'fylke') for df in myDfList ]
    brutusdata = pd.concat( myDfList, axis=1).reset_index()
    skrivdataframe.skrivdf2xlsx( brutusdata, '../resultater/verifiserBrutusdata.xlsx')


#--------------------------------------------------------------------------
    # Gjentar for 2024 - kommuner 
    staalbru   = lastnedvegnett.fylker2024( staalbru ) 
    ikke_staal  = lastnedvegnett.fylker2024( ikke_staal ) 
    ferjekai   = lastnedvegnett.fylker2024( ferjekai ) 

    lengde_staal     = staalbru.groupby(   'fylke').agg( {'LENGDE' : 'sum'}).reset_index()
    lengde_ikkestaal = ikke_staal.groupby( 'fylke').agg( {'LENGDE' : 'sum'}).reset_index()

    lengde_ikkestaal.rename( columns={'LENGDE' : 'Lengde bruer av andre materialtyper enn stål (m)'}, inplace=True )
    lengde_staal.rename( columns={'LENGDE' : 'Lengde bruer av stål (m)'}, inplace=True )

    antall_ferjekai = ferjekai.groupby(      'fylke').agg( { 'BYGGVERKSNUMMER' : 'count' } ).reset_index()
    antall_ferjekai.rename(    columns={'BYGGVERKSNUMMER' : 'Ferjekaibruer og tilleggskaier (antall)'},    inplace=True )

    myDfList = [ lengde_staal, lengde_ikkestaal, antall_ferjekai ]
    myDfList = [ df.set_index( 'fylke') for df in myDfList ]
    brutusdata = pd.concat( myDfList, axis=1).reset_index()
    skrivdataframe.skrivdf2xlsx( brutusdata, '../resultater/bruer_ferjekaier.xlsx')


