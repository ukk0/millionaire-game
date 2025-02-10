from utils.helpers import *

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