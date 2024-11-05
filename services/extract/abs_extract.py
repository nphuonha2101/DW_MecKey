from abc import ABC

from db.db_manager import DatabaseManager
from event.event_bus import EventBus
from event.event_level import EventLevel
from services.abstract_services import AbstractService
import requests


class AbsExtract(AbstractService, ABC):
    def __init__(self, database_manager: DatabaseManager, event_bus: EventBus):
        super().__init__(database_manager, event_bus)


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