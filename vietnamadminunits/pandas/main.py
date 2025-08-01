from ..parser.parser_34 import parse_address_34
from ..parser.parser_63 import parse_address_63
from ..converter import convert_address
import warnings

def standardize_admin_unit_columns(df, province: str, district: str=None, ward: str=None, mode: int=34, inplace=False, prefix: str='standardized_', suffix :str='', short_name=True, convert_to_latest=False):
    '''
    Standardize the admin unit columns of a DataFrame.

    :param df: pd.DataFrame.
    :param province: Province column name.
    :param district: District column name.
    :param ward: Ward column name.
    :param mode: 34 or 63.
    :param inplace: Replace values of old columns with standardized values.
    :param prefix: Add prefix to column names if inplace = False.
    :param suffix: Add suffix to column names if inplace = False.
    :param short_name: Get short name or long name of admin unit.
    :param convert_to_latest: Convert old admin unit to new admin unit.
    :return: pd.DataFrame
    '''

    # INITIATIVE VARS
    admin_unit_columns = [l for l in [ward, district, province] if l]  # Remove None
    latest_mode = 34

    # RAISE
    if not province:
        raise ValueError('The name of the province column must be provided')

    if convert_to_latest:
        if mode != 63:
            raise ValueError('At present, only mode 63 is supported for the conversion to the latest version.')
        if not district or not ward:
            warnings.warn('The names of the District or Ward columns are not provided. Therefore, only the Province level will be converted.', UserWarning)
    else:
        if mode not in [34, 63]:
            raise ValueError('Mode must be 34 or 63.')

        if mode == 34 and district:
            arnings.warn('Mode 34 is not support with the district level.', UserWarning)

        if mode == 63 and ward and not district:
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
    if convert_to_latest:
        parser = lambda x: convert_address(address=x, from_mode=mode, to_mode=latest_mode)
    else:
        if mode == 34:
            level = 2 if ward else 1
            parser = lambda x: parse_address_34(address=x, level=level, keep_street=False)
        elif mode == 63:
            level = 3 if ward else 2 if district else 1
            parser = lambda x: parse_address_63(address=x, level=level, keep_street=False)
        else:
            raise ValueError("Mode must be 34 or 63.")

    df_address['admin_unit'] = df_address['address'].apply(parser)


    # SPLIT ADMIN UNIT TO COLUMNS
    for col_type, col_name in zip(['province', 'district', 'ward'], [province, district, ward]):
        if not col_name:
            continue
        if col_type == 'district' and convert_to_latest:
            continue  # skip if in convert_to_latest mode

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