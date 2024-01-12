import random

# Define a list of questions, correct answers, and incorrect answers
question_bank = [
    {"question": "Koks yra pagrindinis miesto aikštės pastatas?", "correct_answer": "Rotušė", "incorrect_answers": ["Mokykla", "Bažnyčia"]},
    {"question": "Kokia yra Lietuvos sostinė?", "correct_answer": "Vilnius", "incorrect_answers": ["Kaunas", "Klaipėda"]},
    # Add more questions here...
]

# Shuffle the question bank to randomize the order
random.shuffle(question_bank)

# Store the current question index
current_question_index = 0

# def get_current_question():
#     global current_question_index
#     return question_bank[current_question_index]

def next_question():
    global current_question_index
    question = question_bank[current_question_index]
    
    current_question_index += 1

    # If all questions have been asked, reset the index and shuffle the question bank again
    if current_question_index == len(question_bank):
        current_question_index = 0
        random.shuffle(question_bank)
        
    return question
