from abc import ABC, abstractmethod

from injector import inject
from numpy.f2py.auxfuncs import throw_error

from db.db_manager import DatabaseManager
import os
from dotenv import load_dotenv

from event.event import Event
from event.event_bus import EventBus
from event.event_level import EventLevel
from event.event_type import EventType
from model.file_config import FileConfig

load_dotenv()

class AbstractService(ABC):

    @inject
    def __init__(self, database_manager: DatabaseManager, event_bus: EventBus):
        self.database_manager = database_manager
        self.event_bus = event_bus

    @abstractmethod
    def run(self):
        pass

    def update_ui(self, event_level, message):
        """Gửi thông điệp đến UI."""
        self.event_bus.publish(EventType.SERVICE_NOTIFY, Event(event_level, message))

    def get_file_config(self, feed_key):
        try :
            self.database_manager.connect_to_db(
                os.getenv('CONTROL_DB_HOST'),
                os.getenv('CONTROL_DB_USER'),
                os.getenv('CONTROL_DB_PASSWORD'),
                os.getenv('CONTROL_DB_NAME')
            )

            query = f"SELECT * FROM ${os.getenv('FILE_CONFIG_TABLE_NAME')} WHERE feed_key = %s"
            result = self.database_manager.call_query(query, (feed_key,))

            file_config = FileConfig(*result[0])

            self.database_manager.close_connection()
            return file_config
        except Exception as e:
            throw_error(e)
        finally:
            self.database_manager.close_connection()

    def create_file_log(self, id_config, status, file_path):
        try:
            self.database_manager.connect_to_db(
                os.getenv('CONTROL_DB_HOST'),
                os.getenv('CONTROL_DB_USER'),
                os.getenv('CONTROL_DB_PASSWORD'),
                os.getenv('CONTROL_DB_NAME')
            )

            query = f"INSERT INTO ${os.getenv('FILE_LOG_TABLE_NAME')} (id_config, status, file_path) VALUES (%s, %s, %s)"
            self.database_manager.call_query(query, (id_config, status, file_path))

            last_id_query = "SELECT LAST_INSERT_ID()"
            last_id_result = self.database_manager.call_query(last_id_query)
            last_id = last_id_result[0][0]

            self.database_manager.close_connection()
            return last_id
        except Exception as e:
            throw_error(e)
        finally:
            self.database_manager.close_connection()

    def update_file_log(self, id, status):
        try:
            self.database_manager.connect_to_db(
                os.getenv('CONTROL_DB_HOST'),
                os.getenv('CONTROL_DB_USER'),
                os.getenv('CONTROL_DB_PASSWORD'),
                os.getenv('CONTROL_DB_NAME')
            )

            query = f"UPDATE ${os.getenv('FILE_LOG_TABLE_NAME')} SET status = %s WHERE id = %s"
            self.database_manager.call_query(query, (status, id))

            self.database_manager.close_connection()
        except Exception as e:
            throw_error(e)
        finally:
            self.database_manager.close_connection()

    def get_file_log(self, id):
        try:
            self.database_manager.connect_to_db(
                os.getenv('CONTROL_DB_HOST'),
                os.getenv('CONTROL_DB_USER'),
                os.getenv('CONTROL_DB_PASSWORD'),
                os.getenv('CONTROL_DB_NAME')
            )

            query = f"SELECT * FROM ${os.getenv('FILE_LOG_TABLE_NAME')} WHERE id = %s"
            result = self.database_manager.call_query(query, (id,))

            self.database_manager.close_connection()
            return result
        except Exception as e:
            throw_error(e)
        finally:
            self.database_manager.close_connection()





