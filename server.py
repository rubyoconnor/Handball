from flask import Flask, render_template, request, redirect, url_for
from db_functions import run_search_query_tuples
from datetime import datetime

app = Flask(__name__)
db_path = 'data/handball_db.sqlite'


@app.template_filter()
def news_date(sqlite_dt):
    # create a date object
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%a %d %b %Y %H:%M %p")


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/events')
def events():
    return render_template("events.html")

@app.route('/howtoplay')
def howtoplay():
    return render_template("howtoplay.html")

@app.route('/regions')
def regions():
    return render_template("regions.html")

@app.route('/news')
def news():

    # query for the page
    sql = """select news.news_id, news.title, news.subtitle, news.content, news.newsdate, member.name
         from news
         join member on news.member_id= member.member_id
         order by news.newsdate desc;
         """

    result = run_search_query_tuples(sql, (), db_path, True)
    print(result)
    return render_template("news.html", news=result)


if __name__ == "__main__":
    app.run(debug=True)