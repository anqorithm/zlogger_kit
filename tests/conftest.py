import pytest
import os


@pytest.fixture(autouse=True)
def cleanup_test_logs():
    """Clean up test logs before and after each test"""
    test_dir = "test_logs"
    if os.path.exists(test_dir):
        for file in os.listdir(test_dir):
            os.remove(os.path.join(test_dir, file))
        os.rmdir(test_dir)

    yield

    if os.path.exists(test_dir):
        for file in os.listdir(test_dir):
            os.remove(os.path.join(test_dir, file))
        os.rmdir(test_dir)
