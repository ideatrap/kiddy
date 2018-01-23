import numpy as np
import datetime
import pandas as pd

def is_PH(date, country): #is it public holiday?
    holidays = pd.read_csv('db/holiday.csv')
    for day in holidays['Date']:
        if date == day:
            return True
    return False


def open_act(act_df, date): #list of open activities
    act_index_open_morning = []
    act_index_open_afternoon = []

    #getting attribute of the date
    str_date = date.split('-')
    date_std = datetime.datetime(int(str_date[0]), int(str_date[1]), int(str_date[2]),8,0,0)
    date_day_of_week = date_std.weekday()+1 # 1 for Monday, 2 for Saturday
    date_PH = is_PH(date, 'SG')


    #start from highest priority

    #iterate through
    for index, act in act_df.iterrows():
        status = 'open'

        time_dic = act['biz_hour']
        if str(time_dic) == 'nan':
            #it always open
            act_index_open_morning.append(index)
            act_index_open_afternoon.append(index)
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


    return act_index_open_morning, act_index_open_afternoon #ls_act_index_open_morning
