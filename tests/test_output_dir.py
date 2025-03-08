import os
import unittest

from src.utils.data_saver import OUTPUT_DIR


class TestOutputDirectory(unittest.TestCase):
    def test_output_directory_location(self):
        expected_path = os.path.abspath(os.path.join(os.getcwd(), "output"))
        self.assertEqual(OUTPUT_DIR, expected_path, "OUTPUT_DIR is not set correctly")

    def test_output_directory_creation(self):
        os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure directory exists
        self.assertTrue(os.path.exists(OUTPUT_DIR), "OUTPUT_DIR was not created")

if __name__ == "__main__":
    unittest.main()
