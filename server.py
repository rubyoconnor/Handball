from flask import Flask, render_template, request, redirect, url_for, session
from db_functions import run_search_query_tuples, run_commit_query
from datetime import datetime

app = Flask(__name__)
app.secret_key = "kasjdkfjadonviovre"
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

@app.route('/news_formpage', methods =['GET', 'POST'])
def news_formpage():
    # colllect data from the web address
    # this happens regardless of GET or POST
    data = request.args
    required_keys = ['id', 'task']
    # check that we have the required keys
    # run error page if a problem
    for k in required_keys:
        if k not in data.keys():
            message = "Do not know what to do with create read update on news (key not present)"
            return render_template('error.html', message=message)

            # yes, we have an id and a task key
            # if I have arrived directly from the page
    if request.method == "GET":
        # is the task to delete ?
        if data['task'] == 'delete':
            sql = "delete from news where news_id = ?"
            values_tuple = (data['id'],)
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('news'))

        elif data['task'] == 'update':
            sql = """ select title, subtitle, content from news where news_id=?"""
            values_tuple = (data['id'],)
            result = run_search_query_tuples(sql, values_tuple, db_path, True)
            result = result[0]
            return render_template("news_formpage.html",
                                    **result,
                                    id = data['id'],
                                    task = data['task'],)

        elif data['task'] == 'add':
            # dummy data for testing
            temp = {'title': 'Test Title', 'subtitle': 'Test subtitle', 'content': 'Test Content'}
            return render_template("news_formpage.html",
                                    id=0,
                                    task=data['task'],
                                    title=temp['title'],
                                    subtitle=temp['subtitle'],
                                    content=temp['content'])

        else:
            message = "Unrecognised task coming from news page"
            return render_template(error.html, message=message)

    elif request.method == "POST":
       # collected form information
       f = request.form
       print(f)
       if data['task'] =='add':
           # add the new news entry to the database
           sql = """insert into news(title,subtitle,content, newsdate, member_id) 
                                values(?,?,?, datetime('now', 'localtime'),2)"""
           values_tuple = (f['title'], f['subtitle'], f['content'])
           result = run_commit_query(sql, values_tuple, db_path)
           # this will redirect to news page to see the newly added news item
           return redirect(url_for('news'))

       elif data['task'] == 'update':
           # we are updating so 'rewrite' all the data even if
           sql = """update news set title=?, subtitle=?, content=?, 
                   newsdate=datetime('now', 'localtime') where news_id=?"""
           values_tuple = (f['title'], f['subtitle'], f['content'], data['id'])
           result = run_commit_query(sql, values_tuple, db_path)
           # collect the data from the form and update the database at the sent id
           return redirect(url_for('news'))
       else:
           # let's put in an error catch
           message = "Unrecognised task coming from news form submission"
           return render_template('error.html', message=message)



@app.route('/signup', methods=["GET", "POST"])
def signup():

    if request.method =="POST":
        f = request.form
        print(f)

        return render_template("confirm.html", form_data=f)

    elif request.method =="GET":
        temp_form_data={
            "firstname" : "Jess",
            "secondname": "Batten",
            "email": "jb@gmail.com",
            "aboutme": "I like sport",
        }
        return render_template("signup.html", **temp_form_data)

@app.route('/login', methods=["GET", "POST"])
def login():
    print(session)
    error = "Your credentials are not recognised"
    if request.method == "GET":
        return render_template("log-in.html", email='joyce@marsden.com', password="temp")

    elif request.method == "POST":
        f = request.form
        sql = """select name, password, authorisation from member where email= ?"""
        values_tuple=(f['email'],)
        result = run_search_query_tuples(sql,values_tuple, db_path, True)
        if result:
            result = result[0]
            if result ['password'] == f['password']:
                # start a session
                session['name']=result['name']
                session['authorisation'] = result['authorisation']
                print(session)
                return redirect(url_for('index'))
            else:
                return render_template("log-in.html", email='joyce@marsden.com', password="temp", error=error)

        else:
            return render_template("log-in.html", email='joyce@marsden.com', password="temp", error=error)

        return "<h1>Posting from log in form</h1>"

app.run(debug=True)