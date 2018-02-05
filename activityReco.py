import pandas as pd
import pytz
import datetime
import dateTimeCheck
import personalize
import tools
import card_class

SGT = pytz.timezone('Asia/Singapore')
today = datetime.datetime.now(tz=SGT)



def get_activities ():
    acitivities = pd.read_csv('db/activity.csv')

    #replacing None in min age to 0, max to be 200
    acitivities['min_age'].fillna(0, inplace = True)
    acitivities['max_age'].fillna(200, inplace = True)

    #TODO potentially convert all text to lower case to avoid input error

    acitivities = tools.parse_date_time(acitivities)

    return acitivities
#find the next Tue in Singapore time
def next_sat():
    today_str = '{:%Y-%m-%d}'.format(today)

    #TODO needs to get full code for next Tue. here it's hard coded

    next_sat = '2018-01-27'

    return today_str

#calculate kids' age till today
def cal_age(date, child):
    if child.age_input != None:
        return child.age_input
    elif child.birth_year == None:
        return -1 #most flexible scenario
    else:
        year = child.birth_year
        return -1
def list_to_dataFrame (ls, df):
    #new_df =
#    for i in ls:
    pass




def reco (activities, child_list, date, time = "", num_act=1):
    cards = []
    result = {}
    result['date'] = date
    result['activities'] = []

    for child in child_list:
        result['child_id'] = child.id
        #Age filter - find all activities that meeting age requirement
        age = cal_age(date, child)
        #age appropriate
        if age == -1: #not considering age constraint
            act_age = activities
        else:
            act_age = activities[(activities.min_age <= age) & (activities.max_age >= age)]
            act_age = tools.reindex(act_age)

        #get the list of activities that open
        act_date_df_ls = dateTimeCheck.open_activities(act_age, date, time)

        #personalize the activity based on personal activity record
        i = 0
        for act_df in act_date_df_ls: #iterate through morning and afternoon session
            act_result_df = personalize.personalize(act_df, child, num_act)
            for index, act in act_result_df.iterrows():
                result['activities'].append({})
                result['activities'][i]['activity_id'] = act['activity_id']
                result['activities'][i]['biz_hour'] = []
                for j in range (len(act['opening_hour'])):
                    open_str = 'opening_hour_' + str(j)
                    close_str = 'closing_hour_' + str(j)
                    result['activities'][i]['biz_hour'].append({open_str:act['opening_hour'][0][0]})
                    result['activities'][i]['biz_hour'].append({close_str:act['opening_hour'][0][1]})
                result['activities'][i]['activity_name'] = act['name']
                if i%2 == 0 and len(act_date_df_ls) == 2:
                    result['activities'][i]['time'] = 'Morning'
                elif i%2 == 1 and len(act_date_df_ls) == 2:
                    result['activities'][i]['time'] ='Afternoon'
                else:
                    result['activities'][i]['time'] = time
                i = 1+i
    #return cards
    return result

def activity_reco (child_list, date, time="", num_act =1):
    #read in activity database
    activities = get_activities()
    reco_act = reco(activities, child_list, date, time, num_act)
    return reco_act
