from ..parser.parser_34 import parse_address_34
from ..parser.parser_63 import parse_address_63

def standardize_admin_unit_columns(df, province: str, district: str=None, ward: str=None, mode: int=34, inplace=False, prefix: str='standardized_', suffix :str='', short_name=True):
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
    :return: pd.DataFrame
    '''

    if not province:
        raise ValueError('Province column name must be provided.')

    if mode not in [34, 63]:
        raise ValueError('Mode must be 34 or 63.')

    if mode == 34 and district:
        raise ValueError('Mode 34 not works with district.')

    if mode == 63 and province and ward and not district:
        raise ValueError('District column name must be provided to parse ward')

    admin_unit_columns = [ward, district, province] if mode == 63 else [ward, province]
    admin_unit_columns = [l for l in admin_unit_columns if l] # Remove None
    original_columns = df.columns.tolist()

    # Create distinct address
    df['address'] = ''
    for column in admin_unit_columns:
        df['address'] += ',' + df[column].fillna('')
    df_address = df[['address']].drop_duplicates()

    # Parse address to admin unit
    if mode == 34:
        if ward:
            level = 2
        else:
            level = 1
        df_address['admin_unit'] = df_address['address'].apply(lambda x: parse_address_34(address=x, level=level, keep_street=False))

    if mode == 63:
        if ward:
            level = 3
        elif district:
            level = 2
        else:
            level = 1
        df_address['admin_unit'] = df_address['address'].apply(lambda x: parse_address_63(address=x, level=level, keep_street=False))

    # Get admin unit level
    if province:
        if short_name:
            df_address[province if inplace else f"{prefix}{province}{suffix}"] = df_address['admin_unit'].apply(lambda x: x.short_province if x else None)
        else:
            df_address[province if inplace else f"{prefix}{province}{suffix}"] = df_address['admin_unit'].apply(lambda x: x.province if x else None)
    if district:
        if short_name:
            df_address[district if inplace else f"{prefix}{district}{suffix}"] = df_address['admin_unit'].apply(lambda x: x.short_district if x else None)
        else:
            df_address[district if inplace else f"{prefix}{district}{suffix}"] = df_address['admin_unit'].apply(lambda x: x.district if x else None)
    if ward:
        if short_name:
            df_address[ward if inplace else f"{prefix}{ward}{suffix}"] = df_address['admin_unit'].apply(lambda x: x.short_ward if x else None)
        else:
            df_address[ward if inplace else f"{prefix}{ward}{suffix}"] = df_address['admin_unit'].apply(lambda x: x.ward if x else None)


    # Drop admin_unit column
    df_address.drop(columns=['admin_unit'], inplace=True)

    # Drop old column if inplace
    if inplace:
        df.drop(columns=admin_unit_columns, inplace=True, errors='ignore')

    # Add standardized admin unit columns to original df
    df = df.merge(df_address, on='address', how='left')

    # Drop address column
    df.drop(columns=['address'], inplace=True)

    # Keep column position if inplace
    if inplace:
        df = df[original_columns]

    return df