# Neht Graff Cypher Support
Some Cypher clauses return values not relevant to the visualization.
These clauses may result in unexpected behavior.

[List of Cypher Clauses](https://neo4j.com/docs/cypher-manual/current/clauses/)

## Reading Clauses
|     Clause     | Support |
|:--------------:|:-------:|
|      MATCH     |   Yes   |
| OPTIONAL MATCH |   Yes   |

## Projecting Clauses
| Clause | Support |
|:------:|:-------:|
| RETURN |   Yes   |
|  WITH  |    No   |
| UNWIND |    No   |
|   AS   |    No   |

## Reading Sub-clauses
|  Clause  | Support |
|:--------:|:-------:|
|   WHERE  |   Yes   |
| ORDER BY |   Yes   |
|   SKIP   |   Yes   |
|   LIMIT  |   Yes   |

## Reading Hints
None

## Writing Clauses
None

## Set Operations
|   Clause  | Support |
|:---------:|:-------:|
|   UNION   |   Yes   |
| UNION ALL |    No   |

## Importing Data
None

## Schema Clauses
None