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


@app.route("/")
def get_news():
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = 'bbc'
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather("New York, US")
    return render_template("home.html", articles=feed['entries'], weather=weather)


def get_weather(query):
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=8e26c6b10c21db76ff2ec69d1b08c87e'
    query = urllib.parse.quote(query)
    url = api_url.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"descrition":
                   parsed['weather'][0] ['description']
                   }
    return


if __name__ == '__main__':
    app.run(port=5000, debug=True)

