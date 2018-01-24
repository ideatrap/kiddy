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
                start_hour  = act['biz_hour'][act['biz_special_date'][date]][0]
                end_hour  = act['biz_hour'][act['biz_special_date'][date]][1]
                if start_hour > end_time or end_hour < start_time:
                    #the activity opens after the end time, or
                    #it ends before the start time
                    #consider as closed
                    df = df.drop(index)
                    continue

    #check public holiday
    #check business day
    #check normal

    return df


def open_activities(act_df, date, time = ""): #list of open activities

    open_act_df_morning = open_act_filter(act_df, date, '8:00','12:00')
    open_act_df_afternoon = open_act_filter(act_df, date,'13:00','18:00')
    open_act_df_evening = open_act_filter(act_df, date, '19:00','22:00')

    act_index_open_morning = [] #list with activity_id
    act_index_open_afternoon = []
    act_index_open =[]


    print(open_act_df_morning)

    '''
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
            #not always open. there is special schedule
            #get the open hour options
            #biz_hour_dic
            #example:  {'A': ['9:30', '17:00'], 'B': ['9:30', '18:00']}
            biz_hour = act["biz_hour"]
            biz_hour_ls = str(biz_hour).split(";")
            biz_hour_dic ={}
            for i in biz_hour_ls:
                hour_start = i.split('-')[1].split('to')[0]
                hour_end = i.split('-')[1].split('to')[1]
                biz_hour_dic[i.split('-')[0]]= [hour_start,hour_end]

            #check


            #get special day schedule:
            special_date = act['biz_special_date']
            special_date_ls = str(special_date).split(";")





            debug = special_date_ls


            #print(debug)

    #check special day
    #check pubic schedule
    #check week day duration

    if time == "": #need to compile morning and afternoon dataframe
        morning_df = act_df[act_df['activity_id'].isin(act_index_open_morning)]
        afternoon_df= act_df[act_df['activity_id'].isin(act_index_open_afternoon)]

        morning_df = tools.reindex(morning_df)
        afternoon_df = tools.reindex(afternoon_df)

        result.append(morning_df)
        result.append(afternoon_df)
    '''
    return [act_df,act_df]
