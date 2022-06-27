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



"""
def calculate_pre_trained_model_score(data):
    

    # using spact large german model
    nlp = spacy.load("de_core_news_lg")

    print("\n\nCalculating score...")
    new_test_data = []

    for text, annots in data:
        new_test_data.append(Example.from_dict(nlp.make_doc(text), annots))

    scores_model = nlp.evaluate(new_test_data)

    #print scores that you want
    precision_model = scores_model["ents_p"]
    recall_model = scores_model["ents_r"]
    f_score_model = scores_model["ents_f"]
    scores_entities = scores_model["ents_per_type"]

    print("\n================ Accuracy scores using Pre-trained large model =================\n")
   
    print("================= Overall scores =================\n")
    print("Precision : ",precision_model)
    print("Recall : ",recall_model)
    print("F1 Score : ",f_score_model)
   
    print("\n================= Entity wise score =================\n")
   
    print("============= Person Entity score =================\n")
    print("Precision : ",scores_entities['PERSON']['p'])
    print("Recall : ",scores_entities['PERSON']['r'])
    print("F1 Score : ",scores_entities['PERSON']['r'])

    print("\n============= Location Entity score =================\n")
    print("Precision : ",scores_entities['LOC']['p'])
    print("Recall : ",scores_entities['LOC']['r'])
    print("F1 Score : ",scores_entities['LOC']['r'])
"""


"""data = load_data()

calculate_custom_model_accuracy(data)

calculate_pre_trained_model_score(data)"""