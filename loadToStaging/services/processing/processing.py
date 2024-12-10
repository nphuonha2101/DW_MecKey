import pymysql

from event.event import Event
from event.event_level import EventLevel
from event.event_type import EventType
from model.file_config import FileConfig
from dotenv import load_dotenv, dotenv_values
from event.event_bus import EventBus
from model.file_log import FileLog
from services.status.service_status import ServiceStatus
from services.status.status_message import status_message

load_dotenv()

class Processing:
    def __init__(self, event_bus: EventBus):
        self.connection = None
        self.cursor = None
        self.event_bus = event_bus
        self.feed_key = None
        self.file_log = None
        self.file_config = None
        self.env = None


    def set_feed_key(self, feed_key):
        self.feed_key = feed_key

    def update_progress_to_ui(self, event_level: EventLevel, message):
        """Update service progress to UI (Ex: Ready extract, Extracting, Successful extract, Failed extract, ...)"""
        print(f"{event_level}: {message}")
        self.event_bus.publish(EventType.SERVICE_NOTIFY_PROGRESS, Event(event_level, message))

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

    # Mở kết nối database
    def connect_to_db(self, host, user, password, db, port=3306):
        """Connect to database"""
        try:
            self.connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                db=db,
                port=port
            )
            self.cursor = self.connection.cursor()
        except Exception as e:
            raise RuntimeError(
                f"{e}. Please check your connection information and try again. (Make sure connection information in .env file is correct)")

    # Đóng kết nối
    def close_connection(self):
        """Close connection"""
        self.cursor.close()
        self.connection.close()

    # Lấy file_config có running = true
    def get_file_config(self, feed_key):
        """Get file configuration"""
        try:
            self.cursor.execute("SELECT * FROM file_config WHERE feed_key = %s", (feed_key,))
            result = self.cursor.fetchone()
            if result:
                return FileConfig(*result)
            else:
                raise RuntimeError(f"File configuration running not found.")
        except Exception as e:
            raise RuntimeError(f"Failed to get file configuration. Caused by: {e}")

    def get_file_log_by_file_path_status(self, file_path: str, status: str):
        """Get file configuration by file path and status"""
        try:
            self.cursor.execute(
                f"SELECT * FROM file_log  WHERE file_path = '{file_path}' AND status = '{status}' AND is_active = 1")
            result = self.cursor.fetchone()
            if result:
                return FileLog(*result)
            else:
                raise RuntimeError(
                    f"File log with file path '{file_path}' and status '{status}' not found.")
        except Exception as e:
            raise RuntimeError(f"Failed to get file log. Caused by: {e}")

    # Lấy file log theo status và feed_key
    def get_file_log_by_status_and_feed_key(self, status: ServiceStatus, feed_key):
        """Get file log by status and feed key"""
        try:
            self.cursor.execute("SELECT file_log.* FROM file_log INNER JOIN file_config ON file_log.id_config = file_config.id WHERE file_log.status = %s AND file_config.feed_key = %s AND file_log.is_active = 1", (ServiceStatus.get_value(status), feed_key))
            result = self.cursor.fetchone()
            if result:
                return FileLog(*result)
            else:
                raise RuntimeError(f"File log with status {status} not found.")
        except Exception as e:
            raise RuntimeError(f"Failed to get file log by status {status}. Caused by {e}")

    # Lấy file config theo status và file path (MANUAL RUN)
    def get_file_config_by_status_and_file_path(self, status: str, file_path:str):
        """Get file configuration by status and file path"""
        try:
            self.cursor.execute(
                f"SELECT file_config.* FROM file_config INNER JOIN file_log ON file_config.id = file_log.id_config WHERE file_log.status = '{status}' AND file_log.file_path = '{file_path}' AND file_log.is_active = 1")
            result = self.cursor.fetchone()
            if result:
                return FileConfig(*result)
            else:
                raise RuntimeError(
                    f"File configuration with status '{status}' and file path '{file_path}' not found.")
        except Exception as e:
            raise RuntimeError(f"Failed to get file configuration. Caused by: {e}")

    # Lấy file log theo status và feed_key (AUTO RUN)
    def get_file_log(self, feed_key):
        try:
            # Lấy file log với status = RP (Ready to process)
            log_file = self.get_file_log_by_status_and_feed_key(ServiceStatus.RP, feed_key)

            self.update_log_to_ui(EventLevel.INFO, f"File log with status RP found. Processing {log_file.file_path}")
            return log_file
        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Cannot get file log with status RP. Caused by: {e}")
            self.update_progress_to_ui(EventLevel.ERROR, f"Processing failed! No file log is ready for processing. Now checking for file log with status FP")

            # Lấy file log với status = FP (Failed to process)
            try:
                log_file = self.get_file_log_by_status_and_feed_key(ServiceStatus.FP, feed_key)
                self.update_log_to_ui(EventLevel.INFO, f"File log with status FP found. Processing {self.file_log.file_path}")
                return log_file
            except Exception as e:
                self.update_log_to_ui(EventLevel.ERROR, f"Cannot get file log with status FP. Caused by: {e}")
                self.update_progress_to_ui(EventLevel.ERROR, f"Processing failed! No file log is ready for processing.")

                print(f"Failed to get file log with status RP or FP. Caused by: {e}")

                return None

    # Insert file_log
    def create_file_log(self, procname, config_id, status: ServiceStatus, file_path):
        """Create file log"""
        try:
            self.cursor.execute("USE control_db;")
            self.cursor.callproc(procname, (config_id, ServiceStatus.get_value(status), file_path, status_message.get(status)))
            self.connection.commit()
        except Exception as e:
            raise RuntimeError(f"Failed to create file log. Caused by: {e}")

    def truncate_table(self):
        self.cursor.execute(f"TRUNCATE TABLE {self.file_config.staging_raw_table_name}")
        self.connection.commit()

    # Replace sql command
    def replace_sql(self, insert_sql, db_name):
        insert_sql = insert_sql.replace('%file_path%', f"'{self.file_log.file_path}'", 1)
        insert_sql = insert_sql.replace('%db_name%', f"`{db_name}`", 1)
        insert_sql = insert_sql.replace('%raw_table_name%', f"`{self.file_config.staging_raw_table_name}`", 1)
        insert_sql = insert_sql.replace('%file_delimiter%', f"'{self.file_config.file_delimiter}'", 1)
        insert_sql = insert_sql.replace('%line_terminator%', f"'{self.file_config.line_terminator}'", 1)
        return insert_sql

    # Load
    def load_file_to_table(self, insert_sql):
        print(insert_sql)
        # self.cursor.execute("USE data_staging_db;")
        self.cursor.execute(insert_sql)
        self.connection.commit()

    def run(self, status=None, file_path=None):
        # 2.1 Load các biến môi trường từ file .env
        env_variables = self.load_env()
        try:
            # 2.2 Tạo kết nối tới control_db
            self.connect_to_db(env_variables['CONTROL_DB_HOST'], env_variables['CONTROL_DB_USER'],
                               env_variables['CONTROL_DB_PASSWORD'], env_variables['CONTROL_DB_NAME'], int(env_variables['CONTROL_DB_PORT']))
        except Exception as e:
            # 2.14 - Thông báo lỗi nếu không kết nối được
            self.update_log_to_ui(EventLevel.ERROR, f"Failed to connect to database. Caused by: {e}")
            self.update_progress_to_ui(EventLevel.ERROR, f"Failed to connect to database. Caused by: {e}")

            # 2.15 - Đóng kết nối
            self.close_connection()

            raise RuntimeError('Failed to connect to database. Please check your connection information and try again. (Make sure connection information in .env file is correct)')

        # 2.3.a - Lấy file config bằng file_path và status (MANUAL RUN)
        if status is not None and file_path is not None:
            try:
                print(status, file_path)
                self.file_config = self.get_file_config_by_status_and_file_path(status, file_path)
            except Exception as e:
                # 2.14 - Thông báo lỗi nếu không lấy được file config
                self.update_log_to_ui(EventLevel.ERROR, f"Failed to get file configuration. Caused by: {e}")
                self.update_progress_to_ui(EventLevel.ERROR, f"Failed to get file configuration. Caused by: {e}")
                # 2.15 - Đóng kết nối
                self.close_connection()

                raise RuntimeError('Failed to get file configuration.')

        # 2.3.b - Lấy file config bằng feed_key (AUTO RUN)
        else:
            try:
                self.file_config = self.get_file_config(self.feed_key)
            except Exception as e:
                # 2.14 - Thông báo lỗi nếu không lấy được file config
                self.update_log_to_ui(EventLevel.ERROR, f"Failed to get file configuration. Caused by: {e}")
                self.update_progress_to_ui(EventLevel.ERROR, f"Failed to get file configuration. Caused by: {e}")
                # 2.15 - Đóng kết nối
                self.close_connection()
                raise RuntimeError('Failed to get file configuration.')


        # 2.4.a - Lấy file log với file_path và status (MANUAL RUN)
        if status is not None and file_path is not None:
            try:
                self.file_log = self.get_file_log_by_file_path_status(file_path, status)
            except Exception as e:
                # 2.14 - Thông báo lỗi nếu không lấy được file log
                self.update_log_to_ui(EventLevel.ERROR, f"Failed to get file configuration. Caused by: {e}")
                self.update_progress_to_ui(EventLevel.ERROR, f"Failed to get file configuration. Caused by: {e}")
                # 2.15 - Đóng kết nối
                self.close_connection()

                raise RuntimeError(f'Failed to get file log with file path and status. By: {e}')

        # 2.4.b - Lấy file log với feed_key và status = RP hoặc FP (AUTO RUN)
        else:
            try:
                # 2.4 Lấy ra file_log với status = RP
                self.file_log = self.get_file_log(self.feed_key)
            except Exception as e:
                # 2.14 - Thông báo lỗi nếu không lấy được file log
                self.update_log_to_ui(EventLevel.ERROR, f"Failed to get file configuration. Caused by: {e}")
                self.update_progress_to_ui(EventLevel.ERROR, f"Failed to get file configuration. Caused by: {e}")
                # 2.15 - Đóng kết nối
                self.close_connection()

                raise RuntimeError(f'Failed to get file log with status RP or FP. By: {e}')

        # 2.5 Insert file_log với status = PX
        self.create_file_log(env_variables['CREATE_FILE_LOG_PROC_NAME'], self.file_config.id, ServiceStatus.PX, self.file_log.file_path)
        self.update_progress_to_ui(EventLevel.INFO, f"{self.__class__.__name__} " + " is running")

        try:
            # 2.6 Tạo kết nối tới data_staging_db
            self.connect_to_db(env_variables['STAGING_DB_HOST'], env_variables['STAGING_DB_USER'],
                               env_variables['STAGING_DB_PASSWORD'], env_variables['STAGING_DB_NAME'], int(env_variables['STAGING_DB_PORT']))

            # 2.7 Truncate bảng raw
            self.truncate_table()
            print("ok")

        except Exception as e:
            # 2.13 - Insert vào file_log với status = FP
            self.create_file_log(env_variables['CREATE_FILE_LOG_PROC_NAME'], self.file_config.id, ServiceStatus.FP, self.file_log.file_path)
            # 2.14 - Thông báo lỗi nếu không kết nối được
            self.update_log_to_ui(EventLevel.ERROR, f"Failed to connect to database. Caused by: {e}")
            self.update_progress_to_ui(EventLevel.ERROR, f"Failed to connect to database. Caused by: {e}")
            # 2.15 - Đóng kết nối
            self.close_connection()
            return


        # 2.8 Thay đổi câu lệnh sql với file_path, db_name, raw_table_name, file_delimiter, line_delimiter
        insert_sql = self.replace_sql(env_variables['INSERT_TO_STAGING_SQL'], "data_staging_db")

        try:
            # 2.9 Load dữ liệu của file D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads\akko_YYYY_MM_DD.csv vào bảng raw_akko trong data_staging_db
            self.load_file_to_table(insert_sql)
            # 2.10 Insert vào file_log với status = SP
            self.create_file_log(self.env['CREATE_FILE_LOG_PROC_NAME'], self.file_config.id, ServiceStatus.SP, self.file_log.file_path)
            # 2.11 Thông báo thành công
            self.update_log_to_ui(EventLevel.SUCCESS, f"Successful")
            self.update_progress_to_ui(EventLevel.SUCCESS, f"Successful")
            # 2.12  Insert vào file_log với status = RT
            self.create_file_log(self.env['CREATE_FILE_LOG_PROC_NAME'], self.file_config.id, ServiceStatus.RT, self.file_log.file_path)
            # 2.15 - Đóng kết nối
            self.close_connection()
        except Exception as e:
            # 2.13 Insert vào file_log với status = FP
            self.create_file_log(self.env['CREATE_FILE_LOG_PROC_NAME'], self.file_config.id, ServiceStatus.FP, self.file_log.file_path)
            # 2.14 - Thông báo lỗi nếu không kết nối được
            self.update_log_to_ui(EventLevel.ERROR, f"Failed to load")
            self.update_progress_to_ui(EventLevel.ERROR, f"Failed to load")
            # 2.15 - Đóng kết nối
            self.close_connection()
            raise RuntimeError(e)



