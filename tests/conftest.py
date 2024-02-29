import pytest
import pandas as pd
import sys
sys.path.append(".")
from translation_utils import MBartTranslator, Translator
from app import flask_app

@pytest.fixture
def translator_MBart():
    return MBartTranslator

@pytest.fixture
def translator():
    return Translator('MBart')

@pytest.fixture
def translation_row_valid():
    data = {
        'Target': 'English',
        'Source': 'Finnish',
        'Text': 'Lorem Ipsum'
    }

    df = pd.DataFrame([data])
    return df.iloc[0]

@pytest.fixture
def translation_row_invalid():
    data = {
        'Target': 'English',
        'Source': 'INVALID',
        'Text': 'Lorem Ipsum'
    }

    df = pd.DataFrame([data])
    return df.iloc[0]

@pytest.fixture
def app():
    return flask_app

@pytest.fixture
def translation_data():
    data = [
        {
            'Source': 'Finnish',
            'Target': 'English',
            'Text': 'Lorem Ipsum'
        }
    ]

    return data