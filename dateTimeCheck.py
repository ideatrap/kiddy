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

    start_time = tools.standardize_time(start_time)
    end_time = tools.standardize_time(end_time)

    df_output = df
    df_output['opening_hour'] = df_output['biz_date']


    for index, act in df.iterrows():
    #start from highest priority
        status = 'unsure'
        opening_hour = []
        rows_drop = []
        #check special date
        if date in act['biz_special_date'].keys():
            #part of the special day
            if act['biz_special_date'][date] == 'close':
                #the acitivities is closed for the daily
                #go to the next activity
                df_output = df_output.drop(index)
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
                        status = 'open'
                        opening_hour.append([act_start_hour, act_end_hour])
                if is_open == 'closed':
                    df_output = df_output.drop(index)
                    continue
                    '''
                    condition for activities closed
                    if act_end_hour < start_time or act_start_hour <= start_time:
                        #the activity opens after the end time, or
                        #it ends before the start time
                        #consider as closed
                        #considered as open as long as it opens one second in the time windo
                    '''
        if status == 'open':
            #it's open. no need to continue to check
            #append the business hour to the new column
            df_output= df_output.set_value(index, "opening_hour", opening_hour)
            continue

        #check public holiday
        if is_date_PH:
            if str(act['biz_PH_hour']) != 'nan' :
                if act['biz_PH_hour'] == 'close':
                    df_output = df_output.drop(index)
                    continue
                else:
                    hours_ls = act['biz_PH_hour']
                    is_open = "closed"
                    for hour in hours_ls:
                        #loop through all possible hours <- for theatre play
                        act_start_hour  = act['biz_hour'][hour][0]
                        act_end_hour  = act['biz_hour'][hour][1]

                        if act_end_hour > start_time and act_start_hour <= end_time:
                            is_open = 'open'
                            status = 'open'
                            opening_hour.append([act_start_hour, act_end_hour])
                    if is_open == 'closed':
                        df_output = df_output.drop(index)
                        continue

        if status == 'open':
            #it's open. no need to continue to check
            df_output= df_output.set_value(index, "opening_hour", opening_hour)
            continue

        #check business day
        if act['biz_date'] != [] :
            #when there is condition in business date
            act_date_start = act['biz_date'][0]
            act_date_end = act['biz_date'][1]
            if date < act_date_start or date > act_date_end:
                #this is a closed condition. stop searching. otherwise, unsure
                df_output = df_output.drop(index)
                continue

        #check regular schedule
        if act['biz_day_of_week_hour'] != {}:
            hours_ls = act['biz_day_of_week_hour'][str(date_day_of_week)]

            if hours_ls == 'close':
                df_output = df_output.drop(index)
                continue
            else:
                is_open = "closed"
                for hour in hours_ls:
                    #loop through all possible hours <- for theatre play
                    act_start_hour  = act['biz_hour'][hour][0]
                    act_end_hour  = act['biz_hour'][hour][1]

                    if act_end_hour > start_time and act_start_hour <= end_time:
                        is_open = 'open'
                        status = 'open'
                        opening_hour.append([act_start_hour, act_end_hour])
                if is_open == 'closed':
                    df_output = df_output.drop(index)
                    continue

        if status == 'open':
            #it's open. no need to continue to check
            df_output= df_output.set_value(index, "opening_hour", opening_hour)
            continue

        #if there is specific hour
        if act['biz_hour'] != {}:
            act_start_hour = act['biz_hour']['A'][0]
            act_end_hour = act['biz_hour']['A'][1]
            if act_end_hour > start_time and act_start_hour <= end_time:
                status = 'open'
                df_output= df_output.set_value(index, "opening_hour", [[act_start_hour, act_end_hour]])
            else:
                df_output = df_output.drop(index)
                continue
        else:
            #it always open
            status == 'open'
            df_output= df_output.set_value(index, "opening_hour", [['00:00','24:00']])

    df_output = tools.reindex(df_output)
    return df_output


def open_activities(act_df, date, start_time = "", slots = 2): #list of open activities

    if start_time == "" and slots == 2:
        open_act_df_morning = open_act_filter(act_df, date, '8:00','12:00')
        open_act_df_afternoon = open_act_filter(act_df, date,'13:00','18:00')
        return [open_act_df_morning, open_act_df_afternoon]
    elif start_time == "" and slots == 1:
        open_act_df = open_act_filter(act_df, date, '8:00','18:00')
        return [open_act_df]
    else:
        hour = int(start_time.split(":")[0])
        end_time = min(24, hour+1)
        end_time = str(end_time)+":"+start_time.split(":")[1]
        open_act_df_hour = open_act_filter(act_df, date, start_time, end_time)
        return [open_act_df_hour]
