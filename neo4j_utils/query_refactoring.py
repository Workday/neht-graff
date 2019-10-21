from pygments.lexers import get_lexer_by_name
from pygments.token import Token


def insert_string(original, insertion, index):
    """
    Insert a new string at the given index of the provided string
    :param original: string to be inserted into
    :param insertion: string to insert
    :param index: index of insertion
    :return: original with completed insertion
    """
    return original[:index+1] + insertion + original[index+1:]


def insert_variable_token(insertion_list, value, index):
    """
    Insert a tuple containing a Token object and a value into a list
    Intended for adding new variables into a list of tokens returned by the py2neo cypher lexer
    :param insertion_list: list to be inserted into
    :param value: value to insert
    :param index: index of insertion
    :return: insertion_list with completed insertion
    """
    return insertion_list[:index + 1] + [(Token.Name.Variable, value)] + insertion_list[index+1:]


def assemble_clause_from_tokens(token_list):
    """
    Assemble each string value from a list of tuples into a string, representing an individual clause in a cypher query
    :param token_list: A list of tuples in the format (Token, value) which is returned by the py2neo cypher lexer
    :return: string representing part of a cypher query
    """
    reassembled = ''
    for tup in token_list:
        reassembled += tup[1]
    return reassembled


def assemble_query_from_clauses(clauses_list):
    """
    For each list of tuples in clauses_list, assemble the values from each tuple into a string and append it
    to the string representing the full query
    :param clauses_list: A list of lists containing tuples in the format (Token, value)
    :return: string representing a full cypher query
    """
    query = ''
    for clause in clauses_list:
        query += assemble_clause_from_tokens(clause)
    return query


def split_by_clause(tokens):
    """
    Split a list of tuples in the form (Token, value) into a list of sub lists containing tuples representing
    cypher clauses.
    :param tokens: list of tuples in the form (Token, value)
    :return: list of sub lists containing tuples
    """
    clause_start = 0
    clauses = []
    for i in range(1, len(tokens)):
        if tokens[i][0] == Token.Keyword:
            clauses.append(tokens[clause_start:i])
            clause_start = i
        if i == len(tokens)-1:
            clauses.append(tokens[clause_start:i])

    return clauses


def refactor_query(query):
    """
    Refactor cypher query to request a return variable for each node(()) or relationship([]) pattern in the string.
    'MATCH (a)--() RETURN a' will be refactored to 'MATCH (a)-[var0]-(var1) return a, var0, var1'
    :param query: string representing a full cypher query
    :return: string representing refactored cypher query
    """
    if query == '' or None:
        return ''
    lexer = get_lexer_by_name('py2neo.cypher')
    tokens = list(lexer.get_tokens(query))
    clause_statements = split_by_clause(tokens)

    # Check MATCH clause to ensure all nodes-() and relationships-[] request a return variable
    vars = []
    match_clause = clause_statements[0]
    index = 0
    end_index = len(match_clause)
    while index < end_index:
        if match_clause[index][1].endswith(('(', '[')):  # check if node or relationship has a variable
            if match_clause[index+1][1].startswith((':', ']', ')')):  # no variable is present, one must be added
                new_var = 'var' + str(len(vars))
                vars.append(new_var)
                match_clause = insert_variable_token(match_clause, new_var, index)  # add new variable with form 'var#'
                end_index += 1
            else:  # a variable is present and must be recorded
                new_var = match_clause[index+1][1]
                if new_var not in vars:
                    vars.append(new_var)
        if '--' in match_clause[index][1]:
            new_var = 'var' + str(len(vars))
            vars.append(new_var)
            match_clause[index] = (match_clause[index][0], insert_string(match_clause[index][1], '['+new_var+']', 1))
        index += 1
    clause_statements[0] = match_clause

    for i in range(0, len(clause_statements)):
        if clause_statements[i][0][1].upper() == 'RETURN':
            new_return_clause = clause_statements[i][:1]
            for i2 in range(0, len(vars)):
                new_return_clause.append((Token.Text.Whitespace, ' '))
                new_return_clause.append((Token.Name.Variable, vars[i2]))
                if i2 < len(vars)-1:
                    new_return_clause.append((Token.Punctuation, ','))
                else:
                    new_return_clause.append((Token.Text.Whitespace, ' '))
            clause_statements[i] = new_return_clause

    return assemble_query_from_clauses(clause_statements)

