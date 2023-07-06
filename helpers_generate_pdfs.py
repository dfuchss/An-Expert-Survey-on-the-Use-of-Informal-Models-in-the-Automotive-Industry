from typing import List, Dict, Union, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import ticker
from matplotlib.text import Text

from translate import translate, translations_reverse


def get_range(questions: List[str], name: str) -> Tuple[int, int]:
    """Finds the range of a question in the list of questions (headings).
    :param questions: The list of questions (headings).
    :param name: The question of the question.
    :return: The start index (inclusive) and the end index (exclusive) of the question.
    """
    name = translate(name)

    start_inclusive = questions.index(name)
    end_exclusive = len(questions)
    for i in range(start_inclusive + 1, len(questions)):
        if questions[i] != "":
            end_exclusive = i
            break
    return start_inclusive, end_exclusive


def _create_answer_option_count_dict_additionals(has_additionals: bool, consider_additionals: bool,
                                                 participant_row: List[str], end: int,
                                                 answer_x_option_x_count: Dict[
                                                     str, Union[int, Dict[str, int]]]) -> None:
    if has_additionals and consider_additionals and participant_row[end - 1] != "":
        additional_answers = [x.strip() for x in participant_row[end - 1].split(",")]
        for additional_answer in additional_answers:
            if additional_answer not in answer_x_option_x_count.keys():
                answer_x_option_x_count[additional_answer] = 0
            answer_x_option_x_count[additional_answer] += 1


def _create_answer_option_count_dict_add_missing_options(answer_x_option_x_count: Dict[str, Union[int, Dict[str, int]]],
                                                         add_missing_options: bool, answer_values: List[str]) -> None:
    if add_missing_options:
        for option in answer_x_option_x_count.keys():
            for answer in answer_values:
                available_answers_x_count = answer_x_option_x_count[option]
                if not isinstance(available_answers_x_count, dict):
                    continue
                if answer not in answer_x_option_x_count[option].keys():
                    answer_x_option_x_count[option][answer] = 0


def create_answer_option_count_dict(questions: List[str], option_row: List[str], participants_answers: List[List[str]],
                                    question: str, has_additionals: bool, consider_additionals: bool,
                                    add_missing_options: bool = True) -> Dict[str, Union[int, Dict[str, int]]]:
    """Returns a dictionary that maps an answer to the options and the count of the option for the given answer.
    E.g., if the question is "What is your favorite color?" and the answers are "red", "blue", "green", and your options are "like" and "dislike", then the result could be
    a dictionary that maps red to {"like": 10, "dislike": 2}, blue to {"like": 5, "dislike": 7}, and green to {"like": 3, "dislike": 9}.
    :param questions: The list of questions (headings) from the CSV.
    :param option_row: The row that contains the options for all questions from the CSV.
    :param participants_answers: The answers of the participants from the CSV as array of rows (also arrays) (in the example this row would contain like or dislike).
    :param question: The question for which the answers should be analyzed.
    :param has_additionals: Whether the question has additional answers (last column free text).
    :param consider_additionals: Whether the additional answers should be considered in the result as new possible answer.
    :param add_missing_options: Whether missing options should be added to the result with count 0. (needed for nice looking histograms)
    """
    start, end = get_range(questions, question)
    answer_x_option_x_count: Dict[str, Union[int, Dict[str, int]]] = {}
    answer_values: List[str] = []
    for participant_row in participants_answers:
        answer_indexes = range(start, end - 1) if has_additionals else range(start, end)
        for answer_idx in answer_indexes:
            if participant_row[answer_idx] == "":
                continue
            if option_row[answer_idx] not in answer_x_option_x_count.keys():
                answer_x_option_x_count[option_row[answer_idx]] = {}
            if participant_row[answer_idx] not in answer_x_option_x_count[option_row[answer_idx]].keys():
                answer_x_option_x_count[option_row[answer_idx]][participant_row[answer_idx]] = 0
            answer_x_option_x_count[option_row[answer_idx]][participant_row[answer_idx]] += 1
            answer_values.append(participant_row[answer_idx])

        _create_answer_option_count_dict_additionals(has_additionals, consider_additionals, participant_row, end,
                                                     answer_x_option_x_count)

    # print(answer_x_option_x_count)
    _create_answer_option_count_dict_add_missing_options(answer_x_option_x_count, add_missing_options, answer_values)
    return answer_x_option_x_count


