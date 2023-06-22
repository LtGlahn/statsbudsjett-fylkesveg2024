import pandas as pd
import numpy as np

import STARTHER
import nvdbapiv3
import skrivdataframe
import nvdbgeotricks
import lastnedvegnett

def finnlengder( row ):
    if np.isnan( row['Lengde, offisiell'] ):
        return row['Sum lengde alle løp']
    else:
        return row['Lengde, offisiell']

sok = nvdbapiv3.nvdbFagdata( 581 )
sok.filter( {'vegsystemreferanse' : 'Fv' } )
tun = nvdbgeotricks.nvdbsok2GDF( sok )
tun.to_file( '../resultater/vegnettFV.gpkg', layer='tunnel', driver='GPKG')

# Mangler offisiell lengde, men det viser seg at de har verdi for "sum samlet lengde"
# tun[ tun['Lengde, offisiell'].isnull()][['Navn', 'Lengde, offisiell', 'Sum lengde alle løp', 'Antall parallelle hovedløp']]

tun['Lengde'] = tun.apply( finnlengder, axis=1)

undersjoisk = tun[ tun['Undersjøisk'] == 'Ja'].groupby( 'fylke' ).agg( { 'Lengde' : 'sum' } ).reset_index()
landtunnel = tun[ tun['Undersjøisk'] != 'Ja'].groupby( 'fylke' ).agg( { 'Lengde' : 'sum' } ).reset_index()

undersjoisk.rename( columns={ 'Lengde' : 'Lengde undersjøiske tunnelløp (m)' }, inplace=True )
landtunnel.rename( columns={ 'Lengde' : 'Lengde ikke-undersjøiske tunnelløp (m)' }, inplace=True )
tunnelltall = pd.merge( landtunnel, undersjoisk, on='fylke', how='left' )
skrivdataframe.skrivdf2xlsx( tunnelltall, '../resultater/verifiserTunnel.xlsx' )

#-------------------------
# 2024- fylker
tun = lastnedvegnett.fylker2024( tun )

undersjoisk = tun[ tun['Undersjøisk'] == 'Ja'].groupby( 'fylke' ).agg( { 'Lengde' : 'sum' } ).reset_index()
landtunnel = tun[ tun['Undersjøisk'] != 'Ja'].groupby( 'fylke' ).agg( { 'Lengde' : 'sum' } ).reset_index()

undersjoisk.rename( columns={ 'Lengde' : 'Lengde undersjøiske tunnelløp (m)' }, inplace=True )
landtunnel.rename( columns={ 'Lengde' : 'Lengde ikke-undersjøiske tunnelløp (m)' }, inplace=True )
tunnelltall = pd.merge( landtunnel, undersjoisk, on='fylke', how='left' )
skrivdataframe.skrivdf2xlsx( tunnelltall, '../resultater/tunneler.xlsx' )

