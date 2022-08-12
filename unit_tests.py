#!/usr/bin/env python3
"""
Tests for e164convert
"""
import imp 
import json
import unittest

ec = imp.load_source("e164convert", "/home/david/MSWE2022/e164convert/e164convert") #has no .py extension

def load_cases(filename: str) -> list:
    """Load test cases list from the relevant file in testcases/"""
    try:
        with open(f"testcases/{filename}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Test case file '{filename}.json' not found under testcases/")

class TestClean(unittest.TestCase):
    """Tests for clean(user_input: str)"""
    
    def test_clean(self):
        for case in load_cases("unit_clean"):
            self.assertEqual(ec.clean(case[0]), case[1], f"clean({case[0]}) should return {case[1]}")

class TestIsUKValid(unittest.TestCase):
    """Tests for is_uk_valid(phone_number: str)"""
    
    def test_is_uk_valid(self):
        for case in load_cases("unit_isukvalid"):
            self.assertEqual(ec.is_uk_valid(case[0]), case[1], f"is_uk_valid({case[0]}) should return {case[1]}")

class TestGetE164(unittest.TestCase):
    """Tests for get_e164(phone_number: str)"""
    
    def test_get_e164(self):
        for case in load_cases("unit_gete164"):
            self.assertEqual(ec.get_e164(case[0]), case[1], f"get_e164({case[0]}) should return {case[1]}")

def main():
    unittest.main()
 
if __name__ == "__main__":
    main()
