import requests
import json

class ChatSession(object):
    def __init__(self):
        self.intent = None
        # entities is a dict, { 'type': [ value] }
        self.entities = {}
        # url for cognitive services, add the seq
        self.url = 'https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/a00658e3-a161-47d0-b29e-b73e5efe42bb?subscription-key=db06809c4cf54d028abebbe5da08b92f&verbose=true&timezoneOffset=480&q='


    def get_EntityValue(self, entity):
        if entity in self.entities:
            return self.entities[entity]
        else:
            return None

    def get_IntentEntities(self, sentence):
        target_url = self.url + sentence
        r = requests.get(target_url)
        r = json.loads(r.text)
        print(r)
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

    def get_similarity(self, new_entities):
        similar = True
        for item in self.entities:
            if item not in new_entities:
                similar = False
        return similar

    def response(self, sentence):
        new_intent, new_entities = self.get_IntentEntities(sentence)
        # print('intent %s; new_intent %s' %(self.intent,new_intent))
        if not new_intent == 'None':
            self.intent = new_intent
            self.entities = new_entities
        else:
            if self.get_similarity(new_entities):
                self.entities = new_entities
            else:
                self.intent = new_intent
                self.entities = new_entities

        if self.intent == None:
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


    def get_UESTC(self, sentence):
        print('Query from database!')
        return 1

    def get_Weather(self, places, time):
        print('Querying the weather of' + places[0] + ', please wait!')
        return 2

    def get_Ticket(self, places, time):
        print('Querying the ticket from ' + places[0] + ' to ' + places[1])
        return 3

    def get_FreeTalk(self, sentence):
        print('Tuling machine')
        return 4





if __name__ == "__main__":
    A = ChatSession()
    while True:
        seq = input('Please enter your question(# to qiut)')
        if seq == '#':
            break
        A.response(seq)

