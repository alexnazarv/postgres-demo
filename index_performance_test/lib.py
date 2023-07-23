import time
from typing import List

from connection import make_conn
from psycopg2 import connect, sql

TABLE_INDEXED = 'test_table'
TABLE_STATISTIC = 'measured'

COLUMNS_INDEXED = ['varchar0', 'integer0', 'date0']
INDEXES = ['gin', 'brin', 'gist', 'bloom', 'rum', 'hash', 'btree']

OPERAND_CHECK_VALUES = {'varchar': 'Allyson Lowe',
                        'integer': 23579207,
                        'date': '2023-11-29'}


def index_make_create_duration(table_indexed, index_name, index_type, column, cursor):
    start_time = time.time()
    query = sql.SQL('create index {} on {} using {}({})') \
                        .format(sql.SQL(index_name),
                                sql.Identifier(table_indexed),
                                sql.SQL(index_type),
                                sql.Identifier(column))
    cursor.execute(query)
    return (time.time() - start_time).__round__(2)


def operands_time_execution(datatype: str, column: str, cursor,
                            table_indexed: str = TABLE_INDEXED,
                            operand_check_values: dict = OPERAND_CHECK_VALUES):
    check_value = operand_check_values[datatype]

    if datatype == 'varchar':
        operands = ['=', 'like', 'in']
    elif datatype in ['integer','date']:
        operands = ['=', '>', 'in']
    
    operands_durations = {}
    for operand in operands:
        if operand in ['=','>','in']:
            if operand in ['=','>']:
                query = sql.SQL("""select count(*)
                                     from {}
                                    where {} {} {}""")
            else:
                query = sql.SQL("""select count(*)
                                     from {}
                                    where {} {} ({})""")
            
            query = query.format(sql.Identifier(table_indexed),
                                 sql.Identifier(column),
                                 sql.SQL(operand),
                                 sql.Placeholder())
            start_time = time.time()
            cursor.execute(query, (check_value,))
            operands_durations[operand] = (time.time() - start_time).__round__(2)

        elif operand == 'like':
            query = sql.SQL("""select count(*)
                                from {}
                                where {} {} {}""") \
                       .format(sql.Identifier(table_indexed),
                               sql.Identifier(column),
                               sql.SQL(operand),
                               sql.Literal('%' + check_value + '%'))
            start_time = time.time()
            cursor.execute(query)
            operands_durations[operand] = (time.time() - start_time).__round__(2)            
    return operands_durations


def insert_statistic(table_statistic: str, index_type: str, datatype: str,
                     index_creation_duration: float, cursor: connect,
                     operands_durations: dict) -> None:
    data_dicted = {
                  'indextype': index_type, 'DataType': datatype,
                  'creationduration': index_creation_duration
                  }
    data_parsed = list(zip(*{**data_dicted, **operands_durations}.items()))

    fields = data_parsed[0]
    data = data_parsed[1]

    query = sql.SQL('insert into {} ({}) values ({})') \
                .format(sql.Identifier(table_statistic),
                        sql.SQL(', ').join(map(sql.Identifier, fields)),
                        sql.SQL(', ').join(sql.Placeholder() * len(fields)))
    cursor.execute(query, data)


def insert_index_size(index_name: str, index_type: str,
                      datatype:str, table_statistic: str, cursor) -> None:
    select_query = sql.SQL('(select pg_size_pretty(pg_table_size({})))') \
                      .format(sql.Literal(index_name))
    update_query = sql.SQL("""update {} set {} = {}
                              where indextype = {}
                                and "DataType" = {}""") \
                      .format(sql.Identifier(table_statistic),
                              sql.Identifier('indexsize'),
                              select_query,
                              sql.Literal(index_type),
                              sql.Literal(datatype))
    cursor.execute(update_query)


def indexes_check(index_type: str,
                  cursor: connect,
                  columns_indexed: List,
                  table_indexed: str,
                  table_statistic: str) -> None:
    for column in columns_indexed:
        datatype = column.rstrip('0')
        index_name = f'{index_type}_{datatype}'

        index_creation_duration = index_make_create_duration(table_indexed, index_name,
                                                             index_type, column, cursor)
        operands_durations = operands_time_execution(datatype, column, cursor)
        insert_statistic(table_statistic, index_type, datatype, 
                         index_creation_duration, cursor, operands_durations)
        insert_index_size(index_name, index_type, datatype, table_statistic, cursor)
        cursor.execute(sql.SQL('drop index {}').format(sql.SQL(index_name)))


if __name__=='__main__':
    with make_conn() as cursor:
        for index in INDEXES:
            indexes_check(index_type=index, cursor=cursor,
                          columns_indexed=COLUMNS_INDEXED,
                          table_indexed=TABLE_INDEXED,
                          table_statistic=TABLE_STATISTIC)
