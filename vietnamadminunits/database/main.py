import sqlite3
from pathlib import Path

MODULE_DIR = Path(__file__).parent.parent


def query(sql: str):
    '''
    Retrieve administrative unit data from the database.

    :param sql: SQL string

    :return: Data as a list of JSON-like dictionaries. It is compatible with `pd.DataFrame`.
    '''
    with sqlite3.connect(MODULE_DIR / 'data/dataset.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        result = cursor.execute(sql)
        records = [dict(r) for r in result.fetchall()]
        return records


def get_data(fields='*', table: str='admin_units', limit: int=None):
    '''
    Retrieve administrative unit data from the database.

    :param fields: Column name(s) to retrieve.
    :param table: Table name, either `'admin_units'` (34-province) or `'admin_units_legacy'` (63-province).

    :return: Data as a list of JSON-like dictionaries. It is compatible with `pd.DataFrame`.
    '''
    if isinstance(fields, list):
        fields = ','.join(fields)
    sql = f'SELECT DISTINCT {fields} FROM [{table}]'
    if limit:
        sql += f' LIMIT {limit}'
    records = query(sql)
    return records