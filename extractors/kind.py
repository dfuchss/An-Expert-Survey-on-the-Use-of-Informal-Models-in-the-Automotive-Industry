from typing import Dict

from helpers_generate_pdfs import create_answer_option_count_dict, create_histogram
from translate import translations, yes, no


def _merge(answer_x_option_x_count, target_answer, additional_answer):
    """Merges the additional answer into the target answer and deletes the additional answer."""

    if target_answer in translations().keys():
        target_answer = translations()[target_answer]
    if additional_answer in translations().keys():
        additional_answer = translations()[additional_answer]

    answer_x_option_x_count[target_answer] = {
        yes(): answer_x_option_x_count[target_answer].get(yes(), 0) + answer_x_option_x_count[additional_answer].get(
            yes(), 0),
        no(): answer_x_option_x_count[target_answer].get(no(), 0) + answer_x_option_x_count[additional_answer].get(no(),
                                                                                                                   0)
    }
    answer_x_option_x_count.pop(additional_answer, None)


def kind(questions, options, answers):
    answer_x_option_x_count = create_answer_option_count_dict(questions, options, answers,
                                                              "Um welche Arten von Diagrammen / Modelle handelt es sich typischerweise (z.B. Zustandsdiagramme, Aktivitätsdiagramme, …)",
                                                              True, True)
    for answer in answer_x_option_x_count.keys():
        option_x_count_or_int = answer_x_option_x_count[answer]
        if isinstance(option_x_count_or_int, dict):
            continue
        # Create int to dict
        answer_x_option_x_count[answer] = {yes(): option_x_count_or_int, no(): 0}

    # Remove not saying answers (custom answer)
    answer_x_option_x_count.pop("tbd.", None)

    # Merge deployment and deployment modelle
    _merge(answer_x_option_x_count, "Deployment-Modelle", "Deployment")

    # Merge SW-Architekturmodelle, E/E-Architekturmodelle and Architekturmodelle
    _merge(answer_x_option_x_count, "Architekturmodelle", "SW-Architekturmodelle")
    _merge(answer_x_option_x_count, "Architekturmodelle", "E/E-Architekturmodelle")

    # Remove "no" answers
    for answer in answer_x_option_x_count.keys():
        option_x_count = answer_x_option_x_count[answer]
        option_x_count.pop(no(), None)

    return answer_x_option_x_count


def create_kind_histogram(kind_data: Dict[str, Dict[str, int]]):
    create_histogram(kind_data, "Kind", 42, x_axis_label=False, order_by_numbers=True)
