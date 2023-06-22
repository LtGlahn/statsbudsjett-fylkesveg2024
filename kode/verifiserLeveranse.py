"""
Verifiserer dataproduksjon med 2023-fylkesnummer mot fjorårets leveranse
"""

from copy import deepcopy
import pdb 

import pandas as pd

import STARTHER 
import nvdbgeotricks  
import skrivdataframe
import lastnedvegnett


if __name__ == '__main__': 

    ifjor = pd.read_excel( '../resultater/Grunnlagsdata-inntekt-fylkeskommunene2023.xlsx', header=3 )
    ifjor = ifjor[ ~ifjor['Fylkesnr.'].isnull()].copy()
    columns = [ 'Fylkesnr.', 'Fylkesnavn', 'Lengde vegnett (km)',
                'Lengde vegnett som har ÅDT-data (km)', 'Feltlengde \n(km)',
                'Trafikkarbeid \n(mill. kjtkm/døgn)',
                'Veglengde med \nÅDT > 1500 \n(km)', 'Rekkverk\n(lm)',
                'Lyspunkt i dagen (antall)',
                'Lengde \nikke-undersjøiske tunnelløp \n(m)',
                'Lengde undersjøiske  tunnelløp \n(m)', 'Lengde bruer av stål \n(m)',
                'Lengde bruer av andre material-typer enn stål \n(m)',
                'Ferjekaibruer og tilleggskaier\n(antall)', 'G/S-veglengde \n(km)',
                'Veg med fartsgrense 50 km/t eller lavere \n(km)']
    
    # Får heltall på ting
    ifjor['Lyspunkt i dagen (antall)'] = ifjor['Lyspunkt i dagen (antall)'].astype(int)
    ifjor['Ferjekaibruer og tilleggskaier\n(antall)'] = ifjor['Ferjekaibruer og tilleggskaier\n(antall)'].astype(int)    

    ifjor = ifjor.add_prefix( '2023: ' )
 
    ifjor['fylke'] = ifjor['2023: Fylkesnr.'].astype( int )
    ifjor.drop( columns=['2023: Fylkesnr.'], inplace=True  )
 
    brutusdata = pd.read_excel( '../resultater/verifiserBrutusdata.xlsx')
    vegnett    = pd.read_excel( '../resultater/verifiserVeglengder.xlsx')
    aadt       = pd.read_excel( '../resultater/verifiserÅDTanalyse.xlsx')
    rekkverk   = pd.read_excel( '../resultater/verifiserRekkverk.xlsx')
    lys        = pd.read_excel( '../resultater/verifiserBelysningspunkt.xlsx')
    tunnel     = pd.read_excel( '../resultater/verifiserTunnel.xlsx')
    sykkel     = pd.read_excel( '../resultater/verifiserSykkelveg.xlsx')
    fart50     = pd.read_excel( '../resultater/verifiserFartMax50kmt.xlsx')

    
    myDfList = [vegnett, aadt, ifjor, brutusdata, rekkverk, lys, tunnel, sykkel, fart50 ]
    myDfList = [ df.set_index( 'fylke') for df in myDfList ]
    verifiser = pd.concat( myDfList, axis=1 ).reset_index()

    columns = ['fylke', '2023: Fylkesnavn', 
        '2023: Lengde vegnett (km)',
        'Lengde vegnett (km)',
       '2023: Lengde vegnett som har ÅDT-data (km)', 
       'Lengde veg som har ÅDT-data (km)',
        '2023: Feltlengde \n(km)',
        'Feltlengde (km)',
       '2023: Trafikkarbeid \n(mill. kjtkm/døgn)',
        'Trafikkarbeid (mill kjøretøykm)',
       '2023: Veglengde med \nÅDT > 1500 \n(km)',
       'Lengde Ådt > 1500 (km)', 
       '2023: Rekkverk\n(lm)',
       'Rekkverk (lm)',
       '2023: Lyspunkt i dagen (antall)',
       'Lyspunkt i dagen (antall)',
       '2023: Lengde \nikke-undersjøiske tunnelløp \n(m)',
       'Lengde ikke-undersjøiske tunnelløp (m)',
       '2023: Lengde undersjøiske  tunnelløp \n(m)',
       'Lengde undersjøiske tunnelløp (m)',
       '2023: Lengde bruer av stål \n(m)',
    #    'Lengde stålbru V0',
        'Lengde bruer av stål (m)',       
        '2023: Lengde bruer av andre material-typer enn stål \n(m)',
        # 'Lengde bru ikke stål V0',       
       'Lengde bruer av andre materialtyper enn stål (m)',
        '2023: Ferjekaibruer og tilleggskaier\n(antall)',
    #    'Ferjekaibrutillegg V0',
       'Ferjekaibruer og tilleggskaier (antall)',
    #    'Ferjekaibruer og tilleggskaier (antall) V2'
       '2023: G/S-veglengde \n(km)',
       'G/S-veglengde (km)',
       '2023: Veg med fartsgrense 50 km/t eller lavere \n(km)',
        'Veg med fartsgrense 50 km/t eller lavere (km)'          
      ]
    
    # skrivdataframe.skrivdf2xlsx( verifiser[columns], '../resultater/verifiserMotIfjor.xlsx')
    nvdbgeotricks.skrivexcel( '../resultater/verifiserMotIfjor.xlsx', verifiser[columns] )
