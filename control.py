import requests
import json
import tuling
from utils import call_once
from collections import namedtuple
from get_weather import Weather

"""
In this file I decide to rewrite the entry of the chatbot, and it has following steps:
S1. Extract the entities and classify the intent of the seq, current I use LUIS
S2. According to the intent and entities, Program need to store or refresh the intent
and entities from last conversation, in order to realize context chatting
S3. For different intent, I use different func to return the answer
e.g: intent: 'None'， call get_FreeTalk() (use tuling machine)
     intent: '查询天气', call get_Weather()
     ...
     intent: '学校问题', call get_UESTC() to query database, we have already dealt with it

response() is the entry func of this class, it receive a seq and return an ans
"""
class ChatSession(object):
    def __init__(self):
        self.intent = 'None'
        # entities is a dict, { 'type': [ value] }
        self.entities = {}
        # url for cognitive services, add the seq
        self.url = 'https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/a00658e3-a161-47d0-b29e-b73e5efe42bb?subscription-key=db06809c4cf54d028abebbe5da08b92f&verbose=true&timezoneOffset=480&q='

        # weather class, used for weather question
        self.weather = None
        # quesitones in database, used for uestc question
        self.UESTC_QA = None
        # price question
        self.ticket = None

    # get a seq, and return the response
    def response(self, sentence):
        new_intent, new_entities = self.get_IntentEntities(sentence)
        if not new_intent == 'None':
            self.intent = new_intent
            self.entities = new_entities
        else:
            if self.is_similar(new_entities):
                self.entities = new_entities
            else:
                self.intent = new_intent
                self.entities = new_entities

        if self.intent == 'None':
            return self.get_FreeTalk(sentence)
        elif self.intent == '查询天气':
            places = self.get_EntityValue('地点')
            time = self.get_EntityValue('datetimeV2')
            return self.get_Weather(places, time)
        elif self.intent == '查询票价':
            places = self.get_EntityValue('地点')
            time = self.get_EntityValue('datetimeV2')
            return self.get_Ticket(places, time)
        else:
            return self.get_UESTC(sentence)

    def get_EntityValue(self, entity):
        if entity in self.entities:
            return self.entities[entity]
        else:
            return None

    # get intent and entities from 'sentence'
    def get_IntentEntities(self, sentence):
        target_url = self.url + sentence
        r = requests.get(target_url)
        r = json.loads(r.text)
        #print(r)
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

    def get_UESTC(self, sentence):
        # TODO: Fix this function

        print('Query from database!')
        return 1

    def get_Weather(self, places, time):
        if self.weather == None:
            self.weather = Weather()

        city = places[0]
        self.weather.put(city)
        self.weather.put('天气')
        return self.weather.get_weather()

    def get_Ticket(self, places, time):
        print('Querying the ticket from ' + places[0] + ' to ' + places[1])
        return 3

    def get_FreeTalk(self, sentence):
        print('Tuling machine')
        r = tuling.send_question(sentence, None)
        return r['text']





if __name__ == "__main__":
    A = ChatSession()

    while True:
        seq = input('Please enter your question(# to qiut)')
        if seq == '#':
            break
        print(A.response(seq))



