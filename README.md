# transkribus-custom-ner-de
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/RISE-UNIBAS/transkribus-custom-ner-de/HEAD?labpath=interactive.ipynb)

Custom named entity recognition (persons, locations) using [spaCy](https://spacy.io/) for German texts annotated in [Transkribus](https://readcoop.eu/transkribus/?sc=Transkribus).

Access this binder at the following URL

https://mybinder.org/v2/gh/RISE-UNIBAS/transkribus-custom-ner-de/HEAD?labpath=interactive.ipynb

## Creator
This software and sample dataset were created by the University of Basel's Research and Infrastructure Support RISE (rise@unibas.ch) in May 2022.

## File structure and data overview
- Python module in [/transkribus_custom_ner_de](https://github.com/RISE-UNIBAS/transkribus-custom-ner-de/tree/main/transkribus_custum_ner_de).

- Documentation in [/docs](https://github.com/RISE-UNIBAS/transkribus-custom-ner-de/tree/main/docs).

- Sample data set in [/sample](https://github.com/RISE-UNIBAS/transkribus-custom-ner-de/tree/main/sample). The input data stem from the digital collection "Stenographisches Protokoll der Verhandlungen des ... Zionisten-Kongresses ... in ..." (ZDB mark: 2176334-3, persistent link: https://sammlungen.ub.uni-frankfurt.de/cm/periodical/titleinfo/3476254) provided by the Goethe University Frankfurt.

- Tests in [/tests](https://github.com/RISE-UNIBAS/transkribus-custom-ner-de/tree/main/tests).

## Tutorial

This tutorial aims to show you how to get from a document in Transkribus to a custom NER model. 

### First step: prepare your documents for training in Transkribus

This section explains how to prepare your documents using the [Transkribus Expert Client](https://readcoop.eu/transkribus/download/) in order to train a spaCy model for named entity recognition. Basic familiarity with the Transkribus Expert Client is assumed (see [READ-COOP](https://readcoop.eu/transkribus/resources/how-to-guides/) for tutorials). First the workflow is presented and then a detailed annotation sample is provided.

#### Workflow

The preparation workflow involves five sub-steps:

1. Create a collection in Transkribus and upload your documents. Automatically or manually segment and transcribe the documents, and carry out corrections if necessary. Be sure that you are happy with the result since there is no going back.
2. Choose a representative sample of all documents. Think about the required sample size and make sure to include as much variety as possible.
3. Define which entities you want to annotate and specify annotation guidelines.  Try to be explicit in recording all annotation decisions you are making.
4. Annotate the representative sample. Try to ensure that annotations across all documents are consistent. Of course, annotation guidelines will likely have to be amended during the annotation process. Again, be sure that you are happy with the result since there is no going back.
5. Export the annotated representative sample (again, there is no going back from here).

#### Sample annotation

For a general introduction on how to annotate text using the Transkribus Expert Client, see https://readcoop.eu/transkribus/howto/how-to-enrich-transcribed-documents-with-mark-up/. 

### Second step: train, evaluate, and apply a custom NER model using spaCy 

This section explains how to train, evaluate, and apply a custom NER model using spaCy with the annotated representative sample created in the previous section. For this, either the [Binder](https://mybinder.org/v2/gh/RISE-UNIBAS/transkribus-custom-ner-de/HEAD?labpath=interactive.ipynb) or the `Client` class of the `transkribus_custom_ner_de` module can be employed:

```
from __future__ import annotations
from transkribus_custom_ner_de.client import Client
import os.path

DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
WORD_REMOVE = ["Beifall", Händeklatschen"]
PERSON_NAMES = ['Gustav Gottheil']
LOCATION_NAMES = ['Boston', 'Roman']
GOLD_STANDARD = PARENT_DIR + "/sample/gold_standard.zip"
TEXT_PATH = PARENT_DIR + "/sample/text_unanalyzed.txt"

my_client = Client()
my_client.train_model(zip_url=GOLD_STANDARD,
                      word_remove=WORD_REMOVE,
                      person_names=PERSON_NAMES,
                      location_names=LOCATION_NAMES,
                      epochs=100,
                      _local=True)
my_client.save_model()
my_client.evaluate_model()
my_client.apply_model(text_url=TEXT_PATH,
                      _local=True)
my_client.result
my_client.save_result2csv()
```

## License

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
