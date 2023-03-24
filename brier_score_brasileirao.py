## projeto inspirado em postagens de @sonofacorner no twitter

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

## definindo o ano de análise

ano = 2021

## importando o arquivo com as probabilidades para os jogos da base do site 538

jogos = pd.read_csv('https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv')


## restringindo a análise para o brasileirao (liga 2105) e o ano definido acima

bra = jogos[jogos.league_id == 2105]
bra = bra[bra.season == ano]


## criando coluna para adicionar o Brier Score para cada jogo no df

bra = bra.assign(resultado = "")

bra = bra.reset_index(drop=True)

t = 0
while t < len(bra.league):
    if bra.score1[t] > bra.score2[t]:
        bra.resultado[t] = 1
        t += 1
    elif bra.score1[t] == bra.score2[t]:
        bra.resultado[t] = 0
        t += 1
    elif bra.score1[t] < bra.score2[t]:
        bra.resultado[t] = -1
        t += 1

bra = bra.assign(brier="")

t = 0
while t < len(bra.season):
    if bra.resultado[t] == 1:
        bra.brier[t] = 1/3*((bra.prob1[t] - 1)**2 + bra.prob2[t]**2 + bra.probtie[t]**2)
        t += 1
    elif bra.resultado[t] == 0:
        bra.brier[t] = 1/3*(bra.prob1[t]**2 + bra.prob2[t]**2 + (bra.probtie[t]-1)**2)
        t += 1
    elif bra.resultado[t] == -1:
        bra.brier[t] = 1/3*(bra.prob1[t]**2 + (bra.prob2[t] - 1)**2 + bra.probtie[t]**2)
        t += 1
        
bra.date = pd.to_datetime(bra.date)
bra = bra.assign(rodada=np.repeat(range(1,39),10))


## gerando df com a média ponderada do índice para as 38 rodadas, uma a uma

times = bra[['team1']].drop_duplicates()
plot_df = pd.DataFrame()

for time in times["team1"]:
    aux_df = bra[(bra["team1"] == time) | (bra["team2"] == time)].copy()
    # compute cumulative average
    cum_mean = (
        aux_df["brier"].expanding().mean()
    )
    
    new_df = pd.DataFrame()
    new_df["cum_mean"] = cum_mean
    new_df["time"] = time
    new_df['brier'] = aux_df.brier
    new_df['xgdif'] = abs(aux_df.xg1 - aux_df.score1)+abs(aux_df.xg2 - aux_df.score2)
    
    plot_df = plot_df.append(new_df)
     
plot_df = plot_df.reset_index(drop=True)
plot_df = plot_df.assign(rodada = np.tile(range(1,39),20))
 
## definindo a ordem de plot pelo valor acumulado na última rodada, do maior ao menor (mais imprevisível ao menos)
ordem = plot_df[plot_df.rodada == 38]
ordem = ordem.sort_values(by=['cum_mean'])
ordem = ordem.assign(pos = "")

## colocando a ordem de classificação final no campeonato
ordem.loc[ordem.time=='Atletico Mineiro','pos'] = 1
ordem.loc[ordem.time=='Flamengo','pos'] = 2
ordem.loc[ordem.time=='Palmeiras','pos'] = 3
ordem.loc[ordem.time=='Fortaleza','pos'] = 4
ordem.loc[ordem.time=='Corinthians','pos'] = 5
ordem.loc[ordem.time=='Bragantino','pos'] = 6
ordem.loc[ordem.time=='Fluminense','pos'] = 7
ordem.loc[ordem.time=='América Mineiro','pos'] = 8
ordem.loc[ordem.time=='Atlético Goianiense','pos'] = 9
ordem.loc[ordem.time=='Santos','pos'] = 10
ordem.loc[ordem.time=='Ceará','pos'] = 11
ordem.loc[ordem.time=='Internacional','pos'] = 12
ordem.loc[ordem.time=='São Paulo','pos'] = 13
ordem.loc[ordem.time=='Atlético Paranaense','pos'] = 14
ordem.loc[ordem.time=='Cuiaba','pos'] = 15
ordem.loc[ordem.time=='Juventude','pos'] = 16
ordem.loc[ordem.time=='Grêmio','pos'] = 17
ordem.loc[ordem.time=='Bahía','pos'] = 18
ordem.loc[ordem.time=='Sport Recife','pos'] = 19
ordem.loc[ordem.time=='Chapecoense AF','pos'] = 20

ordem = ordem.reset_index(drop=True)


lista_times = pd.unique(ordem.time).tolist()


## definindo cores para a linha de cada time no gráfico final
df_cores = pd.DataFrame()
df_cores['time'] = lista_times

dict_cores = {'Atletico Mineiro':'black','Palmeiras':'green','Chapecoense AF':
              'darkgreen','Atlético Paranaense':'red','Bahía':'blue','Sport Recife':
                  'red','Corinthians':'black','Flamengo':'darkred','Juventude':'green',
                  'Fortaleza':'darkblue','Fluminense':'darkred','América Mineiro':
                      'green','Ceará':'black','Internacional':'red','São Paulo':
                          'red','Grêmio':'dodgerblue','Santos':'black',
                          'Atlético Goianiense':'red','Cuiaba':'darkgreen',
                          'Bragantino':'black', 'Avaí':'blue','Coritiba':
                              'darkgreen','Goiás':'darkgreen','Botafogo':'black'}
    
