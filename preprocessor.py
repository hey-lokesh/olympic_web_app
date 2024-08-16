import pandas as pd
def preprocess(df,region_df):
    df = df[df['Season'] == 'Summer']
    df = df.merge(region_df, on='NOC', how='left')
    df = pd.concat([df, pd.get_dummies(df['Medal']).astype(int)], axis=1)
    return df
def preprocess2(df,region_df):
    df = df[df['Season'] == 'Summer']
    df = df.merge(region_df, on='NOC', how='left')
    return df

