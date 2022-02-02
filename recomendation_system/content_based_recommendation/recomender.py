import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from preprocess.preprocess import get_rating


def get_user(user_id,rating):
    x=rating[rating['user_id']==user_id]
    return x

def get_group_rating(all_users_rating,similarity):
    new_dict={'anime_id':[],'rating':[]}
    m=all_users_rating.groupby('anime_id')
    for name,group in m:
        group:pd.DataFrame
        new_dict['anime_id'].append(name)
        x=group.apply(lambda x:similarity[similarity['user_id']]['similarity']*x['rating'],axis=1)
        r=sum(x)
        new_dict['rating']=r
    return pd.DataFrame(new_dict)



def get_taring_set(user_id,users=None):
    rating=get_rating()
    m=pd.read_csv("../preprocess/feature_vector.csv")
    x=get_user(user_id,rating)
    anime_ids=set(x['anime_id'])
    if users is not None:
        similarity=users
        users=users['user_id']
        user_ratings=[]
        for user in users:
            user_anime_rating = get_user(user, rating)
            anime_ids.update(user_anime_rating)
            user_ratings.append(user_anime_rating)
        all_users_rating=pd.concat(user_ratings)
        get_group_rating(all_users_rating,similarity)
    clf=RandomForestRegressor()
    x_train=m[m.anime_id.isin(list(anime_ids))]
    y=pd.merge(x_train,x,on='anime_id',how='outer')
    x_train.drop(columns="anime_id",inplace=True)
    clf.fit(x_train,y['rating_y'])
    x_test=m[~m['anime_id'].isin(x['anime_id'])]
    anime_ids=x_test['anime_id']
    x_test.drop(columns="anime_id", inplace=True)
    y=clf.predict(x_test)
    result=pd.DataFrame({"anime_id":anime_ids,'label':y})
    result=result.sort_values('label')
    return result[-10:]

print(get_taring_set(1))

