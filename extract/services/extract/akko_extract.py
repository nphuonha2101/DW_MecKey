import os
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import pymysql

from event.event_bus import EventBus
from event.event_level import EventLevel
from model.file_config import FileConfig
import pandas as pd
from datetime import datetime
from utils.convert_utils import convert_price
from services.status.service_status import ServiceStatus
from services.status.status_message import status_message
from event.event import Event
from event.event_type import EventType
import requests


def generate_file_name(data_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # return f'{data_path}/akko_{timestamp}.csv'
    result = f'{data_path}/akko_{timestamp}.csv'
    result = result.replace("\\", "/")
    result = result.replace("//", "/")
    return result


def scrape_product_in_list(detail_soup, ul_tag):
    """Trích xuất thông tin chi tiết của sản phẩm từ danh sách ul trên trang chi tiết."""
    data = {
        'name': 'Unknown',  # Thêm giá trị mặc định
        'price': 'Unknown',  # Thêm giá trị mặc định
        'image': 'https://akkogear.com.vn/wp-content/uploads/2020/06/3108-3087-hotkey-upload.jpg',  # URL ảnh
        'model': None,
        'mode': None,
        'switch': None,
        'hotswap': 'Unknown',  # Không có thông tin hotswap trong đoạn này
        'keycap': None,
        'size': None,
        'weight': 'Unknown',  # Không có thông tin về weight
        'accessory': None
    }

    for li in ul_tag.find_all('li'):
        text = li.get_text(strip=True)
        if 'Model' in text:
            data['model'] = text.split(':')[-1].strip()
        elif 'Kết nối' in text:
            data['mode'] = text.split('–')[0].split(':')[-1].strip()
            data['size'] = text.split('Kích thước:')[-1].strip()
        elif 'Keycap' in text:
            data['keycap'] = text.split(':')[-1].strip()
        elif 'Loại switch' in text:
            data['switch'] = text.split(':')[-1].strip()
        elif 'Phụ kiện' in text:
            data['accessory'] = text.split(':')[-1].strip()

    switch_table = detail_soup.find('table', class_='woocommerce-product-attributes shop_attributes')
    switch_value = switch_table.find('td').get_text(strip=True)
    data['switch'] = switch_value

    print(data)
    return data


def scrape_product_in_text(p_tag):
    """Trích xuất thông tin chi tiết của sản phẩm từ đoạn văn bản trên trang chi tiết."""
    content_lines = p_tag.decode_contents().split('<br/>')

    # Khởi tạo dictionary để lưu trữ kết quả
    data = {
        'model': '',
        'mode': '',
        'size': '',
        'weight': '',
        'keycap': '',
        'switch': '',
        'accessory': ''
    }

    for line in content_lines:
        for line in content_lines:
            if 'Model:' in line:
                data['model'] = line.split('Model:')[-1].strip()
            elif 'Kết nối:' in line:
                data['mode'] = line.split('Kết nối:')[-1].strip()
            elif 'Kích thước:' in line:
                size_weight = line.split('|')
                data['size'] = size_weight[0].split('Kích thước:')[-1].strip()
                if len(size_weight) > 1:
                    data['weight'] = size_weight[1].split('Trọng lượng')[-1].strip()
            elif 'Keycap:' in line:
                data['keycap'] = line.split('Keycap:')[-1].strip()
            elif 'Loại switch:' in line:
                data['switch'] = line.split('Loại switch:')[-1].strip()
            elif 'Phụ kiện:' in line:
                data['accessory'] = line.split('Phụ kiện:')[-1].strip()

    print(data)
    return data


def scrape_product_in_table(table_tag):
    """Trích xuất thông tin chi tiết của sản phẩm từ bảng trên trang chi tiết."""
    data = {
        'model': None,
        'mode': None,
        'switch': None,
        'hotswap': None,
        'keycap': None,
        'size': None,
        'weight': None,
        'accessory': None
    }

    # Tìm tất cả các dòng trong bảng
    rows = table_tag.find_all('tr')

    # Lặp qua các dòng và gán giá trị tương ứng vào dictionary
    for row in rows:
        cells = row.find_all('td')
        key = cells[0].get_text(strip=True)
        value = cells[1].get_text(strip=True)

        if key == 'Model':
            data['model'] = value
        elif key == 'Cấu Trúc':
            data['mode'] = value
        elif key == 'Switches':
            data['switch'] = value
        elif key == 'Hot Swappable':
            data['hotswap'] = value
        elif key == 'Keycaps':
            data['keycap'] = value
        elif key == 'Kích Thước':
            data['size'] = value
        elif key == 'Trọng lượng':
            data['weight'] = value
        elif key == 'Phụ Kiện':
            data['accessory'] = value

    print(data)
    return data


def parse_product(product):
    """Trích xuất thông tin từ một sản phẩm."""
    # Lấy hình ảnh, tên, giá và link chi tiết
    image = product.select_one('img.show-on-hover')['src'] if product.select_one('img.show-on-hover') else ''
    name = product.select_one('.name a').text.strip() if product.select_one('.name a') else ''
    price = product.select_one('bdi').text.strip() if product.select_one('bdi') else ''
    detail_url = product.select_one('.image-fade_in_back a')['href'] if product.select_one(
        '.image-fade_in_back a') else ''
    return image, name, price, detail_url


class AkkoExtract:
    def __init__(self, event_bus: EventBus):
        self.file_path = None
        self.config = None
        self.connection = None
        self.cursor = None
        self.event_bus = event_bus

    def fetch_page(self, url):
        """Fetch page from url then return response"""
        try:
            response = requests.get(url)
            response.raise_for_status()  # Kiểm tra lỗi HTTP
            return response
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            self.update_log_to_ui(EventLevel.ERROR, f"Error fetching {url}: {e}")
            return None

    def scrape_product_details(self, detail_url):
        """Trích xuất thông tin chi tiết của sản phẩm từ trang chi tiết."""
        detail_response = self.fetch_page(detail_url)
        if detail_response is None:
            return {}

        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

        for table in detail_soup.find_all('table'):
            if table.find('td', string="Model"):
                table_with_model = table
                print("Found table with model")
                return scrape_product_in_table(table_with_model)

        # Check for ul tags
        ul_tags = detail_soup.find_all('ul')

        for ul in ul_tags:
            li = ul.find('li', string=lambda content: "Model" in content if content else False)
            if li:
                print("Found <ul> with 'Model'")
                return scrape_product_in_list(detail_soup, ul)

        # Check for p tags
        p_tags = detail_soup.find_all('p')

        for p_tag in p_tags:
            if 'Model' in p_tag.get_text():
                print("Found <p> with 'Model'")
                return scrape_product_in_text(p_tag)

        print("No relevant tags found")
        return {}

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

    def create_file_log(self, procname, config_id, status: ServiceStatus, file_path):
        """Create file log"""
        try:
            self.cursor.callproc(procname,
                                 (config_id, ServiceStatus.get_value(status), file_path, status_message.get(status)))
            self.connection.commit()
        except Exception as e:
            raise RuntimeError(f"Failed to create file log. Caused by: {e}")

    def get_file_config_by_file_path_status(self, file_path, status):
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

    def crawl(self, base_url, start_page, num_pages):
        try:
            product_details = []

            for page in range(start_page, num_pages + 1):
                url = f"{base_url}{page}/"
                response = None
                try:
                    # 1.5.2.1 - Send request to fetch page
                    response = self.fetch_page(url)
                except Exception as e:
                    raise RuntimeError(f"Failed to fetch page {page}. Caused by: {e}")

                if response is not None:
                    # 1.5.2.2 - Crawl data
                    soup = BeautifulSoup(response.text, 'html.parser')
                    products = soup.select('div.product-small.col')
                    for product in products:
                        image, name, price, detail_url = parse_product(product)

                        if not detail_url:
                            print(f"Skipping product {name} with no detail URL")
                            continue
                        if not image:
                            print(f"Skipping product {name} with no image")
                            continue

                        if not price:
                            print(f"Skipping product {name} with no price")
                            continue

                        price = convert_price(price)
                        details = self.scrape_product_details(detail_url)

                        # 1.5.2.3 - Append data to list
                        product_details.append({
                            'name': name,
                            'price': price,
                            'image': image,
                            **details,
                        })
                    print(f"Finished scraping page {page}")

                    self.update_log_to_ui(EventLevel.SUCCESS, f"Finished scraping page {page}")
                    time.sleep(1)
                else:
                    raise RuntimeError(f"Failed to fetch page {page}. Response is None")

            df = pd.DataFrame(product_details)

            df.drop(columns=['hotswap'], inplace=True)
            # Generate id
            df['id'] = range(1, len(df) + 1)
            # Make id column stand at first column
            df = df[['id'] + df.columns[:-1].tolist()]
            # Make date column at the tail of df
            df['date'] = pd.to_datetime(datetime.now().date())

            # 1.5.2.4 - Return DataFrame
            return df
        except Exception as e:
            # 1.5.2.5 - Raise error
            raise RuntimeError(f"Failed to extract data. Caused by: {e}")

    def load_environment(self):
        try:
            load_dotenv()
            return {'ctrlDbHost': os.getenv('CONTROL_DB_HOST'),
                    'ctrlDbUser': os.getenv('CONTROL_DB_USER'),
                    'ctrlDbPassword': os.getenv('CONTROL_DB_PASSWORD'),
                    'ctrlDbName': os.getenv('CONTROL_DB_NAME'),
                    'ctrlDbPort': os.getenv('CONTROL_DB_PORT'),
                    'feedKey': os.getenv('AKKO_FEED_KEY'),
                    'configTableName': os.getenv('FILE_CONFIG_TABLE_NAME'),
                    'logTableName': os.getenv('FILE_LOG_TABLE_NAME'),
                    'insertLogProcName': os.getenv('CREATE_FILE_LOG_PROC_NAME'),
                    }
        except Exception as e:
            raise RuntimeError(f"Failed to load environment variables. Caused by: {e}")

    def run(self, status=None, file_path=None):
        print(status, file_path)
        # 1.1 - Load environment variables
        env_variables = self.load_environment()
        print(env_variables)

        try:
            # 1.2 - Connect to database
            self.connect_to_db(env_variables['ctrlDbHost'], env_variables['ctrlDbUser'],
                               env_variables['ctrlDbPassword'], env_variables['ctrlDbName'], int(env_variables['ctrlDbPort']))
        except Exception as e:
            self.update_log_to_ui(EventLevel.ERROR, f"Failed to connect to database. Caused by: {e}")
            self.update_progress_to_ui(EventLevel.ERROR, f"Failed to connect to database")
            raise RuntimeError(f"Failed to connect to database. Caused by: {e}")


        if status is not None and file_path is not None:
            try:
                # 1.3.a - Get file configuration by file path and status for manual run
                self.config = self.get_file_config_by_file_path_status(file_path, status)
                print(self.config)
            except Exception as e:
                # 1.6 - Failed to get file log then update log and progress to UI
                self.update_log_to_ui(EventLevel.ERROR, f"Failed to get file log. Caused by: {e}")
                self.update_progress_to_ui(EventLevel.ERROR, f"Failed to get file log. Caused by: {e}")

                # 1.8 - Close connection
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
                # 1.5.2 - Crawl data
                data_frame = self.crawl(self.config.source_url, self.config.start_page, self.config.num_pages)
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