df_cores = df_cores.assign(cor="")


t=0
while t<len(df_cores.time):
    df_cores.cor[t] = dict_cores[df_cores.time[t]]
    t += 1



## gerando a imagem com um gráfico para cada uma das 20 equipes (5 x 4)
lista_inds = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),
              (2,2),(2,3),(3,0),(3,1),(3,2),(3,3),(4,0),(4,1),(4,2),(4,3)]

imagem, eixos = plt.subplots(5,4,tight_layout=True,figsize=(15,10),sharey=True,sharex=True,facecolor='floralwhite')
plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)

imagem.suptitle('Brier Score - Brasileirão 2021\nQuais foram os times mais previsíveis do campeonato?\nby @rkujom, based on @sonofacorner', fontsize = 16,weight='bold')

v = 0
while v < len(lista_times):
    time = lista_times[v]
    
    df = plot_df[plot_df.time == time]
    df = df.reset_index(drop=True)
    
    cor = df_cores[df_cores.time==time]['cor'].tolist()[0]
    pos = ordem[ordem.time==time]['pos'].tolist()[0]
    
    eixos[lista_inds[v][0],lista_inds[v][1]].plot(df.rodada,df.cum_mean,color=cor)
    eixos[lista_inds[v][0],lista_inds[v][1]].set_title(time+' ('+str(pos)+'º)',pad=3,loc='left',fontsize=12,weight="bold")
    eixos[lista_inds[v][0],lista_inds[v][1]].set_facecolor('floralwhite')
    eixos[lista_inds[v][0],lista_inds[v][1]].set_xticks(np.arange(0,39,5))
    eixos[lista_inds[v][0],lista_inds[v][1]].set_xlabel('Rodada')
    eixos[lista_inds[v][0],lista_inds[v][1]].set_ylabel('Brier Score')
    
    eixos[lista_inds[v][0],lista_inds[v][1]].annotate(
        xy = (df.rodada.values[-1]-1.35, df.cum_mean.values[-1]+.05),
        text = round(df.cum_mean.values[-1],3),
        textcoords = "offset points",
        ha = "center",
        va = "center",
        color = cor,
        weight = "bold",
        size = 10
    )
    
    if lista_inds[v][0]==4:
        label_x=True
    else:
        label_x=False
        
    if lista_inds[v][1]==0:
        label_y=True
    else:
        label_y=False
    
    eixos[lista_inds[v][0],lista_inds[v][1]].grid(ls = "--", color = "lightgrey")
    eixos[lista_inds[v][0],lista_inds[v][1]].spines["top"].set_visible(False)
    eixos[lista_inds[v][0],lista_inds[v][1]].spines["right"].set_visible(False)
    
    for x in lista_times:
            if x == time:
                continue
            aux_df = plot_df[plot_df["time"] == x].reset_index(drop = True)
            eixos[lista_inds[v][0],lista_inds[v][1]].plot(
                aux_df.rodada,
                aux_df["cum_mean"],
                color = "gray",
                alpha = 0.15,
                lw = 1.25,
                zorder = 2
            )
        
        
    v += 1
    


## gerando gráfico de dispersão entre a posição no campeonato X Brier Score médio final
x = ordem.pos.values
y = ordem.cum_mean.values
nomes = ordem.time.values

pontos, axes = plt.subplots(1,1,tight_layout=True,figsize=(12,10),facecolor='floralwhite')
pontos.suptitle('Brier Score x Posição no Campeonato\nBrasileirão 2022 (até 16ª rodada)\nby @rkujom',fontsize=20)
axes.scatter(x=x,y=y,color='black',s=0.1)
for i, txt in enumerate(nomes):
    axes.annotate(txt,(x[i],y[i]),fontsize=13)
axes.set_facecolor('floralwhite')
axes.grid(ls='--',color='lightgrey')
axes.spines["top"].set_visible(False)
axes.spines["right"].set_visible(False)
plt.xticks(np.arange(min(x)-1, max(x)+1, 5.0))
plt.ylabel("Brier Score",fontsize=20)
plt.xlabel("Posição no Campeonato",fontsize=20)


'''gerando gráfico de dispersão entre a probabilidade de empate X Brier Score do jogo,
para os 380 jogos do campeonato. '''

img, axes = plt.subplots(1,1,tight_layout=True,figsize=(10,8),facecolor='floralwhite')
img.suptitle('Probabilidade de Empate x Brier Score\nBrasileirão 2021\nby @rkujom',fontsize=18,weight='bold')
axes.scatter(bra[bra.resultado==0]['brier'],bra[bra.resultado==0]['probtie'],color='green',label='Empate')
axes.scatter(bra[bra.resultado!=0]['brier'],bra[bra.resultado!=0]['probtie'],color='red',label="Vitória/Derrota")
axes.set_facecolor('floralwhite')

axes.grid(ls = "--", color = "lightgrey")
axes.spines["top"].set_visible(False)
axes.spines["right"].set_visible(False)
axes.legend(loc='upper right')
plt.ylabel("Probabilidade Empate",fontsize=12)
plt.xlabel("Brier Score",fontsize=12)
