import random
from typing import List, Tuple
import spacy
from spacy.training.example import Example


def train_spacy_ner(
    training_data: list[Tuple],
    output_path: str,
    epochs: int = 30,
    labels: List[str] = [],
    model: str = None,
) -> None:
    random.shuffle(training_data)

    nlp = spacy.blank("en") if model is None else spacy.load(model)
    nlp.disable_pipes("tagger", "parser")
    # Set up the NER pipeline (if not already in place)
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe("ner", last=True)

    for label in labels:
        ner.add_label(label)

    # Training loop
    nlp.begin_training()
    for epoch in range(epochs):
        losses = {}
        for text, annotations in training_data:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.5, losses=losses)
        print(f"Losses at epoch {epoch}: {losses}")

    nlp.to_disk(output_path)
