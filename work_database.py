import psycopg2


class workWithDatabase:

    def __init__(self):
        self.conn = psycopg2.connect(
                database='person_database',
                user='Nikolay_VK',
                password='12345678',
                host='127.0.0.1',
                port='5432',
            )
        self.c = self.conn.cursor()

    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXIST persons (id integer primary key, ids_search json)""")
        self.conn.commit()

    def insert_data(self, id, ids_search):
        self.c.execute("""INSERT INTO persons (id, ids_search) VALUES (%s,%s)""", (id, ids_search))
        self.conn.commit()

    def update_date(self, ids_search, id):
        self.c.execute("""UPDATE persons SET ids_search=%s WHERE id=%s""", (ids_search, id))
        self.conn.commit()

    def select_data(self, id):
        self.c.execute("""SELECT ids_search FROM persons WHERE id=%s""", (id,))
        return self.c.fetchone()
