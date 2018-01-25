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


def open_act_filter (df, date, start_time, end_time):
    #getting attribute of the date
    #date expected to be '2018-01-10'
    #time expected to be '10:00'
    str_date = date.split('-')
    date_std = datetime.datetime(int(str_date[0]), int(str_date[1]), int(str_date[2]),8,0,0)
    date_day_of_week = date_std.weekday()+1 # 1 for Monday, 2 for Saturday
    is_date_PH = is_PH(date, 'SG')


    for index, act in df.iterrows():
    #start from highest priority
    #check special date
        if date in act['biz_special_date'].keys():
            #part of the special day
            if act['biz_special_date'][date] == 'close':
                #the acitivities is closed for the daily
                #go to the next activity
                df = df.drop(index)
                continue
            else:
                hours_ls = act['biz_special_date'][date]
                is_open = "closed"
                for hour in hours_ls:
                    #loop through all possible hours <- for theatre play
                    act_start_hour  = act['biz_hour'][hour][0]
                    act_end_hour  = act['biz_hour'][hour][1]

                    if act_end_hour > start_time and act_start_hour <= end_time:
                        is_open = 'open'
                if is_open == 'closed':
                    df = df.drop(index)
                    continue
                    '''
                    condition for activities closed
                    if act_end_hour < start_time or act_start_hour <= start_time:
                        #the activity opens after the end time, or
                        #it ends before the start time
                        #consider as closed
                        #considered as open as long as it opens one second in the time windo
                    '''

    #check public holiday

        if is_date_PH:
            if str(act['biz_PH_hour']) != 'nan' :
                print(act['biz_PH_hour'])



    #check business day
    #check normal
    #print(df)
    return df


def open_activities(act_df, date, time = ""): #list of open activities

    open_act_df_morning = open_act_filter(act_df, date, '8:00','12:00')
    #open_act_df_afternoon = open_act_filter(act_df, date,'13:00','18:00')

    #print(open_act_df_morning)

    return [open_act_df_morning]
