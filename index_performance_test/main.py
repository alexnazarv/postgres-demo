from lib import indexes_check
from connection import make_conn

TABLE_INDEXED = 'testdb.public.test_table'
COLUMNS_INDEXED = ['varchar0', 'integer0', 'date0']

TABLE_STATISTIC = 'testdb.public.measured'
INDEXES = ['hash', 'B-tree', 'GIN', 'BRIN']

OPERAND_CHECK_VALUES = {'varchar': 'Allyson Lowe',
                        'integer': 23579207,
                        'date': '2023-11-29'}



# if __name__ == '__main__':
#     with make_conn() as cursor:
#         for index in INDEXES:
#             indexes_check(index=index, cursor=cursor, columns_indexed=COLUMNS_INDEXED)


