#!/usr/bin/env python

import os
import json

import tornado.ioloop
import tornado.log
import tornado.web

class WeatherHandler(tornado.web.RequestHandler):
  def start_conversation (self):
    response = {
      'expectUserResponse': True,
      'expectedInputs': [
        {
          'possibleIntents': {'intent': 'actions.intent.TEXT'},
          'inputPrompt': {
            'richInitialPrompt': {
              'items': [
                {
                  'simpleResponse': {
                    'ssml': '<speak>What city would you like the weather for?</speak>'
                  }
                }
              ]
            }
          }
        }
      ]
    }
    
    self.set_header('Google-Assistant-API-Version', 'v2')
    self.write(response)
    
  def get_weather (self, city):
    response = {}
    
    self.set_header('Google-Assistant-API-Version', 'v2')
    self.write(response)
    
  def get (self):
    city = self.get_query_argument('city', '')
    if city:
      self.get_weather(city)
      
    else:
      self.start_conversation()
      
  def post (self):
    data = json.loads(self.request.body.decode('utf-8'))
    print(data['conversation']['type'])
    print(data['conversation']['conversationId'])
    
    if data['conversation']['type'] == 'NEW':
      self.start_conversation()
      
    else:
      city = data['inputs'][0]['arguments'][0]['textValue'].lower()
      self.get_weather(city)
      
def make_app():
  return tornado.web.Application([
    (r"/weather-app", WeatherHandler),
  ], autoreload=True)

if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  
  app = make_app()
  app.listen(int(os.environ.get('PORT', '8000')))
  tornado.ioloop.IOLoop.current().start()
  