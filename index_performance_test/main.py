from lib import indexes_check
from conn import make_conn

TABLE_INDEXED = 'test_table'
TABLE_STATISTIC = 'measured'

COLUMNS_INDEXED = ['varchar0', 'integer0', 'date0']
# INDEXES = ['gin', 'gist', 'bloom', 'rum', 'brin', 'hash', 'btree']
INDEXES = ['brin', 'hash', 'btree']

OPERAND_CHECK_VALUES = {'varchar': 'Xiomara Ware',
                        'integer': 38346606,
                        'date': '2023-07-03'}

if __name__=='__main__':
    with make_conn() as cursor:
        for index in INDEXES:
            indexes_check(index_type=index, cursor=cursor,
                          columns_indexed=COLUMNS_INDEXED,
                          table_indexed=TABLE_INDEXED,
                          table_statistic=TABLE_STATISTIC)

