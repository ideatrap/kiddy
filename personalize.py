import random
#for now. it uses random number
def personalize (act_df, child):
    length = act_df.shape[0]
    activity_index = random.randint(0,length-1)
    activity_id = act_df.get_value(activity_index, 'activity_id')
    return activity_id
