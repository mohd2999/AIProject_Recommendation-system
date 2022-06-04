import pickle
import pandas as pd
import requests
import streamlit as st

#import the cosine similarity
cos_sim = pickle.load(open("cos_sim.pkl", "rb"))

#import the moive list
moivesl_list = pickle.load(open("moives.pkl", "rb"))
moive_list = moivesl_list["Title"].values
index = pd.DataFrame(moivesl_list)


def fetch_poster(title):
    tmp = ""
    seg = list(title.split(" "))
    for i in range(len(seg)):
        if i == 0:
            tmp += seg[i]
        else:
            tmp += "+" + seg[i]

    resp = requests.get("http://www.omdbapi.com/?t=" + tmp + "&apikey=5a525073")
    data = resp.json()

    return data["Poster"]


def recommend_moive(title):
    movies = []
    moive_poster = []
    # map index with title
    idx = moivesl_list[moivesl_list['Title'] == title].index[0]
    print(idx)
    # calculate similarity cost
    score = pd.Series(cos_sim[idx]).sort_values(ascending = False)
    # top 10 in score
    top10 = list(score.iloc[1:11].index)
    # print(top10)

    # add moive to the list
    for i in top10:
        movies.append(moive_list[i])
        moive_poster.append(fetch_poster(moive_list[i]))
    return movies, moive_poster

#title of the page
st.title("Movie Recommendation System: Content Based")
#movie selection
selectMoive = st.selectbox("Please Select a Moive :", index)
#display the top 5 movies as colomuns
if st.button("Recommend"):
    titlemoive, poster = recommend_moive(selectMoive)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(titlemoive[0])
        st.image(poster[0])

    with col2:
        st.text(titlemoive[1])
        st.image(poster[1])
    with col3:
        st.text(titlemoive[2])
        st.image(poster[2])
    with col4:
        st.text(titlemoive[3])
        st.image(poster[3])
    with col5:
        st.text(titlemoive[4])
        st.image(poster[4])
