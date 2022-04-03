import streamlit as st
import pandas as pd
import numpy as np
import subprocess
import sys
subprocess.run([f"playwright","install-deps"])
subprocess.run([f"{sys.executable}","cpgrm.py"])
subprocess.run([f"{sys.executable}","scrapCM.py"])
subprocess.run([f"{sys.executable}","scrapcgrs.py"])


st.markdown("<h1 style='text-align: center; color: blue;'>DASHBOARD</h1>", unsafe_allow_html=True)


cmlt=pd.read_csv("cmlt.csv",names=["Sr. No","Total complaints","work in progress","closed","outside RTS"],sep='\t')
st.markdown("<h3 style='color: gray;'>ECGRS COMPLAINTS</h3>", unsafe_allow_html=True)
st.table(cmlt.style.set_properties(**{'border': '1.3px solid black','color': 'black'}))



cmpt=pd.read_csv("cmpt.csv",header=None,encoding='cp1252')
cmpt=cmpt[0].str.split(r'(\d+)',expand=True)
cmpt.drop(cmpt.columns[[0]], axis=1, inplace=True)
cmpt.columns=['No of CMwindows','STEP']
cmpt=cmpt[['STEP','No of CMwindows']]

ind =list(range(0,21))
cpgm=pd.read_csv('cpgm.csv',header=None,names=['col1'])
# drop rows where col1 have text 'View list of grievance(s)'
cpgm.drop(cpgm.index[[2,5,8,11,14,17,20]],inplace=True)
nopm=cpgm[cpgm['col1'].str.contains(r'(\d+)')].dropna().values
steps=cpgm[cpgm['col1'].str.contains(r'(\D+)')].dropna().values
cpgm=pd.DataFrame(np.column_stack([steps,nopm]),columns=['STEP','No of grievances'])

C1,C2=st.columns(2)
with C1:
    st.markdown("<h3 style='text-align: center; color: gray;'>CM WINDOWS STATUS</h3>", unsafe_allow_html=True)
    st.table(cmpt.style.set_properties(**{'border': '1.3px solid black','color': 'black'}))

with C2:
    st.markdown("<h3 style='text-align: center; color: gray;'>PM WINDOWS STATUS</h3>", unsafe_allow_html=True)
    st.table(cpgm.style.set_properties(**{'border': '1.3px solid black','color': 'black'}))
