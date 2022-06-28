# transkribus-custom-ner-de

Custom named entity recognition (persons, locations) using [spaCy](https://spacy.io/) for German texts annotated using [Transkribus](https://readcoop.eu/transkribus/?sc=Transkribus).

Access this binder at the following URL

ADD URL

## Creator
This software and sample dataset were created by the University of Basel's Research and Infrastructure Support RISE (rise@unibas.ch) in May 2022.

## File structure and data overview
- Python module in [/transkribus_custom_ner_de](https://github.com/RISE-UNIBAS/transkribus-custom-ner-de/tree/main/transkribus_custum_ner_de).

- Documentation in [/docs](https://github.com/RISE-UNIBAS/transkribus-custom-ner-de/tree/main/docs).

- Sample data set in [/sample](https://github.com/RISE-UNIBAS/transkribus-custom-ner-de/tree/main/sample). The input data stem from the digital collection "Stenographisches Protokoll der Verhandlungen des ... Zionisten-Kongresses ... in ..." (ZDB mark: 2176334-3, persistent link: https://sammlungen.ub.uni-frankfurt.de/cm/periodical/titleinfo/3476254) provided by the Goethe University Frankfurt.
  - [/sample/gold_standard.zip](https://github.com/RISE-UNIBAS/transkribus-custom-ner-de/tree/main/sample/gold_standard.zip) is the protocol of 1897, automatically segmented and transcribed using PyLaya Transkribus Print M1 (model 39995) without manual corrections, manually annotated with `person` and `place` labels, exported as PAGE XML Zip file.
  - [/sample/text_unanalyzed.txt](https://github.com/RISE-UNIBAS/transkribus-custom-ner-de/tree/main/sample/text_unanalyzed.txt) is the protocol of 1899, automatically segmented and transcribed using PyLaya Transkribus Print M1 (model 39995) without manual corrections, exported as plain text file.

- Tests in [/tests](https://github.com/RISE-UNIBAS/transkribus-custom-ner-de/tree/main/tests).

## Tutorial

This tutorial shows how to get from a document in Transkribus to a custom NER model. 

### First step: prepare your documents for training in Transkribus

This section explains how to prepare your documents using the [Transkribus Expert Client](https://readcoop.eu/transkribus/download/) in order to train a spaCy model for named entity recognition. Basic familiarity with the Transkribus Expert Client is assumed (see [READ-COOP](https://readcoop.eu/transkribus/resources/how-to-guides/) for tutorials). First the workflow is presented and then a detailed annotation sample is provided.

#### Workflow

The preparation workflow involves five sub-steps:

1. Create a collection in Transkribus and upload your documents. Automatically or manually segment and transcribe the documents, and carry out corrections if necessary. Be sure that you are happy with the result since there is no going back.
2. Choose a representative sample of all documents. Think about the required sample size and make sure to include as much variety as possible.
3. Define which entities you want to annotate and specify annotation guidelines.  Try to be explicit in recording all annotation decisions you are making. [!todo add link to annotation best practices]
4. Annotate the representative sample. Try to ensure that annotations across all documents are consistent. Of course, annotation guidelines will likely have to be amended during the annotation process. Again, be sure that you are happy with the result since there is no going back.
5. Export the annotated representative sample (again, there is no going back from here).

#### Sample annotation

https://readcoop.eu/transkribus/howto/how-to-enrich-transcribed-documents-with-mark-up/

### Second step: train, evaluate, and apply a custom NER model using spaCy 

This section explains how to train, evaluate, and apply a custom NER model using spaCy with the annotated representative sample created in the previous section. For this, either the Binder [URL] or the `Client` class of the `transkribus_custom_ner_de` module can be employed.

## License

- CC BY 4.0 https://creativecommons.org/licenses/by/4.0/