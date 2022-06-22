""" inference.py

"""

from typing import List
from pandas import DataFrame
import spacy


def predict(model: spacy.Language,
            text: DataFrame,
            word_remove: List[str] = None) -> tuple:
    """ Return persons and locations extracted from text using (custom) trained spaCy model for NER.

    :param model: the (custom) spaCy NER model
    :param text: text formatted as DataFrame
    :param word_remove: list of words to remove, defaults to None
    """

    # predict entities for text per line using the model:
    all_persons = []
    all_locations = []
    for line in text:
        doc = model(line)
        all_persons.append([ent.text for ent in doc.ents if ent.label_ == 'PERSON' and ent.text not in word_remove])
        all_locations.append([ent.text for ent in doc.ents if ent.label_ == 'LOC' and ent.text not in word_remove])

    return all_persons, all_locations

    #output['persons'] = pd.Series(all_persons)
    #output['locations'] = pd.Series(all_locations)

    #return output

"""
    # storing results in csv file
    output.to_csv('Custom_NER_inference_results.csv',index=False)
    """

"""

# todo: cont here

#loading custom trained spacy model
model_path = ".../de_spacy_custom" # todo: change path
nlp = load_custom_spacy_model(model_path)

# add words in the list to remove
word_remove = ["BASEL", "HÃ¤ndeklatschen"]


#extracting entities from list
df = pd.read_csv('C:/Users/User/kaushal/03_Protokoll-Zionistenkongress-Basel_1899.txt', delimiter = "\n", header=None, names=["text"])
data = list(df['text'])

all_persons, all_locations = generate_prediction_list(nlp, data)

df['Custom-trained_Spacy_Person'] = pd.Series(all_persons)
df['Custom-trained_Spacy_Location'] = pd.Series(all_locations)

# storing results in csv file
df.to_csv('Custom_NER_inference_results.csv',index=False)

print("results stored in csv file....")
"""
