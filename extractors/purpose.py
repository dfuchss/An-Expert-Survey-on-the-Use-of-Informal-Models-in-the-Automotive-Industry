from typing import Dict

from helpers_generate_pdfs import create_answer_option_count_dict, create_histogram, simplify_label_to_symbol


def purpose(questions, options, answers):
    return create_answer_option_count_dict(questions, options, answers,
                                           "Wie häufig werden solche informellen Diagramme für die folgenden Zwecke genutzt?",
                                           True, False)


def create_purpose_histogram(purpose_data: Dict[str, Dict[str, int]]):
    create_histogram(purpose_data, "Purpose", 27, simplify_label_function=simplify_label_to_symbol, rotation=90,
                     horizontalalignment='center')
