import json

# Use Translated versions ..
_translated = True
_translations = {}
_translations_reverse = {}


def translated():
    """Returns if the translated version shall be used"""
    global _translated
    return _translated


def translations():
    """Returns the translations: German -> English"""
    global _translations
    return _translations


def translations_reverse():
    """Returns the translations: English -> German"""
    global _translations_reverse
    return _translations_reverse


def load_translations():
    """Loads the translations from the file translations.json"""
    if not translated():
        return

    global _translations, _translations_reverse
    translation_file = open('translations.json', 'r', encoding='utf-8-sig')
    _translations = json.load(translation_file)
    translation_file.close()

    # Remove empty translations and trim keys and delete empty translations
    for key in list(_translations.keys()):
        if _translations[key] is None or _translations[key] == "":
            del _translations[key]
            continue
        if key.strip() != key:
            _translations[key.strip()] = _translations[key].strip()
            del _translations[key]

    # Create reverse translations
    _translations_reverse = {v: k for k, v in _translations.items()}


def translate(text):
    """Translates the given text to the translated version if the translated version shall be used"""
    if translated():
        if text in translations().keys():
            text = translations()[text]
        else:
            raise Exception("No translation for " + text)
    return text


def yes():
    """Returns the translated version of Ja"""
    return "Ja" if not translated() else translate("Ja")


def no():
    """Returns the translated version of Nein"""
    return "Nein" if not translated() else translate("Nein")
