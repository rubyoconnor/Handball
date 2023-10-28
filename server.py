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
    sql = """select news.news_id, news.title, news.subtitle, news.content, news.newsdate, member.firstname
         from news
         join member on news.member_id= member.member_id
         order by news.newsdate desc;
         """

    result = run_search_query_tuples(sql, (), db_path, True)
    print(result)
    return render_template("news.html", news=result)

@app.route('/news_formpage', methods =['GET', 'POST'])
def news_formpage():
    # collect data from the web address
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
        # if task is to delete
        if data['task'] == 'delete':
            # using the news_id to delete the news item
            sql = "delete from news where news_id = ?"
            values_tuple = (data['id'],)
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('news'))

        # if task is to update
        elif data['task'] == 'update':
            # taking the info that is already there
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
            return render_template("error.html", message=message)
    elif request.method == "POST":
       # collected form information
       f = request.form
       print(f)
       if data['task'] =='add':
           # add the the new news entry to the database
           sql = """insert into news(title,subtitle,content, newsdate, member_id) 
                                values(?,?,?, datetime('now', 'localtime'), ?)"""
           values_tuple = (f['title'], f['subtitle'], f['content'], session['member_id'])
           result = run_commit_query(sql, values_tuple, db_path)
           # this will redirect to news page to see the newly added news item
           return redirect(url_for('news'))

       elif data['task'] == 'update':
           # we are updating so 'rewrite' all the data
           sql = """update news set title=?, subtitle=?, content=?, 
                   newsdate=datetime('now', 'localtime') where news_id=?"""
           values_tuple = (f['title'], f['subtitle'], f['content'], data['id'])
           result = run_commit_query(sql, values_tuple, db_path)
           # collect the data from the form and update the database at the sent id
           return redirect(url_for('news'))
       else:
           # error catch
           message = "Unrecognised task coming from news form submission"
           return render_template('error.html', message=message)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # collecting form information
        f = request.form
        print(f)

        return render_template("confirm.html", form_data=f)

    elif request.method == "GET":
        temp_form_data = {
            "firstname": "Jess",
            "secondname": "Batten",
            "username": "jessbatten",
            "password": "temp",
            "authorisation" : "1",
        }

        return render_template("signup.html", **temp_form_data)

    else:
        return render_template("signup.html", **temp_form_data)

@app.route('/login', methods=["GET", "POST"])
def login():
    print(session)
    # error message
    error = "Your credentials are not recognised"
    if request.method == "GET":
        return render_template("log-in.html", username='', password="")

    elif request.method == "POST":
        # collecting form info
        f = request.form
        # query for login
        sql = """select member_id, firstname, secondname, password, authorisation from member where username= ?"""
        values_tuple=(f['username'],)
        result = run_search_query_tuples(sql,values_tuple, db_path, True)
        if result:
            result = result[0]
            # if password entered matches password in member_table
            if result ['password'] == f['password']:
                    # start a session
                    session['firstname'] = result['firstname']
                    session['authorisation'] = result['authorisation']
                    session['member_id'] = result['member_id']
                    return redirect(url_for('index'))

            # error message will print
            else:
                return render_template("log-in.html", username='', password="", error=error)

        # error message will print
        else:
            return render_template("log-in.html", username='', password="", error=error)


@app.route('/logout')
def logout():
    # logging out
    session.clear()
    return redirect(url_for('index'))


@app.route('/draw')
def draw():
    # query for the page
    sql = """select draw.draw_id, draw.gamedate, draw.teamone, draw.teamtwo, draw.location, draw.gametime
           from draw
           """

    result = run_search_query_tuples(sql, (), db_path, True)
    print()

    return render_template("draw.html", draw=result)

@app.route('/results')
def results():
     # query for the page
    sql = """select results.result_id, results.gamedate, results.teamone, results.teamtwo, results.teamonescore, 
             results.teamtwoscore, results.winner
             from results
            """

    result = run_search_query_tuples(sql, (), db_path, True)
    print()

    return render_template("results.html", results=result)


