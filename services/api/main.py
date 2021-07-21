from copy import deepcopy
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from enum import Enum
import spacy


def load_models():
    """
    load the models from disk
    and put them in a dictionary

    Returns:
        dict: loaded models
    """
    models = {
        "en_sm": spacy.load("api/ml/models/en_sm"),
        "fr_sm": spacy.load("api/ml/models/fr_sm"),
    }
    print("models loaded from disk")
    return models


models = load_models()


class ModelLanguage(str, Enum):
    fr = "fr"
    en = "en"


class ModelSize(str, Enum):
    sm = "sm"
    md = "md"
    lg = "lg"


class UserRequestIn(BaseModel):
    text: str
    model_language: ModelLanguage = "en"
    model_size: ModelSize = "sm"


class EntityOut(BaseModel):
    start: int
    end: int
    type: str
    text: str


class EntitiesOut(BaseModel):
    entities: List[EntityOut]
    anonymized_text: str


app = FastAPI()


@app.post("/entities", response_model=EntitiesOut)
def extract_entities(user_request: UserRequestIn):
    text = user_request.text
    language = user_request.model_language
    model_size = user_request.model_size

    model_key = language + "_" + model_size

    model = models[model_key]
    doc = model(text)

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


@app.get("/")
def hello():
    return {"message": "hello Mirakl !!"}
