import csv
from typing import List

from extractors.kind import kind, create_kind_histogram
from extractors.phase import phase, create_phase_histogram
from extractors.profession import profession, create_profession_histogram
from extractors.purpose import purpose, create_purpose_histogram
from extractors.reuse import reuse, create_reuse_histogram
from extractors.persistence import persistence, create_persistence_histogram
from translate import translated, load_translations


def main():
    load_translations()

    filename = "results-survey.csv" if not translated() else "results-survey-translated.csv"

    data = csv.reader(open(filename, "r", encoding='utf-8-sig'), delimiter=";")
    data = list(data)
    questions: List[str] = data[0]
    answer_options: List[str] = data[1]
    answers: List[List[str]] = data[2:]

    # print(questions)
    # print(answer_options)
    # print(answers)

    profession_data = profession(questions, answer_options, answers)
    create_profession_histogram(profession_data)

    purpose_data = purpose(questions, answer_options, answers)
    create_purpose_histogram(purpose_data)

    phase_data = phase(questions, answer_options, answers)
    create_phase_histogram(phase_data)

    persistence_data = persistence(questions, answer_options, answers)
    create_persistence_histogram(persistence_data)

    kind_data = kind(questions, answer_options, answers)
    create_kind_histogram(kind_data)

    reuse_data = reuse(questions, answer_options, answers)
    create_reuse_histogram(reuse_data)


if __name__ == '__main__':
    main()
