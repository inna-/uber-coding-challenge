#!/usr/bin/python
import unittest

from csvtodb import *

class CSVTests(unittest.TestCase):
    def test_foodParser1(self):
        food = "Hot dogs:burgers: soda"
        parsed = foodParser(food)
        self.assertEqual(3, len(parsed))
        self.assertEqual('hot dogs', parsed[0])
        self.assertEqual('burgers', parsed[1])
        self.assertEqual('soda', parsed[2])
        parsed = foodParser(food)
        self.assertEqual(len(set(parsed)), len(parsed))

    def test_formatting(self):
        food = "a : B:c:d"
        parsed = foodParser(food)
        for item in parsed:
            self.assertEqual(item.strip(), item)
            self.assertEqual(item.lower(), item)

    def test_singleton(self):
        food = "pizza"
        parsed = foodParser(food)
        self.assertEqual(["pizza"], parsed)

    def test_foodParser2(self):
        food = "Vietnamese sandwiches: various meat rice plates & bowls: vermicelli: spring rolls: sticky rice: Vietnamese Goi: coffee:  various flavored tea : various soda and juices: water."

        parsed = foodParser(food)
        self.assertEqual(len(set(parsed)), len(parsed))

if __name__ == "__main__":
    unittest.main()
