import feedparser
from flask import Flask
from flask import render_template
from flask import request

import json
import urllib
# import urllib3

app = Flask(__name__)

RSS_FEEDS = {
              'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
              'cnn': 'http://rss.cnn.com/rss/edition.rss',
              'fox': 'http://feeds.foxnews.com/foxnews/latest',
              'reuters-science': 'http://feeds.reuters.com/reuters/scienceNews',
              'reuters-topnews': 'http://feeds.reuters.com/reuters/topNews'
              }
DEFAULTS = {'publication': 'bbc',
            'city': 'London, UK'}

@app.route("/")
def home():
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    return render_template("home.html", articles=articles['entries'], weather=weather)


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = 'bbc'
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed


def get_weather(query):
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=8e26c6b10c21db76ff2ec69d1b08c87e'
    query = urllib.parse.quote(query)
    url = api_url.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0] ['description'],
                   "temperature" : parsed["main"]['temp'],
                   "city": parsed['name'],
                   "country": parsed['sys']['country']
                  }
    return weather


if __name__ == '__main__':
    app.run(port=5000, debug=True)

