# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 14:50:38 2020

@author: jpmantyl
"""

def kitupiikki_parse():
    
    import re
    import pandas as pd
    
    fname = 'paakirja_2016_2018_output_testi_tab_separated.csv'
    
    def read_tili(tili):
        tili_split = re.split('\t',tili)
        tilinimi = tili_split[0]
        
        df = pd.DataFrame([re.split('\t',x) for x in re.split('\n',tili)[1:]])
        #header = re.split('\t',tili_split[1])
        #header.extend(list(range(len(df.columns) - len(header))))
        #df.columns = header
        df['tili'] = tilinimi
        return df
    
    
    with open(fname, 'r',encoding='utf-8') as kitupiikkifile:
        kitupiikkidata = kitupiikkifile.read()
        
    
    kitupiikki_list = re.split('\n(?=\")',kitupiikkidata)
    
    kitupiikki_tili = re.split('\n(?=\")',kitupiikki_list[1])[0] # sisältää tilin headerin (esim. TILI 1109  OH-952)
    df = read_tili(kitupiikki_tili)
        
    for tili_raw in kitupiikki_list[2:]:
        tili = re.split('\n(?=Vaihto)',tili_raw)[0] # sisältää tilin headerin (esim. TILI 1109  OH-952)
        df_ = read_tili(tili)
        df = df.append(df_)
    
    
    #df = df[['Tos.','Tap.pvm','Teksti','Debet','Kredit','Saldo','tili']]
    cols = re.split('\t',kitupiikki_list[0])
    cols.append('tili')
    df.columns = cols
    df.columns = df.columns.str.replace('.','')
    df.columns = df.columns.str.replace(' ','')
    df.columns = df.columns.str.replace('"','')
    df.columns = df.columns.str.replace('€','')
    df.columns = df.columns.str.lower()
    
    df['debet'] = df.debet.str.replace(',','.')
    df['kredit'] = df.kredit.str.replace(',','.')
    df['saldo'] = df.saldo.str.replace(',','.')
    
    df['debet'] = df.debet.str.replace('"','')
    df['kredit'] = df.kredit.str.replace('"','')
    df['saldo'] = df.saldo.str.replace('"','')
    df['selite'] = df.selite.str.replace('"','')
    df['tili'] = df.tili.str.replace('"','')
    
    
    df['pvm'] = pd.to_datetime(df['pvm'])
    df['debet'] = pd.to_numeric(df['debet'])
    df['kredit'] = pd.to_numeric(df['kredit'])
    df['saldo'] = pd.to_numeric(df['saldo'])
    
    df['tosite'] = df.selite.str.split(' : ',expand=True)[[0]] #Poimitaan selite-sarakkeen mahdollinen alussa oleva numero tositteeseen
    
    df = df[['tosite','pvm','selite','debet','kredit','saldo','tili']]
    df.columns = ['tos','tappvm','teksti','debet','kredit','saldo','tili']
    
    return df


