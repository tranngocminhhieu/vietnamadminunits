import sqlite3
from pathlib import Path

MODULE_DIR = Path(__file__).parent.parent

def query(sql: str):
    '''
    :param sql: SQL
    :return: JSON
    '''
    with sqlite3.connect(MODULE_DIR / 'data/dataset.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        result = cursor.execute(sql)
        records = [dict(r) for r in result.fetchall()]
        return records

def get_data(fields='*', table: str='admin_units'):
    '''
    :param fields: string or list.
    :param table: admin_units or admin_units_63
    :return: JSON
    '''
    if isinstance(fields, list):
        fields = ','.join(fields)
    sql = f'SELECT DISTINCT {fields} FROM [{table}]'
    records = query(sql)
    return records


if __name__ == '__main__':
    print(get_data(fields='*', table='admin_units'))