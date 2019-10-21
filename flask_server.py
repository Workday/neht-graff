from flask import Flask, request, render_template, jsonify, g
from neo4j import GraphDatabase, basic_auth, CypherError

from config import *
from neo4j_utils import result_parsing, query_refactoring

app = Flask(__name__, template_folder='./templates')


def get_db():
    if 'db' not in g:
        g.db = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(user=NEO4J_CREDS[0], password=NEO4J_CREDS[1]))
    return g.db


def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()


def submit(query):
    """
    Submits the specified query using a driver representing an established connection to a neo4j database
    Catches errors for blank queries and invalid Cypher syntax
    :param query: String containing a Cypher query
    :return: Iterable of 1 or more Neo4j records
    """

    if not query:
        return 'Query is null.', 1, ''
    elif query == '':
        return 'Query is blank', 2, ''
    else:
        try:
            driver = get_db()
            with driver.session() as session:
                result = session.run(query)
                return result, 0, ''
        except CypherError as e:
            return 'Query is invalid', 3, e.message
        finally:
            close_db()


# GET response: render graph.html
# POST response: submit search bar query to specified DB, then render graph.html
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        refactored_query = query_refactoring.refactor_query(request.form['query'])
        print('Refactored query: ', refactored_query)
        result, code, message = submit(refactored_query)
        if code == 0:
            records_json = result_parsing.parse_records(result)
            return render_template('./graph.html', json_data=records_json, error='Enter query: ')
        else:
            print('ERROR: ' + str(message))
            return render_template('./graph.html', error=result, message=message)
    else:
        return render_template('./graph.html')


@app.route('/submit_query', methods=['POST'])
def query_pivot():
    query = request.get_json()
    query = query_refactoring.refactor_query(query)
    result, code, message = submit(query)
    if code == 0:
        result_json = result_parsing.parse_records(result)
        return jsonify(result_json)
    else:
        print('ERROR: ' + str(message))
        return jsonify(message)


if __name__ == '__main__':
    app.run(port=FLASK_PORT)
