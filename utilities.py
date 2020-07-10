"""
This file holds utility functions that are too long for the sin-ingles file or
repetitive in terms of logic.
"""
from scraper import scrape_verb
from termcolor import colored
from random import choice


# mapping the simple version from the study-verbs.txt file to what the tense is
# named in the conjugation tables scraped from Word Reference
TENSES_MAPPING = {
    "present": "presente",
    "imperfect": "imperfecto",
    "past": "pretérito",
    "future": "futuro",
    "conditional": "condicional",
    "past perfect": "pretérito perfecto",
    "imperfect perfect": "pluscuamperfecto",
    "future perfect": "futuro perfecto",
    "conditional perfect": "condicional perfecto",
    "present subjunctive": "subjuntivo presente",
    "imperfect subjunctive": "subjuntivo imperfecto",
    "future subjunctive": "subjuntivo futuro",
    "positive command": "afirmativo",
    "negative command": "negativo"
}


def get_study_verbs_dataset():
    """Scrape all verbs in the study-verbs.txt file and return the tenses
    required as stated."""
    # will hold all the requested tenses
    tenses = list()
    contents = None  # will hold the contents of study-verbs.txt

    # will hold all the verbs with all the tenses
    results = dict()

    # will hold all the verbs with only the requested tenses
    final_results = dict()

    with open("study-verbs.txt", "r") as verbs:
        lines = verbs.readlines()  # read each line of the file
        contents = [line.rstrip() for line in lines]  # remove the newline

    # loop through all the requested tenses
    for tense in contents[0].split(", "):
        if tense == "all":  # if the tense is all, add all the tenses
            tenses.concat(TENSES_MAPPING.values())
        else:  # otherwise only add the tenses specified
            tenses.append(tense)

    # for every verb specified in study-verbs.txt
    for verb in contents[1:]:
        # get the conjugations from WordReference
        conjugations = scrape_verb(verb)

        # check and add to results if not found
        if verb not in results:
            results[verb] = dict()

        # set the verb to the conjugations
        results[verb] = conjugations

    # loop through all the verbs in results
    for verb, conjugations in results.items():
        # save a copy in final_results (just the verb = {})
        final_results[verb] = dict()

        # loop through each tense
        for tense_name, tense in conjugations.items():
            # loop through each requested tense
            for requested_tense in tenses:
                # the requested tense equals the current tense...
                if tense_name == TENSES_MAPPING[requested_tense]:
                    # only save said tense to final_results
                    final_results[verb][tense_name] = tense

    # return the list with only the requested tenses
    return final_results


def is_done(obj):
    """Given an object, determine if it is done or not by looping through it
    and returning True if all verbs are seen and False otherwise."""
    # loop through every verb
    for verb, conjugations in obj.items():
        # loop through every tense
        for tense, conjugation_table in conjugations.items():
            # loop through every pronoun
            for pronoun, has_been_seen in conjugation_table.items():
                # if the verb has not been seen...
                if not has_been_seen:
                    return False  # in other words, is NOT done

    return True  # in other words, IS done


def start_flashcard(obj):
    """Given an object of verbs, quiz the user by randomly selecting words
    until everything is completed."""
    seen = dict()  # holds all the conjugations seen
    incorrect = dict()  # holds all the conjugations gotten incorrect

    # loop through every verb
    for verb, conjugations in obj.items():
        seen[verb] = dict()
        incorrect[verb] = dict()

        # loop through every tense
        for tense, conjugation_table in conjugations.items():
            seen[verb][tense] = dict()
            incorrect[verb][tense] = dict()

            # loop through every pronoun
            for pronoun, conjugation in conjugation_table.items():
                seen[verb][tense][pronoun] = False  # never seen
                incorrect[verb][tense][pronoun] = 0  # never gotten incorrect

    # while the user has not seen every conjugation
    while not is_done(seen):
        # get a random verb, tense, and pronoun
        random_verb = choice(list(obj.keys()))
        random_tense = choice(list(obj[random_verb].keys()))
        random_pronoun = choice(list(obj[random_verb][random_tense].keys()))

        # get the correct answer
        answer = obj[random_verb][random_tense][random_pronoun]

        # ask the user to input the answer
        query = f"{random_verb} / {random_tense} / {random_pronoun} "
        response = input(colored(f"\t\t{query}", "blue"))

        while True:
            # if the response is incorrect
            if response != answer:
                print(colored("\t\t\t¡no está correcto!", "red"))

                # increment the current conjugation by 1 in incorrect
                # for analysis purposes
                incorrect[random_verb][random_tense][random_pronoun] += 1

                # ask the user to input the answer (again)
                query = f"{random_verb} / {random_tense} / {random_pronoun} "
                response = input(colored(f"\t\t{query}", "blue"))
            else:
                # tell the user they are correct and break out of this loop
                print(colored("\t\t\t¡está correcto!", "green"))
                break

        # the user saw this conjugation
        seen[random_verb][random_tense][random_pronoun] = True

    # return the list of incorrect conjugations (for analysis)
    return incorrect


def create_analysis(obj):
    """Given an object, create an analysis on what to work on based on the
    answers given incorrectly."""
    analysis = ""  # will hold the contents of verbs-analysis.txt

    # loop through every verb
    for verb, conjugations in obj.items():
        # loop through every conjugation
        for tense, conjugation_table in conjugations.items():
            # loop through every number incorrect
            for pronoun, n_incorrect in conjugation_table.items():
                # only record if the user has gotten it wrong at least once
                if n_incorrect > 0:
                    analysis += f"{verb}/{tense}/{pronoun}: {n_incorrect}x\n"

    # delete the current contents of verbs-analysis.txt
    open("verbs-analysis.txt", "w").close()

    # write the analysis
    with open("verbs-analysis.txt", "w") as verbs_analysis_file:
        verbs_analysis_file.write(analysis)
