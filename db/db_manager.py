import pymysql
from numpy.f2py.auxfuncs import throw_error


class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect_to_db(self, host, user, password, db):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db
        )
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def call_procedure(self, procedure_name, args=None):
        try:
            self.cursor.callproc(procedure_name, args)
            self.connection.commit()
            return self.cursor.fetchall()
        except Exception as e:
            raise RuntimeError(e)

    def call_query(self, query, args=None):
        try:
            self.cursor.execute(query, args)
            self.connection.commit()
            return self.cursor.fetchall()
        except Exception as e:
            raise RuntimeError(e)

    def call_function(self, function_name, args=None):
        try:
            self.cursor.callfunc(function_name, args)
            self.connection.commit()
            return self.cursor.fetchall()
        except Exception as e:
            raise RuntimeError(e)

