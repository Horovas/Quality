import psycopg2
from playwright.sync_api import sync_playwright 
from credentials import server, database, login, password


URL = "https://delivery-on-demand.enterprise.com/feature/?checkpoint=overview"
transaction = None

def transaction_check(): 
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        captured_json = None

        url_part = "when-delivered"


        with page.expect_request(lambda request: url_part in request.url, timeout=15000) as first_request:
            print("Открываем главную страницу")

            # wait_until ["commit", "domcontentloaded", "load", "networkidle"]
            page.goto(URL, wait_until="load")
            print("Страница открыта, ожидаем появления нужного служебного запроса")

        captured_request = first_request.value
        print(f"Запрос обнаружен: {captured_request.url}")

        try:
            captured_json = captured_request.post_data_json
            print("Отправленный payload (Request JSON)")
            import pprint
            pprint.pprint(captured_json)
            
            transaction = captured_json["transactionId"]
            print(f"Нужная часть: {transaction}")

        except Exception as e:
            print(f"Ошибка. Не удалось прочитать JSON из тела запроса: {e}")
            print(f"Сырые данные: {captured_json.post_data}")

        browser.close()

    return transaction

def db_check(transaction):
    connection = psycopg2.connect(
        host=server,
        database=database,
        user=login,
        password=password
    )
    c = connection.cursor()
    
    db_request = f"""
        SELECT 
            agent_id,
            contract_no,
            transaction_id,
            delivery_id
        FROM database23.schema23.transaction_process
        WHERE transaction_id = (%s)
    """

    c.execute(db_request, (transaction,)) # so it is tuple
    data = c.fetchall()
    print(f"Данные в базе: {data}")

    if transaction == data[3]:
        print("Успешно. Данные в ответе JSON и в БД совпадают")
    else:
        print("Ошибка. Данные в ответе JSON и в БД не совпадают")

if __name__ == '__main__':
    transaction = transaction_check()
    db_check(transaction)
