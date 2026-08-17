import pyodbc 
import argparse
from credentials import server, database, login, password


def get_operations_count(*, cursor, order_id):
    statement = f'''S
        SELECT count(id_operation) 
        FROM database.dbo.info_table
        WHERE id_order = {order_id}
    '''
    cursor.execute(statement)
    data = cursor.fetchone()
    return data[0]


def get_order_is_active(*, cursor, order_id):
    statement = f'''
        SELECT is_active 
        FROM database.dbo.info_table 
        WHERE id_order = {order_id}
    '''
    cursor.execute(statement)
    data = cursor.fetchall()
    active_cut = []
    for ticket in data:
        active_cut.append(ticket.is_active)
    return active_cut


def get_payment_info(*, cursor, order_id):
    statement = f'''
        SELECT order_id, payment_method, status, refund_sum 
        FROM database2.dbo.transactions 
        WHERE order_id = {order_id}
    '''
    cursor.execute(statement)
    data = cursor.fetchall()
    return data[0]


def get_transaction_state(*, cursor, tickets_count, index, payment_info):
    statement = f'''
        SELECT code, index, description, status
        FROM database2.dbo.transaction_status
        WHERE index = {payment_info.index}
    '''
    cursor.execute(statement)
    data_transaction_state = cursor.fetchall()
    state = data_transaction_state[0]

    print(f'payment order id: {payment_info.order_id}')
    print(f'tickets count: {tickets_count} | index {index}')
    print(f'payment method: {payment_info.way}')
    print(f'paybox state:{payment_info.index}, {state.code}, {state.description}')
    print(f'paybox refund amount: {payment_info.refund_amount}')
    print()


def get_payments(*, cursor, order_id):
    statement = f'''
        SELECT sum(Amount) 
        FROM database.dbo.payments 
        WHERE id_order = {order_id} AND type <> 1
    '''
    cursor.execute(statement)
    data = cursor.fetchone()
    data_trimmed = data[0]
    print('payments total+:', str(data_trimmed))

    statement = f'''
        SELECT sum(Amount) 
        FROM database.dbo.payments 
        WHERE id_order = {order_id} AND payment_method_id = 3
    '''
    cursor.execute(statement)
    data = cursor.fetchone()
    data_trimmed = data[0]
    print('payments cashback+:', str(data_trimmed))

    statement = f'''
        SELECT sum(Amount) 
        FROM database.dbo.payments 
        WHERE id_order = {order_id} AND type = 3
    '''
    cursor.execute(statement)
    data = cursor.fetchone()
    data_trimmed = data[0]
    print('payments service fee+:', str(data_trimmed))

    statement = f'''
        SELECT sum(Amount) 
        FROM database.dbo.payments 
        WHERE id_order = {order_id} AND type = 1
    '''
    cursor.execute(statement)
    data = cursor.fetchone()
    data_trimmed = data[0]
    print('payments total-:', str(data_trimmed))


def get_return_info(*, cursor, order_id):
    statement = f'''
        SELECT Price, IdPerformance 
        FROM database.dbo.Returns 
        WHERE id_operation IN (
            SELECT id_operation 
            FROM database.dbo.info_table
            WHERE id_order = {order_id})
    '''
    cursor.execute(statement)
    data = cursor.fetchall()
    if data:
        data_trimmed = data[0]
        print('returns.price:', str(data_trimmed.Price))
        print('returns.id_performance:', str(data_trimmed.IdPerformance))
    else:
        print('NO REFUND DATA')


def run(*, cursor, order_id):
    tickets_count = get_tickets_count(
        cursor=cursor,
        order_id=order_id,
    )
    topical = get_order_is_topical(
        cursor=cursor,
        order_id=order_id,
    )
    paybox_info = get_paybox_info(
        cursor=cursor,
        order_id=order_id,
    )
    get_transaction_state(
        cursor=cursor,
        tickets_count=tickets_count,
        topical=topical,
        paybox_info=paybox_info,
    )
    get_payments(
        cursor=cursor,
        order_id=order_id,
    )
    get_return_info(
        cursor=cursor,
        order_id=order_id,
    )


def main(*, order_id):
    creds = f'''
        DRIVER={{ODBC Driver 17 for SQL Server}};
        SERVER={server};
        DATABASE={database};
        UID={login};
        PWD={password}
    '''
    connection = pyodbc.connect(creds)
    cursor = connection.cursor()

    try:
        run(cursor=cursor, order_id=order_id)
    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('id', help='order id here', type=int)
    args = parser.parse_args()

    main(order_id=args.id)
