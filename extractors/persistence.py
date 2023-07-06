from typing import Dict

from helpers_generate_pdfs import create_answer_option_count_dict, create_histogram, simplify_label_to_symbol
from translate import translations


def simplify_store(answer: str):
    if answer in translations().keys():
        answer = translations()[answer]

    if "PowerPoint" in answer:
        return "Digital"
    if "fotografiert" in answer or "photographed" in answer:
        return "Photo"
    if "manuell" in answer or "manually" in answer:
        return "Manual"
    if "Whiteboard" in answer or "whiteboard" in answer:
        return "Whiteboard"

    raise Exception("Unknown answer: " + answer)


def persistence(questions, options, answers):
    return create_answer_option_count_dict(questions, options, answers,
                                           "Wie werden informelle Modelle typischer Weise festgehalten? Beurteilen Sie, wie häufig informelle Modell auf folgende Art in Ihrer Abteilung festgehalten werden.",
                                           False, False)


def create_persistence_histogram(persistence_data: Dict[str, Dict[str, int]]):
    create_histogram(persistence_data, "Persistence", 18, simplify_store, simplify_label_to_symbol, 90,
                     horizontalalignment='center')
