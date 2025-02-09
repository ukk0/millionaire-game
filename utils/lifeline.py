from typing import Dict
import random

class Lifeline:

    @staticmethod
    def assign_difficulty_based_percentages(answers_dict, correct_answer, difficulty):
        base_percentages = {
            'easy': random.randint(60, 90),
            'medium': random.randint(40, 60),
            'hard': random.randint(25, 40)
        }
        correct_percentage = base_percentages[difficulty]
        remaining_percentage = 100 - correct_percentage
        wrong_answers = [key for key in answers_dict.keys() if key != correct_answer]

        assigned = []
        for _ in range(len(wrong_answers) - 1):
            max_value = remaining_percentage - sum(assigned)
            value = random.randint(0, max_value)
            assigned.append(value)

        assigned.append(remaining_percentage - sum(assigned))
        random.shuffle(assigned)
        results = {key: 0 for key in answers_dict.keys()}
        results[correct_answer] = correct_percentage
        for i, key in enumerate(wrong_answers):
            results[key] = assigned[i]

        return results

    @staticmethod
    def fifty_fifty(answers_dict, correct_answer) -> Dict:
        incorrect_options = [key for key, value in answers_dict.items() if key != correct_answer]
        to_remove = random.sample(incorrect_options, 2)
        reduced_answers_dict = {
            key: value for key, value in answers_dict.items() if key not in to_remove
        }
        return reduced_answers_dict

    @staticmethod
    def ask_audience(answers_dict, correct_answer, difficulty):
        results = Lifeline.assign_difficulty_based_percentages(answers_dict, correct_answer, difficulty)
        print("Here are the audience votes:")
        for key, value in results.items():
            print(f"{key}: {value}%")

    @staticmethod
    def call_friend(answers_dict, correct_answer, difficulty):
        results = Lifeline.assign_difficulty_based_percentages(answers_dict, correct_answer, difficulty)
        friend_response = max(results, key=results.get)
        if difficulty == "easy":
            print(f"I'm quite confident it's {friend_response}.")
        elif difficulty == "medium":
            print(f"Hmm, I would probably say {friend_response}.")
        else:
            print(f"It could be {friend_response}, but I'm not entirely sure.")