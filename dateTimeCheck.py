import numpy as np
import datetime
import pandas as pd
import tools

def is_PH(date, country): #is it public holiday?
    holidays = pd.read_csv('db/holiday.csv')
    for day in holidays['Date']:
        if date == day:
            return True
    return False


def open_act(act_df, date, time = ""): #list of open activities
    act_index_open_morning = []
    act_index_open_afternoon = []
    act_index_open =[]

    #getting attribute of the date
    str_date = date.split('-')
    date_std = datetime.datetime(int(str_date[0]), int(str_date[1]), int(str_date[2]),8,0,0)
    date_day_of_week = date_std.weekday()+1 # 1 for Monday, 2 for Saturday
    date_PH = is_PH(date, 'SG')


    #start from highest priority

    #iterate through
    for index, act in act_df.iterrows():
        status = 'open'
        result = []
        time_dic = act['biz_hour']
        if str(time_dic) == 'nan':
            #it always open
            if time == "":
                act_index_open_morning.append(act_df.iloc[index]['activity_id'])
                act_index_open_afternoon.append(act_df.iloc[index]['activity_id'])
            else:
                print("Error! hasn't start to implement specific time open check")
                print("Error from dateTimeCheck.py")
                exit()
        else:
            special_date = act['biz_special_date']
            #print(special_date)

        '''
        if str(act) == 'nan':
            #potentially open
        else:
        '''

    #check special day
    #check pubic schedule
    #check week day duration

    if time == "": #need to compile morning and afternoon list
        morning_df = act_df[act_df['activity_id'].isin(act_index_open_morning)]
        afternoon_df= act_df[act_df['activity_id'].isin(act_index_open_afternoon)]

        morning_df = tools.reindex(morning_df)
        afternoon_df = tools.reindex(afternoon_df)

        result.append(morning_df)
        result.append(afternoon_df)

    return result
