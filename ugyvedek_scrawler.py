# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 20:18:19 2021

@author: Kőszeghy Dániel
"""

import os
import requests

 
url = "https://ouny.magyarugyvedikamara.hu/licoms/common/service/requestparser?name=pubsearcher&action=search&type=ugyved&status=aktiv&p="

allresult = 11495# on 2021.02.09 
if allresult % 25 == 0:
    lastpage = allresult // 25
else:
    last_page = allresult //25 + 1 # 25 lawyerper page + one as the residue

os.mkdir('lawyer_pages')
os.chdir('lawyer_pages')
    
for i in range(1, last_page+1): # for the open interval
    html = requests.get(url + str(i))
    with open('p'+ str(i) + '.html','w')  as htmlfile:
        htmlfile.write(html.text)
        print('p' + str(i) + ' is done')
        htmlfile.close()
        