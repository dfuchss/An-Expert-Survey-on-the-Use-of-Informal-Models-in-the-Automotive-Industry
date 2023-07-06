from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from helpers_generate_pdfs import get_range
from translate import yes


def profession(questions: List[str], options: List[str], answers: List[List[str]]) -> Dict[str, int]:
    start, end = get_range(questions, "Welchen fachlichen Hintergrund haben Sie?")
    answer_x_count: Dict[str, int] = {}

    for answer in answers:
        for idx in range(start, end - 1):
            if answer[idx] != yes():
                continue
            if options[idx] not in answer_x_count.keys():
                answer_x_count[options[idx]] = 0
            answer_x_count[options[idx]] += 1
        if answer[end - 1] != "":
            if answer[end - 1] not in answer_x_count.keys():
                answer_x_count[answer[end - 1]] = 0
            answer_x_count[answer[end - 1]] += 1
    print(answer_x_count)
    return answer_x_count


def create_profession_histogram(profession_data: Dict[str, int]):
    df = pd.DataFrame.from_dict(profession_data, orient='index', columns=['count'])
    # Sort by count
    plt.tight_layout()
    df = df.sort_values(by=['count'], ascending=False).reset_index()
    # Rename column
    df = df.rename(columns={"index": "Profession"})
    df = df.rename(columns={"count": "Count"})
    # sns.set_palette(sns.dark_palette(color='white',n_colors=len(profession_data.keys())))
    plot = sns.barplot(data=df, x="Profession", y="Count", hue="Profession", dodge=False)
    plot.set_xticklabels([])
    for i in plot.containers:
        plot.bar_label(i, )

    plt.savefig("fig/Profession.pdf")
    plt.close()
