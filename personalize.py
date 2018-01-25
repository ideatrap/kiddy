import random
#for now. it uses random number
def personalize (act_df, child):
    index_ls =[]

    '''
        randomly select two activities

    '''
    num = 1 #number of activities to recommend
    length = act_df.shape[0]
    print('length:', length)
    for i in range (num):
        index = random.randint(0,length-1)
        index_ls.append(index)
        i = i +1
    print('index_ls:', index_ls)
    df_result = act_df.loc[index_ls] #location must be list
    return df_result
