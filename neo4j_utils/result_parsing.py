from json import dump


def serialize_node(node_record):
    """
    Creates a dictionary containing the attributes of a neo4j Node object
    Necessary to make Node object attributes serializable for JSON conversion
    :param node_record: Neo4j record containing a Node object
    :return: Dictionary containing Node attributes
    """
    node_dict = {
        'id': node_record.id,
        'labels': [],
        'properties': {}
    }

    # Get labels
    for label in node_record.labels:
        node_dict['labels'].append(label)

    # Get properties
    for key in node_record.keys():
        node_dict['properties'][key] = node_record.get(key)

    return node_dict


def serialize_relationship(rel_record):
    """
    Creates a dictionary containing the attributes of a neo4j Relationship object
    :param rel_record: neo4j record object
    :return: dictionary containing Relationship attributes
    """
    return {
        'id': rel_record.id,
        'type': rel_record.type,
        'source': serialize_node(rel_record.nodes[0])['id'],
        'target': serialize_node(rel_record.nodes[1])['id']
    }


def serialize_path(path_record):
    """ q
    Creates a dictionary containing the attributes of a neo4j Path object
    Necessary to make Path object attributes serializable for JSON conversion
    :param path_record: neo4j record containing a Path object
    :return: dictionary containing Path attributes
    """
    return {
        'source': serialize_node(path_record.start)['id'],
        'target': serialize_node(path_record.end)['id']
    }


def parse_records(result):
    """
    Converts neo4j records to JSON containing paths and nodes
    :param result: neo4j response containing 1 or more record objects
    :return: dictionary
    """
    graph = {
        'paths': [],
        'nodes': []
    }

    node_cnt = 0
    relationship_cnt = 0

    for node in result.graph().nodes:
        graph['nodes'].append(serialize_node(node))
        node_cnt += 1
    for rel in result.graph().relationships:
        graph['paths'].append(serialize_relationship(rel))
        relationship_cnt += 1

    # print(dumps(graph, indent=4, sort_keys=True))
    with open('./data/test.json', 'w') as outfile:
        dump(graph, outfile, indent=4, sort_keys=True)

    return graph


def insert_string(original, insertion, index):
    """
    Insert a string at the given index of the provided string
    :param original: string to be inserted into
    :param insertion: string to insert
    :param index: index of insertion
    :return: initial string with completed insertion
    """
    return original[:index+1] + insertion + original[index+1:]


def create_var(var_list, var_count):
    """
    create a new variable accounting for currently used variable names
    format: var#
    :param var_list: list of strings containing currently used variables
    :param var_count: number of currently used variables
    :return: tuple containing the new variable name and current variable count
    """
    new_var = 'var' + str(var_count)
    var_list.append(new_var)
    var_count += 1
    return new_var, var_count


def refactor_query(query):
    """
    DEPRECATED
    New query refactoring method found in query_refactoring.py
    :param query:
    :return:
    """
    var_count = 0
    vars = []
    has_limit = False
    return_index = 0
    limit = 0
    index = 0
    end_index = len(query)

    while index < end_index:
        char = query[index]
        if query[index:index+5].upper() == 'MATCH':
            index += 5
        elif char in [' ', '=', '>', '<']:  # characters to skip
            index += 1
        elif char in ['(', '[']:  # check if node or relationship has a variable
            if query[index+1] in [':', ']', ')']:   # no variable is present and one must be added
                (new_var, var_count) = create_var(vars, var_count)
                end_index += len(new_var)
                query = insert_string(query, new_var, index)  # add new variable with format 'var#'
                index += len(new_var) + 2
            else:  # a variable is present and must be recorded
                for index2 in range(index+1, len(query)):
                    char2 = query[index2]
                    if char2 in [':', ']', ')']:
                        var = query[index+1:index2]
                        index += index2 - index
                        if var not in vars:
                            vars.append(var)
                            var_count += 1
                        break
        elif char == '-':
            if query[index+1] == '-':  # arrow does not request relationship object
                (new_var, var_count) = create_var(vars, var_count)
                end_index += len(new_var) + 2
                query = insert_string(query, '[' + new_var + ']', index)
                index += len(new_var) + 2
            else:
                index += 1
        elif query[index:index+5].upper() == 'LIMIT':  # get value of limit if present
            has_limit = True
            limit = query[index+5:]
            index += 5

        elif query[index:index+6].upper() == 'RETURN':  # get the index of the return statement
            return_index = index+6
            index += 6
        else:
            index += 1

    query = query[:return_index]

    for i in range(0, len(vars)):
        query += ' ' + vars[i]
        if i < len(vars)-1:
            query += ','

    if has_limit:
        query += ' LIMIT' + limit

    print(query)
    return query


