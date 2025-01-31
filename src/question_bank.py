import json

QUESTIONS_FILE = "questions.json"

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
