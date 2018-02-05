
import activityReco
import jsonpickle
import json
import pprint

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
        json_card = jsonpickle.encode(card)
        pprint.pprint(json.loads(json_card))
        print('\n')


def card_to_dic(card):
    dic = {}
    dic['child_id'] = card.child_id
    dic['date'] = str(card.date)

    dic['activity_id'] = card.activity_id

    dic['biz_hour'] = {}
    for i in range (len(card.biz_hour)):
        open_str = 'opening_hour_' + str(i)
        close_str = 'closing_hour_' + str(i)
        dic['biz_hour'][open_str] = card.biz_hour[i][0]
        dic['biz_hour'][close_str] = card.biz_hour[i][1]

    dic['time'] = card.time
    dic['activity_name'] = card.activity_name



    return dic

def main():
    child_list = []

    child_list = initialize_child()
    date = activityReco.next_sat()
    #result = activityReco.activity_reco(child_list,date_list, '01:00')
    cards = activityReco.activity_reco(child_list,date, '')

    result = []
    for card in cards:
        result.append(card_to_dic(card))

    return result

if __name__ == "__main__":
    cards = main()
    print_cards(cards)
    #print(cards)
