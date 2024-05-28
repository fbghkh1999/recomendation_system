import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler

from preprocess.preprocess import get_anime, get_rating



def get_genres(df):
    genres = {}
    for genre in df['genre']:
        try:
            genre = genre.split(", ")
            for g in genre:
                try:
                    genres[g]+=1
                except:
                    genres[g]=1
        except:
            pass
    return list(genres.keys())

def get_features():
    df = get_anime()

    genres=get_genres(df)
    features:list=[]
    features.extend(genres)
    features.append('type')
    features.append('episodes')
    features.append('rating')
    features.append('members')
    return features,genres
def get_feature_genre(genres,x):
    if x is np.NAN:
        return None
    x_genre=x.split(", ")
    x_genre_vector=[]
    for genre in genres:
        if genre in x_genre:
            x_genre_vector.append(1)
        else:
            x_genre_vector.append(0)
    return x_genre_vector

def create_feature_vector():
    headers,genres=get_features()
    anime = get_anime()
    anime.replace('Unknown', np.NAN, inplace=True)
    anime.dropna(inplace=True)
    cleanup_nums = {'type': {"Movie": 1, "TV": 2,'Special':3,'Music':4,'ONA':5,'OVA':6}}
    df=pd.DataFrame(columns=headers,index=anime['anime_id'])
    anime.replace(cleanup_nums, inplace=True)
    df['type']=anime['type']
    df['members'] = anime['members']
    df['rating'] = anime['rating']
    df['episodes']=anime['episodes']
    num_cols = ['members', 'rating', 'episodes']

    # apply standardization on numerical features
    for i in num_cols:
        scale = StandardScaler().fit(df[[i]])
        # transform the training data column
        df[i] = scale.transform(df[[i]])
    anime['genre']=anime.apply(lambda x:get_feature_genre(genres,x['genre']),axis=1)
    for i,j in enumerate(genres):
        df[j]=anime.apply(lambda x:x['genre'][i] if x['genre'] is not None else None,axis=1)
    df.dropna(inplace=True)
    df.to_csv("feature_vector.csv")

create_feature_vector()