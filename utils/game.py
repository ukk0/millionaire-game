from utils.player import Player
from utils.lifeline import Lifeline
import sys
import random


game_rules = ("Answer 15 multiple-choice questions to win the top prize.\n "
              "Questions will get harder as you progress.\n "
              "You can walk away anytime with your winnings, but a wrong answer\n "
              "drops you to the last safe tier.\n"

              "Lifelines: \n"
              "- '50:50' removes 2 wrong options,\n"
              "- 'Ask the Audience' shows preferences and\n"
              "- 'Phone a friend' gives simulated help.\n"
              "Good luck!\n\n")


prize_tiers = {
    1: 100,
    2: 200,
    3: 300,
    4: 500,
    5: 1000,
    6: 2000,
    7: 4000,
    8: 8000,
    9: 16000,
    10: 32000,
    11: 64000,
    12: 125000,
    13: 250000,
    14: 500000,
    15: 1000000
}


def create_player():
    player_name = None
    while not player_name:
        player_name = input("What is you name?")
        if player_name:
            print(f"Welcome to the game {player_name}.")
            return Player(player_name)


def get_next_question(player_obj):
    if player_obj.questions_answered <= 5:
        questions = player_obj.easy_questions
    elif 5 < player_obj.questions_answered <= 10:
        questions = player_obj.medium_questions
    else:
        questions = player_obj.hard_questions
    return questions.pop()


def check_win_amount(player_obj):
    if not player_obj.wants_to_play:
        return prize_tiers[player_obj.questions_answered]
    elif 5 <= player_obj.questions_answered < 10 and not player_obj.no_wrong_answer:
        return prize_tiers[5]
    elif 10 <= player_obj.questions_answered < 15 and not player_obj.no_wrong_answer:
        return prize_tiers[10]
    else:
        return 0


def print_out_question(question_obj, answers_dict=None):
    print((question_obj["question"]["text"]))
    correct_answer = [question_obj["correctAnswer"]]
    if not answers_dict:
        wrong_answers = question_obj["incorrectAnswers"]
        all_answers = wrong_answers + correct_answer
        answers_dict = {
            "A": all_answers.pop(random.randint(0,len(all_answers)-1)),
            "B": all_answers.pop(random.randint(0,len(all_answers)-1)),
            "C": all_answers.pop(random.randint(0,len(all_answers)-1)),
            "D": all_answers.pop(random.randint(0,len(all_answers)-1))
        }
    correct_answer_key = [key for key, value in answers_dict.items() if value == correct_answer[0]]
    rows = [
        f"{key}: {value}" for key, value in answers_dict.items()
    ]
    for row in rows:
        print(row)
    print("\n")
    return answers_dict, correct_answer_key[0]


def print_out_lifelines(player_obj):
    if player_obj.fifty_fifty_available:
        print("1: 50/50")
    if player_obj.ask_audience_available:
        print("2: Ask the audience")
    if player_obj.call_friend_available:
        print("3: Phone a friend")


def handle_quitting(player_obj):
    print(f"Your game has ended and you are going home with ${player_obj.current_winnings}. Thanks for playing!")
    sys.exit()


def handle_lifeline(response, player_obj, answers_dict, question_obj, correct_answer):
    if response == "1" and player_obj.fifty_fifty_available:
        reduced_answers = Lifeline.fifty_fifty(answers_dict, correct_answer)
        answers_dict, _ = print_out_question(question_obj, reduced_answers)
        player_obj.fifty_fifty_available = False

    elif response == "2" and player_obj.ask_audience_available:
        difficulty = question_obj["difficulty"]
        Lifeline.ask_audience(answers_dict, correct_answer, difficulty)
        player_obj.ask_audience_available = False

    elif response == "3" and player_obj.call_friend_available:
        difficulty = question_obj["difficulty"]
        Lifeline.call_friend(answers_dict, correct_answer, difficulty)
        player_obj.call_friend_available = False

    else:
        print("You've already used that lifeline!")

    return answers_dict


def process_response(response, player_obj, answers_dict, question_obj):
    if response.upper() in list(answers_dict.keys()):
        if answers_dict[response.upper()] == question_obj["correctAnswer"]:
            player_obj.questions_answered += 1
            player_obj.current_winnings = prize_tiers[player_obj.questions_answered]
            print(f"Congratulations, that's correct! You have won ${player_obj.current_winnings}!\n\n")

            if player_obj.questions_answered == 15:
                print("That's the end of the game. Thanks for playing!")
                return "GAME_OVER"
            return "CORRECT"

        else:
            player_obj.no_wrong_answer = False
            win_amount = check_win_amount(player_obj)
            print(f"That's incorrect. Your game has ended. You have won ${win_amount}")
            print(f"The correct answer would've been {question_obj['correctAnswer']}.")
            return "GAME_OVER"

    elif response.upper() == "Q":
        handle_quitting(player_obj)

    elif response in ["1", "2", "3"]:
        return "USE_LIFELINE"

    else:
        return "INVALID"


def ask_next_question(player_obj):
    question_obj = get_next_question(player_obj)
    print(
        f"Question number {player_obj.questions_answered + 1}, "
        f"it is worth ${prize_tiers[player_obj.questions_answered + 1]}\n\n"
    )
    answers_dict, correct_answer = print_out_question(question_obj)
    print_out_lifelines(player_obj)

    while True:
        response = input(
            "\nPlease provide your answer A/B/C/D or 1/2/3 to use a lifeline. Press Q to quit here.\n")
        action = process_response(response, player_obj, answers_dict, question_obj)

        if action == "CORRECT":
            break
        elif action == "GAME_OVER":
            break
        elif action == "USE_LIFELINE":
            answers_dict = handle_lifeline(response, player_obj, answers_dict, question_obj, correct_answer)
        elif action == "INVALID":
            continue


def run_game():
    while True:
        response = input(
            "Welcome to 'Who wants to be a millionaire'!\nDo you want to be a millionaire? (Y/N)"
        )
        if response.upper() in ["Y", "YES"]:
            player_obj = create_player()
            break
        if response.upper() in ["N", "NO"]:
            sys.exit()
        else:
            print("Please provide a valid response.")
    print(game_rules)

    while player_obj.wants_to_play and player_obj.no_wrong_answer and player_obj.questions_answered < 15:
        ask_next_question(player_obj)


if __name__ == "__main__":
    run_game()
