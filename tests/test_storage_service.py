import pytest
import tempfile
import shutil
from src.storage_service import StorageService


class TestStorageService:
    @pytest.fixture
    def temp_service(self):
        temp_dir = tempfile.mkdtemp()
        service = StorageService(data_dir=temp_dir)
        yield service
        shutil.rmtree(temp_dir)

    def test_add_history_record(self, temp_service):
        record = {"action": "test", "user": "john"}
        result = temp_service.add_history_record(record)
        assert result is True

    def test_get_all_history_records(self, temp_service):
        record = {"action": "test"}
        temp_service.add_history_record(record)
        records = temp_service.get_all_history_records()
        assert len(records) == 1
        assert records[0]["action"] == "test"

    def test_get_all_config(self, temp_service):
        temp_service.save_config_entry("key1", "value1")
        config = temp_service.get_all_config()
        assert config["key1"] == "value1"

    def test_save_config_entry(self, temp_service):
        result = temp_service.save_config_entry("test_key", "test_value")
        assert result is True
