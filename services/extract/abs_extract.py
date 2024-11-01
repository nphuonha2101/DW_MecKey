from abc import ABC, abstractmethod

from db.db_manager import DatabaseManager
from event.event_level import EventLevel
from services.abstract_services import AbstractService
import requests


class AbsExtract(AbstractService, ABC):
    def __init__(self, database_manager: DatabaseManager):
        super().__init__(database_manager)

    def fetch_page(self, url):
        """Gửi yêu cầu đến một URL và trả về phản hồi."""
        try:
            response = requests.get(url)
            response.raise_for_status()  # Kiểm tra lỗi HTTP
            return response
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            self.update_ui(EventLevel.ERROR, f"Error fetching {url}: {e}")
            return None