
import activityReco


class Child:
    #Compulsory field
    id = None

    #Optional Fields
    birth_year = None
    birth_month = None
    birth_day = None
    age_input = None
    name = None


def initialize_child():
    child = Child ()
    child.id = 1
    child.name = 'Trump'
    child.age_input = 2
    child_list = []
    child_list.append(child)

    return child_list

def print_cards(cards):
    for card in cards:
        print("\nDate: ", card.date, " ", card.half_day)
        #print("Child ID: ", card.child_id)
        #print("Activity ID: ", card.activity_id)
        print(" ----   ", card.activity_name)
        print("Opening hour: ", card.biz_hour)


'''
 -------   Execution   --------
'''
child_list = []
date_list = []

child_list = initialize_child()
date_list = activityReco.next_sat()
#result = activityReco.activity_reco(child_list,date_list, '01:00')
result = activityReco.activity_reco(child_list,date_list, '')

print_cards(result)
