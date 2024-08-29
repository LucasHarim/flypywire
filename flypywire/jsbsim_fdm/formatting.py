
ILLEGAL_CHARS = '\-/.'
TRANSLATE_TO = '_' * len(ILLEGAL_CHARS)
TRANSLATION_TABLE = str.maketrans(ILLEGAL_CHARS, TRANSLATE_TO)

def make_valid_name(name: str) -> str:
    
    return name.translate(TRANSLATION_TABLE)

