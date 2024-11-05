import os

from db.db_manager import DatabaseManager
from event.event_bus import EventBus
from event.event_level import EventLevel
from model.file_config import FileConfig
from services.abstract_services import AbstractService
from services.status.service_status import ServiceStatus
from services.status.status_message import status_message


class LoadToWarehouse(AbstractService):
    def __init__(self, database_manager: DatabaseManager, event_bus: EventBus):
        super().__init__(database_manager, event_bus)
        self.file_log = None

    def check_load(self, file_config):
        try: 
            self.file_log = self.get_file_log_by_status_and_feed_key(ServiceStatus.RL, file_config.feed_key)
      
            self.update_progress_to_ui(EventLevel.INFO, status_message.get(ServiceStatus.RL))
            self.update_log_to_ui(EventLevel.INFO, f"File log found for the given status and feed key. {self.file_log}")
            return True;
        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, "No file log found for the given status and feed key. Caused by: {e}")
            self.update_progress_to_ui(EventLevel.ERROR, f"Load failed! No file log is ready for loading. Now checking for file log with status FL")

            try:
                self.file_log = self.get_file_log_by_status_and_feed_key(ServiceStatus.FL, file_config.feed_key)
                self.update_progress_to_ui(EventLevel.INFO, status_message.get(ServiceStatus.FL))
                self.update_log_to_ui(EventLevel.INFO, f"File log found for the given status and feed key. {self.file_log}")
                return True;
            except Exception as e:
                self.update_log_to_ui(EventLevel.ERROR, "No file log found for the given status and feed key. Caused by: {e}")
                self.update_progress_to_ui(EventLevel.ERROR, "Load failed! No file log is ready for loading.")
                return False;

    def load_data(self, file_config: FileConfig):

        self.create_file_log(file_config.id, ServiceStatus.LX, self.file_log.file_path)
        self.update_progress_to_ui(EventLevel.INFO, status_message.get(ServiceStatus.LX))
        self.update_log_to_ui(EventLevel.INFO, f"Loading data for file: {self.file_log.file_path}")

        try:
            self.database_manager.connect_to_db(
                os.getenv('DATA_WAREHOUSE_DB_HOST'),
                os.getenv('DATA_WAREHOUSE_DB_USER'),
                os.getenv('DATA_WAREHOUSE_DB_PASSWORD'),
                os.getenv('DATA_WAREHOUSE_DB_NAME')
            )

            self.database_manager.call_procedure(file_config.load_proc_name, ())
            return True;


        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Error getting file config: {e}")
            raise RuntimeError(e)
        finally:
            self.database_manager.close_connection()

    def run(self):
        feed_key = os.getenv('AKKO_FEED_KEY')
        file_config = self.get_file_config(feed_key)

        is_ready = self.check_load(file_config)

        if (is_ready):
            is_success = self.load_data(file_config)
            if (is_success):
                self.create_file_log(file_config.id, ServiceStatus.SL, self.file_log.file_path)
                self.update_progress_to_ui(EventLevel.SUCCESS, status_message.get(ServiceStatus.SL))
            else:
                self.create_file_log(file_config.id, ServiceStatus.FL, self.file_log.file_path)
                self.update_progress_to_ui(EventLevel.ERROR, status_message.get(ServiceStatus.FL))
