#!/usr/bin/env python

import os
import json

import tornado.ioloop
import tornado.log
import tornado.web

import jwt
import requests

API_KEY = os.environ.get('OPEN_WEATHER_MAP_KEY', '39898a022aa2873f702f847f4c2ecafb')
PROJECT_ID = os.environ.get('PROJECT_ID', 'mrs-weather')

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
    
    self.set_header("Content-Type", 'application/json')
    self.set_header('Google-Assistant-API-Version', 'v2')
    self.write(json.dumps(response, indent=2))
    
  def get_weather (self, city):
    api_response = requests.get(
      'http://api.openweathermap.org/data/2.5/weather',
      params={'q': city, 'APPID': API_KEY}
    )
    data = api_response.json()
    temp = round(1.8 * (data['main']['temp'] - 273) + 32)
    
    response = {
      'expectUserResponse': False,
      'finalResponse': {
        'richResponse': {
          'items': [
            {
              'simpleResponse': {
                'ssml': '<speak>The temperature in {} is {} degrees.</speak>'.format(city, temp)
              }
            }
          ]
        }
      }
    }
    
    self.set_header("Content-Type", 'application/json')
    self.set_header('Google-Assistant-API-Version', 'v2')
    self.write(json.dumps(response, indent=2))
    
  def get (self):
    city = self.get_query_argument('city', '')
    if city:
      self.get_weather(city)
      
    else:
      self.start_conversation()
      
  def post (self):
    token = self.request.headers.get("Authorization")
    jwt_data = jwt.decode(token, verify=False)
    if jwt_data['aud'] != PROJECT_ID:
      self.set_status(401)
      self.write('Token Mismatch')
      
    data = json.loads(self.request.body.decode('utf-8'))
    intent = data['inputs'][0]['intent']
    print(intent)
    print(data['conversation']['conversationId'])
    
    if intent == 'actions.intent.MAIN':
      self.start_conversation()
      
    else:
      city = data['inputs'][0]['arguments'][0]['textValue']
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
  
