import streamlit as st
from PIL import Image

import sqlite3
import pandas.io.sql as psql
import pandas as pd
import os

db_name = 'master.db'
conn = sqlite3.connect(db_name)
c = conn.cursor()

query = '''
SELECT *
FROM boxsize
'''
c.execute(query)

st.sidebar.subheader('Item_size')
size1 = st.sidebar.text_input('length（cm）')
size2 = st.sidebar.text_input('width（cm）')
d = st.sidebar.text_input('depth（cm）')

buffer = st.sidebar.radio(
     "buffer",
     ('none', '1cm', '2cm'))

if buffer == '1cm':
    st.write('')
elif buffer == '2cm':
    st.write('')
else:
    st.write('')

st.sidebar.subheader('box_size')

if len(size1) == 0:
    st.warning('Please enter a value.')
elif len(size2) == 0:
    st.warning('Please enter a value.')
elif len(d) == 0:
    st.warning('Please enter a value.')
else:
    size1 = int(size1)*10
    size2 = int(size2)*10
    d = int(d)*10

    if size1 >= size2:
        l = size1
        w = size2
        d = d
    else:
        l = size2
        w = size1
        d = d

    if l > 645:
        st.error('Over 160-A size. Please search again.')
    elif w > 410:
        st.error('Over 160-A size. Please search again.')
    elif d > 503:
        st.error('Over 160-A size. Please search again.')
    else:
        query_select = '''
        SELECT * 
        FROM boxsize 
        WHERE length > ?
        AND width > ?
        AND depth > ?
        '''
        c.execute(query_select, (l,w,d, ) )
        result = c.fetchall()

        df = pd.DataFrame(result, columns=[x[0] for x in c.description])
        df = df.drop('index', axis=1)
        conn.close()

        st.success('Success：Display search results.')

        select = result[0][1]
        st.title(select)

        path = os.getcwd()
        box_name = select + '.png'
        image = Image.open(path + '/image/' + box_name)
        st.image(image)

        # df = df['material_name']
        st.sidebar.write(df)