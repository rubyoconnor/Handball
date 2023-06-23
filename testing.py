from db_functions import run_search_query_tuples

def get_news(db_path):
    sql = """select news.title, news.subtitle, news.content, member.name
    from news
    join member on news.member_id = member.member_id; 
    """

    result = run_search_query_tuples(sql, (), db_path, True)

    for row in result:
        for k in row.keys():
            print(k)
            print(row[k])



if __name__ == "__main__":
    db_path = 'data/handball_db.sqlite'
    get_news(db_path)
