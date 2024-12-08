import pymysql

from event.event import Event
from event.event_bus import EventBus
from event.event_type import EventType
from model.file_config import FileConfig
from model.file_log import FileLog

from event.event_level import EventLevel
from services.status.service_status import ServiceStatus
from dotenv import load_dotenv, dotenv_values

from services.status.status_message import status_message

load_dotenv()


class Transform:

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.cursor = None
        self.connection = None
        self.file_log = None
        self.file_config = None
        self.env = None
        self.feed_key = None

    def set_feed_key(self, feed_key):
        self.feed_key = feed_key

    # Update tiến trình tới UI
    def update_progress_to_ui(self, event_level: EventLevel, message):
        """Update service progress to UI (Ex: Ready extract, Extracting, Successful extract, Failed extract, ...)"""
        print(f"{event_level}: {message}")
        self.event_bus.publish(EventType.SERVICE_NOTIFY_PROGRESS, Event(event_level, message))

    # Update log tới UI
    def update_log_to_ui(self, event_level: EventLevel, message):
        """Update service log to UI. (Ex: Error fetching {url}: {e})"""
        print(f"{event_level}: {message}")
        self.event_bus.publish(EventType.SERVICE_NOTIFY_LOG, Event(event_level, message))

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

    # Tạo kết nối tới control_db và kiểm tra kết nối thông báo lỗi lên ui nếu có lỗi
    def connect_to_db(self, host, user, password, db_name, port=3306):
        try:
            self.connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                db=db_name,
                port=port
            )
            self.cursor = self.connection.cursor()
        except Exception as e:
            raise RuntimeError(e)

    # Lấy ra file_config bằng feed_key
    def get_file_config(self, feed_key):
        """Get file configuration"""
        try:
            self.cursor.execute(f"SELECT * FROM file_config WHERE feed_key = '{feed_key}'")
            result = self.cursor.fetchone()
            if result:
                return FileConfig(*result)
            else:
                raise RuntimeError(f"File configuration running not found.")
        except Exception as e:
            raise RuntimeError(f"Failed to get file configuration. Caused by: {e}")

    # Lấy ra file_config bằng status và file_path cho MANUAL RUN
    def get_file_config_by_status_and_file_path(self, status: str, file_path: str):
        """Get file configuration by status and file_path."""
        try:
            query = f"SELECT file_config.* FROM file_config INNER JOIN file_log ON file_config.id = file_log.id_config WHERE file_log.status = %s AND file_log.file_path = %s"
            self.cursor.execute(query, (status, file_path))
            result = self.cursor.fetchone()
            print(f"Query result: {result}")
            if result:
                return FileConfig(*result)
            else:
                raise RuntimeError(f"File configuration not found.")
        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Failed to get file configuration. Caused by: {e}")
            raise RuntimeError(f"Failed to get file configuration. Caused by: {e}")

    # Lấy ra file_log bằng status và feed_key
    def get_file_log_by_status_feed_key(self, status, feed_key):
        """Get the latest file log to transform."""
        try:
            query = f"SELECT * FROM file_log WHERE is_active = 1 AND status = %s AND id_config = (SELECT id FROM file_config WHERE feed_key = %s)"
            self.cursor.execute(query, (ServiceStatus.get_value(status), feed_key))
            file_log = self.cursor.fetchone()
            if file_log:
                return FileLog(*file_log)
        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Error retrieving latest file log: {e}")
            self.update_progress_to_ui(EventLevel.ERROR,
                                       f"Transformation failed! Caused by: {e}")


    def get_file_log_by_file_path_and_status(self, file_path: str, status: str):
        """Get detail file log with file_path and status."""
        try:
            query = f"SELECT * FROM {self.env.get('FILE_LOG_TABLE_NAME')} WHERE file_path = %s AND status = %s"
            self.cursor.execute(query, (file_path, status))
            result = self.cursor.fetchone()
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
            self.cursor.execute("USE control_db;")
            self.call_procedure(self.env.get('CREATE_FILE_LOG_PROC_NAME'), (
            id_config, ServiceStatus.get_value(status), file_path, status_message.get(status)))
        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Failed to insert file log")
            self.update_progress_to_ui(EventLevel.ERROR, "Load failed! Failed to insert file log")
            raise RuntimeError(e)

    def call_procedure(self, procedure_name, args=None):
        """Call a procedure. Example: call_procedure('procedure_name', (arg1, arg2, arg3))"""
        try:
            self.cursor.callproc(procedure_name, args)
            self.connection.commit()
            return self.cursor.fetchall()
        except Exception as e:
            raise RuntimeError(e)

    def transform_data(self):
        try:
            self.cursor.execute(f"USE {self.env['STAGING_DB_NAME']};")
            self.call_procedure(self.file_config.transform_proc_name, ())
        except Exception as e:
            self.update_progress_to_ui(EventLevel.ERROR, f"Transformation failed due to: {e}")
            self.update_log_to_ui(EventLevel.ERROR, f"Critical error during transformation: {e}")
            raise RuntimeError(f"Error during transformation: {e}")

    # Đóng kết nối tới database
    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def run(self, status=None, file_path=None):

        # 3.1. Load .env
        self.load_env()

        # 3.2. Tạo kết nối tới control_db
        try:
            self.connect_to_db(self.env.get('CONTROL_DB_HOST'), self.env.get('CONTROL_DB_USER'), self.env.get('CONTROL_DB_PASSWORD'), self.env.get('CONTROL_DB_NAME'), int(self.env.get('CONTROL_DB_PORT')))
        except Exception as e:
            # 3.12 - Thông báo lỗi
            self.update_log_to_ui(EventLevel.ERROR, f"Failed to connect to control_db")
            self.update_progress_to_ui(EventLevel.ERROR, "Load failed! Failed to connect to control_db")
            raise RuntimeError(e)

        # 3.3.a - Lấy ra file_config bằng status và file_path (MANUAL RUN)
        if status is not None and file_path is not None:
            try:
                self.file_config = self.get_file_config_by_status_and_file_path(status, file_path)
            except Exception as e:
                # 3.12 - Thông báo lỗi
                self.update_log_to_ui(EventLevel.ERROR, f"Failed to get file config")
                self.update_progress_to_ui(EventLevel.ERROR, f"Load failed! Failed to get file config")
                # 3.13 Đóng kết nối database
                self.close_connection()
                raise RuntimeError(e)

        # 3.3.b - Lấy ra file_config bằng feed_key (AUTO RUN)
        else:
            try:
                self.file_config = self.get_file_config(self.feed_key)
            except Exception as e:
                # 3.12 - Thông báo lỗi
                self.update_log_to_ui(EventLevel.ERROR, f"Failed to get file config")
                self.update_progress_to_ui(EventLevel.ERROR, f"Load failed! Failed to get file config")
                # 3.13 Đóng kết nối database
                self.close_connection()
                raise RuntimeError(e)

        # 3.4.a - Lấy ra file_log bằng status và file_path (MANUAL RUN)
        if status is not None or file_path is not None:
            try:
                self.file_log = self.get_file_log_by_file_path_and_status(file_path, status)
            except Exception as e:
                # 3.12 - Thông báo lỗi
                self.update_log_to_ui(EventLevel.ERROR, f"Failed to get file log")
                self.update_progress_to_ui(EventLevel.ERROR, f"Load failed! Failed to get file log")
                # 3.13 Đóng kết nối database
                self.close_connection()
                raise RuntimeError(e)
        # 3.4.b - Lấy ra file_log bằng feed_key và status (AUTO RUN)
        else:
            try:
                # Lấy ra file_log bằng feed_key và status = RT (Ready to transform)
                self.file_log = self.get_file_log_by_status_feed_key(ServiceStatus.RT, self.feed_key)
            except Exception as e:
                # 3.12 - Thông báo lỗi
                self.update_log_to_ui(EventLevel.ERROR, f"Failed to get file log. Caused by: {e}")
                self.update_progress_to_ui(EventLevel.ERROR, f"Load failed! Failed to get file log")

                try:
                    # Lấy ra file_log bằng feed_key và status = FT (Failed to transform)
                    self.file_log = self.get_file_log_by_status_feed_key(ServiceStatus.FT, self.feed_key)
                except Exception as e:
                    # 3.12 - Thông báo lỗi
                    self.update_log_to_ui(EventLevel.ERROR, f"Failed to get file log. Caused by: {e}")
                    self.update_progress_to_ui(EventLevel.ERROR, f"Load failed! Failed to get file log")
                    # 3.13 - Đóng kết nối database
                    self.close_connection()
                    raise RuntimeError(e)

        # 3.5. Tạo kết nối tới data_staging_db
        try:
            self.connect_to_db(self.env.get('STAGING_DB_HOST'), self.env.get('STAGING_DB_USER'), self.env.get('STAGING_DB_PASSWORD'), self.env.get('STAGING_DB_NAME'), int(self.env.get('STAGING_DB_PORT')))
        except Exception as e:
            # 3.11 - Thêm vào file_log với status = FT (Failed to transform)
            self.insert_file_log(self.file_config.id, ServiceStatus.FT, self.file_log.file_path)
            # 3.12 - Thông báo lỗi
            self.update_log_to_ui(EventLevel.ERROR, f"Failed to connect to data_staging db")
            self.update_progress_to_ui(EventLevel.ERROR, "Load failed! Failed to connect to data_staging db")
            # 3.13 - Đóng kết nối database
            self.close_connection()
            raise RuntimeError(e)

        try:
            # 3.6 Insert file_log với status = TX
            self.insert_file_log(self.file_config.id, ServiceStatus.TX, self.file_log.file_path)
            # 3.7. Transform data
            self.transform_data()
        except Exception as e:
            # 3.11. Insert file_log với status = FT (Failed to transform)
            self.insert_file_log(self.file_config.id, ServiceStatus.FT, self.file_log.file_path)
            # 3.12 - Thông báo lỗi
            self.update_log_to_ui(EventLevel.ERROR, f"Failed to load data to warehouse")
            self.update_progress_to_ui(EventLevel.ERROR, status_message.get(ServiceStatus.FT))
            # 3.13 - Đóng kết nối database
            self.close_connection()
            raise RuntimeError(e)

        # 3.8. Insert file_log với status = ST (Success transform)
        self.insert_file_log(self.file_config.id, ServiceStatus.ST, self.file_log.file_path)
        # 3.9. Insert file_log với status = RL (Ready to load)
        self.insert_file_log(self.file_config.id, ServiceStatus.RL, self.file_log.file_path)
        # 3.10 - Thông báo thành công
        self.update_log_to_ui(EventLevel.SUCCESS, "Data transformed successfully")
        self.update_progress_to_ui(EventLevel.SUCCESS, "Transform Success")
        # 3.13 - Đóng kết nối database
        self.close_connection()

