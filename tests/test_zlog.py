import os
import json
from datetime import datetime
from unittest import TestCase
from zoneinfo import ZoneInfo

from zlogger_kit.zlog import ZLog
from zlogger_kit.models import ZLogConfig, ZNetworkRequest, ZNetworkResponse
from zlogger_kit.enums import ZLogLevel, ZNetworkOperation, ZModule


class TestZLog(TestCase):
    def setUp(self):
        self.test_dir = "test_logs"
        self.config = ZLogConfig(
            module=ZModule.TEST_JSON_FORMAT,
            log_path=self.test_dir,
            time_zone="Asia/Riyadh",
            json_format=True,
        )
        os.makedirs(self.test_dir, exist_ok=True)
        self.logger = ZLog.init(self.config)

    def tearDown(self):
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)
        ZLog._instances = {}

    def test_singleton_pattern(self):
        logger1 = ZLog.init(self.config)
        logger2 = ZLog.init(self.config)
        self.assertIs(logger1, logger2)

        other_config = ZLogConfig(
            module=ZModule.OTHER,
            log_path=self.test_dir,
            time_zone="UTC",
            json_format=True,
        )
        logger3 = ZLog.init(other_config)
        self.assertIsNot(logger1, logger3)

    def test_log_file_creation(self):
        test_time = datetime(2024, 1, 1, tzinfo=ZoneInfo("Asia/Riyadh"))
        self.logger.set_current_time(test_time)
        self.logger.info("Test message")

        expected_filename = f"{ZModule.TEST_JSON_FORMAT.value}-2024-01-01.log"
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, expected_filename)))

    def test_log_levels(self):
        test_time = datetime(2024, 1, 1, tzinfo=ZoneInfo("Asia/Riyadh"))
        self.logger.set_current_time(test_time)

        test_message = "Test message"
        self.logger.debug(test_message)
        self.logger.info(test_message)
        self.logger.warn(test_message)
        self.logger.error(test_message)

        log_file = os.path.join(
            self.test_dir, f"{ZModule.TEST_JSON_FORMAT.value}-2024-01-01.log"
        )
        with open(log_file, "r") as f:
            logs = f.readlines()

        self.assertEqual(len(logs), 4)
        for log, level in zip(
            logs, [ZLogLevel.DEBUG, ZLogLevel.INFO, ZLogLevel.WARNING, ZLogLevel.ERROR]
        ):
            log_data = json.loads(log)
            self.assertEqual(log_data["level"], level.value)
            self.assertEqual(log_data["message"], test_message)

    def test_error_logging(self):
        test_error = ValueError("Test error")
        self.logger.error("Error occurred", error=test_error)

        log_file = os.path.join(
            self.test_dir,
            f"{ZModule.TEST_JSON_FORMAT.value}-{datetime.now().strftime('%Y-%m-%d')}.log",
        )
        with open(log_file, "r") as f:
            log_data = json.loads(f.readline())

        self.assertEqual(log_data["error"], str(test_error))
        self.assertEqual(log_data["level"], ZLogLevel.ERROR.value)

    def test_network_logging(self):
        test_time = datetime(2024, 1, 1, tzinfo=ZoneInfo("Asia/Riyadh"))
        self.logger.set_current_time(test_time)

        request = ZNetworkRequest(method="GET", url="https://api.example.com")
        self.logger.network_request(request, ip="127.0.0.1")

        response = ZNetworkResponse(status_code=200)
        self.logger.network_response(response, ip="127.0.0.1")

        log_file = os.path.join(
            self.test_dir, f"{ZModule.TEST_JSON_FORMAT.value}-2024-01-01.log"
        )
        with open(log_file, "r") as f:
            logs = f.readlines()

        request_log = json.loads(logs[0])
        response_log = json.loads(logs[1])

        self.assertEqual(request_log["operation"], ZNetworkOperation.REQUEST.value)
        self.assertEqual(request_log["method"], "GET")
        self.assertEqual(request_log["url"], "https://api.example.com")
        self.assertEqual(request_log["ip"], "127.0.0.1")

        self.assertEqual(response_log["operation"], ZNetworkOperation.RESPONSE.value)
        self.assertEqual(response_log["status_code"], 200)
        self.assertEqual(response_log["ip"], "127.0.0.1")

    def test_text_format_logging(self):
        config = ZLogConfig(
            module=ZModule.TEST_TEXT_FORMAT,
            log_path=self.test_dir,
            time_zone="Asia/Riyadh",
            json_format=False,
        )
        logger = ZLog.init(config)
        test_time = datetime(2024, 1, 1, tzinfo=ZoneInfo("Asia/Riyadh"))
        logger.set_current_time(test_time)

        test_message = "Test message"
        logger.info(test_message)

        log_file = os.path.join(self.test_dir, "test_text_format-2024-01-01.log")
        with open(log_file, "r") as f:
            log_line = f.readline().strip()

        expected_components = [
            "2024-01-01",
            "[INFO]",
            "Test",
            test_message,
        ]

        for component in expected_components:
            self.assertIn(component, log_line)

    def _is_json(self, string):
        try:
            json.loads(string)
            return True
        except json.JSONDecodeError:
            return False
