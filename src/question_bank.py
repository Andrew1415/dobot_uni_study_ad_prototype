import json
import os
import logging

QUESTIONS_FILE = "questions.json"
STATISTICS_FILE = "statistics.json"

def read_categories(file_name) -> dict:
    with open(file_name) as f:
        return json.load(f)

categories = read_categories(QUESTIONS_FILE)

# Index questions in categories
questions_index = {category: 0 for category in categories}

def next_question(category):
    global current_question_index

    # Retrieve the questions for the current category
    questions = categories[category]

    # Get the next question
    question = questions[questions_index[category]]

    # Move index to the next question
    questions_index[category] += 1

    # If all questions have been asked, reset the index
    if questions_index[category] == len(questions):
        questions_index[category] = 0

    return question

def update_statistics(category):
    if os.path.exists(STATISTICS_FILE):
        with open(STATISTICS_FILE, "r") as f:
            statistics = json.load(f)
    else:
        statistics = {category: 0 for category in categories.keys()}
    
    statistics[category] += 1
    logging.info(f'Answered category {category} {statistics[category]} times')
    
    
    with open(STATISTICS_FILE, "w") as f:
        json.dump(statistics, f, indent=4)
