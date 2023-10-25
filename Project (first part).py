#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm


# <h1>Projekt: Szymon, Maciej<h1>

# In[7]:


emisja = pd.read_excel('Emisja.xlsx')
emisja.head()


# ## <center>1. Wstęp </center>
# 

# 
#    Zjawisko globalnego ocieplenia jest w naszych czasach coraz poważniejszym problemem. Przewiduje się, że za 20 lat klimat będzie podobny do tego, który obecnie jest w Hiszpanii. Tereny okołorównikowe coraz bardziej pustynnieją, co stanowi poważny problem dla państw Afrykańskich, jak na przykład Etiopia. Prognozy na rok 2050 wykazują rozległe problemy spowodowane suszami, które mają zmusić wiele milionów ludzi do migracji na obfitsze w wodę tereny. Unia Europejska desperacko stara się ratować klimat, poprzez obostrzenia industrialne i handel prawami do emisji dwutlenku węgla. Właśnie w tych czasach, szczególnie potrzebne są badania odnośnie tego co wpływa na emisję CO2. 
#     Celem naszej pracy jest analiza wydzielania CO2 przez poszczególne województwa w Polsce. Jakimi sposobami wytwarzania energii można najlepiej opisać jego łączną emisję. Jak można pogrupować województwa na skupienia metodą aglomeracyjną i jaką wiedzę nam to da?

# ## <center> 2.Dane oraz podstawowe statystyki opisowe </center>

# Nasze dane zawierają następujące zmienne objaśniające:
# * zużycie węgla kamiennego w tysiącach ton
# * zużycie gazu ziemnego [TJ]
# * pojazdy (samochody osobowe, autobusy, motocykle) w sztukach
# * procentowy udział energii odnawialnej w energii ogółem.
# 
# Zmienna objaśniająca to 
# * Emisja dwutlenku węgla w tysiącach ton	.
# 
# Podstawowe statystyki opisowe prezentują się następująco:

# In[8]:


emisja.describe()


# Na ich podstawie nie da się wyciągnąć żadnych pewnych wniosków, ale dają wstępny pogląd na dane.

# In[8]:


emisja.Wooj.value_counts()


# Dokonaliśmy podziału kategorialnego województw, ze względu na to w jakiej części Polski się znajdują.
# W każdej z kategorii znajdują się trzy województwa, z jednym wyjątkiem jakim jest północ Polski, tam są cztery.

# In[14]:


emisja.Wooj.value_counts().plot.bar(color='pink',
alpha=0.6,
title='Podzial wojewodztw',
edgecolor='red',
linewidth=2,
ylabel='Ile w kategorii')


# Porównano wybrane z statystyki opisowe ze względu na zmienną kategorialną.

# In[83]:


emisja.groupby('Wooj').agg(['mean','median','max','min'])


# In[78]:


plt.bar(emisja.W, emisja.Emisja,
       edgecolor='pink',
        color='yellow',
       width= 0.9,
       )
plt.title('Emisja CO2 [tys.ton]')
plt.xticks(rotation=90)
plt.show()


# Najwyższa emisja CO2 odnotowana została w województwie łódzkim, mazowieckim i śląskim. Najniższe wartości zaobserwowano w województwie lubuskim i podlaskim.

# In[77]:


plt.bar(emisja.W, emisja.Wegiel,
       edgecolor='pink',
        color='red',
       )
plt.title('Zużycie wegla kamiennego [tys.ton]')
plt.xticks(rotation=90)
plt.show()


# Największe zużycie węgla kamiennego zaobserwowano w województwie śląskim i mazowieckim. Natomiast województwo lubuskie, podlaskie i warmińsko-mazurskie wykazuje bardzo niskie zużycie tego surowca.

# In[76]:


plt.bar(emisja.W, emisja.Gaz,
       edgecolor='pink',
        color='brown',
       )
plt.title('Zużycie gazu ziemnego [TJ]')
plt.xticks(rotation=90)
plt.show()


# W przypadku zużycia gazu ziemnego województwo mazowieckie wyróżnia się na tle pozostałych obserwacji. 
# Po raz kolejny województwa podlaskie i warmińsko-mazurskie znajdują się w grupie z najmniejszymi wartościami zmiennej. 

# In[79]:


plt.bar(emisja.W, emisja.Odna,
       edgecolor='pink',
        color='navy',
       )
plt.title('Udział energii odnawialnej w produkcji energii elektrycznej ')
plt.xticks(rotation=90)
plt.show()


# Odnawialne źródła energii stanowią domenę województw położonych na północy. Wszystkie znajdujące się w tej kategorii wykazały duże wartości tej zmiennej. Duża jest również grupa, która wykazuje praktycznie zerowe wartości. Jest to m.in. województwo śląskie czy łódzkie.

# ## <center> 3. Korelacja i grupowanie </center>

# In[84]:


corr_matrix = emisja.corr()
corr_matrix


# In[85]:


sns.heatmap(corr_matrix,
           vmin = -1,
           vmax = 1,
           square = True,
           annot = True)


