import os
from typing import Any, Text, Dict, List
import pandas as pd
import csv
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

with open('company.csv', 'r') as file:
    reader = csv.reader(file)
    japack = ' '.join([' '.join(row) for row in reader])

# class CompanyAPI(object):

#     def __init__(self):
#         self.db = pd.read_csv("company.csv")

#     def fetch_restaurants(self):
#         return self.db.head()

#     def format_restaurants(self, df, header=True) -> Text:
#         return df.to_csv(index=False, header=header)


class ChatGPT(object):

    def __init__(self):
        self.url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-3.5-turbo"
        self.headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer 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"
        }
        self.prompt = "Assume that you are representing WDI company where `you` refers to WDI, I will ask you questions based on the following content: " \
            
        self.history = {}

    def ask_company(self, japack, question):
        content  = self.prompt + "\n\n" + japack + "\n\n" + question
        body = {
            "model":self.model, 
            "messages":[{"role": "user", "content": content}]
        }
        try:
            result = requests.post(
                url=self.url,
                headers=self.headers,
                json=body,
            )
            response = result.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error occurred: {e}")
            response = "Sorry, I could not find an answer to your question at this time. Please try again later."

        return response

    def ask_tech(self, question):
        content=question
        body = {
            "model":self.model, 
            "messages":[{"role": "user", "content": content}]
        }
        try:
            result = requests.post(
                url=self.url,
                headers=self.headers,
                json=body,
            )
            
            response = result.json()["choices"][0]["message"]["content"]
            self.history[question] = response
            print("History...",self.history)
        except Exception as e:
            print(f"Error occurred: {e}")
            response = "Sorry, I could not find an answer to your question at this time. Please try again later."
        
        return response

chatGPT = ChatGPT()

class AboutUs(Action):
    def name(self) -> Text:
        return "about_us"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Entered the Run Actions:---->>>>>>>")
        # previous_results = tracker.get_slot("results")
        question = tracker.latest_message["text"]
        print("Questions: ",question)
        answer = chatGPT.ask_company(japack, question)
        print("Answer: ",answer)
        dispatcher.utter_message(text = answer)

class AboutTech(Action):
    def name(self) -> Text:
        return "about_technology"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Entered Technology Run Actions:---->>>>>>>")
        # previous_results = tracker.get_slot("results")
        question = tracker.latest_message["text"]
        print("Questions: ",question)
        read = ["python","flutter","laravel","business","analyst","php", "javaScript", "react.js", "business plan", "react","reactjs","vue","angular","react native","reactnative","wordpress","word press","startup"]
        answers = []
        for keyword in read:
            if keyword in question:
                answer = chatGPT.ask_tech(question)
                answers.append(answer)
        if answers:
            response = "Here's what I found:\n" + "\n".join(answers)
        else:
            response = "Sorry, I don't have any information on that topic."
        print("ANSWER: ", response)
        dispatcher.utter_message(text=response)


