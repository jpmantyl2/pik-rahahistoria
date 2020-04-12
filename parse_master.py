# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 16:34:43 2020

@author: janne.mantyla
"""


from hansa_parse import hansa_parse
from kitupiikki_parse import kitupiikki_parse

df_hansa = hansa_parse()
df_kitupiikki = kitupiikki_parse()

df = df_hansa.append(df_kitupiikki)
