from ..parser import parse_address, ParseMode
from ..converter import convert_address, ConvertMode
import warnings
from typing import Union

def standardize_admin_unit_columns(df, province: str, district: str=None, ward: str=None, parse_mode: Union[str, ParseMode]=ParseMode.latest(), convert_mode: Union[str, ConvertMode]=None, inplace=False, prefix: str='standardized_', suffix :str='', short_name: bool=True):
    '''
    Standardizes administrative unit columns (`province`, `district`, `ward`) in a DataFrame.

    :param df: `pandas.DataFrame` object.
    :param province: Province column name.
    :param district: District column name.
    :param ward: Ward column name.
    :param parse_mode: One of the `ParseMode` values. Use `'LEGACY'` for the 63-province format (pre-merger), or `'FROM_2025'` for the new 34-province format. Default is `ParseMode.latest()`.
    :param convert_mode: One of the `ConvertMode` values. Currently, only `'CONVERT_2025'` is supported.
    :param inplace: Replace the original columns with standardized values instead of adding new ones.
    :param prefix: Add a prefix to the column names if `inplace=False`.
    :param suffix: Add a suffix to the column names if `inplace=False`.
    :param short_name: Use short or full names for standardized administrative units.

    :return: `pandas.DataFrame` object.
    '''

    # INITIATIVE VARS
    admin_unit_columns = [l for l in [ward, district, province] if l]  # Remove None

    # RAISE
    if not province:
        raise ValueError('The name of the province column must be provided')

    if convert_mode:
        if not district or not ward:
            warnings.warn('The names of the District or Ward columns are not provided. Therefore, only the Province level will be converted.', UserWarning)
    else:
        if parse_mode in [ParseMode.FROM_2025, ParseMode.FROM_2025.value] and district:
            warnings.warn('Mode 34 is not support with the district level.', UserWarning)

        if parse_mode in [ParseMode.LEGACY, ParseMode.LEGACY.value] and ward and not district:
            raise ValueError('The name of the district column must be provided in order to parse the ward data.')



    # INITIATIVE VARS
    df = df.copy()
    original_columns = df.columns.tolist()


    # CREATE ADDRESS COLUMN, IT IS MERGING KEY
    df['address'] = ''
    for column in admin_unit_columns:
        df['address'] += ',' + df[column].fillna('')
    df_address = df[['address']].drop_duplicates()


    # PARSE ADDRESS TO NEW ADMIN UNIT
    if convert_mode:
        parser = lambda x: convert_address(address=x, mode=convert_mode)
    else:
        if parse_mode in [ParseMode.FROM_2025, ParseMode.FROM_2025.value]:
            level = 2 if ward else 1
        elif parse_mode in [ParseMode.LEGACY, ParseMode.LEGACY.value]:
            level = 3 if ward else 2 if district else 1
        parser = lambda x: parse_address(address=x, mode=parse_mode, level=level, keep_street=False)


    df_address['admin_unit'] = df_address['address'].apply(parser)


    # SPLIT ADMIN UNIT TO COLUMNS
    for col_type, col_name in zip(['province', 'district', 'ward'], [province, district, ward]):
        if not col_name:
            continue
        if col_type == 'district' and convert_mode:
            continue  # skip if in convert_mode mode

        attr = f"{'short_' if short_name else ''}{col_type}"
        target_col = col_name if inplace else f"{prefix}{col_name}{suffix}"
        df_address[target_col] = df_address['admin_unit'].apply(lambda x: getattr(x, attr) if x else None)


    # ADD NEW ADMIN UNIT COLUMNS TO DF
    # Drop original columns (province/district/ward) if inplace
    if inplace:
        df.drop(columns=admin_unit_columns, inplace=True, errors='ignore')

    # Merge standardized columns to df
    df = df.merge(df_address.drop(columns=['admin_unit']), on='address', how='left')

    # Drop address columns
    df.drop(columns=['address'], inplace=True)

    # Keep original column position if inplace
    if inplace:
        original_columns = [col for col in original_columns if col in df.columns]
        df = df[original_columns]

    return df