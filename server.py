import urllib.parse
import crawler
import crawler.spider
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return app.send_static_file('index.html')


@app.route('/path/')
@app.route('/path/<target>')
def path(target=None):
    print(urllib.parse.quote("baidu.com/s?wq=123123"))
    return 'Hello ' + urllib.parse.unquote(target)


@app.route('/direct', methods=['GET', 'POST'])
def direct():
    if request.method == "POST":
        result = crawler.spider.crawler(request.form['url'])
        return result.craw()

