""" train.py

Function to train a spaCy NER model on previously extracted entities.
"""

from __future__ import unicode_literals, print_function
from spacy.training import Example
from spacy.util import minibatch, compounding
from typing import List
import os
import random
import spacy


def custom_ner_training(gold_standard: List[tuple],
                        save_dir: str,
                        person_names: List[str] = None,
                        location_names: List[str] = None,
                        epochs: int = 100):
    """ Train a spaCy NER model on previously extracted entities.

    :param gold_standard: gold standard as defined by spaCy
    :param save_dir: complete path to directory where model is saved
    :param person_names: person names to be included for entity ruler, defaults to None
    :param location_names: location names to be included for entity ruler, defaults to None
    :param epochs: number of training epochs, defaults to 100
    """

    try:
        assert os.path.isdir(save_dir)
    except AssertionError:
        exit(f"Error: {save_dir} does not exist, exiting.")

    nlp = spacy.blank('de')

    # set up the pipeline:
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe('ner')

    person_patterns = []
    if person_names is not None:
        person_patterns = [{"label": "PERSON", "pattern": person_name} for person_name in person_names]

    location_patterns = []
    if location_names is not None:
        location_patterns = [{"label": "LOC", "pattern": location_name} for location_name in location_names]

    patterns = person_patterns + location_patterns

    # Creating Entity Ruler with custom patterns
    cfg = {"overwrite_ents": True}
    nlp.add_pipe('entity_ruler', before='ner', config=cfg).add_patterns(patterns)
    nlp.to_disk(save_dir)
    
    # adding data
    for _, annotations in gold_standard:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    print("Training {0} epochs...".format(epochs), end=" ")

    # training code:
    nlp.begin_training()
    for itn in range(epochs):
        print(f"{itn + 1}", end=" ")
        random.shuffle(gold_standard)
        losses = {}
        # batch up the examples using spaCy's minibatch:
        batches = minibatch(gold_standard, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)
            example = []
            # update the model with iterating each text:
            for i in range(len(texts)):
                doc = nlp.make_doc(texts[i])
                example.append(Example.from_dict(doc, annotations[i]))
            
            # update the model
            nlp.update(example, drop=0.5, losses=losses)

    # save trained model to directory:
    print("\nTraining completed,", end=" ")
    nlp.to_disk(save_dir)
    print(f"saved model to {save_dir}.")

