
def reindex (df):
    df.reset_index(inplace=True)
    return df.drop('index',axis = 1)

def standardize_time(time):
    if ':' not in time:
        time = time+':00'
    hour = time.split(':')[0]
    minute = time.split(':')[1]
    if len(hour) == 1:
        return '0'+time
    else:
        return time


def parse_date_time(df):
    for index, act in df.iterrows():
        #parse the biz_hour
        biz_hour = act["biz_hour"]
        biz_hour_ls = str(biz_hour).split(";")
        biz_hour_dic ={}
        if biz_hour_ls != ['nan']:
            for i in biz_hour_ls:
                hour_start = i.split('-')[1].split('to')[0]
                hour_end = i.split('-')[1].split('to')[1]
                hour_start = standardize_time(hour_start)
                hour_end = standardize_time(hour_end)
                biz_hour_dic[i.split('-')[0]]= [hour_start,hour_end]
        df= df.set_value(index, "biz_hour", biz_hour_dic)

        #parse the daily schedule
        biz_day = act['biz_day_of_week_hour']
        biz_day_ls = str(biz_day).split(";")
        biz_day_dic = {}
        if biz_day_ls != ['nan']:
            for i in biz_day_ls:
                biz_day_dic[i.split('-')[0]]= i.split('-')[1]
        df= df.set_value(index, "biz_day_of_week_hour", biz_day_dic)

        #parse the business dates for events
        #biz_date
        biz_date = act['biz_date']
        biz_date_ls = str(biz_date).split("to")
        if biz_date_ls == ['nan']: biz_date_ls = []
        df= df.set_value(index, "biz_date", biz_date_ls)

        #parse biz_special_date

        biz_special = act['biz_special_date']
        biz_special_ls = str(biz_special).split(";")
        biz_special_dic = {}
        if biz_special_ls != ['nan']:
            for i in biz_special_ls:
                biz_special_dic[i.split(':')[0]]= i.split(':')[1]
        df= df.set_value(index, "biz_special_date", biz_special_dic)

    return df
