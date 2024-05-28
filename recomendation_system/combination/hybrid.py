import pandas as pd


def get_phase_one():
    return pd.read_csv("./movies.csv")
def get_phase_two():
    return pd.read_csv("./phase_2.csv")
def get_best():
    ph1=get_phase_one()
    ph2=get_phase_two()
    movies=ph1['anime_id']
    ph2=ph2[movies]
    ph2.sort_values(by=[0], ascending=False, inplace=True)
    print(ph2.head(10))
