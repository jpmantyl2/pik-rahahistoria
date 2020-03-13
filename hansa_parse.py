# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 20:50:38 2019

@author: jpmantyl
"""

import re
import pandas as pd

fname = 'hansa_export.txt'


def read_tili(hansa_tili):
    hansa_split = re.split('\n',hansa_tili)
    tilinimi = hansa_split[0]
    
    df = pd.DataFrame([re.split('\t',x) for x in hansa_split[2:]])
    header = re.split('\t',hansa_split[1])
    header.extend(list(range(len(df.columns) - len(header))))
    df.columns = header
    df['tili'] = tilinimi
    return df


with open(fname, 'r') as hansafile:
    hansadata = hansafile.read()
    
    
hansa_list = re.split('\n\n(?=TILI)',hansadata)

hansa_tili = re.split('\n(?=Vaihto)',hansa_list[1])[0] # sisältää tilin headerin (esim. TILI 1109  OH-952)
df = read_tili(hansa_tili)
    
for hansa_tili_raw in hansa_list[2:]:
    hansa_tili = re.split('\n(?=Vaihto)',hansa_tili_raw)[0] # sisältää tilin headerin (esim. TILI 1109  OH-952)
    df_ = read_tili(hansa_tili)
    df = df.append(df_)

df = df[['Tos.','Tap.pvm','Teksti','Debet','Kredit','Saldo','tili']]
df.columns = df.columns.str.replace('.','')
df.columns = df.columns.str.lower()

df['debet'] = df.debet.str.replace(',','.')
df['kredit'] = df.kredit.str.replace(',','.')
df['saldo'] = df.saldo.str.replace(',','.')


df['tappvm'] = pd.to_datetime(df['tappvm'])
df['debet'] = pd.to_numeric(df['debet'])
df['kredit'] = pd.to_numeric(df['kredit'])
df['saldo'] = pd.to_numeric(df['saldo'])
