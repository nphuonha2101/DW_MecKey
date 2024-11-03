import os

from db.db_manager import DatabaseManager
from event.event_bus import EventBus
from event.event_level import EventLevel
from services.abstract_services import AbstractService
from services.status.service_status import ServiceStatus
from services.status.status_message import status_message


class LoadToWarehouse(AbstractService):
    def __init__(self, database_manager: DatabaseManager, event_bus: EventBus):
        super().__init__(database_manager, event_bus)

    def check_load(self, feed_key):
        file_log = self.get_file_log_by_status_and_feed_key(ServiceStatus.RL, feed_key)
        if file_log is not None:
            self.update_progress_to_ui(EventLevel.INFO, status_message.get(ServiceStatus.RL))
            return True;
        else:
            self.update_log_to_ui(EventLevel.ERROR, "No file log found for the given status and feed key.")
            return False;

    def insert_status(self, feed_key, status):
        file_config = self.get_file_config(feed_key)
        try:
            self.database_manager.connect_to_db(
                os.getenv('CONTROL_DB_HOST'),
                os.getenv('CONTROL_DB_USER'),
                os.getenv('CONTROL_DB_PASSWORD'),
                os.getenv('CONTROL_DB_NAME')
            )

            self.database_manager.call_procedure('insert_file_log', (status.value, file_config.source_url, file_config.folder_data_path, status_message.get(status)))
            self.update_progress_to_ui(EventLevel.INFO, status_message.get(status))

        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Error getting file config: {e}")
            raise RuntimeError(e)
        finally:
            self.database_manager.close_connection()

    def load_data(self, feed_key):

        self.insert_status(feed_key, ServiceStatus.LX)

        try:
            self.database_manager.connect_to_db(
                os.getenv('DATA_WAREHOUSE_DB_HOST'),
                os.getenv('DATA_WAREHOUSE_DB_USER'),
                os.getenv('DATA_WAREHOUSE_DB_PASSWORD'),
                os.getenv('DATA_WAREHOUSE_DB_NAME')
            )

            self.database_manager.call_procedure('LoadToKeyboardDim', ())
            return True;


        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Error getting file config: {e}")
            raise RuntimeError(e)
            return False;
        finally:
            self.database_manager.close_connection()

    def run(self):
        feed_key = "akko_feed"
        is_ready = self.check_load(feed_key)
        if (is_ready):
            is_success = self.load_data(feed_key)
            if (is_success):
                self.insert_status(feed_key, ServiceStatus.SL)
            else:
                self.insert_status(feed_key, ServiceStatus.FL)
