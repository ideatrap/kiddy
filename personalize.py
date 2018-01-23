import random
#for now. it uses random number
def personalize (act_df, child):

    length = act_df.shape[0]
    index = random.randint(0,length-1)

    index_ls =[]
    index_ls.append(index)

    df_result = act_df.loc[index_ls] #location must be list
    return df_result
