# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 18:37:29 2020

@author: User
"""

import pandas as pd
from  bs4 import  BeautifulSoup
import os
from pathlib import Path, PureWindowsPath
import re
import webbrowser
import json

#%% -
## The files is scrapped with request.py, from the frame-website of a query, subtracting the last parameter ('p' as page) from 1 to length variable:
## E.g.(p=400): https://ouny.magyarugyvedikamara.hu/licoms/common/service/requestparser?name=pubsearcher&action=search&type=ugyved&status=aktiv&p=400

path = PureWindowsPath(r'C:\Users\User\Documents\ugyvedek_html_pages') # path to folder of pages
length = 460 # number of pages
talalatok = 11493 # number of result = lawyers = rows
lawyers = {} # containers
ugyved ={}

def i(): # iterator, but not an regular iterator protocol
    for j,i in enumerate(range(1, length + 1)):
        p = 'p' + str(i)
        pi = path / p # appending the pathname 
        with open(pi, 'r') as page:
                yield BeautifulSoup(page, 'html.parser') # -> soup
        print(j, pi)
#%%
firstpage =  next(i()) #example

#%%
ugyved = {}  # temporary container for the first part(primer) of the html tree, gives all the lawyers of a page
ugyved2 = {} # temporary container for the second part of the html tree, gives all the lawyers of a page
dfmain = pd.DataFrame() #  main collector DF
m = 0 # counter

for m, soup in enumerate(i()): # iterating over pages
    # soup = next(i()) # for testing one
    for n, lawyer in enumerate(
            soup.find_all(name='div', attrs={'class':'media'})):# over lawyers (firstly on their media class) 
        title = lawyer.find('h4') # find title
        if ugyved.get('naem') == None :  # naem = name, first check, to create list of name
            ugyved['naem'] = []
            ugyved['naem'].append(title.string.split('(')[0].strip())  # string magic
        else:
            ugyved['naem'].append(title.string.split('(')[0].strip()) # all after
        if ugyved.get('type') == None : # first check and create
                ugyved['type'] = []
                ugyved['type'].append(title.string.split('-')[1].strip()) #string magic
        else:
                ugyved['type'].append(title.string.split('-')[1].strip()) # as above
        # print(type(lawyer))
        ugyved2[n] = [] # allocating the n. lawyer, with n-th key 
        law_attrs =  {} # alloc, this is the running container for a row of lawyer

        for nn, law_attr in enumerate(lawyer.find_all( 
                name='div', attrs={'class':'form-group'})): # fetching the div for secondary data from the html tree of one lawyer
            k = law_attr.findNext(name='label').string # key
            v = law_attr.findNext(name='p', attrs='form-control-static').string #value

            law_attrs[k] = v # collecting the data in the temp dict

		ugyved2[n].append(law_attrs) # collecting, the next one will be at n+1 lawyer
        dfpage = pd.DataFrame(data=[ugyved['naem'], ugyved['type']],
                              index=['name', 'lawyer']).T # put the primer infos of the lawyers of n-th page in a dataframe and some corrections
	
    ind = pd.Index(range(len(dfmain), len(dfmain)+len(dfpage))) # create the extended index for this n-th page of lawyer
    dfpage.set_index(ind, inplace=True) # fill the new index

    attrs_page_df = pd.DataFrame([pd.Series(ugyved2[n][0]) for n in ugyved2.keys()]) # put the secondary infos of the lawyers in a df
    attrs_page_df.set_index(ind, inplace=True) # set the extended (and same) index on it

    dfpage = dfpage.join(attrs_page_df) # merge the primer and secondary dataframes 
    dfmain = pd.concat([dfmain, dfpage]) # merge to the main Df
    ugyved, ugyved2 = {}, {} #clear the temporary dictionaries

#%%
dfmain.to_csv("ugyvedek_table_v2.csv", encoding='utf-32') #save
