import random
import json
questions_file = "questions.json"

f = open(questions_file)
categories = json.load(f)

# Store the current question index and category
current_question_index = {category: 0 for category in categories}
current_category = list(categories.keys())[0]

def next_question(category=None):
    global current_question_index, current_category

    if category:
        current_category = category

    # Retrieve the questions for the current category
    category_questions = categories[current_category]

    # Get the next question
    question = category_questions[current_question_index[current_category]]

    current_question_index[current_category] += 1

    # If all questions have been asked, reset the index
    if current_question_index[current_category] == len(category_questions):
        current_question_index[current_category] = 0

    return question