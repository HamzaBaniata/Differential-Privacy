import random
import string
from os import name, system

number_of_voters = 10000
probability = 0.25
candidate_to_be_changed = 'x'
candidate_not_to_be_changed = 'y'
candidate = ['x', 'y']
list_of_voters = set()
list_of_voters_who_voted = []
dict_of_votes = {'x': {"voters": [],
                       "Total_num_of_votes": 0},
                 'y': {"voters": [],
                       "Total_num_of_votes": 0}}

actual_number_of_votes_for_x = 0


def differentially_private_vote_generator(this_candidate):
    if this_candidate == candidate_to_be_changed:
        print("the vote might be changed!")
        p = random.random()
        print("The generated probability = " + str(p))
        global actual_number_of_votes_for_x
        actual_number_of_votes_for_x += 1
        if p <= probability:
            print('the vote has been changed')
            return candidate_not_to_be_changed
        else:
            print('the vote has NOT been changed')
    return this_candidate


def vote(voter, this_candidate):
    new_vote = differentially_private_vote_generator(this_candidate)
    if voter not in list_of_voters_who_voted:
        if new_vote in dict_of_votes:
            list_of_voters_who_voted.append(voter)
            dict_of_votes[new_vote]["voters"].append(voter)
            dict_of_votes[new_vote]["Total_num_of_votes"] += 1


def calculate_all_true_votes():
    total_number_of_votes_for_x = (4 * dict_of_votes[candidate_to_be_changed]["Total_num_of_votes"] - 1)/2
    dict_of_votes[candidate_to_be_changed]["total_num_of_votes+lost"] = actual_number_of_votes_for_x
    dict_of_votes[candidate_not_to_be_changed]["total_num_of_votes+lost"] = (
            dict_of_votes[candidate_not_to_be_changed]["Total_num_of_votes"] -
            (dict_of_votes[candidate_to_be_changed]["total_num_of_votes+lost"] -
             dict_of_votes[candidate_to_be_changed]["Total_num_of_votes"]))


def clear():
    try:
        # for windows
        if name == 'nt':
            _ = system('cls')
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')
    except Exception as e:
        pass


def test_method():
    for i in range(number_of_voters):
        list_of_voters.add(''.join(random.choices(string.ascii_uppercase + string.digits, k=10)))
    for voter in list_of_voters:
        this_candidate = random.choice(list(dict_of_votes.keys()))
        print("Voter: " + voter + " originally voted for " + this_candidate)
        vote(voter, this_candidate)
        clear()


test_method()
# print(dict_of_votes)


def publish_final_results():
    calculate_all_true_votes()
    print('lost number of votes from ' + candidate_to_be_changed + " = " +
          str(actual_number_of_votes_for_x - dict_of_votes[candidate_to_be_changed]["Total_num_of_votes"]))
    # print(dict_of_votes)
    print("number of votes that ideally had to be lost according to the defined probability = " +
          str(int(probability * actual_number_of_votes_for_x)))
    print('Actual Number of votes for this candidate = ' + str(actual_number_of_votes_for_x))
    print('Differentially private number of votes for this candidate = ' +
          str(dict_of_votes[candidate_to_be_changed]["Total_num_of_votes"]))


publish_final_results()
