import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import time
from matplotlib import pyplot as plt
import numpy as np
from adjustText import adjust_text

url = 'https://fbref.com/pt/comps/24/10986/cronograma/2021-Serie-A-Resultados-e-Calendarios'

page = requests.get(url)

soup = bs(page.content,'html.parser')

jogos = soup.find_all('td',{'data-stat':'match_report'})
lista_links = []

for jogo in jogos:
    if jogo.find('a') is None:
        continue
    else:
        lista_links.append(jogo.find('a').get('href'))

df_players = pd.DataFrame(columns = ['ID','Nome','Clube','ClubeID'])

numerojogo = 1

df_final_gols = pd.DataFrame(columns=['Evento','ID','Nome','Min','Time','Placar'])

for link in lista_links:

    url = 'https://fbref.com/'+link
    
    page = requests.get(url)
    
    soup = bs(page.content,'html.parser')
    
    casa = soup.find_all('strong')[2].find('a').text
    casa_id = soup.find_all('strong')[2].find('a').get('href').split('/')[3]
    if soup.find_all('strong')[5].find('a') is None:
        fora = soup.find_all('strong')[4].find('a').text
        fora_id = soup.find_all('strong')[4].find('a').get('href').split('/')[3]
    else:
        fora = soup.find_all('strong')[5].find('a').text
        fora_id = soup.find_all('strong')[5].find('a').get('href').split('/')[3]
    
    trs = soup.find_all('tr')
    lista_ids = []
    lista_jogs = []
    
    df_jogs = pd.DataFrame()
    
    for tr in trs:
        if tr.find('a') is None:
            continue
        else:
            lista = tr.find('a').get('href').split('/')
            if lista[4] == "":
                continue
            else:
                lista_ids.append(lista[3])
                lista_jogs.append(lista[4])
            
    df_jogs['ID'] = lista_ids
    df_jogs['Nome'] = lista_jogs
    
    df_jogs = df_jogs.drop_duplicates('ID')
    
    t = 1
    while t < len(trs):
        if trs[t].text is None:
            t += 1
        else:
            if len(trs[t].text.split(' (')) > 1:
                pos = t-2
                t = t + len(trs)
            else:
                t += 1
    
    
                
    lista_clube = []
    t = 0
    while t < len(df_jogs.ID):
        if t < pos:
            lista_clube.append(casa)
            t += 1
        else:
            lista_clube.append(fora)
            t += 1
            
    df_jogs['Clube'] = lista_clube
    
    df_jogs = df_jogs.assign(ClubeID = "")
    t = 0
    while t < len(df_jogs.Clube):
        if df_jogs.Clube[t] == casa:
            df_jogs.ClubeID[t] = casa_id
            t += 1
        elif df_jogs.Clube[t] == fora:
            df_jogs.ClubeID[t] = fora_id
            t += 1
    
    df_players = df_players.append(df_jogs)
    
    eventos_casa = soup.find_all('div',{'class':'event a'})
    eventos_fora = soup.find_all('div',{'class':'event b'})
    
    
    lista_eventos = []
    lista_jogid_evento = []
    lista_jognome_evento = []
    lista_min = []
    lista_time = []
    lista_placar = []
    lista_jogos = []
    
    df_gols = pd.DataFrame()
    
    for evento in eventos_casa:
        if evento.find('div',{'style':'display: none;'}).text[:7] == '\xa0—\xa0Goal':
            lista_eventos.append('Gol')
            lista_jogid_evento.append(evento.find_all('a')[0].get('href').split('/')[3])
            lista_jognome_evento.append(evento.find_all('a')[0].get('href').split('/')[4])
            if len(evento.find('div').text.replace('\t','').replace('\n','').split('&')[0].split('+'))==2:
                lista_min.append(evento.find('div').text.replace('\t','').replace('\n','').split('&')[0].split('+')[0])
            else:
                lista_min.append(evento.find('div').text.replace('\t','').replace('\n','').split('&')[0][-2:])
            lista_time.append('c')
            if evento.find('div',{'style':'display: none;'}).text[-4:-1] == 'Goa':
                lista_placar.append(evento.find('small').text)
            else:
                lista_placar.append(evento.find('div',{'style':'display: none;'}).text[-4:-1])
            lista_jogos.append(numerojogo)
        elif evento.find('div',{'class':'event_icon penalty_goal'}) is not None:
            lista_eventos.append('Gol')
            lista_jogid_evento.append(evento.find_all('a')[0].get('href').split('/')[3])
            lista_jognome_evento.append(evento.find_all('a')[0].get('href').split('/')[4])
            if len(evento.find('div').text.replace('\t','').replace('\n','').split('&')[0].split('+'))==2:
                lista_min.append(evento.find('div').text.replace('\t','').replace('\n','').split('&')[0].split('+')[0])
            else:
                lista_min.append(evento.find('div').text.replace('\t','').replace('\n','').split('&')[0][-2:])
            lista_time.append('c')
            lista_placar.append(evento.find('small').text)
            lista_jogos.append(numerojogo)
        else:
            continue
        
    for evento in eventos_fora:
        if evento.find('div',{'style':'display: none;'}).text[:7] == '\xa0—\xa0Goal':
            lista_eventos.append('Gol')
            lista_jogid_evento.append(evento.find_all('a')[0].get('href').split('/')[3])
            lista_jognome_evento.append(evento.find_all('a')[0].get('href').split('/')[4])
            if len(evento.find('div').text.replace('\t','').replace('\n','').split('&')[0].split('+'))==2:
                lista_min.append(evento.find('div').text.replace('\t','').replace('\n','').split('&')[0].split('+')[0])
            else:
                lista_min.append(evento.find('div').text.replace('\t','').replace('\n','').split('&')[0][-2:])
            lista_time.append('f')
            if evento.find('div',{'style':'display: none;'}).text[-4:-1] == 'Goa':
                lista_placar.append(evento.find('small').text)
            else:
                lista_placar.append(evento.find('div',{'style':'display: none;'}).text[-4:-1])
            lista_jogos.append(numerojogo)    
        elif evento.find('div',{'class':'event_icon penalty_goal'}) is not None:
            lista_eventos.append('Gol')
            lista_jogid_evento.append(evento.find_all('a')[0].get('href').split('/')[3])
            lista_jognome_evento.append(evento.find_all('a')[0].get('href').split('/')[4])
            if len(evento.find('div').text.replace('\t','').replace('\n','').split('&')[0].split('+'))==2:
                lista_min.append(evento.find('div').text.replace('\t','').replace('\n','').split('&')[0].split('+')[0])
            else:
                lista_min.append(evento.find('div').text.replace('\t','').replace('\n','').split('&')[0][-2:])
            lista_time.append('c')
            lista_placar.append(evento.find('small').text)
            lista_jogos.append(numerojogo)
        else:
            continue
    
    
    df_gols['Jogo'] = lista_jogos
    df_gols['Evento'] = lista_eventos
    df_gols['ID'] = lista_jogid_evento
    df_gols['Nome'] = lista_jognome_evento
    df_gols['Min'] = lista_min
    df_gols['Time'] = lista_time
    df_gols['Placar'] = lista_placar
        
    df_final_gols = df_final_gols.append(df_gols)
        
    print(numerojogo)
    numerojogo += 1
        
    time.sleep(4)



