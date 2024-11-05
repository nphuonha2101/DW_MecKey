from logging.config import fileConfig

from db.db_manager import DatabaseManager
from event.event_bus import EventBus
from services.abstract_services import AbstractService
from event.event_level import EventLevel
from services.status.service_status import ServiceStatus
import os
from dotenv import load_dotenv

load_dotenv()


class AkkoTransform(AbstractService):
    def __init__(self, database_manager: DatabaseManager, event_bus: EventBus):
        super().__init__(database_manager, event_bus)
        self.file_log = None

    def run(self):
        self.update_progress_to_ui(EventLevel.INFO, f"{self.__class__.__name__} is running")
        try:
            self.file_log = self.get_latest_file_log()
            if not self.file_log:
                self.update_progress_to_ui(EventLevel.ERROR, "No file log found for transformation.")
                return

            self.perform_transformation()

            # Update file log status to Successful
            self.create_file_log(self.file_log.id_config, ServiceStatus.ST, self.file_log.file_path)
            self.update_progress_to_ui(EventLevel.SUCCESS,
                                       f"Transformation successful for file: {self.file_log.file_path}")

        except Exception as e:
            self.update_progress_to_ui(EventLevel.ERROR,
                                       f"{self.__class__.__name__} encountered an error. Caused by: {e}")
            print(f"Error: {e}")
            # Update file log status to Failed
            self.create_file_log(self.file_log.id_config, ServiceStatus.FT, self.file_log.file_path)

    def get_latest_file_log(self):
        """Get the latest file log to transform."""
        try:
            feed_key = os.getenv('AKKO_FEED_KEY')
            return self.get_file_log_by_status_and_feed_key(ServiceStatus.RT, feed_key)
        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Error retrieving latest file log: {e}")
            return None

    def perform_transformation(self):
        """Perform the data transformation logic."""
        try:
            # Placeholder for transformation logic
            # You would include your specific transformation steps here.
            # For example:
            # 1. Load data from the source
            # 2. Apply transformations
            # 3. Save transformed data to target

            self.update_progress_to_ui(EventLevel.INFO, f"Transforming data for file: {self.file_log.file_path}")

            # Simulate a transformation process
            # TODO: Replace this with actual transformation code.
            transformed_data = self.transform_data(self.file_log.file_path)

        except Exception as e:
            raise RuntimeError(f"Error during transformation: {e}")

    def transform_data(self, file_config):
        try:
            # self.create_file_log(file_config.id, ServiceStatus.ST, file_config.file_path)
            self.update_progress_to_ui(EventLevel.INFO, f"Transforming data for file: {self.file_log.file_path}")
            try:
                self.create_file_log(self.file_log.id_config, ServiceStatus.ST, self.file_log.file_path)
            except Exception as e:
                self.update_progress_to_ui(EventLevel.ERROR, f"Error during transformation: {e}")
                raise RuntimeError(f"Error during transformation: {e}")

            try:
                self.database_manager.connect_to_db(
                    os.getenv('STAGING_DB_HOST'),
                    os.getenv('STAGING_DB_USER'),
                    os.getenv('STAGING_DB_PASSWORD'),
                    os.getenv('STAGING_DB_NAME')
                )

                self.database_manager.call_procedure('InsertToAkkoTransformed', ())
                return True;


            except Exception as e:
                self.update_log_to_ui(EventLevel.ERROR, f"Error getting file config: {e}")
                raise RuntimeError(e)
                return False;
            finally:
                self.database_manager.close_connection()

        except Exception as e:
            raise RuntimeError(f"Error during transformation: {e}")
