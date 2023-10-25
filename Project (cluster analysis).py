#!/usr/bin/env python
# coding: utf-8

# In[60]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm


# In[61]:


emisja = pd.read_excel('Emisja.xlsx',
       index_col = 'W')
emisja.head()


# In[62]:


emisja2 = emisja.iloc[:, :6]
emisja2


# Poniższy obraz przedstawia wyniki analizy skupień.

# In[63]:


# wykonanie grupowania i wizualizacji - inne ustawienia
sns.clustermap(emisja2.iloc[:, :-1], 
               z_score= 1,
               cmap='Blues',
               cbar_pos=(1.2, 0.15, 0.1, 0.4),
               annot=True,
               linewidth=0.1,
               linecolor='black',
               figsize=(7,12))


# Można zaobserwować kilka grup:
# -województwo Łódzkie stanowiące pierwsza grupę samodzielnie
# -druga grupa składa się z województw: Warmińsko-Mazurskiego, Podlaskiego, Zachodniopomorskiego, Kujawsko Pomorskiego oraz Pomorskiego
# -trzecia grupa to województwa: Lubelskie, Wielkopolskie, Opolskie, Świętokrzyskie, Lubuskie, Podkarpackie, Dolnośląskie oraz małopolskie
# -czwartą grupę stanowi samodzielnie województwo Mazowieckie
# -piątą grupę stanowi województwo Śląskie
# 	Podział ten jest niezwykle ciekawy, gdyż aż trzy grupy są pojedynczymi województwami. Jeśli chodzi o województwo Śląskie, podejrzewamy, że może odstawać ze względu na bardzo dużą ilość zużywanego węgla kamiennego. Województwo Mazowieckie cechuje się bardzo dużym zużyciem gazu ziemnego, znacznie powyżej średniej, a z kolei województwo Łódzkie cechuje się wysoką produkcją CO2, przy jednoczesnych niskich poziomach zmiennych objaśniających.
# Cechą łączącą drugą grupę jest to, że wszystkie znajdują się w północnej części Polski. Jednocześnie warto zauważyć, że u wszystkich tych województw, odnawialne źródła energii stanowią relatywnie duży odsetek całej energii.
# W kwestii trzeciej grupy, ciężko jest znaleźć jeden konkretny czynnik wspólny, można przypuszczać, że są to państwa względnie wyśrodkowane i nie wyróżniające się niczym szczególnym, co jest właśnie cechą która je łączy.
# 

# Dokonano również analizy metodą Warda:

# In[42]:


sns.clustermap(emisja2.iloc[:, :-1],
z_score=1,
method='ward',
figsize=(8,10),
cmap='Spectral')


# Ilość wartości zawierających się w przedziale od 0 do -1 świadczy, że wiele województw wykazuje podobne wartości wykorzystywanych zmiennych. Wyróżniają się województwa położone na północy kraju, z udziałem energii odnawialnych w wytwarzaniu elektryczności powyżej średniej. Umieszczone w tym przypadku w jednej grupie województwo Mazowieckie i Śląskie wykazuje w każdym przypadku wartości odbiegające znacznie od średniej. 

# In[66]:



colors = emisja2['Wooj'].map({'Centrum':'red','Polnoc':'orange','Wschod':'green','Zachod':"brown",'Poludnie':"blue"})

sns.clustermap(emisja2.iloc[:, :-2],
z_score=1,
row_colors = colors,
figsize=(8,10),
method='ward',
linecolor='white',
linewidth=0.1)


# W przypadku metody Warda, po uwzględnieniu naszej zmiennej kategorialnej można zauważyć, że tendencje do łączenia się w grupy mają województwa północne i wschodnie (kolor zielony i pomarańczowy) oraz województwa centralne i południowe (kolor niebieski i czerwony)

# Dla sprawdzenia postanowiliśmy usunąć województwo Mazowieckie i Śląskie. Zawyżanie statystyk przez oba te województwa widać gdy metodę Warda zastosujemy po ich usunięciu:

# In[51]:


emisja2.drop(["MAZOWIECKIE", "ŚLĄSKIE"], inplace = True)


# In[52]:


sns.clustermap(emisja2.iloc[:, :-1],
z_score=1,
method='ward',
figsize=(8,10),
cmap='Spectral')


# Przepraszamy za utrudnienia :) Prosimy wrócić do głównego pliku.
