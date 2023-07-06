import json
import os.path

translate_dict = {}


def translate(text):
    """Translates the given text and returns the translation.
    Additionally, if the text contains a comma, the text is split by comma and each part is translated separately."""

    global translate_dict
    if text == "":
        return ""

    if text not in translate_dict.keys():
        print("Translate: " + text)
        translate_dict[text] = input("Translation: ")

    if "," not in text:
        return translate_dict[text]

    for part in text.split(','):
        if part in translate_dict.keys():
            continue
        print("Translate part (" + part + ") of: " + text + " or skip by enter nothing")
        part_translation = input("Translation: ")
        if part_translation is None or part_translation == "":
            translate_dict[part] = None
        translate_dict[part] = part_translation

    translation_file = open("translations.json", "w")
    translation_file.write(json.dumps(translate_dict, indent=4, sort_keys=True))
    translation_file.close()
    return translate_dict[text]


def translate_interactive():
    """Translates the survey results interactively. The results are written to results-survey-translated.csv."""

    global translate_dict
    input_file = open('results-survey.csv', 'r', encoding='utf-8-sig')
    output_file = open('results-survey-translated.csv', 'w', encoding='utf-8-sig')

    if os.path.exists('translations.json'):
        # load existing translations
        tfile = open('translations.json', 'r', encoding='utf-8-sig')
        translate_dict = json.load(tfile)
        tfile.close()

    for line in input_file:
        elements = line.strip().split(';')
        translated_elements = []
        for e in elements:
            translated_elements.append(translate(e))
        output_file.write(';'.join(translated_elements))
        output_file.write('\n')
    input_file.close()
    output_file.close()

    # save translations
    translation_file = open("translations.json", "w")
    translation_file.write(json.dumps(translate_dict, indent=4, sort_keys=True))
    translation_file.close()


if __name__ == '__main__':
    """Translate the survey results."""
    translate_interactive()
