from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, Enum, Float,\
    select, and_, desc, func

meta = MetaData()
engine = create_engine('postgresql://flask:flask@localhost/flask_base', echo=True)
dataset = Table(
    'dataset', meta,
    Column('id', Integer, primary_key=True),
    Column('date', Date),
    Column('channel', String(50), nullable=False),
    Column('country', String(2), nullable=False),
    Column('os', Enum('ios', 'android', name='os')),
    Column('impressions', Integer, nullable=False),
    Column('clicks', Integer, nullable=False),
    Column('installs', Integer, nullable=False),
    Column('spend', Float, nullable=False),
    Column('revenue', Float, nullable=False)
)


def get_all():
    s = 'dataset.select()'
    conn = engine.connect()
    result = conn.execute(eval(s))
    for row in result:
        print(row)


def main_constructor(values):
    where_query = order_query = group_query = ''
    select_query = 'dataset.select()'

    if 'cols' in values:
        labels, cols_query = get_cols(values['cols'], [])
        print(f'cols_query = {cols_query}')
        select_query = f'select([{cols_query}])'
        print(f'select_query = {select_query}')
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
    print(f'query before = {query}')
    for label in labels:
        replace_string = f'dataset.c.{label}'
        if replace_string in query:
            query = query.replace(replace_string, f'"{label}"')
    print(f'query after = {query}')
    return query


def prepare_cols(col):
    if '>=' in col or '<=' in col:
        return
    elif '=' in col:
        col = col.replace('=', '==')
        col = col.replace('date_from==', 'date>=')
        col = col.replace('date_to==', 'date<=')
    return col

def get_cols(cols, labels):
    print(f'cols before {cols}')
    result_cols = ''
    for col in cols.split():
        print(f'COL = {col}')
        if 'sum' in col:
            if ':' in col:
                cpi_cols = get_cpi(col)
                labels.append('CPI')
                result_cols += cpi_cols
                continue
            col = col.replace('sum(', '').replace(')', '')
            result_cols += f'func.sum(dataset.c.{col}).label("{col}"),'
            labels.append(col)
            continue

        if 'desc(' in col:
            col = col.replace('desc(', '').replace(')', '')
            result_cols += 'desc(dataset.c.' + col + '),'
        else:
            result_cols += 'dataset.c.' + col + ','
    print(f'labels = {labels}')
    print(f'cols after {result_cols}')
    if labels:
        return labels, result_cols[:-1]
    else:
        return result_cols[:-1]


def get_cpi(col):
    # If we have (revenue/installs) it returns (dataset.c.revenue / dataset.c.installs)
    col = col.replace('sum(', '')
    cols = col.split(':')
    result_cols = ''
    for item in cols:
        item = f'dataset.c.{item}'
        result_cols = f'{result_cols}{item}/'
    result_cols = 'func.sum(' + result_cols[:-1] + '.label("CPI"),'
    return result_cols


def get_result(where_query, group_query, order_query, select_query):
    conn = engine.connect()
    query = select_query + where_query + group_query + order_query
    print(query)
    result = conn.execute(eval(query))
    return result