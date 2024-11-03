from abc import ABC, abstractmethod

from injector import inject

from db.db_manager import DatabaseManager
import os
from dotenv import load_dotenv

from event.event import Event
from event.event_bus import EventBus
from event.event_level import EventLevel
from event.event_type import EventType
from model.file_config import FileConfig
from model.file_log import FileLog
from services.status.service_status import ServiceStatus
from services.status.status_message import status_message

load_dotenv()

class AbstractService(ABC):

    @inject
    def __init__(self, database_manager: DatabaseManager, event_bus: EventBus):
        self.database_manager = database_manager
        self.event_bus = event_bus

    @abstractmethod
    def run(self):
        pass

    def update_progress_to_ui(self, event_level: EventLevel, message):
        """Update service progress to UI (Ex: Ready extract, Extracting, Successful extract, Failed extract, ...)"""
        self.event_bus.publish(EventType.SERVICE_NOTIFY_PROGRESS, Event(event_level, message))

    def update_log_to_ui(self, event_level: EventLevel, message):
        """Update service log to UI. (Ex: Error fetching {url}: {e})"""
        self.event_bus.publish(EventType.SERVICE_NOTIFY_LOG, Event(event_level, message))

    def get_file_config(self, feed_key):
        """Get file config by feed key"""
        try :
            self.database_manager.connect_to_db(
                os.getenv('CONTROL_DB_HOST'),
                os.getenv('CONTROL_DB_USER'),
                os.getenv('CONTROL_DB_PASSWORD'),
                os.getenv('CONTROL_DB_NAME')
            )

            query = f"SELECT * FROM {os.getenv('FILE_CONFIG_TABLE_NAME')} WHERE feed_key = %s"
            result = self.database_manager.call_query(query, (feed_key,))

            file_config = FileConfig.from_db(result[0])

            return file_config
        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Error getting file config: {e}")
            raise RuntimeError(e)
        finally:
            self.database_manager.close_connection()

    def create_file_log(self, id_config: int, status: ServiceStatus, file_path: str):
        """Create a new file log in the database"""
        try:
            self.database_manager.connect_to_db(
                os.getenv('CONTROL_DB_HOST'),
                os.getenv('CONTROL_DB_USER'),
                os.getenv('CONTROL_DB_PASSWORD'),
                os.getenv('CONTROL_DB_NAME')
            )

            query = f"INSERT INTO {os.getenv('FILE_LOG_TABLE_NAME')} (id_config, status, file_path, description) VALUES (%s, %s, %s, %s)"
            self.database_manager.call_query(query, (id_config, ServiceStatus.get_value(status), file_path, status_message[status]))

            last_id_query = "SELECT LAST_INSERT_ID()"
            last_id_result = self.database_manager.call_query(last_id_query)
            last_id = last_id_result[0][0]

            return last_id
        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Error creating file log: {e}")
            raise RuntimeError(e)
        finally:
            self.database_manager.close_connection()

    def get_file_log(self, id: int):
        """Get file log by id"""
        try:
            self.database_manager.connect_to_db(
                os.getenv('CONTROL_DB_HOST'),
                os.getenv('CONTROL_DB_USER'),
                os.getenv('CONTROL_DB_PASSWORD'),
                os.getenv('CONTROL_DB_NAME')
            )

            query = f"SELECT * FROM {os.getenv('FILE_LOG_TABLE_NAME')} WHERE id = %s"
            results = self.database_manager.call_query(query, (id,))
            file_log = FileLog.from_db(results[0])

            return file_log
        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Error getting file log: {e}")
            raise RuntimeError(e)
        finally:
            self.database_manager.close_connection()

    def get_file_log_by_status_and_feed_key(self, status: ServiceStatus, feed_key: str):
        """
        Get file log by status and feed key. For example: Get file log by status = ServiceStatus.EXTRACTED and feed key = 'akko'
        . It's necessary to get the latest file log by status and feed key if another service starts to run
        """
        try:
            self.database_manager.connect_to_db(
                os.getenv('CONTROL_DB_HOST'),
                os.getenv('CONTROL_DB_USER'),
                os.getenv('CONTROL_DB_PASSWORD'),
                os.getenv('CONTROL_DB_NAME')
            )   

            query = f"SELECT * FROM {os.getenv('FILE_LOG_TABLE_NAME')} WHERE status = %s AND id_config = (SELECT id FROM {os.getenv('FILE_CONFIG_TABLE_NAME')} WHERE feed_key = %s)"
            results = self.database_manager.call_query(query, (ServiceStatus.get_value(status), feed_key))
            file_log = FileLog.from_db(results[0])

            return file_log
        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Error getting file log by status and feed key: {e}")
            raise RuntimeError(e)
        finally:
            self.database_manager.close_connection()



