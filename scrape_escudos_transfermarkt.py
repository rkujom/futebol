from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time

''' script para webscraping dos nomes e escudos dos principais clubes da américa latina'''


headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}



lista_anos = []

for ano in range(2015,2022):
    lista_anos.append(str(ano))

ligas = ['BRA1','BRA2','BRA3','BRA4','BRC','MEXA','AR1N','URU1','CLPD','COLP',
         'PR1A','VZ1L','PER1','BO1C']

lista_nome = []
lista_foto = []
lista_liga = []

for liga in ligas:
    for ano in lista_anos:

        url = 'https://www.transfermarkt.com.br/campeonato-brasileiro-serie-a/startseite/wettbewerb/'+liga+'/plus/?saison_id='+ano
    
        page = requests.get(url, headers=headers)
            
        soup = bs(page.content,'html.parser')
        
        nomes = soup.find_all('td',{'class':'no-border-links hauptlink'})
        
        for nome in nomes:
            lista_nome.append(nome.find('a').text)
            
            id_clube = nome.find('a').get('href').split('/')[4]
            
            lista_foto.append('https://tmssl.akamaized.net/images/wappen/head/'+id_clube+'.png')
            
            lista_liga.append(liga)
            
        time.sleep(2)
        print(liga+ano)

        
df_clubes = pd.DataFrame({'Clube':lista_nome,'LinkFoto':lista_foto,'Liga':lista_liga})    

dic_pais = {'BRA1':'Brasil','BRA2':'Brasil','AR1N':'Argentina','URU1':'Uruguai',
            'CLPD':'Chile','COLP':'Colombia','BRA3':'Brasil','MEXA':'Mexico',
            'BRC':'Brasil','BRA4':'Brasil','PR1A':'Paraguai','VZ1L':'Venezuela',
            'PER1':'Peru','BO1C':'Bolivia'}

for index, row in df_clubes.iterrows():
    df_clubes.Liga[index] = dic_pais[df_clubes.Liga[index]]

df_clubes = df_clubes.rename(columns={'Liga':'País'})
 
df_clubes = df_clubes.drop_duplicates(['Clube','País']).reset_index(drop=True)

for index, row in df_clubes.iterrows():
    if df_clubes.LinkFoto[index].split('/')[-1].split('.')[0].isdigit():
        continue
    else:
        df_clubes = df_clubes.drop(index)

df_clubes.to_csv('ClubesEscudos.csv')
