""" predict.py

Function to predict named entities for text based on (custom) trained spaCy model.
"""

from typing import List
from pandas import DataFrame
import spacy


def predict(model: spacy.Language,
            dataframe: DataFrame,
            word_remove: List[str] = None) -> tuple:
    """ Return persons and locations extracted from text using (custom) trained spaCy model for NER.

    :param model: the (custom) spaCy NER model
    :param dataframe: text formatted as DataFrame
    :param word_remove: list of words to remove, defaults to None
    """

    if word_remove is None:
        word_remove = []

    # predict entities for text per line using the model:
    all_persons = []
    all_locations = []
    for line in list(dataframe["text"]):
        doc = model(line)
        all_persons.append([ent.text for ent in doc.ents if ent.label_ == 'PERSON' and ent.text not in word_remove])
        all_locations.append([ent.text for ent in doc.ents if ent.label_ == 'LOC' and ent.text not in word_remove])

    return all_persons, all_locations

