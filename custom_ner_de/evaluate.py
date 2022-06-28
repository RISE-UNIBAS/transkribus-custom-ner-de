""" evaluate.py

Evaluate function.
"""

from spacy import Language
from spacy.training import Example
from typing import List


def evaluate_model(model: Language = None,
                   gold_standard: List[tuple] = None) -> None:
    """ Evaluate a (custom) NER model based on a gold standard.

    :param model: the NER model, defaults to None
    :param gold_standard: the gold standard, defaults to None
    """

    data = [Example.from_dict(model.make_doc(text), annotation) for text, annotation in gold_standard]
    scores_model = model.evaluate(data)

    print("-- Model scores:")
    print("Precision: ", scores_model["ents_p"])
    print("Recall: ", scores_model["ents_r"])
    print("F1 Score: ", scores_model["ents_f"])
    print("-- Person entity scores:")
    print("Precision: ", scores_model["ents_per_type"]['PERSON']['p'])
    print("Recall: ", scores_model["ents_per_type"]['PERSON']['r'])
    print("F1 Score: ", scores_model["ents_per_type"]['PERSON']['f'])
    print("-- Location entity scores:")
    print("Precision: ", scores_model["ents_per_type"]['LOC']['p'])
    print("Recall: ", scores_model["ents_per_type"]['LOC']['r'])
    print("F1 Score: ", scores_model["ents_per_type"]['LOC']['f'])
