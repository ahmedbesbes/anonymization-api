from copy import deepcopy
import spacy


class Model:
    def __init__(self, path):
        self._model_path = path
        self.model = spacy.load(self._model_path)

    def predict(self, text):
        doc = self.model(text)

        entities = [
            {
                "start": ent.start_char,
                "end": ent.end_char,
                "type": ent.label_,
                "text": ent.text,
            }
            for ent in doc.ents
        ]

        anonymized_text = list(deepcopy(text))

        for entity in entities:
            start = entity["start"]
            end = entity["end"]
            anonymized_text[start:end] = "X" * (end - start)

        anonymized_text = "".join(anonymized_text)

        return {"entities": entities, "anonymized_text": anonymized_text}
