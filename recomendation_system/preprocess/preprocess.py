from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd


def get_anime():
    df=pd.read_csv("../anime.csv")
    return df

def get_rating():
    df=pd.read_csv("../rating.csv")
    return df
def get_anime_rating(x,all):
    all[x['anime_id']] = x['rating']
    return all
def rating_anime_user_group():
    rating = get_rating()
    grouped =rating.groupby('user_id')
    user_dict={}
    for name,group  in grouped:
        group:pd.DataFrame
        all={}
        group.apply(lambda x:get_anime_rating(x,all),axis=1)
        user_dict[name]=all
    return user_dict
def get_rating_anime(input):
    print("start thread")
    column,rating,data =input
    anime_rating = rating[rating['anime_id'] == column]
    joined = data.join(anime_rating, how='outer')
    print("data joined")
    return {column : joined['rating']}

def get_anime_rating_data_frame():
    anime = get_anime()
    user_dict=rating_anime_user_group()
    index=list(user_dict.keys())
    columns={}
    for anime in anime['anime_id'].unique():
        columns[anime]=np.full([1,len(index)],np.NAN).tolist()[0]
    counter=0
    for user,value in user_dict.items():
        for key,rating in value.items():
            try:
                columns[key][counter]=rating
            except:
                pass
        counter+=1
    user_data=pd.DataFrame(columns,index=index)
    user_data.to_csv("data.csv")

def filter_data(x,anime_rating):
    try:
        anime_user = anime_rating[anime_rating['user_id'] == x['user_id']]
    except:
        return None

    if len(anime_user['rating'])==0:
        return None
    else:
        m=list(anime_user['rating'])[0]
        print(m)
        return m

# get_anime_rating_data_frame()


# rating_anime_user_group()