df_final_gols = df_final_gols.assign(pontos = '')
df_final_gols = df_final_gols.assign(dif = '')
df_final_gols = df_final_gols.reset_index(drop=True)

 


df_rodadas = pd.DataFrame()

df_rodadas['Jogo'] = range(1,381)

df_rodadas['Rodada'] = np.repeat(range(1,39),10)



lista_rodadas = []
t = 0

while t < len(df_final_gols):
    jogo = df_final_gols.Jogo[t]
    rodada = df_rodadas[df_rodadas.Jogo == jogo]['Rodada'].tolist()[0]
    lista_rodadas.append(rodada)
    t += 1
    
df_final_gols['Rodada'] = lista_rodadas
   
t = 0
while t < len(df_final_gols):
    casa = int(df_final_gols.Placar[t][:1])
    fora = int(df_final_gols.Placar[t][2:4])
    dif = casa - fora
    
    if df_final_gols.Time[t] == 'c':
        if casa > fora and dif == 1:
            pontos = 3
            pond = 1
        elif casa > fora and dif > 1:
            pontos = 3
            pond = 1/dif
        elif casa == fora:
            pontos = 1
            oond = 1
        else:
            pontos = 0
            pond = 1/-dif
    elif  df_final_gols.Time[t] == 'f':
        if casa < fora and dif == -1:
            pontos = 3
            pond = 1
        elif casa < fora and dif < -1:
            pontos = 3
            pond = 1/-dif
        elif casa == fora:
            pontos = 1
            pond = 1
        else:
            pontos = 0
            pond = 1/dif
    df_final_gols.pontos[t] = pontos
    df_final_gols.dif[t] = pond
    t += 1

