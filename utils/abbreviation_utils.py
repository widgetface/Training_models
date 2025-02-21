import string
import json
import os.path
import logging
from utils.stop_words import STOP_WORDS


class Abbreviations:
    def __init__(self, file_path: str) -> None:
        try:
            if os.path.isfile(file_path):
                with open(file_path, "r") as json_file:
                    self.abbreviations = json.load(json_file)
        except FileNotFoundError as fne:
            logging.error(f"Failed to initialize object: {fne}")
            raise

    def is_not_stopword(self, word: str) -> bool:
        return word in STOP_WORDS

    def remove_duplicate_word(self, sentence: str, word: str) -> str:
        count = sentence.count(word)
        return sentence if count <= 1 else sentence.replace(word, "", count - 1)

    def replace_abbreviations(self, sentence: str) -> str:
        for word in sentence.split(" "):
            word = word.upper()
            if self.is_not_stop_word(word):
                abbreviation_value = self.abbreviations.get(word[:1], None)
                if abbreviation_value:
                    sentence.replace(word, abbreviation_value)
                    self.remove_duplicate_word(sentence, abbreviation_value)
        return sentence

    def find_replace_abbrevition(self, text: str) -> str:
        sentences = text.split(".")

        for sentence in sentences:
            sentence = self.replace_abbrevitions(sentence)

        return sentences
