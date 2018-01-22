import pandas as pd
import pytz
import datetime
import random

SGT = pytz.timezone('Asia/Singapore')
today = datetime.datetime.now(tz=SGT)

class Card:
    #Compulsary field
    date = None
    child_id = None
    activity_id = None

def get_activities ():
    acitivities = pd.read_csv('db/activity.csv')

    #replacing None in min age to 0, max to be 200
    acitivities['min_age'].fillna(0, inplace = True)
    acitivities['max_age'].fillna(200, inplace = True)
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

def is_PH(date, country):
    holidays = pd.read_csv('db/holiday.csv')
    for day in holidays['Date']:
        if date == day:
            return True

    return False

def reco (activities, child_list, date_list):
    list_card = []
    for date in date_list:
        for child in child_list:

            #Age filter - find all activities that meeting age requirement
            age = cal_age(date, child)
            #age appropriate
            if age == -1: #not considering age constraint
                act_age = activities
            else:
                act_age = activities[(activities.min_age <= age) & (activities.max_age >= age)]
                act_age.reset_index(inplace=True)
                act_age= act_age.drop('index',axis = 1)


            #date filter -- determine whether the activity is open for the day
            ls_act_index_open = []
            str_date = date.split('-')
            date_std = datetime.datetime(int(str_date[0]), int(str_date[1]), int(str_date[2]),8,0,0)
            date_day_of_week = date_std.weekday()+1 # 1 for Monday, 2 for Saturday
            date_PH = is_PH(date, 'SG')




            act_age_date = act_age




            #personalize the activity for the personalize
            #for now. it uses random number
            print('\n ************************')
            print(date_PH)

            length = act_age_date.shape[0]
            activity_index = random.randint(0,length-1)
            activity_id = act_age.get_value(activity_index, 'activity_id')



            card = Card ()
            card.date = date
            card.child_id = child.id
            card.activity_id = activity_id

            list_card.append(card)
    return list_card

def activity_reco (child_list, date_list):
    #read in activity database
    activities = get_activities()
    date_child_act = reco(activities, child_list, date_list)
    return date_child_act
