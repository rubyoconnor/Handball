from db_functions import run_search_query_tuples

def get_draw(db_path):
    sql = """select program.title """
    from program

    result = run_search_query_tuples(sql, (), db_path)
    print(result)


if __name__ == "__main__":
    db_path = 'data/handball_db.sqlite'
    get_draw(db_path)