from .lexicon_en import LEXICON_EN

from .lexicon_ru import LEXICON_RU

LEXICON = {
    'default': 'en',
    'ru': LEXICON_RU,
    'en': LEXICON_EN,
}


def get_translation(lang: str, key: str) -> str | None:
    if LEXICON.get(lang) is None:
        lang = LEXICON['default']
    return LEXICON[lang].get(key)