df_final_gols = df_final_gols.assign(pontospond = '')

t = 0
while t < len(df_final_gols):
    if df_final_gols.pontos[t] == 0:
        df_final_gols.pontospond[t] = df_final_gols.dif[t]
        t += 1
    else:
        df_final_gols.pontospond[t] = df_final_gols.pontos[t] * df_final_gols.dif[t]
        t += 1

lista_ids = []
lista_jogs = []
lista_pontos = []
lista_gols = []
  
for jogador in pd.unique(df_final_gols.ID):
    aux_df = df_final_gols[df_final_gols.ID == jogador]
    total = sum(aux_df.pontospond)
    lista_ids.append(jogador)
    lista_jogs.append(aux_df.Nome.tolist()[0])
    lista_pontos.append(total)
    lista_gols.append(len(aux_df))
    
df_pontos = pd.DataFrame()
df_pontos['ID'] = lista_ids    
df_pontos['Nome'] = lista_jogs
df_pontos['Pontos'] = lista_pontos
df_pontos['Gols'] = lista_gols


df_acumulado = pd.DataFrame(columns = ['ID','Nome','Rodada','Pontos','Gols'])

for rodada in range(1,39):
    lista_ids = []
    lista_nomes = []
    lista_rodada = []
    lista_pontos = []
    lista_gols = []
    df_rodada_jogs = pd.DataFrame()
    for jogador in pd.unique(df_final_gols.ID):
        
        lista_ids.append(jogador)
        lista_nomes.append(df_final_gols[df_final_gols.ID == jogador]['Nome'].tolist()[0])
        lista_rodada.append(rodada)
        
        aux_df = df_final_gols[(df_final_gols.ID == jogador)&(df_final_gols.Rodada <= rodada)]
        soma = len(aux_df)
        lista_gols.append(soma)
        total = sum(aux_df.pontospond)
        lista_pontos.append(total)
        
        
    df_rodada_jogs['ID'] = lista_ids
    df_rodada_jogs['Nome'] = lista_nomes
    df_rodada_jogs['Rodada'] = lista_rodada
    df_rodada_jogs['Pontos'] = lista_pontos
    df_rodada_jogs['Gols'] = lista_gols
    
    df_acumulado = df_acumulado.append(df_rodada_jogs)
 
    
 
for rodada in range(1,39):
    aux_df = df_acumulado[df_acumulado.Rodada == rodada]
    
    df_plot = aux_df[aux_df.Gols >= 8]
    df_top = df_plot.nlargest(10,columns=['Pontos'])
    
    for jogador in df_top.ID:
        df_plot.drop(df_plot.loc[df_plot['ID']==jogador].index,inplace=True)
    
    img, axes = plt.subplots(1,1,figsize=(10,8),tight_layout=True,facecolor='floralwhite')
    axes.set_title('Gols x Pontos\n'+str(rodada)+'a Rodada')
    axes.set_xticks(range(0,40))
    axes.set_yticks(range(0,20))
    
    x = df_plot.Pontos.values
    y = df_plot.Gols.values
    names = df_plot.Nome.values
    
    axes.scatter(x=x,y=y,s=0.005)
    
    texts = []
    
    for x, y, s in zip( x, y, names):
        texts.append(plt.text(x,y,s))
    
    adjust_text(texts, only_move={'points':'y', 'texts':'y'})
    
    
    x_top = df_top.Pontos.values
    y_top = df_top.Gols.values
    nomes = df_top.Nome.values
    
    axes.scatter(x=x_top,y=y_top,s=0.005)
    
    texts = []
    
    for x, y, s in zip( x_top, y_top, nomes):
        texts.append(plt.text(x,y,s))
    
    adjust_text(texts, only_move={'points':'y', 'texts':'y'})
    
    axes.grid(ls = "-.", color = "lightgrey")
    axes.set_facecolor('floralwhite')
    axes.spines["top"].set_visible(False)
    axes.spines["right"].set_visible(False)
