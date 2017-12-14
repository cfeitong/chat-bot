"""
In this file I decide to rewrite the entry of the chatbot, and it has following steps:
S1. Extract the entities and classify the intent of the seq, current I use LUIS
S2. According to the intent and entities, Program need to store or refresh the intent
and entities from last conversation, in order to realize context chatting
S3. For different intent, I use different func to return the answer
e.g: intent: 'None'， call get_freetalk() (use tuling machine)
     intent: '查询天气', call get_weather()
     ...
     intent: '学校问题', call get_uestc() to query database, we have already dealt with it
"""

import json
from collections import namedtuple

import requests

import tuling
from get_weather import Weather
from similarity import QuestionSet
import sqlite_api as sql


class ChatSession(object):
    """
    response() is the entry func of this class, it receive a seq and return an ans

    """

    def __init__(self, uestc_qa, weather, ticket, freetalk):
        """\
        Args:
            uestc_qa: An object of QuestionSet control the QA pair in the database
            weather: An object of Weather, used for querying weather
            ticket: Not write, used for querying price
            freetalk: for open area talk
        """
        self.intent = 'None'
        # entities is a dict, { 'type': [ value] }
        self.entities = {}
        # url for cognitive services, add the seq
        self.url = 'https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/a00658e3-a161-47d0-b29e-b73e5efe42bb?subscription-key=db06809c4cf54d028abebbe5da08b92f&verbose=true&timezoneOffset=480&q='

        # weather class, used for weather question
        self.weather = weather
        # quesitones in database, used for uestc question
        self.uestc_qa = uestc_qa
        # price question
        self.ticket = ticket

        self.freetalk = freetalk

    # get a seq, and return the response
    def response(self, sentence):
        new_intent, new_entities = self.get_intententities(sentence)
        if new_intent != 'None':
            self.intent = new_intent
            self.entities = new_entities
        else:
            if self.is_similar(new_entities):
                self.entities = new_entities
            else:
                self.intent = new_intent
                self.entities = new_entities

        if self.intent == 'None':
            return self.get_freetalk(sentence)
        elif self.intent == '查询天气':
            places = self.get_entityvalue('地点')
            time = self.get_entityvalue('datetimeV2')
            return self.get_weather(places, time)
        elif self.intent == '查询票价':
            places = self.get_entityvalue('地点')
            time = self.get_entityvalue('datetimev2')
            return self.get_ticket(places, time)
        else:
            return self.get_uestc(sentence)

    def get_entityvalue(self, entity):
        if entity in self.entities:
            return self.entities[entity]
        else:
            return None

    # get intent and entities from 'sentence'
    def get_intententities(self, sentence):
        target_url = self.url + sentence
        r = requests.get(target_url)
        r = json.loads(r.text)
        # print(r)
        intent = r['topScoringIntent']['intent']
        entities_list = r['entities']
        entities = {}
        for item in entities_list:
            if item['type'] not in entities:
                entities[item['type']] = []
                entities[item['type']].append(item['entity'])
            else:
                entities[item['type']].append(item['entity'])
        return intent, entities

    # judge the old entities is or not similar with the new entities
    def is_similar(self, new_entities):
        if new_entities == {}:
            return False
        similar = True
        for item in self.entities:
            if item not in new_entities:
                similar = False
        return similar

    # function for specfic intent

    def get_uestc(self, sentence):
        if self.uestc_qa is None:
            raise ValueError("QuestionSet class is not instantiated!")
        ans = self.uestc_qa.match(sentence)
        return ans[1]

    def get_weather(self, places, time):
        if self.weather is None:
            self.weather = Weather()

        city = places[0]
        self.weather.put(city)
        self.weather.put('天气')
        return self.weather.get_weather()

    def get_ticket(self, places, time):
        # TODO: Fix this function
        print('Querying the ticket from ' + places[0] + ' to ' + places[1])
        return 3

    def get_freetalk(self, sentence):
        print('Tuling machine')
        r = tuling.send_question(sentence, None)
        return r['text']

Data = namedtuple("Data", ["question", "answer"])
texts = sql.select("question, answer")
data = [Data(q, a) for q, a in texts]

QA = QuestionSet(data)
weather = Weather()

sess = ChatSession(QA, weather, None, None)


def main():
    # Prepare database
    from collections import namedtuple
    import sqlite_api as sql
    Data = namedtuple("Data", ["question", "answer"])
    texts = sql.select("question, answer")
    data = [Data(q, a) for q, a in texts]

    QA = QuestionSet(data)
    weather = Weather()

    chatbot = ChatSession(QA, weather, None, None)

    ans = chatbot.get_uestc("电子科大的历史")
    print(ans)
    while True:
        seq = input('Please enter your question(# to qiut)')
        if seq == '#':
            break
        print(chatbot.response(seq))


if __name__ == "__main__":
    main()
