import json
import random
import spacy
from spacy.training import Example
from spacy.util import minibatch


ABBREV_FILE_PATH = "./data/updated_abbreviations.json"
TRAINING_MODEL_PATH = "./model/trained"
ABBREV_ENTITY_LABEL = "CLIN_ABBREV"
NER = "ner"


def create_training_data(key, value):
    forward = f"({key}) {value}"
    backwards = f"{value} ({key})"
    key_length = len(key)
    string_length = len(backwards)
    ftd = (
        f"{forward}",
        {"entities": [(1, key_length + 1, ABBREV_ENTITY_LABEL)]},
    )
    btd = (
        f"{backwards}",
        {"entities": [(len(value) + 2, string_length - 1, ABBREV_ENTITY_LABEL)]},
    )

    return (ftd, btd)


def prepare_spacy_training_data():
    training_data = []
    # df = open("./data/spacy_training_data", "w")
    with open(ABBREV_FILE_PATH, "r") as json_file:
        data = json.load(json_file)

        for key, value in data.items():
            if type(value) is list:
                for val in value:
                    print(val)
                    [ftd, btd] = create_training_data(key=key, value=val)
                    training_data = training_data + [ftd, btd]
            else:
                [ftd, btd] = create_training_data(key, value)
                training_data = training_data + [ftd, btd]

    return training_data


# Load a blank spaCy model or a pre-trained model
nlp = spacy.blank("en")

# Define some training data
tdata = prepare_spacy_training_data()
random.shuffle(tdata)
TRAIN_DATA = tdata

# Set up the NER pipeline (if not already in place)
if "ner" not in nlp.pipe_names:
    ner = nlp.create_pipe("ner")
    nlp.add_pipe("ner", last=True)

ner.add_label(ABBREV_ENTITY_LABEL)

# Training loop
optimizer = nlp.begin_training()
for epoch in range(30):
    losses = {}
    for text, annotations in TRAIN_DATA:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        nlp.update([example], drop=0.5, losses=losses)
    print(f"Losses at epoch {epoch}: {losses}")

nlp.to_disk(TRAINING_MODEL_PATH)
