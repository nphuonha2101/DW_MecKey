from dotenv import dotenv_values
from db.db_manager import DatabaseManager
from event.event import Event
from event.event_bus import EventBus
from event.event_level import EventLevel
from event.event_type import EventType
from model.file_config import FileConfig
from model.file_log import FileLog
from services.status.service_status import ServiceStatus
from services.status.status_message import status_message

class LoadToWarehouse:
    def __init__(self, database_manager: DatabaseManager, event_bus: EventBus):
        self.database_manager = database_manager
        self.event_bus = event_bus
        self.file_log = None
        self.file_config = None
        self.env = None
        self.feed_key = None

    # Set feed_key cho service
    def set_feed_key(self, feed_key):
        self.feed_key = feed_key


    # Load .env vào biến env
    def load_env(self):
        try:
            self.env = dotenv_values(".env")
            if not self.env:
                raise ValueError("No environment variables found in .env file.")
            return self.env
        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Failed to load environment variables")
            self.update_progress_to_ui(EventLevel.ERROR, "Load failed! Failed to load environment variables")
            raise RuntimeError(e)

    def update_progress_to_ui(self, event_level: EventLevel, message):
        """Update service progress to UI (Ex: Ready extract, Extracting, Successful extract, Failed extract, ...)"""
        print(f'event_level: {event_level}, message: {message}')
        self.event_bus.publish(EventType.SERVICE_NOTIFY_PROGRESS, Event(event_level, message))

    def update_log_to_ui(self, event_level: EventLevel, message):
        """Update service log to UI. (Ex: Error fetching {url}: {e})"""
        print(f'event_level: {event_level}, message: {message}')
        self.event_bus.publish(EventType.SERVICE_NOTIFY_LOG, Event(event_level, message))

    # Tạo kết nối tới control_db và kiểm tra kết nối thông báo lỗi lên ui nếu có lỗi
    def connect_to_control_db(self):
        self.database_manager.connect_to_db(
            self.env.get('CONTROL_DB_HOST'),
            self.env.get('CONTROL_DB_USER'),
            self.env.get('CONTROL_DB_PASSWORD'),
            self.env.get('CONTROL_DB_NAME'),
            int(self.env.get('CONTROL_DB_PORT'))
        )

    # Lấy ra file_config bằng feed_key
    def get_file_config(self, feed_key):
        """Get file configuration"""
        try:
            self.database_manager.cursor.execute(f"SELECT * FROM file_config WHERE feed_key = %s", (feed_key,))
            result = self.database_manager.cursor.fetchone()
            if result:
                return FileConfig(*result)
            else:
                raise RuntimeError(f"File configuration running not found.")
        except Exception as e:
            raise RuntimeError(f"Failed to get file configuration. Caused by: {e}")

    # Lấy ra file_config theo status và file_path (MANUAL RUN)
    def get_file_config_by_status_and_file_path(self, status: str, file_path: str):
        print(f"status: {status}, file_path: {file_path}")
        query = f"SELECT * FROM file_config INNER JOIN file_log ON file_config.id = file_log.id_config WHERE file_log.status = %s AND file_log.file_path = %s"
        self.database_manager.call_query(query, (status, file_path))
        result = self.database_manager.cursor.fetchone()
        file_config = FileConfig.from_db(result[0])
        return file_config

    # # Lấy ra file_log bằng status và feed_key
    # def get_file_log_by_status_feed_key(self, status, feed_key):
    #     query = f"SELECT * FROM file_log WHERE is_active = %s AND status = %s AND id_config = (SELECT id FROM file_config WHERE feed_key = %s)"
    #     self.database_manager.call_query(query, (1, ServiceStatus.get_value(status), feed_key))
    #     result = self.database_manager.cursor.fetchone()
    #     if result is None:
    #         raise RuntimeError("No file configuration found for the given status and file path.")
    #     file_log = FileLog.from_db(result[0])
    #     return file_log

    # Lấy ra file_log bằng status và feed_key
    def get_file_log_by_status_feed_key(self, status, feed_key):
        """Get the latest file log to transform."""
        try:
            print(ServiceStatus.get_value(status), feed_key)
            query = f"SELECT * FROM file_log WHERE is_active = 1 AND status = %s AND id_config = (SELECT id FROM file_config WHERE feed_key = %s)"
            self.database_manager.cursor.execute(query, (ServiceStatus.get_value(status), feed_key))
            file_log = self.database_manager.cursor.fetchone()
            if file_log:
                return FileLog(*file_log)
        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Error retrieving latest file log: {e}")
            self.update_progress_to_ui(EventLevel.ERROR,
                                       f"Transformation failed! Caused by: {e}")


    def get_file_log_by_status_and_file_path(self, file_path: str, status: str):
        """Get detail file log with file_path and status."""
        try:
            query = f"SELECT * FROM {self.env.get('FILE_LOG_TABLE_NAME')} WHERE file_path = %s AND status = %s"
            self.database_manager.cursor.execute(query, (file_path, status))
            result = self.database_manager.cursor.fetchone()
            if result:
                return FileLog(*result)
            else:
                raise RuntimeError(f"File log not found.")
        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Failed to get file log. Caused by: {e}")
            raise RuntimeError(f"Failed to get file log. Caused by: {e}")

    # Insert vào file_log
    def insert_file_log(self, id_config: int, status: ServiceStatus, file_path: str):
        try:
            self.database_manager.cursor.execute("USE control_db;")
            self.database_manager.call_procedure(self.env.get('CREATE_FILE_LOG_PROC_NAME'), (id_config, ServiceStatus.get_value(status), file_path, status_message.get(status)))
        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Failed to insert file log")
            self.update_progress_to_ui(EventLevel.ERROR, "Load failed! Failed to insert file log")
            raise RuntimeError(e)

    # Tạo kết nối tới data_warehouse_db và kiểm tra kết nối thông báo lỗi lên ui nếu có lỗi
    def connect_to_warehouse_db(self):
         self.database_manager.connect_to_db(
            self.env.get('DATA_WAREHOUSE_DB_HOST'),
            self.env.get('DATA_WAREHOUSE_DB_USER'),
            self.env.get('DATA_WAREHOUSE_DB_PASSWORD'),
            self.env.get('DATA_WAREHOUSE_DB_NAME'),
            int(self.env.get('DATA_WAREHOUSE_DB_PORT'))
         )


    # Gọi procedure load vào data_warehouse_db
    def call_load_to_warehouse_procedure(self, file_config):
        try:
            self.database_manager.call_procedure(file_config.load_proc_name, ())
        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Failed to call load to warehouse procedure")
            self.update_progress_to_ui(EventLevel.ERROR, "Load failed! Failed to call load to warehouse procedure")
            raise RuntimeError(e)

    # Đóng kết nối tới database
    def close_connection(self):
        self.database_manager.cursor.close()
        self.database_manager.connection.close()


    def run(self, status:str = None, file_path:str = None):
        # 4.1. Load .env
        self.load_env()

        # 4.2. Tạo kết nối tới control_db
        try:
            self.connect_to_control_db()
        except Exception as e:
            # 4.10 - Thông báo lỗi
            self.update_log_to_ui(EventLevel.ERROR, f"Failed to connect to control_db")
            self.update_progress_to_ui(EventLevel.ERROR, "Load failed! Failed to connect to control_db")
            raise RuntimeError(e)

        # 4.3.a - Lấy ra file_config với status và file_path (MANUAL RUN)
        if status is not None and file_path is not None:
            try:
                self.file_config = self.get_file_config_by_status_and_file_path(status, file_path)
            except Exception as e:
                # 4.10 - Thông báo lỗi
                self.update_log_to_ui(EventLevel.ERROR, f"Failed to get file config")
                self.update_progress_to_ui(EventLevel.ERROR, f"Load failed! Failed to get file config")
                # 4.13 - Đóng kết nối database
                self.close_connection()
                raise RuntimeError(e)

        # 4.3.b - Lấy ra file_config với feed_key (AUTO RUN)
        else:
            try:
                self.file_config = self.get_file_config(self.feed_key)
            except Exception as e:
                # 4.10 - Thông báo lỗi
                self.update_log_to_ui(EventLevel.ERROR, f"Failed to get file config")
                self.update_progress_to_ui(EventLevel.ERROR, f"Load failed! Failed to get file config")
                # 4.13 - Đóng kết nối database
                self.close_connection()
                raise RuntimeError(e)

        # 4.3.a - Lấy ra file_log với status và file_path (MANUAL RUN)
        if status is not None and file_path is not None:
            try:
                self.file_log = self.get_file_log_by_status_and_file_path(status, file_path)
            except Exception as e:
                # 4.10 - Thông báo lỗi
                self.update_log_to_ui(EventLevel.ERROR, f"Failed to get file log. Caused by: {e}")
                self.update_progress_to_ui(EventLevel.ERROR, f"Load failed! Failed to get file log")
                # 4.13 - Đóng kết nối database
                self.close_connection()
                raise RuntimeError(e)

        # 4.3.b - Lấy ra file_log với status = RL hoặc FL và feed_key (AUTO RUN)
        else:
            try:
                # Lấy ra file_log với status = RL
                self.file_log = self.get_file_log_by_status_feed_key(ServiceStatus.RL, self.file_config.feed_key)
            except Exception as e:
                # 4.10 - Thông báo lỗi
                self.update_log_to_ui(EventLevel.ERROR, f"Failed to get file log. Caused by: {e}")
                self.update_progress_to_ui(EventLevel.ERROR, f"Load failed! Failed to get file log")

                try:
                    # Lấy ra file_log với status = FL (Failed to load)
                    self.file_log = self.get_file_log_by_status_feed_key(ServiceStatus.FL, self.file_config.feed_key)
                except Exception as e:
                    # 4.10 - Thông báo lỗi
                    self.update_log_to_ui(EventLevel.ERROR, f"Failed to get file log. Caused by: {e}")
                    self.update_progress_to_ui(EventLevel.ERROR, f"Load failed! Failed to get file log")
                    # 4.13 - Đóng kết nối database
                    self.close_connection()
                    raise RuntimeError(e)


        print(self.file_log)
        # 4.5. Insert file_log với status = LX
        self.insert_file_log(self.file_config.id, ServiceStatus.LX, self.file_log.file_path)

        # 4.6. Tạo kết nối tới data_warehouse_db
        try:
            self.connect_to_warehouse_db()
        except Exception as e:
            # 4.9. Insert file_log với status = FL (Failed to load)
            self.insert_file_log(self.file_config.id, ServiceStatus.FL, self.file_log.file_path)
            # 4.10 - Thông báo lỗi
            self.update_log_to_ui(EventLevel.ERROR, f"Failed to connect to warehouse. Caused by: {e}")
            self.update_progress_to_ui(EventLevel.ERROR, "Load failed! Failed to connect to warehouse")
            # 4.13 - Đóng kết nối database
            self.close_connection()
            raise RuntimeError(e)

        try:
            # 4.7. Gọi procedure load vào data_warehouse_db
            self.call_load_to_warehouse_procedure(self.file_config)
        except Exception as e:
            # 4.9. Insert file_log với status = FL
            self.insert_file_log(self.file_config.id, ServiceStatus.FL, self.file_log.file_path)
            # 4.10 - Thông báo lỗi
            self.update_log_to_ui(EventLevel.ERROR, f"Failed to load data to warehouse. Caused by: {e}")
            self.update_progress_to_ui(EventLevel.ERROR, status_message.get(ServiceStatus.FL))
            # 4.13 - Đóng kết nối database
            self.close_connection()
            raise RuntimeError(e)

        # 4.8. Insert file_log với status = SL
        self.insert_file_log(self.file_config.id, ServiceStatus.SL, self.file_log.file_path)
        # 4.12 - Thông báo thành công
        self.update_progress_to_ui(EventLevel.SUCCESS, status_message.get(ServiceStatus.SL))
        # 4.13 - Đóng kết nối database
        self.close_connection()