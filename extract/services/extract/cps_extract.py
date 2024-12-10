from dotenv import load_dotenv
from event.event_bus import EventBus
import requests
from event.event_level import EventLevel
from event.event_type import EventType
from services.status.service_status import ServiceStatus
from event.event import Event
from services.status.status_message import status_message
import pymysql
import os
from model.file_config import FileConfig
import time
import pandas as pd
from datetime import datetime


def generate_file_name(data_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    result = f'{data_path}/cps_{timestamp}.csv'
    result = result.replace("\\", "/")
    result = result.replace("//", "/")
    return result


def parse_product_details(response):
    """Parse product details"""
    products_details_in_page = []

    print(response)

    if response['data']['products'] is None:
        return pd.DataFrame()

    try:
        for product in response['data']['products']:
            product_detail = {
                'name': product['general'].get('name', 'N/A'),
                'keycap': product['general']['attributes'].get('ban_phim_key_cap', 'N/A'),
                'type': product['general']['attributes'].get('ban_phim_loai', 'N/A'),
                'number_of_keys': product['general']['attributes'].get('ban_phim_so_phim', 0),
                'mode': product['general']['attributes'].get('chuot_ban_phim_ket_noi', 'N/A'),
                'led': product['general']['attributes'].get('chuot_ban_phim_led', 'N/A'),
                'battery': product['general']['attributes'].get('chuot_ban_phim_pin', 'N/A'),
                'compatibility': product['general']['attributes'].get('chuot_ban_phim_tuong_thich', 'N/A'),
                'size': product['general']['attributes'].get('dimensions', 'N/A'),
                'image': 'https://cellphones.com.vn/media/catalog/product' + product['general']['attributes'].get(
                    'image', ''),
                'manufacturer': product['general']['attributes'].get('phone_accessory_brands', 'N/A'),
                'weight': product['general']['attributes'].get('product_weight', 'N/A'),
                'sku': product['general'].get('sku', 'N/A'),
                'price': float(product['filterable'].get('price', 0)),
                'discount_price': float(product['filterable'].get('special_price', 0)),
            }

            products_details_in_page.append(product_detail)

        df = pd.DataFrame(products_details_in_page)

        return df
    except Exception as e:
        raise RuntimeError(f"Failed to parse product details. Caused by: {e}")


class CellphoneSExtract:
    def __init__(self, event_bus: EventBus):
        self.file_path = None
        self.config = None
        self.event_bus = event_bus

    def fetch_json(self, url, payload):
        """Fetch json from url then return response"""
        try:
            headers = {
                "Content-Type": "application/json",
            }

            if payload is not None:
                response = requests.post(url, data=payload, headers=headers)
            else:
                raise RuntimeError("Payload is required.")
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            self.update_log_to_ui(EventLevel.ERROR, f"Error fetching {url}: {e}")
            return None

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

    def close_connection(self):
        """Close connection"""
        self.cursor.close()
        self.connection.close()

    def get_file_config(self, feed_key):
        """Get file configuration"""
        try:
            self.cursor.execute(f"SELECT * FROM file_config WHERE feed_key = '{feed_key}'")
            result = self.cursor.fetchone()
            if result:
                return FileConfig(*result)
            else:
                raise RuntimeError(f"File configuration with feed_key '{feed_key}' not found.")
        except Exception as e:
            raise RuntimeError(f"Failed to get file configuration. Caused by: {e}")

    def get_file_config_by_file_path_status(self, file_path: str, status: str):
        """Get file configuration by file path and status"""
        try:
            self.cursor.execute(
                f"SELECT file_config.* FROM file_log INNER JOIN file_config ON file_log.id_config = file_config.id  WHERE file_path = '{file_path}' AND status = '{status}'")
            result = self.cursor.fetchone()
            if result:
                return FileConfig(*result)
            else:
                raise RuntimeError(
                    f"File log with file path '{file_path}' and status '{ServiceStatus.get_value(status)}' not found.")
        except Exception as e:
            raise RuntimeError(f"Failed to get file log. Caused by: {e}")

    def create_file_log(self, procname, config_id, status: ServiceStatus, file_path):
        """Create file log"""
        try:
            self.cursor.callproc(procname,
                                 (config_id, ServiceStatus.get_value(status), file_path, status_message.get(status)))
            self.connection.commit()
        except Exception as e:
            raise RuntimeError(f"Failed to create file log. Caused by: {e}")

    def update_progress_to_ui(self, event_level: EventLevel, message):
        """Update service progress to UI (Ex: Ready extract, Extracting, Successful extract, Failed extract, ...)"""
        self.event_bus.publish(EventType.SERVICE_NOTIFY_PROGRESS, Event(event_level, message))

    def update_log_to_ui(self, event_level: EventLevel, message):
        """Update service log to UI. (Ex: Error fetching {url}: {e})"""
        self.event_bus.publish(EventType.SERVICE_NOTIFY_LOG, Event(event_level, message))

    def save_df_to_csv_file(self, df, file_path):
        """Save data to file"""
        try:
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            df.to_csv(file_path, index=False)
            os.path.abspath(file_path)
        except Exception as e:
            raise RuntimeError(f"Failed to save data to file. Caused by: {e}")

    def load_environment(self):
        try:
            load_dotenv()
            return {'ctrlDbHost': os.getenv('CONTROL_DB_HOST'),
                    'ctrlDbUser': os.getenv('CONTROL_DB_USER'),
                    'ctrlDbPassword': os.getenv('CONTROL_DB_PASSWORD'),
                    'ctrlDbName': os.getenv('CONTROL_DB_NAME'),
                    'ctrlDbPort': int(os.getenv('CONTROL_DB_PORT')),
                    'feedKey': os.getenv('CPS_FEED_KEY'),
                    'configTableName': os.getenv('FILE_CONFIG_TABLE_NAME'),
                    'logTableName': os.getenv('FILE_LOG_TABLE_NAME'),
                    'insertLogProcName': os.getenv('CREATE_FILE_LOG_PROC_NAME'),
                    'cpsDefaultItemsPerPage': os.getenv('CPS_DEFAULT_ITEMS_PER_PAGE'),
                    'cpsXhrQuery': os.getenv('CPS_XHR_QUERY'),
                    }
        except Exception as e:
            raise RuntimeError(f"Failed to load environment variables. Caused by: {e}")

    def crawl(self, base_url, start_page, num_pages, req_payload, items_per_page):
        try:
            product_details = []

            for page in range(start_page, num_pages + 1):
                response = None
                req_payload = req_payload.replace('%current_page%', str(page))
                req_payload = req_payload.replace('%items_per_page%', str(items_per_page))

                try:
                    # 1.5.2.1 - Fetch json from url
                    response = self.fetch_json(base_url, req_payload)
                    if response is not None:
                        response = response.json()
                except Exception as e:

                    # 1.5.2.5 - Raise error if failed to fetch json
                    raise RuntimeError(f"Failed to crawl data from {base_url}. Caused by: {e}")

                # 1.5.2.2 - Crawling data
                data_crawled = parse_product_details(response)

                # 1.5.2.3 - Append data to list
                product_details.append(data_crawled)

                print(f"Finished scraping page {page}")
                self.update_log_to_ui(EventLevel.SUCCESS, f"Finished scraping page {page}")
                time.sleep(1)
            df = pd.concat(product_details, ignore_index=True)

            print(df)
            # Generate id
            df['id'] = range(1, len(df) + 1)
            # Make id column stand at first column
            df = df[['id'] + df.columns[:-1].tolist()]
            # Make date column at the tail of df
            df['date'] = pd.to_datetime(datetime.now().date())

            # 1.5.2.4 - Return data frame
            return df

        except Exception as e:
            raise RuntimeError(f"Failed to crawl data. Caused by: {e}")

    def run(self, status=None, file_path=None):
        # 1.1 - Load environment variables
        env_variables = self.load_environment()
        # print(env_variables)

        try:
            # 1.2 - Connect to control database
            self.connect_to_db(env_variables['ctrlDbHost'], env_variables['ctrlDbUser'],
                               env_variables['ctrlDbPassword'], env_variables['ctrlDbName'],
                               env_variables['ctrlDbPort'])
        except Exception as e:
            #   1.6 - Failed to connect to database then update log and progress to UI
            self.update_log_to_ui(EventLevel.ERROR, f"Failed to connect to database. Caused by: {e}")
            self.update_progress_to_ui(EventLevel.ERROR, f"Failed to connect to database. Caused by: {e}")

            # 1.8 - Close connection
            self.close_connection()
            return

        if status is not None and file_path is not None:
            try:
                # 1.3.a - Get file configuration by file path and status for manual run
                print(file_path, status)
                self.config = self.get_file_config_by_file_path_status(file_path, status)
                print(self.config)
            except Exception as e:
                # 1.6 - Failed to get file configuration then update log and progress to UI
                self.update_log_to_ui(EventLevel.ERROR, f"Failed to get file configuration. Caused by: {e}")
                self.update_progress_to_ui(EventLevel.ERROR, f"Failed to get file configuration. Caused by: {e}")

                #1.8 - Close connection
                self.close_connection()
                return

        else:
            try:
                # 1.3.b - Get file configuration by feed key for auto run
                self.config = self.get_file_config(env_variables['feedKey'])
            except Exception as e:
                # 1.6 - Failed to get file configuration then update log and progress to UI
                self.update_log_to_ui(EventLevel.ERROR, f"Failed to get file configuration. Caused by: {e}")
                self.update_progress_to_ui(EventLevel.ERROR, f"Failed to get file configuration. Caused by: {e}")

                # 1.8 - Close connection
                self.close_connection()
                return

        # 1.4 - Create file log with status RE (Ready Extract)
        self.file_path = generate_file_name(self.config.folder_data_path)
        self.create_file_log(env_variables['insertLogProcName'], self.config.id, ServiceStatus.RE, self.file_path)

        # 1.5 - Extract data
        try:
            # 1.5.1 - Create file log with status EX (Extracting)
            self.create_file_log(env_variables['insertLogProcName'], self.config.id, ServiceStatus.EX, self.file_path)

            try:
                # 1.5.2 - Start crawling
                data_frame = self.crawl(self.config.source_url, self.config.start_page, self.config.num_pages,
                                        env_variables['cpsXhrQuery'], env_variables['cpsDefaultItemsPerPage'])
            except Exception as e:
                raise RuntimeError(f"Failed to extract data. Caused by: {e}")

            # 1.5.3 - Save data to file
            self.save_df_to_csv_file(data_frame, self.file_path)

            # 1.5.4 -  Create file log with status SE (Successful Extract)
            self.create_file_log(env_variables['insertLogProcName'], self.config.id, ServiceStatus.SE, self.file_path)

            # 1.5.5 - Update log and progress to UI
            self.update_log_to_ui(EventLevel.SUCCESS, "Extract successful")
            self.update_progress_to_ui(EventLevel.SUCCESS, "Extract successful")

            # 1.5.6 - Create file log with status RP (Ready Process)
            self.create_file_log(env_variables['insertLogProcName'], self.config.id, ServiceStatus.RP, self.file_path)
        except Exception as e:
            # 1.6 - Update log and progress to UI
            self.update_log_to_ui(EventLevel.ERROR, f"Failed to extract data. Caused by: {e}")
            self.update_progress_to_ui(EventLevel.ERROR, f"Failed to extract data. Caused by: {e}")

            # 1.7 - Create file log with status FE (Failed Extract)
            self.create_file_log(env_variables['insertLogProcName'], self.config.id, ServiceStatus.FE, self.file_path)
            return
        finally:
            # 1.8 - Close connection
            self.close_connection()
            return