@app.route('/editdraw_page', methods =['GET', 'POST'])
def editdraw_page():
    # collect data from the web address
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
        # the task is to delete ?
        if data['task'] == 'delete':
            # use draw_id to delete draw info
            sql = "delete from draw where draw_id = ?"
            values_tuple = (data['id'],)
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('draw'))

        # the task is to update
        elif data['task'] == 'update':
            # select info that is previously there that the user wants to update
            sql = """ select gamedate, teamone, teamtwo, location, gametime from draw where draw_id=?"""
            values_tuple = (data['id'],)
            result = run_search_query_tuples(sql, values_tuple, db_path, True)
            result = result[0]
            return render_template("editdraw_page.html",
                                    **result,
                                    id = data['id'],
                                    task = data['task'],)
        # the task is to add
        elif data['task'] == 'add':
            # dummy data for testing
            temp = {'teamone': 'teamone', 'teamtwo': 'teamtwo', 'location': 'location'}
            return render_template("editdraw_page.html",
                                    id=0,
                                    task=data['task'],
                                    location=temp['location'],
                                    teamone=temp['teamone'],
                                    teamtwo=temp['teamtwo'],
                                   )

        # error catch
        else:
            message = "Unrecognised task coming from news page"
            return render_template("error.html", message=message)


    elif request.method == "POST":
       # collected form information
       f = request.form
       print(f)
       # task is to add
       if data['task'] =='add':
           # add the new draw entry to the database
           sql = """insert into draw(gamedate, teamone, teamtwo, location, gametime)
                                values(?,?,?,?,?)"""
           values_tuple = (f['gamedate'], f['teamone'], f['teamtwo'], f['location'],f['gametime'])
           result = run_commit_query(sql, values_tuple, db_path)
           # this will redirect to draw page to see the newly added draw item
           return redirect(url_for('draw'))

        # task is to update
       elif data['task'] == 'update':
           # we are updating so 'rewrite' all the data
           sql = """update draw set gamedate=?, teamone=?, teamtwo=?, location=?, gametime=? where draw_id=? 
               """
           values_tuple = (f['gamedate'], f['teamone'], f['teamtwo'], f['location'], f['gametime'], data['id'])
           result = run_commit_query(sql, values_tuple, db_path)
           # collect the data from the form and update the database at the sent id
           return redirect(url_for('draw'))

       else:
           # error catch
           message = "Unrecognised task coming from news form submission"
           return render_template('error.html', message=message)

@app.route('/editresults_page', methods =['GET', 'POST'])
def editresults_page():
    # collect data from the web address
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
            sql = "delete from results where result_id = ?"
            values_tuple = (data['id'],)
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('results'))

        elif data['task'] == 'update':
            sql = """ select gamedate, teamone, teamonescore, teamtwo, teamtwoscore, winner from results where result_id=?"""
            values_tuple = (data['id'],)
            result = run_search_query_tuples(sql, values_tuple, db_path, True)
            result = result[0]
            return render_template("editresults_page.html",
                                    **result,
                                    id = data['id'],
                                    task = data['task'],)

        elif data['task'] == 'add':
            # dummy data for testing
            temp = {'teamone': 'teamone', 'teamonescore': 'teamonescore', 'teamtwo': 'teamtwo','teamtwoscore': 'teamtwoscore', 'winner': 'winner'}
            return render_template("editresults_page.html",
                                    id=0,
                                    task=data['task'],
                                    teamone=temp['teamone'],
                                    teamonescore=temp['teamonescore'],
                                    teamtwo=temp['teamtwo'],
                                    teamtwoscore=temp['teamtwoscore'],
                                    winner=temp['winner'],
                                   )
        else:
            message = "Unrecognised task coming from news page"
            return render_template("error.html", message=message)
    elif request.method == "POST":
       # collected form information
       f = request.form
       print(f)
       if data['task'] =='add':
           # add the new results entry to the database
           sql = """insert into results(gamedate, teamone, teamonescore, teamtwo, teamtwoscore, winner)
                                values(?,?,?,?,?,?)"""
           values_tuple = (f['gamedate'], f['teamone'],f['teamonescore'],f['teamtwo'], f['teamtwoscore'], f['winner'])
           result = run_commit_query(sql, values_tuple, db_path)
           # this will redirect to draw page to see the newly added results item
           return redirect(url_for('results'))

       elif data['task'] == 'update':
           # we are updating so 'rewrite' all the data even if
           sql = """update results set gamedate=?, teamone=?, teamonescore=?, teamtwo=?, teamtwoscore=?, winner=? where result_id=? 
               """
           values_tuple = (f['gamedate'], f['teamone'],f['teamonescore'], f['teamtwo'], f['teamtwoscore'], f['winner'], data['id'])
           result = run_commit_query(sql, values_tuple, db_path)
           # collect the data from the form and update the database at the sent id
           return redirect(url_for('results'))

       else:
           # let's put in an error catch
           message = "Unrecognised task coming from news form submission"
           return render_template('error.html', message=message)

