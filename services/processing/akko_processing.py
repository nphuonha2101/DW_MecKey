from event.event import Event
from event.event_level import EventLevel
from services.abstract_services import AbstractService
import os
from dotenv import load_dotenv
from db.db_manager import DatabaseManager
from event.event_bus import EventBus
from services.status.service_status import ServiceStatus

load_dotenv()



class AkkoProcessing(AbstractService):
    def __init__(self, database_manager: DatabaseManager, event_bus: EventBus):
        super().__init__(database_manager, event_bus)
        self.feed_key = os.getenv('AKKO_FEED_KEY')
        self.file_log = None
        self.file_config = None

    def to_staging(self):
        try:
            self.file_config = self.get_file_config(self.feed_key)
        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Cannot get file config for feed_key={self.feed_key}. Caused by: {e}")
            self.update_log_to_ui(EventLevel.ERROR, f"Processing failed! Caused by: {e}")
            return

        try:
            self.file_log = self.get_file_log_by_status_and_feed_key(ServiceStatus.RP, self.feed_key)
        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Cannot get file log. Caused by: {e}")
            self.update_log_to_ui(EventLevel.ERROR, f"Processing failed! Caused by: {e}")
            return

        # PX: Processing
        self.create_file_log(self.file_config.id, ServiceStatus.PX, self.file_log.file_path)

        data_staging_db_name = os.getenv('STAGING_DB_NAME')
        insert_sql = os.getenv('INSERT_TO_STAGING_SQL')

        insert_sql = insert_sql.replace('%file_path%', f"'{self.file_log.file_path}'", 1)
        insert_sql = insert_sql.replace('%db_name%', f"`{data_staging_db_name}`", 1)
        insert_sql = insert_sql.replace('%raw_table_name%', f"`{self.file_config.staging_raw_table_name}`", 1)

        try:
            print(insert_sql)
            self.database_manager.call_query(f"TRUNCATE {self.file_config.staging_raw_table_name}")
            self.database_manager.call_query(insert_sql)

            # SP
            self.create_file_log(self.file_config.id, ServiceStatus.SP, self.file_log.file_path)
            self.update_log_to_ui(EventLevel.SUCCESS, f"Processing completed successfully. SQL: {insert_sql}")
            self.update_progress_to_ui(EventLevel.SUCCESS, f"Processing successful for file: {self.file_log.file_path}")

        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Cannot insert data into database. Caused by: {e}")
            self.update_log_to_ui(EventLevel.ERROR, f"Processing failed! Caused by: {e}")
            self.create_file_log(self.file_config.id, ServiceStatus.FP, self.file_log.file_path)
            raise RuntimeError(e)


    def run(self):
        self.update_progress_to_ui(EventLevel.INFO, f"${self.__class__.__name__}" + " is running")
        try:
            self.to_staging()
        except Exception as e:
            self.update_progress_to_ui(EventLevel.ERROR, f"${self.__class__.__name__} got problem. Caused by: {e}")
            print(f"Error: {e}")
            return

        # Update RT
        self.create_file_log(self.file_config.id, ServiceStatus.RT, self.file_log.file_path)

        self.update_log_to_ui(EventLevel.INFO, f"Processing {self.file_log.file_path} Completed. Ready for transform")
        self.update_progress_to_ui(EventLevel.INFO, f"Processing {self.file_log.file_path} Complete. Ready for transform")
