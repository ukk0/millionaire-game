from utils.trivia_api import return_questions

class Player:

    wants_to_play = True
    no_wrong_answer = True
    fifty_fifty_available = True
    call_friend_available = True
    ask_audience_available = True
    questions_answered = 0
    current_winnings = 0

    def __init__(self, player_name: str):
        self.player_name = player_name
        self.easy_questions = return_questions(difficulty="easy")
        self.medium_questions = return_questions(difficulty="medium")
        self.hard_questions = return_questions(difficulty="hard")
