from lib import indexes_check
from connection import make_conn

TABLE_INDEXED = 'test_table'
TABLE_STATISTIC = 'measured'

COLUMNS_INDEXED = ['varchar0', 'integer0', 'date0']
INDEXES = ['gin', 'brin', 'gist', 'bloom', 'rum', 'hash', 'btree']

OPERAND_CHECK_VALUES = {'varchar': 'Allyson Lowe',
                        'integer': 23579207,
                        'date': '2023-11-29'}

if __name__=='__main__':
    with make_conn() as cursor:
        for index in INDEXES:
            indexes_check(index_type=index, cursor=cursor,
                          columns_indexed=COLUMNS_INDEXED,
                          table_indexed=TABLE_INDEXED,
                          table_statistic=TABLE_STATISTIC)

