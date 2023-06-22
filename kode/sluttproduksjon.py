"""
Leser en haug med regneark og setter sammen til endelig leveranse
"""

from copy import deepcopy
import pdb 

import pandas as pd

import STARTHER 
import nvdbgeotricks  
import skrivdataframe
import lastnedvegnett


if __name__ == '__main__': 

    nyeFylker = pd.read_csv( 'nyFylkesinndeling.csv', sep=';')
    nyeFylker.rename( columns={'Fylkesnummer2024' : 'fylke', 'Fylke2024' : 'Fylkesnavn'}, inplace=True )
    nyeFylker = nyeFylker[ nyeFylker['Fylkesnavn'] != 'Oslo'].drop_duplicates( subset=['fylke', 'Fylkesnavn'] )[['fylke', 'Fylkesnavn']]
 
    brutusdata = pd.read_excel( '../resultater/bruer_ferjekaier.xlsx')
    vegnett    = pd.read_excel( '../resultater/veglengerFVJuni2023.xlsx')
    trafikk    = pd.read_excel( '../resultater/ÅDTanalyse.xlsx')
    rekkverk   = pd.read_excel( '../resultater/rekkverk.xlsx')
    lys        = pd.read_excel( '../resultater/belysningspunkt.xlsx')
    tunnel     = pd.read_excel( '../resultater/tunneler.xlsx')
    sykkel     = pd.read_excel( '../resultater/sykkelveg.xlsx')
    fart50     = pd.read_excel( '../resultater/fartMax50kmt.xlsx')
    ferjekai   = pd.read_excel( '../resultater/ferjekai.xlsx')

    # Fjerner ferjekai fra Brutusdata, vi bruker NVDB uttrekk i stedet
    brutusdata.drop( columns='Ferjekaibruer og tilleggskaier (antall)', inplace=True )


    myDfList = [nyeFylker, vegnett, brutusdata, trafikk, rekkverk, lys, tunnel, sykkel, fart50, ferjekai ]
    myDfList = [ df.set_index( 'fylke') for df in myDfList ]
    FERDIG = pd.concat( myDfList, axis=1 ).reset_index()

    FERDIG.fillna(0, inplace=True)
    FERDIG['Ferjekaibruer og tilleggskaier (antall)']           = FERDIG['Ferjekaibruer og tilleggskaier (antall)'].astype(int)
    FERDIG['Lengde bruer av stål (m)']                          = FERDIG['Lengde bruer av stål (m)'].astype(int)
    FERDIG['Lengde bruer av andre materialtyper enn stål (m)']  = FERDIG['Lengde bruer av andre materialtyper enn stål (m)'].astype(int)
    FERDIG['Lyspunkt i dagen (antall)']  = FERDIG['Lyspunkt i dagen (antall)'].astype(int)

    FERDIG.rename( columns={'fylke' : 'Fylkesnr 2024'}, inplace=True )

    columns = ['Fylkesnr 2024', 
                'Fylkesnavn', 
                'Lengde vegnett (km)', 
                 'Lengde veg som har ÅDT-data (km)',
                'Feltlengde (km)',
                'Trafikkarbeid (mill kjøretøykm)',
                'Lengde Ådt > 4000 (km)',
                 'Lengde Ådt > 1500 (km)', 
                 'Rekkverk (lm)', 
                 'Lyspunkt i dagen (antall)',
                 'Lengde ikke-undersjøiske tunnelløp (m)',
                'Lengde undersjøiske tunnelløp (m)',       
                'Lengde bruer av stål (m)',
                'Lengde bruer av andre materialtyper enn stål (m)',
                'Ferjekaibruer og tilleggskaier (antall)' ,
                  'G/S-veglengde (km)',
               'Veg med fartsgrense 50 km/t eller lavere (km)'          
                ]
    

    nvdbgeotricks.skrivexcel( '../resultater/Grunnlagsdata-inntekt-Fylkeskommunene2024.xlsx', FERDIG[columns])

