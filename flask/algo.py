import json
from MongoDB.question import question
from MongoDB.userAns import userAns
from MongoDB.ml import ml
from test_questions import Sample
import random
import numpy as np


mlTable = ml()


roles = []

def loadRoles():
    x = mlTable.get()
    
    for weights in x:
        roles.append(weights)

loadRoles()

# characters = [
#     {'name': 'Homer Simpson',         'answers': {1: 1, 2: 1, 3: 1, 4: 0}},
#     {'name': 'SpongeBob SquarePants', 'answers': {1: 1, 2: 1, 3: 1, 4: 0.75}},
#     {'name': 'Sandy Cheeks',          'answers': {1: 0, 2: 0, 3: 0}},
# ]
# print(characters["name"])

questions = {
    1: 'Is your character yellow?',
    2: 'Is your character bald?',
    3: 'Is your character a man?',
    4: 'Is your character short?',
}

questions_so_far = []
answers_so_far = []


def calculate_probabilites(questions_so_far, answers_so_far):
    probabilities = []
    for role in roles:
        probabilities.append({
            'name': role['role'], #edited
            'probability': calculate_character_probability(role, questions_so_far, answers_so_far)
        })

    return probabilities

def calculate_character_probability(role, questions_so_far, answers_so_far):
    # Prior
    P_character = 1 / len(roles)

    # Likelihood
    P_answers_given_character = 1
    P_answers_given_not_character = 1
    for question, answer in zip(questions_so_far, answers_so_far):
        P_answers_given_character *= max(
            1 - abs(answer - character_answer(role, question)), 0.01)

        P_answer_not_character = np.mean([1 - abs(answer - character_answer(not_role, question))
                                          for not_role in role
                                          if not_role['role'] != role['role']])
        P_answers_given_not_character *= max(P_answer_not_character, 0.01)

    # Evidence
    P_answers = P_character * P_answers_given_character + \
        (1 - P_character) * P_answers_given_not_character

    # Bayes Theorem
    P_character_given_answers = (
        P_answers_given_character * P_character) / P_answers

    return P_character_given_answers


def character_answer(role, question):
    if str(question) in role['answer']:
        return role['answer'][str(question)]["weight"]
    return 0.5

def index():
    global questions_so_far, answers_so_far

    question = request.args.get('question')
    answer = request.args.get('answer')
    if question and answer:
        questions_so_far.append(int(question))
        answers_so_far.append(float(answer))

    probabilities = calculate_probabilites(questions_so_far, answers_so_far)

    questions_left = list(set(questions.keys()) - set(questions_so_far))
    print(questions_left)
    if len(questions_left) == 0:
        result = sorted(
            probabilities, key=lambda p: p['probability'], reverse=True)[0]
        print(answers_so_far)
        print(result)
        #if yes update db
        #return render_template('index.html', result=result['name'])
    else:
        next_question = random.choice(questions_left)
        #return render_template('index.html', question=next_question, question_text=questions[next_question])

#



def getNextQuestionOrCareer(questions_left, questions_so_far, answers_so_far):
    probabilities = calculate_probabilites(questions_so_far, answers_so_far)

    if len(questions_left) == 0:
        result = sorted(
            probabilities, key=lambda p: p['probability'], reverse=True)[0]
        return result["role"]
    else:
        next_question = random.choice(questions_left)
        return next_question
