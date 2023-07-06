from typing import Dict

from helpers_generate_pdfs import create_answer_option_count_dict, create_histogram, simplify_label_to_symbol


def phase(questions, options, answers):
    return create_answer_option_count_dict(questions, options, answers,
                                           "Wie häufig setzen Sie informelle Modelle in den folgenden Phasen der Entwicklung ein?",
                                           True,
                                           False)


def create_phase_histogram(phase_data: Dict[str, Dict[str, int]]):
    create_histogram(phase_data, "Phase", 24, simplify_label_function=simplify_label_to_symbol, rotation=90,
                     horizontalalignment='center')