@app.route('/member')
def member():
    # query for the page
    sql = """select member.member_id, member.firstname, member.secondname, 
    member.password, member.username, member.authorisation
           from member
           """

    result = run_search_query_tuples(sql, (), db_path, True)
    print()

    return render_template("member.html", member=result)

@app.route('/updatemember', methods =['GET', 'POST'])
def updatemember():
    # collect data from the web address
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
        # the task to delete
        if data['task'] == 'delete':
            # delete using the member_id
            sql = "delete from member where member_id = ?"
            values_tuple = (data['id'],)
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('member'))

        # the task is to update
        elif data['task'] == 'update':
            sql = """ select firstname, secondname, password, username, authorisation from member where member_id=?"""
            values_tuple = (data['id'],)
            result = run_search_query_tuples(sql, values_tuple, db_path, True)
            result = result[0]
            return render_template("updatemember.html",
                                    **result,
                                    id = data['id'],
                                    task = data['task'],)

        # the task is to add
        elif data['task'] == 'add':
            # dummy data for testing
            temp = {'firstname': 'firstname', 'secondname': 'secondname', 'password': 'password','username':'username','authorisation': 'authorisation'}
            return render_template("updatemember.html",
                                   id=0,
                                   task=data['task'],
                                   firstname='',
                                   secondname='',
                                   username='',
                                   password='',
                                   authorisation=temp['authorisation'],
                                   )

        # error catcher
        else:
            message = "Unrecognised task coming from news page"
            return render_template("error.html", message=message)

    elif request.method == "POST":
       # collected form information
       f = request.form
       print(f)
       if data['task'] =='add':
           # add the new member entry to the database
           sql = """insert into member(firstname, secondname, password, username, authorisation)
                                values(?,?,?,?,?)"""
           values_tuple = (f['firstname'], f['secondname'], f['password'], f['username'], f['authorisation'])
           result = run_commit_query(sql, values_tuple, db_path)
           # this will redirect to member page to see the newly added draw item
           return redirect(url_for('index'))

       elif data['task'] == 'update':
           # we are updating so 'rewrite' all the data
           sql = """update member set firstname=?, secondname=?, password=?, username=?, authorisation=? where member_id=? 
               """
           values_tuple = (f['firstname'], f['secondname'],f['password'], f['username'], f['authorisation'], data['id'])
           result = run_commit_query(sql, values_tuple, db_path)
           # collect the data from the form and update the database at the sent id
           return redirect(url_for('member'))

       else:
           # error catch
           message = "Unrecognised task coming from news form submission"
           return render_template('error.html', message=message)



app.run(debug=True)