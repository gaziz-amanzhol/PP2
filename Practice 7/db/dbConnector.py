import psycopg2
from config.config import load_config
from db.PhoneBook import PhoneBook


class DBConnector:
    def __init__(self):
        self.config = load_config()

    def createTable(self):
        sql = '''
            CREATE SEQUENCE IF NOT EXISTS s;
            CREATE TABLE IF NOT EXISTS phone_nums (
                id INTEGER DEFAULT nextval('s') PRIMARY KEY,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                phone VARCHAR(13) NOT NULL
        );
        '''
        try:
            with psycopg2.connect(**self.config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                conn.commit()
        except Exception as e:
            print("Error on creating new table ", e)

    def getAllRecords(self):
        sql = "SELECT * FROM phone_nums ORDER BY id ASC"
        try:
            with psycopg2.connect(**self.config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    rows_tuple = cur.fetchall()
                    all_users = [PhoneBook(id=row[0], first_name=row[1], last_name=row[2],
                                           phone=row[3]) for row in rows_tuple]
                    return all_users
        except Exception as e:
            print("Error on listing all users ", e)

    def isUserExist(self, user: PhoneBook):
        sql = '''
            SELECT * 
            FROM phone_nums 
            WHERE first_name=%s
        '''
        try:
            with psycopg2.connect(**self.config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (user.first_name,))
                    row = cur.fetchone()  # Use fetchone for a single result
                    return True if row else False
        except Exception as e:
            print("Error on creating new SCORE RACE table ", e)
            return False

    def addNewUser(self, user: PhoneBook):
        sql = '''
                           INSERT INTO phone_nums(first_name, last_name, phone) 
                           VALUES(%s, %s, %s)
                        '''
        try:
            with psycopg2.connect(**self.config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (user.first_name, user.last_name, user.phone))
                    conn.commit()
        except Exception as e:
            print("Error on creating new SCORE RACE table ", e)

    def update(self, user: PhoneBook):
        sql = '''
                UPDATE phone_nums 
                SET phone=%s 
                WHERE first_name=%s 
                '''
        try:
            with psycopg2.connect(**self.config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (user.phone, user.first_name))
                conn.commit()
        except Exception as e:
            print("Error on updating new user ", e)

    def insertManyUsers(self, all_users: list[PhoneBook]):
        incorrect_users = []
        sql = '''
            INSERT INTO phone_nums(first_name, last_name, phone) 
            VALUES (%s, %s, %s) 
        '''
        try:
            with psycopg2.connect(**self.config) as conn:
                with conn.cursor() as cur:
                    for user in all_users:
                        if ((user.phone.startswith("+7") and len(user.phone) == 12) or (user.phone.startswith("8")
                                                                                        and len(
                                    user.phone) == 11)) and user.phone[1:].isdigit():
                            cur.execute(sql, (user.first_name, user.last_name, user.phone))
                        else:
                            incorrect_users.append(user)
                conn.commit()
        except Exception as e:
            print("Error on inserting many user ", e)

        return incorrect_users

    def getLimitOffset(self, limit: int, offset: int):
        sql = '''
               SELECT * 
               FROM phone_nums LIMIT %s OFFSET %s
                '''
        try:
            with psycopg2.connect(**self.config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (limit, offset))
                    rows_tuple = cur.fetchall()
                    all_users = [PhoneBook(id=row[0], first_name=row[1], last_name=row[2],
                                           phone=row[3]) for row in rows_tuple]
                    return all_users
        except Exception as e:
            print("Error on getLimitOffset ", e)

    def deleteUserByFirstName(self, first_name: str):
        sql = "DELETE FROM phone_nums WHERE first_name=%s "
        try:
            with psycopg2.connect(**self.config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (first_name,))
                conn.commit
        except Exception as e:
            print("Error on listing all users ", e)

    def deleteUserByPhone(self, phone):
        sql = "DELETE FROM phone_nums WHERE phone=%s"
        try:
            with psycopg2.connect(**self.config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (phone,))
                conn.commit
        except Exception as e:
            print("Error on listing all users ", e)
