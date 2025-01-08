import csv
import random


def load_questions(filename):
    with open(filename) as file:
        reader = csv.DictReader(file)
        questions = [row for row in reader]
    return questions


def main_game_loop(questions):
    current_level = 1
    lifelines = {'50-50': True, 'swap': True, 'double-back': True}

    while current_level <= 15:
        level_questions = [q for q in questions if int(q['Level']) == current_level]
        current_question = random.choice(level_questions)

        print(f'Level {current_level}: {current_question["Question"]}')
        answers = [current_question['CorrectAnswer'],
                   current_question['IncorrectAnswer1'],
                   current_question['IncorrectAnswer2'],
                   current_question['IncorrectAnswer3']
                   ]
        random.shuffle(answers)

        for i, answer in enumerate(answers, start=1):
            print(f'{i}. {answer}')

        choice = int(input('Choose the correct answer (1-4): '))

        if answers[choice - 1] == current_question['CorrectAnswer']:
            print('Correct! Moving to next level.')
            current_level += 1
        else:
            print('Incorrect! Game Over.')
            break

    if current_level > 15:
        print('Congratulations! You Win!')
    else:
        print('You lose!')


if __name__ == '__main__':
    questions = load_questions('questions.csv')
    main_game_loop(questions)
