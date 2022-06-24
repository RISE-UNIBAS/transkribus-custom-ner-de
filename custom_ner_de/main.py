""" main.py

Main app. """

from __future__ import annotations
from custom_ner_de.client import Client
import os.path

DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
WORD_REMOVE = ["BASEL", "HÃ¤ndeklatschen"]
PERSON_NAMES = ['Gustav Gottheil']
LOCATION_NAMES = ['Boston', 'Roman']
ZIP_PATH = PARENT_DIR + "/sample/Protokoll-Zionistenkongress-Basel_1897-0200.zip"
TEXT_PATH = PARENT_DIR + "/sample/03_Protokoll-Zionistenkongress-Basel_1899.txt"
MODEL_PATH = PARENT_DIR + "/sample/custom_ner_de_model"


def main():

    my_client = Client()

    my_client.train_model(zip_url=ZIP_PATH,
                          word_remove=WORD_REMOVE,
                          person_names=PERSON_NAMES,
                          location_names=LOCATION_NAMES,
                          epochs=1,
                          _local=True)

    my_client.apply_model(text_url=TEXT_PATH,
                          _local=True)

    print(my_client.result)
    my_client.save_result2csv()

    my_client.evaluate_model()
    my_client.evaluate_model(model_path=MODEL_PATH)


main()
