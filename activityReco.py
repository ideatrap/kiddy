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
    acitivities = tools.parse_date_time(acitivities)
    return acitivities
#find the next Tue in Singapore time
def next_sat():
    today_str = '{:%Y-%m-%d}'.format(today)

    #TODO needs to get full code for next Tue. here it's hard coded

    next_sat = '2018-01-27'

    date_list = []
    date_list.append(today_str)
    date_list.append(next_sat)

    return date_list

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




def reco (activities, child_list, date_list, time = ""):
    cards = []

    for date in date_list:
        for child in child_list:

            #Age filter - find all activities that meeting age requirement
            age = cal_age(date, child)
            #age appropriate
            if age == -1: #not considering age constraint
                act_age = activities
            else:
                act_age = activities[(activities.min_age <= age) & (activities.max_age >= age)]
                act_age = tools.reindex(act_age)

            #get the list of activities that open
            act_date_df_ls = dateTimeCheck.open_activities(act_age, date)

            #personalize the activity based on personal activity record
            i = 0
            for act_df in act_date_df_ls: #iterate through morning and afternoon session
                act_result_df = personalize.personalize(act_df, child)
                for index, act in act_result_df.iterrows():
                    card = card_class.Card ()
                    card.date = date
                    card.child_id = child.id
                    card.activity_id = act['activity_id']
                    card.activity_name = act['name']
                    if i == 0 and len(act_date_df_ls) == 2:
                        card.half_day = 'Morning'
                    elif i == 1 and len(act_date_df_ls) == 2:
                        card.half_day = 'Afternoon'
                    else:
                        card.half_day = 'Time: '+ time
                    cards.append(card)
                i = 1+i

    return cards

def activity_reco (child_list, date_list):
    #read in activity database
    activities = get_activities()
    reco_act = reco(activities, child_list, date_list)
    return reco_act
