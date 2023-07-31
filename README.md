# Replication Package: An Expert Survey on the Use of Informal Models in the Automotive Industry
This repository contains the replication package for the paper *An Expert Survey on the Use of Informal Models in the Automotive Industry* by 
[Dominik Fuchß](https://orcid.org/0000-0001-6410-6769), 
[Thomas Kühn](https://orcid.org/0000-0001-7312-2891),
[Jérôme Pfeiffer](https://orcid.org/0000-0002-8953-1064),
[Andreas Wortmann](https://orcid.org/0000-0003-3534-253X), and
[Anne Koziolek](https://orcid.org/0000-0002-1593-3394).
The paper has been accepted at the [TwinArch 2023: The 2nd International Workshop on Digital Twin Architecture](https://www.iese.fraunhofer.de/en/twinarch.html) co-located with [ECSA 2023](https://conf.researchr.org/home/ecsa-2023).


This replication package contains all information from the survey.
The files `results-survey.xlsx`, `results-survey.csv`, and `results-survey-translated.csv` contain the original data from the survey.

## Format of the result files
* The first line contains the question. 
* The second line contains the possible answer options. 
* The following lines contain the answers from one participant each.

* `results-survey.xlsx`: All data exported from LimeSurvey (German). 
    * After export, all lines that do only contain information about the profession and no other data have been removed.
    * For better readability, some answer options have been simplified (this is documented in the xlsx file: Tab "Table Cleanup")
* `results-survey.csv`: A csv version of `results-survey.xlsx`. Used for all scripts.
* `results-survey-translated.csv`: A csv translated version of `results-survey.xlsx`.

## Evaluation Code
Besides the raw data from the survey, the repository contains the code of the evaluation (and its resulting diagrams).

To replicate the evaluation, you need Python3 and have to install the packages defined in `requirements.txt`:

1. Therefore, run `pip3 install -r requirements.txt` (Linux) or `pip install -r requirements.txt` (Windows).

2. Afterwards, you can run `python3 generate_pdfs.py` (Linux) or `python generate_pdfs.py` (Windows) to generate the diagrams. 

3. They are located in the folder `fig`.

### Evaluation Code Structure
For each diagram in the paper, there is a python file in `extractors` that handles the creation of the diagram.
Therefore, most of these files rely on the `helpers_generate_pdfs.py` in the base directory of this replication package. It contains helper methods that interpret the input CSV file.

### Translation of Survey
Since the survey was conducted in German, we had to translate the answers, questions, and options.
This was done by the `translate_cli.py` script.
The result of the translation is stored as Key Value Pairs in the file `translations.json`.
