from typing import Dict

from helpers_generate_pdfs import create_answer_option_count_dict, create_histogram, simplify_label_to_symbol
from translate import translated, translate, translations_reverse


def simplify_reuse(answer: str):
    if answer in translations_reverse().keys():
        answer = translations_reverse()[answer]

    if answer == "Die informellen Artefakte wurden nicht wiederverwendet, da Sie nicht persistiert wurden.":
        return "(1) No reuse, because no store"
    if answer == "Die informellen Artefakte wurden nicht wiederverwendet, obwohl Sie festgehalten wurden.":
        return "(2) No reuse, but store"
    if answer == "Die Fotografien informeller Artefakte wurden zu einem späteren Zeitpunkt wiederverwendet.":
        return "(3) Photo and reuse"
    if answer == "Die Fotografien informeller Artefakte wurden zwar gespeichert, aber nicht mehr zu Rate gezogen.":
        return "(4) Photo, but no reuse"
    if answer == "Das manuelle Übertragen der informellen Modelle war zeitaufwendig.":
        return "(5) Manual transfer is time-consuming"
    if answer == "Das manuelle Übertragen der informellen Modelle war nützlich für die später Arbeit.":
        return "(6) Manual was useful"
    if answer == "Die festgehaltenen informellen Modelle waren schwer zugreifbar/auffindbar.":
        return "(7) Retained models hard to find"
    raise Exception("Unknown answer: " + answer)


def reuse(questions, options, answers):
    answer_x_option_x_count = create_answer_option_count_dict(questions, options, answers,
                                                              "Welche der folgenden Aussagen im Bezug auf die (Wieder-)Verwendung von informellen Modellen stimmen Sie zu?",
                                                              True, True)

    for answer in list(answer_x_option_x_count.keys()):
        data = answer_x_option_x_count[answer]
        if isinstance(data, dict):
            continue
        print("Further Problem (Reuse): " + answer)
        answer_x_option_x_count.pop(answer, None)

    # Remove No Answer Field
    for answer in answer_x_option_x_count.keys():
        no_answer = "Keine Angabe" if not translated() else translate("Keine Angabe")
        answer_x_option_x_count[answer].pop(no_answer, None)

    return answer_x_option_x_count


def create_reuse_histogram(store_data: Dict[str, Dict[str, int]]):
    create_histogram(store_data, "Reuse", 32, simplify_reuse, simplify_label_to_symbol, 90,
                     horizontalalignment='center')
