import pandas as pd
import pytz
import datetime
import dateTimeCheck
import personalize

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



def reco (activities, child_list, date_list, time = ""):
    list_card = []
    list_card_morning = []
    list_card_afternoon = []

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


            #check whether it opens
            #get the list of activities that open
            act_age_date = act_age
            test1, test2 = dateTimeCheck.open_act(act_age, date)

            #personalize the activity for the personalize

            print('\n ************************')
            print(test1, test2)

            activity_id = personalize.personalize(act_age_date, child)

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
