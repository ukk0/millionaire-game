import requests

REQUEST_URL = "https://the-trivia-api.com/v2/questions"

def return_questions(difficulty: str = None):
    payload = {"difficulties": difficulty}
    return requests.get(url=REQUEST_URL, params=payload).json()
