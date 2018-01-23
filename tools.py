def reindex (df):
    df.reset_index(inplace=True)
    return df.drop('index',axis = 1)