def add_ordering_to_option(answer_x_option: str) -> str:
    """Converts the answer and option (combined as string [answer]::[option]) to a string that can be used for sorting.
    Therefore, the result string will be [answer]::[number][option]"""

    answer_x_option = answer_x_option.split("::")
    answer = answer_x_option[0]
    option = answer_x_option[1]
    option_to_check = option

    if option in translations_reverse().keys():
        option_to_check = translations_reverse()[option]

    if option_to_check == "gar nicht":
        return answer + "::0" + option
    if option_to_check == "selten":
        return answer + "::1" + option
    if option_to_check == "eher selten":
        return answer + "::2" + option
    if option_to_check == "eher häufig":
        return answer + "::3" + option
    if option_to_check == "sehr häufig":
        return answer + "::4" + option

    if option_to_check == "Nein":
        return answer + "::0" + option
    if option_to_check == "Ja":
        return answer + "::1" + option

    if option_to_check == "Keine Angabe":
        return answer + "::0" + option
    if option_to_check == "Stimme gar nicht zu":
        return answer + "::1" + option
    if option_to_check == "Stimme eher nicht zu":
        return answer + "::2" + option
    if option_to_check == "Stimme eher zu":
        return answer + "::3" + option
    if option_to_check == "Stimme vollständig zu":
        return answer + "::4" + option

    raise Exception("Unknown option: " + option_to_check)


def option_to_symbol(answer_x_option: str) -> str:
    """Converts the answer and option (combined as string [answer]::[option]) to a symbol like ++ or --."""
    answer_x_option = answer_x_option.split("::")
    answer = answer_x_option[0]
    option = answer_x_option[1]

    if option in translations_reverse().keys():
        option = translations_reverse()[option]

    if option == "gar nicht":
        return "--"
    if option == "selten":
        return "-"
    if option == "eher selten":
        return "-0"
    if option == "eher häufig":
        return "+"
    if option == "sehr häufig":
        return "++"

    if option == "Stimme gar nicht zu":
        return "--"
    if option == "Stimme eher nicht zu":
        return "-"
    if option == "Stimme eher zu":
        return "+"
    if option == "Stimme vollständig zu":
        return "++"

    raise Exception("Unknown option: " + option)


def simplify_answer(answer: str) -> str:
    """Simplifies the answer by removing the part after the first colon."""
    return answer.split(":")[0]


def simplify_label(label) -> str:
    """Simplifies the label by using only the option part of the schema [answer]::[option]."""
    return label.get_text().split("::")[1]


def simplify_label_to_symbol(label) -> str:
    """Simplifies the label by converting it to a symbol. See option_to_symbol for more information."""
    return option_to_symbol(label.get_text())


def create_histogram(answer_x_option_x_count: Dict[str, Dict[str, int]], title: str, ylim: int,
                     simplify_answer_function=simplify_answer,
                     simplify_label_function=simplify_label, rotation: int = 45,
                     horizontalalignment: str = 'right',
                     x_axis_label: bool = True,
                     order_by_numbers:bool = False) -> None:
    """Creates a histogram for the given answer_x_option_x_count. The title is used as the title of the histogram.
    :param answer_x_option_x_count: The answer_x_option_x_count from categorize (return value).
    :param title: The title of the histogram.
    :param ylim: The maximum y value of the histogram.
    :param simplify_answer_function: The function to simplify the answer. Default: simplify_category.
    :param simplify_label_function: The function to simplify the label. Default: simplify_label.
    :param rotation: The rotation of the x labels. Default: 45.
    :param horizontalalignment: The horizontal alignment of the x labels. Default: right.
    :param x_axis_label: Whether to show the x axis label. Default: True.
    :param order_by_numbers: Whether to order the x axis by the numbers. Default: False.
    """
    category_with_option_x_count = {}
    for category in answer_x_option_x_count.keys():
        short_category = simplify_answer_function(category)

        for option in answer_x_option_x_count[category].keys():
            key = short_category + "::" + option
            if key not in category_with_option_x_count.keys():
                category_with_option_x_count[key] = 0
            category_with_option_x_count[key] += answer_x_option_x_count[category][option]

    df = pd.DataFrame.from_dict(category_with_option_x_count, orient='index', columns=['count'])
    df = df.reset_index()
    df = df.rename(columns={"count": "Count"})
    df = df.rename(columns={"index": title + "::Option"})
    df[title] = df[title + "::Option"].apply(lambda x: x.split("::")[0])
    df["Option"] = df[title + "::Option"].apply(lambda x: x.split("::")[1])
    df[title + "::NUMOption"] = df[title + "::Option"].apply(add_ordering_to_option)
    # Sort by Purpose::NUMOption
    df = df.sort_values(by=[title + '::NUMOption'], ascending=True).reset_index()

    if order_by_numbers:
        df = df.sort_values(by=["Count"], ascending=False).reset_index()

    # sns.set_palette(sns.dark_palette(color='white', n_colors=len(category_with_option_x_count.keys())))
    fig, ax = plt.subplots(figsize=(8, 5))

    plot = sns.barplot(data=df, x=title + "::Option", y="Count", hue=title, dodge=False, ax=ax)
    labels: List[Text] = plot.get_xticklabels()
    for label in labels:
        if x_axis_label:
            label.set_text(simplify_label_function(label))
        else:
            label.set_text("")
    plot.set_xticklabels(labels, rotation=rotation, horizontalalignment=horizontalalignment)
    plot.set_xlabel("")
    plot.set_ylim(0, ylim)

    for i in plot.containers:
        plot.bar_label(i, )
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(f"fig/{title}.pdf")
    plt.close()
