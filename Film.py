#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pickle
import streamlit as st
import requests
import numpy as np
import pandas as pd
popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books1.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

split_files = ['part_0.pkl', 'part_1.pkl', 'part_2.pkl', 'part_3.pkl', 'part_4.pkl', 'part_5.pkl', 'part_6.pkl', 'part_7.pkl']  # Add the names of your split files here

# Combine split files
combined_data = []
for file_name in split_files:
    with open(file_name, 'rb') as file:
        chunk = pickle.load(file)
        combined_data.extend(chunk)
  
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

def index():
    return render_template(book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-L'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )


def recommend2(book_name):
    index = np.where(pt.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:5]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))
        
        data.append(item)
    
    return data

st.title('Recommenders by PJ')
st.markdown(""" #### A collaborative filtering based recommender model for providing recommendation of movies and books based on a user preference. """)
activities=["Movie Recommender","Book Recommender"]
option=st.sidebar.selectbox("Select Your Option",activities)
st.subheader(option)

if option=="Movie Recommender":
    # st.header('Movie Recommender System')
    movies = pickle.load(open('movie_list.pkl','rb'))
    similarity = combined_data
#     similarity = pickle.load(open('similarity.pkl','rb'))
    movie_list = movies['title'].values
    selected_movie = st.selectbox("Type or select a movie from the dropdown",movie_list)
    if st.button('Show Recommendation'):
        recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])

        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])
        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])

elif option=="Book Recommender":
    book_list = books['Book-Title'].values
    selected_book = st.selectbox("Type or select a book from the dropdown",book_list)
    if st.button('Show Recommendation'):
        data = recommend2(selected_book)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.text(data[0][0])
            st.image(data[0][2],caption=data[0][1])
        with col2:
            st.text(data[1][0])
            st.image(data[1][2],caption=data[1][1])
        with col3:
            st.text(data[2][0])
            st.image(data[2][2],caption=data[2][1])
        with col4:
            st.text(data[3][0])
            st.image(data[3][2],caption=data[3][1])

# In[ ]:




