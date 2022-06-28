""" test.py

Unittest. """

import os.path
import unittest
from transkribus_custom_ner_de.gold_standard import GoldStandard

DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))


class TestGoldStandard(unittest.TestCase):
    """ Test GoldStandard. """

    def setUp(self) -> None:
        self.input = DIR + "/input.zip"
        self.gold_standard = GoldStandard()
        self.gold_standard_benchmark = DIR + "/gold_standard_benchmark.txt"

    def test_extract_entities(self):
        """ Test extract_entities function. """

        with open(self.gold_standard_benchmark, mode="r", encoding="utf-8") as file:
            gold_standard_benchmark = file.read()
        self.gold_standard.make(zip_path=self.input)
        self.assertEqual(gold_standard_benchmark,  "\n".join(str(item) for item in self.gold_standard.full))


if __name__ == '__main__':
    unittest.main()
