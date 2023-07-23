import time
from typing import List

from connection import make_conn
from psycopg2 import connect, sql

TABLE_INDEXED = 'testdb.public.test_table'
TABLE_STATISTIC = 'testdb.public.measured'

COLUMNS_INDEXED = ['varchar0', 'integer0', 'date0']
INDEXES = ['hash']

OPERAND_CHECK_VALUES = {'varchar': 'Allyson Lowe',
                        'integer': 23579207,
                        'date': '2023-11-29'}


def index_make_create_duration(table_indexed, index_type, index_name, column, datatype, cursor):
    index_name = f'{index_type}_{datatype}'
    start_time = time.time()
    query = sql.SQL('create index {} on {} using {}({})') \
                        .format(sql.SQL(index_name),
                                sql.Identifier(table_indexed),
                                sql.SQL(index_type),
                                sql.Identifier(column))
    cursor.execute(query)
    return (time.time() - start_time).__round__(2)


def insert_statistic(table_statistic: str, index_type: str, datatype: str,
                     index_creation_duration: float, cursor: connect,
                     operands_durations: dict):
    standard_fields = {'IndexType': index_type, 'DataType': datatype,
                       'CreationDuration': index_creation_duration}
    fields = {**standard_fields, **operands_durations}
    # Брать дату из значений fields (для этого нужно fields преобразовать в таплы и разделить на два:
    # первый с навзаниями колонок (нулевые елементы)
    # второй со значениями (первые элементы))
    data = tuple(index_type, datatype, index_creation_duration)
    query = sql.SQL('insert into {} ({}) values {}') \
                .format(sql.Identifier(table_statistic),
                        sql.SQL(', ').join(map(sql.Identifier, fields)),
                        sql.SQL(', ').join(sql.Placeholder() * len(fields)))

    cursor.execute(query, data)


def operands_time_execution(datatype: str, column: str,
                            table_indexed: str = TABLE_INDEXED,
                            operand_check_values: dict = OPERAND_CHECK_VALUES):
    check_value = operand_check_values[datatype]

    if datatype == 'varchar':
        operands = ['=', 'like', 'in']
    elif datatype in ['integer','date']:
        operands = ['=', '>', 'in']
    
    operands_durations = {}
    for operand in operands:
        query = sql.SQL("""select count(*)
                             from {}
                            where {} {} {}""") \
                   .format(sql.Identifier(table_indexed),
                           sql.Identifier(column),
                           sql.SQL(operand),
                           sql.Placeholder())
        start_time = time.time()
        cursor.execute(query, check_value)
        operands_durations['operand'] = (time.time - start_time).__round__(2)

    return operands_durations


def indexes_check(index_type: str,
                  cursor: connect,
                  columns_indexed: List,
                  table_indexed: str,
                  table_statistic: str) -> None:
    for column in columns_indexed:
        datatype = column.rstrip('0')
        index_creation_duration = index_make_create_duration(table_indexed, index_type, column, datatype, cursor)
        operands_durations = operands_time_execution(datatype)

        insert_statistic(table_statistic, index_type, datatype, index_creation_duration, cursor, **operands_durations)





with make_conn() as cursor:
    fields = ['IndexType','DataType','CreationTime']
    data = ('hash', 'varchar', 37.51)
    query = sql.SQL('insert into {} ({}) values {}') \
                .format(sql.Identifier('measured'),
                        sql.SQL(', ').join(map(sql.Identifier, fields)),
                        sql.SQL(', ').join(sql.Placeholder() * len(fields)))

    print(query.as_string(cursor))
    # print(cursor.mogrify(query, data))
    # cursor.execute(query, data)
    # print(type(cursor.fetchone()), cursor.fetchone()[0])
