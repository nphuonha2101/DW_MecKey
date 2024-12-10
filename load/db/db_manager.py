import pymysql

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect_to_db(self, host, user, password, db, port=3306):
        """Connect to database"""
        try:
            self.connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                db=db,
                port=port,
            )
            self.cursor = self.connection.cursor()
        except Exception as e:
            raise RuntimeError(f"{e}. Please check your connection information and try again. (Make sure connection information in .env file is correct)")

    def close_connection(self):
        """Close connection"""
        self.cursor.close()
        self.connection.close()

    def call_procedure(self, procedure_name, args=None):
        """Call a procedure. Example: call_procedure('procedure_name', (arg1, arg2, arg3))"""
        try:
            self.cursor.callproc(procedure_name, args)
            self.connection.commit()
            return self.cursor.fetchall()
        except Exception as e:
            raise RuntimeError(e)

    def call_query(self, query, args=None):
        """Call a query. Example: call_query('SELECT * FROM table WHERE id = %s', (id,))"""
        try:
            self.cursor.execute(query, args)
            self.connection.commit()
            return self.cursor.fetchall()
        except Exception as e:
            raise RuntimeError(e)

    def call_function(self, function_name, args=None):
        """Call a function. Example: call_function('function_name', (arg1, arg2, arg3))"""
        try:
            self.cursor.callfunc(function_name, args)
            self.connection.commit()
            return self.cursor.fetchall()
        except Exception as e:
            raise RuntimeError(e)


