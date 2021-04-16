from sqlalchemy import select, and_, desc, func
from config import dataset, engine


def main_constructor(values):
    '''
    compare a request to database from received  values
    returns result of request
    '''
    where_query = order_query = group_query = ''
    select_query = 'dataset.select()'

    if 'cols' in values:
        labels, cols_query = get_cols(values['cols'], [])
        select_query = f'select([{cols_query}])'
    if 'where' in values:
        where_cols = prepare_cols(values['where'])
        where_cols = get_cols(where_cols, None)
        where_query = f'.where(and_({where_cols}))'
    if 'order' in values:
        order_cols = get_cols(values['order'], None)
        order_cols = prepare_cols(order_cols)
        order_query = f'.order_by({order_cols})'
        order_query = replace_labels(order_query, labels)
    if 'group' in values:
        group_cols = get_cols(values['group'], None)
        group_query = f'.group_by({group_cols})'
        group_query = replace_labels(group_query, labels)
    result = get_result(where_query, order_query, group_query, select_query)
    return result


def replace_labels(query, labels):
    '''
    add "label" in query
    '''
    for label in labels:
        replace_string = f'dataset.c.{label}'
        if replace_string in query:
            query = query.replace(replace_string, f'"{label}"')

    return query


def prepare_cols(col):
    '''
    find and replace '=' to '==' and date_from, date_to to date
    '''
    if '>=' in col or '<=' in col:
        return
    elif '=' in col:
        col = col.replace('=', '==')
        col = col.replace('date_from==', 'date>=')
        col = col.replace('date_to==', 'date<=')
    return col


def get_cols(cols, labels):
    '''
    this functions separating parameters an add necessary prefix to them
    "desc", "sum", "dataset.c"
    '''
    result_cols = ''
    for col in cols.split():
        if 'sum' in col:
            col, label = modify_col(col)
            result_cols += f'func.sum({col}'
            labels.append(label)
            continue
        elif labels == [] and '(' in col:
            col, label = modify_col(col)
            result_cols = f'{result_cols}({col}'
            labels.append(label)
            continue
        if 'desc(' in col:
            col = col.replace('desc(', '').replace(')', '')
            result_cols += 'desc(dataset.c.' + col + '),'
        else:
            result_cols += 'dataset.c.' + col + ','
    if labels:
        return labels, result_cols[:-1]
    else:
        return result_cols[:-1]


def modify_col(col):
    '''
    add labels if it needs, ad CPI. Modify query if '(" in it
    :returns query and label
    '''
    col = col.replace('sum', '').replace('(', '')
    items = col.split(':')
    result_cols = ''
    for item in items:
        res = f'dataset.c.{item}'
        result_cols = f'{result_cols}{res}/'
    if ':' in col:
        return f'{result_cols[:-1]}.label("CPI"),', 'CPI'
    else:
        return f'{result_cols[:-1]}.label("{item[:-1]}"),', item[:-1]


def get_cpi(col):
    # If we have (revenue/installs) it returns (dataset.c.revenue / dataset.c.installs).label("CPI")
    col = col.replace('sum(', '')
    cols = col.split(':')
    result_cols = ''
    for item in cols:
        item = f'dataset.c.{item}'
        result_cols = f'{result_cols}{item}/'
    result_cols = 'func.sum(' + result_cols[:-1] + '.label("CPI"),'
    return result_cols


def get_result(where_query, group_query, order_query, select_query):
    '''
    compile query by parts and execute it
    :returns result of DB request
    '''
    conn = engine.connect()
    query = select_query + where_query + group_query + order_query
    print(query)
    result = conn.execute(eval(query))
    return result