# Macierz korelacji prezentuje się następująco. Nie powinien dziwić fakt, że emisja  dwutlenku węgla jest umiarkowanie ujemnie skorelowana z odnawialnymi źródłami energii. Da się natomiast zaobserwować dość silne dodatnie skorelowanie zmiennej objaśnianej ze zużyciem węgla kamiennego, co może wyjaśniać bardzo dużą emisję CO2 na śląsku, gdzie zużycie węgla jest największe.

# Bardzo prosimy przejść do drugiego pliku :)

# ## <center> 4. Modele ekonometryczne </center>

# In[93]:


emisja = sm.add_constant(emisja)

emisja


# In[94]:


# zdefiniowanie i modelu i oszacowanie jego parametrów
OLS_res = sm.OLS(endog=emisja['Emisja'], #zmienna objaśniana
                 exog=emisja[['const','Gaz','Pojazdy']]).fit()
# wyświetlenie wyników
OLS_res.summary()


# W pierwszym modelu wykorzystaliśmy zmienne:
# -zużycie gazu ziemnego [TJ]
# -pojazdy (samochody osobowe, autobusy, motocykle) w sztukach
# 
# Niestety p-value dla pojazdów okazało się znacznie przekraczać dopuszczalny próg. Ostatecznie w modelu znalazła się stała razem ze zmienną oznaczającą zużycie gazu
# 

# In[101]:


OLS_res = sm.OLS(endog=emisja['Emisja'], #zmienna objaśniana
                 exog=emisja[['const','Gaz']]).fit()
# wyświetlenie wyników
OLS_res.summary()


# I w tym przypadku p-value dla stałej wykracza nieznacznie dopuszczalną wartość. Mimo to wzięliśmy ją pod uwagę. Sam model nie ocenia dobrze zmiennej objaśnianej. R^2 wynoszące 0,33 oznacza, że niewielka zmienność zmiennej objaśnianej została wyjaśniona w niewielkim stopniu. Podobnie dopasowany współczynnik determinacji, który wyniósł 0,29 oznacza, że zmienna objaśniana została wyjaśniona w nikłym stopniu. Model z tymi zmiennymi nie ma szans na prawidłowe przewidywanie wartości zmiennej objaśnianej.

# Następnie wykorzystaliśmy pozostałe 2 zmienne tj. 
# -zużycie węgla kamiennego w tysiącach ton
# -procentowy udział energii odnawialnej w energii ogółem.
# 
# 

# In[97]:


OLS_res = sm.OLS(endog=emisja['Emisja'], #zmienna objaśniana
                 exog=emisja[['const','Wegiel','Odna']]).fit()
# wyświetlenie wyników
OLS_res.summary()


# Mimo p-value minimalnie powyżej progu dla odnawialnych źródeł energii, wszystkie zmienne, razem ze stałą, znalazły się w modelu. R^2 w tym przypadku wynosi 0,65 - w 65% zmienność Emisji CO2 jest wyjaśniana przez przyjęte w modelu zmienne objaśniające. Dopasowane R^2 wynoszące 0,59 oznacza, że informacje o zmiennej objaśnianej są wyjaśniane w 59%. Nie są to wartości idealne jednak pozwalają one z pewnym przekonaniem mówić o występowaniu pewnych zależności. 
# Współczynnik regresji wynoszący 1,59 dla zużycia węgla oznacza, że każde 1000 ton zużytego węgla powoduje wzrost emisji o 1592 ton. Natomiast każdy dodatkowy procent energii odnawialnej wykorzystywanej przy produkcji energii elektrycznej powoduje zmniejszenie się tej emisji 238000 ton. 
# 

# Podsumowując z naszego badania da się wyciągnąć niestety niezbyt przełomowy wniosek, że węgiel i odnawialne źródła energii jako źródła energii, mają wpływ na emisję dwutlenku węgla w danym regionie, z czego zużycie węgla dodatnie, a odnawialne źródła energii odwrotnie. Wynika tak, nie tylko ze zweryfikowanego modelu ekonometrycznego, ale i z macierzy korelacji, na której wyraźnie to, widać zależność. Z analizy skupień można zaobserwować, że województwa w których odnawialne źródła energii stanowią większy odsetek produkcji prądu, różnią się od innych. Udało się również zobaczyć, że województwa: Łódzkie, Mazowieckie oraz Śląskie znacznie różnią się od innych ze względu na badane cechy. Grupowanie metodą Warda pozwoliło zobaczyć pewne zależności między wybranymi regionami Polski oraz to jak wysokie wartości badanych zmiennych prezentują województwa Mazowieckie i Śląskie.  Ostateczne wnioski są takie, że jeśli chcemy zmniejszyć emisję CO2, to niezbędne będzie zamienienie węgla innymi nośnikami energii.

# Źródła: Dane pochodzą ze zbiorów Głównego Urzędu Statystycznego: https://stat.gov.pl 

# In[ ]:




