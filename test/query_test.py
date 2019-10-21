import requests as req

FLASK_URL = 'http://localhost:8080'

queries = [
    # 'MATCH p=()-[r:ORIG]->() RETURN p LIMIT 25',
]


def submit_queries(query_list):
    for query in query_list:
        data = {'query': query}
        test_case = req.post(FLASK_URL, data)
        print('Submitted test query: <', query, '>')
        print(test_case)


if __name__ == '__main__':
    submit_queries(queries)
