""" main.py

Main app. """

from __future__ import annotations
from custom_ner_de.extract import extract_entities
from custom_ner_de.train import custom_ner_training
import os.path

DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
WORD_REMOVE = ["BASEL", "HÃ¤ndeklatschen"]
PERSON_NAMES = ['Gustav Gottheil']
LOCATION_NAMES = ['Boston', 'Roman']

from custom_ner_de.client import Client

Client().run(zip_url="e",
             word_remove=WORD_REMOVE,
             person_names=PERSON_NAMES,
             location_names=LOCATION_NAMES
             )

exit()


def main() -> None:
    """ bla """

    entities = extract_entities(zip_path=PARENT_DIR + "/sample/Protokoll-Zionistenkongress-Basel_1897-0200.zip",
                                word_remove=WORD_REMOVE)

    custom_ner_training(entities=entities,
                        save_dir=PARENT_DIR + "/sample/debug2/",
                        person_names=PERSON_NAMES,
                        location_names=LOCATION_NAMES)


main()
