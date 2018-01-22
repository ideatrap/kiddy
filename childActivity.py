
import activityReco as AR


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

def print_result(ls):
    print('\n ======== Result is =============')
    for card in ls:
        print("Date: ", card.date)
        print("Child ID: ", card.child_id)
        print("Activity ID: ", card.activity_id)
        print('\n')


'''
 -------   Execution   --------
'''
child_list = []
date_list = []

child_list = initialize_child()
date_list = AR.next_sat()
result = AR.activity_reco(child_list,date_list)


print_result(result)
