import unittest
from utils import is_valid_description

class TestSecurityIncident(unittest.TestCase):
    
    def test_description_valid(self):
        # (Boundary case: exactly 5 characters)"""
        # This should pass
        self.assertTrue(is_valid_description("Spill"))
        self.assertTrue(is_valid_description("Spillage in the lab"))

    def test_description_too_short(self):
        # it should be invalid
        self.assertFalse(is_valid_description("Spil"))

    def test_description_long_text(self):
        
        self.assertTrue(is_valid_description("Water leak in the server room"))

    def test_description_empty(self):
        # empty should be false
        self.assertFalse(is_valid_description(""))

if __name__ == '__main__':
    unittest.main()