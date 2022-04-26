#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import streamlit as st


# In[6]:


df = pd.read_csv('player_data_final.csv')
similarity_indexes = pd.read_csv('similarity_matrix.csv').to_numpy()


# In[8]:


def recommend(name,size=20,potential=False):
    index = df[df['Name']==name].index.tolist()[0]
    most_similar_indexes = similarity_indexes[index][1:]
    if potential:
        return df.iloc[most_similar_indexes[:]].where(df.Age<26).sort_values('POT',ascending=False).iloc[:20].loc[:,['Name','Age','OVA','POT','Team & Contract','Height', 'Weight','Joined',
        'Value', 'Wage', 'Release Clause','Attacking','Skill','Movement','Power','Mentality','Defending','Goalkeeping']]
    else:
        return df.iloc[most_similar_indexes[1:size+1]].loc[:,['Name','Age','OVA','POT','Team & Contract','Height', 'Weight','Joined',
        'Value', 'Wage', 'Release Clause','Attacking','Skill','Movement','Power','Mentality','Defending','Goalkeeping']]


# In[4]:

from fuzzywuzzy import fuzz,process


st.title("Player Recommender")
name =st.text_input('Enter Player Name')
number = int(st.number_input('Number of players to recommend',min_value=0,max_value=100))
potential = st.checkbox('Recommend me only young players (<26 years old)')
button =  st.button('Recommend')
if button:
    if name and number>0:
        name_extract = process.extract(name,df.Name)[0][0]
        st.dataframe(recommend(name_extract,size=number,potential=potential),4000,1000)

    else:
        st.text("""Please make sure you satisfy the following:\n
                1.Name must not be empty
                2.Number of players to recommend must be in range [1,100]
                """)
        