""" test.py

Unittest. """

import os.path
import unittest
from custom_ner_de.extract import extract_entities

DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))


class TestExtract(unittest.TestCase):
    """ Test extract function. """

    def setUp(self) -> None:
        self.input = DIR + "/input.zip"

        self.extract_gold = DIR + "/extract_gold.txt"

    def test_extract_entities(self):
        """ blah. """

        entities = extract_entities(zip_path=self.input)
        with open(self.extract_gold, mode="r", encoding="utf-8") as file:
            gold_entities = file.read()
        print(gold_entities)
        self.assertEqual(entities, gold_entities.rstrip())


if __name__ == '__main__':
    unittest.main()