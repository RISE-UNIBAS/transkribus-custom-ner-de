# custom-ner-de

Custom named entity recognition (persons, locations) using spaCy for German texts annotated using Transkribus.

Access this binder at the following URL

ADD URL

## Creator
This software and sample dataset were created by the University of Basel's Research and Infrastructure Support RISE (rise@unibas.ch) in May 2022. 

## File structure and data overview
Tutorial in /docs 

Data in /files with

- text file as .txt of training and testing dataset
- code as Python file (.py) and as Jupyternotebook (.ipynb) with comments as description
- extracted entities from the .xml files to train the model as extensible markup language file (.xml)
- the model 
- extracted entities from the .xml files to train the model as text file (.txt)
- requirements file with the required packages and dependencies to run the code
- result of trained model based on training dataset as CSV file (.csv)
- result of already pre-trained model of the spacy german large package as CSV file (.csv)

## Data processing
- .xml files were extracted from the collection by importing the collection into Transkribus and then marking the PERSON (PER) and LOCATION (LOC) labels. Then the .xml files got exported (202) in an output file.
This output file was then inserted into the python script, which then parses the XML files and extracts the labels to convert them into the spacy format.

- Based on that the spacy format, a pipeline will be built on which the natural langauge processor (nlp) of the spacy package will be trained on. Therefore a "blank" model will be created within the python code where the trained information will be stored in.

- After that the spacy model will be trained using the annotation and the entities 
(Takes up to 3 hours depending on machine and on epochs/batches set)

- Saving the trained model in the output directory for the analysis later on and testing the sample inference using the trained model

## Data analysis
-The first step was to read the .txt-file (or each .txt-file) into Python using Python Version 3.7.9 to process the text and to have a basic identifier that can link any named entities back to the page they appeared on.

-spaCy: the "de_core_news_lg" model is used to parse all the texts and perform a named entity recognition. Every entity tagged as PER, and/or Location (LOC). In addition to that you can use the own created and trained model. The resulting dataframe was saved as a .csv file.

- SpaCy has its own deep learning library called thinc used under the hood for different NLP models.#
SpaCy uses a deep neural network based on CNN. Specifically for Named Entity Recognition, spacy uses:

A transition based approach borrowed from shift-reduce parsers, which is described in the paper Neural Architectures for Named Entity Recognition.

A framework that's called "Embed. Encode. Attend. Predict".

Embed: Words are embedded using a Bloom filter, which means that word hashes are kept as keys in the embedding dictionary, instead of the word itself. This maintains a more compact embeddings dictionary, with words potentially colliding and ending up with the same vector representations.

Encode: List of words is encoded into a sentence matrix, to take context into account. spaCy uses CNN for encoding.

Attend: Decide which parts are more informative given a query, and get problem specific representations.

Predict: spaCy uses a multi layer perceptron for inference.

## Results

Model Performance

- Model is able to identify full names of the person from text where spacy large model extracts partial names.
- Some of the locations present were not part of the training data, which resulted in non extraction on test data but those locations
    are detected by spacy large model.
- There are several data points which overlaps the positions, which is possible cause for False postives.
- Many full text are speaded over multiple lines which results in poor data labelling and affects model accuracy.
- Accuracy_calculation.py can be used to calculate the precision/recall/f1-score of the custom-trained model and the already pre-trained model by spacy using the large 
german package and compares those two results

## Update
- migrated all the code to spacy 3.3, because model comparison with spacy large model requires latest version.
- there is minor update in label generation due to version upgrade.
- Added lists to add persons and locations as a pattern using entity ruler.
- Added list to ignore words in detection.
- Added new script to calculate the various scores. First it gives overall scores then it also gives entity wise various scores.
- Updated the requirements.txt with new library versions.
- Added Jupyter notebook which covers everything with markdown descriptions.

## License

- CC BY 4.0 https://creativecommons.org/licenses/by/4.0/