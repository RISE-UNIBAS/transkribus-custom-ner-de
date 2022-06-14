Python Version : 3.7.9

Information on present files/folder in this folder.

- Folder : de_spacy_custom - custom trained NER model.
- File : Custom_NER_All_Inference_results.csv - Result file which has comparison of extracted entities using custom model and spacy large model
- File : extract_entities_from_XML.py - Python script to extract entities from XML files.
- File : extracted_entities.txt - Output file contains extracted entities from XML file using above mentioned script.
- File : inference_custom_model_test_data.py - Python script to extract entities from text using custom trained model.
- File : README.txt - File which you are reading right now.
- File : requirements.txt - Python libraries dependency file to create virtual environment.
- File : Submission_Custome_NER_From_XML.ipynb - Jupyter Notebook containing all the code.
- File : train_custom_spacy_ner.py - Python script to train NER model.


Model Performance

- Model is able to identify full names of the person from text where spacy large model extracts partial names.
- Some of the locations present were not part of the training data, which resulted in non extraction on test data but those locations
    are detected by spacy large model.
- There are several data points which overlaps the positions, which is possible cause for False postives.
- Many full text are speaded over multiple lines which results in poor data labelling and affects model accuracy.
