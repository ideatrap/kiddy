import random
#for now. it uses random number
def personalize (act_df, child, num):
    index_ls =[]

    '''
        randomly select two activities

    '''
    length = act_df.shape[0]
    for i in range (num):
        index = random.randint(0,length-1)
        index_ls.append(index)
        i = i +1
    df_result = act_df.loc[index_ls] #location must be list
    return df_result
