import random

# Define a dictionary of categories, each containing a list of questions
categories = {
    "Category 1": [
        {"question": "Question 1.1", "correct_answer": "Correct 1.1", "incorrect_answers": ["Incorrect 1.1", "Incorrect 1.2"]},
        {"question": "Question 1.2", "correct_answer": "Correct 1.2", "incorrect_answers": ["Incorrect 1.1", "Incorrect 1.2"]},
        # Add more questions for Category 1...
    ],
    "Category 2": [
        {"question": "Question 2.1", "correct_answer": "Correct 2.1", "incorrect_answers": ["Incorrect 2.1", "Incorrect 2.2"]},
        {"question": "Question 2.2", "correct_answer": "Correct 2.2", "incorrect_answers": ["Incorrect 2.1", "Incorrect 2.2"]},
        # Add more questions for Category 2...
    ],
    "Category 3": [
        {"question": "Question 3.1", "correct_answer": "Correct 3.1", "incorrect_answers": ["Incorrect 3.1", "Incorrect 3.2"]},
        {"question": "Question 3.2", "correct_answer": "Correct 3.2", "incorrect_answers": ["Incorrect 3.1", "Incorrect 3.2"]},
        # Add more questions for Category 3...
    ],
}

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