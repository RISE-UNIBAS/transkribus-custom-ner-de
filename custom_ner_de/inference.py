"""
filename : inference.py

This script is responsible for using custom trained model and generate results on input data.

This script has 2 entity detection functions, first for single text and second for entire dataframe or list.

It will print the results on terminal and save it in csv file.

Execution time : <1 second for single text i/p, 20 seconds on test data provided.
"""

from typing import List
import pandas as pd
import spacy
import warnings

warnings.filterwarnings('ignore')


def predict(model: spacy.Language,
            text_path: str,
            word_remove: List[str] = None) -> tuple:
    """ Return persons and locations extracted form plain text file using (custom) trained spaCy model for NER.

    :param model: the spaCy NER model
    :param text_path: complete path to the plain text file including .txt extension
    :param word_remove: list of words to remove, defaults to None
    """

    #
    output = pd.read_csv(filepath_or_buffer=text_path,
                         delimiter="\n",
                         header=None,
                         names=["text"])
    text = list(output['text'])

    all_persons = []
    all_locations = []

    for line in text:
        doc = model(line)
        all_persons.append([ent.text for ent in doc.ents if ent.label_ == 'PERSON' and ent.text not in word_remove])
        all_locations.append([ent.text for ent in doc.ents if ent.label_ == 'LOC' and ent.text not in word_remove])

    return all_persons, all_locations

    """
    output['persons'] = pd.Series(all_persons)
    output['locations'] = pd.Series(all_locations)

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
