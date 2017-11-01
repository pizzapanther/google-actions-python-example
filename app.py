import os

import tornado.ioloop
import tornado.log
import tornado.web

class WeatherHandler(tornado.web.RequestHandler):
  def get(self):
    self.write("Hello, world")

def make_app():
  return tornado.web.Application([
    (r"/weather-app", WeatherHandler),
  ], autoreload=True)

if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  
  app = make_app()
  app.listen(int(os.environ.get('PORT', '8000')))
  tornado.ioloop.IOLoop.current().start()
  