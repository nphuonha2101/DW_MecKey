import os
import time
from abc import ABC

from bs4 import BeautifulSoup
from dotenv import load_dotenv

from db.db_manager import DatabaseManager
from event.event_level import EventLevel
from model.file_config import FileConfig
from services.extract.abs_extract import AbsExtract
import pandas as pd
from datetime import datetime
from utils.convert_utils import convert_price
from services.status.service_status import ServiceStatus

load_dotenv()


def generate_file_name(data_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f'{data_path}/akko_{timestamp}.csv'


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

    # Lấy thông tin switch từ bảng
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


class AkkoExtract(AbsExtract, ABC):
    def __init__(self, database_manager: DatabaseManager):
        super().__init__(database_manager)
        self.feed_key = os.getenv('AKKO_FEED_KEY')

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
        if ul_tags:
            print(f"Found {len(ul_tags)} <ul> tags")
        else:
            print("No <ul> tags found")

        for ul in ul_tags:
            li = ul.find('li', string=lambda content: "Model" in content if content else False)
            if li:
                print("Found <ul> with 'Model'")
                return scrape_product_in_list(detail_soup, ul)

        # Check for p tags
        p_tags = detail_soup.find_all('p')
        if p_tags:
            print(f"Found {len(p_tags)} <p> tags")
        else:
            print("No <p> tags found")

        for p_tag in p_tags:
            if 'Model' in p_tag.get_text():
                print("Found <p> with 'Model'")
                return scrape_product_in_text(p_tag)

        print("No relevant tags found")
        return {}

    def extract(self, num_pages):
        config: FileConfig = self.get_file_config(self.feed_key)
        if config is None:
            self.update_ui(EventLevel.ERROR, "Failed to load configuration.")
            return
        base_url = config.source_url
        data_path = config.file_path

        file_path = generate_file_name(data_path)

        log_id = self.create_file_log(config.id, ServiceStatus.RE, file_path)

        product_details = []
        num_pages = int(num_pages)
        for page in range(1, num_pages + 1):
            url = f"{base_url}{page}/"
            response = self.fetch_page(url)
            if response is not None:
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
                    product_details.append({
                        'name': name,
                        'price': price,
                        'image': image,
                        **details,  # Thêm thông tin chi tiết vào từ điển
                    })
                print(f"Finished scraping page {page}")
                self.update_ui(EventLevel.SUCCESS, f"Finished scraping page {page}")
                time.sleep(1)  # Thêm thời gian chờ giữa các yêu cầu
            else:
                print(f"Failed to retrieve page {page}.")
                self.update_file_log(log_id, ServiceStatus.FE)
                self.update_ui(EventLevel.ERROR, f"Failed to retrieve page {page}.")
                return

        df = pd.DataFrame(product_details)

        if not os.path.exists(data_path):
            os.makedirs(data_path)

        df.to_csv(file_path, index=False)

        absolute_path = os.path.abspath(file_path)
        print(f"Data saved to '{absolute_path}'.")
        self.update_ui(EventLevel.SUCCESS, f"Data saved to '{absolute_path}'.")

        self.update_file_log(log_id, ServiceStatus.SE)

    def run(self):
        try:
            page = os.getenv('AKKO_PAGE')
            self.update_ui(EventLevel.INFO, f"${self.__class__.__name__}" + " is running")
            self.extract(page)
            self.update_ui(EventLevel.SUCCESS, f"${self.__class__.__name__}" + " is finished")
        except Exception as e:
            self.update_ui(EventLevel.ERROR, f"${self.__class__.__name__} got problem. Caused by: {e}")
            print(f"Error: {e}")


