"""
This file srapes the words and verbs from WordReference as to speed up
development and practicing.
"""
from requests import get
from bs4 import BeautifulSoup


# the de-factor url for conjugations (on WordReference)
CONJUGATOR_URL = "https://www.wordreference.com/conj/EsVerbs.aspx?v="


def get_tense_name(name):
    """Given a tense name, return the properly formatted name."""
    # check to see if there's a weird character in the name
    if "ⓘ" in name:
        index = name.index("ⓘ")  # get the index of weird char
        return name[:index]  # get everything up to the weird char

    return name


def get_pronoun_name(pronoun):
    """Given a pronoun, strip parenthesis and change 3rd person singular to be
    more spelling friendly."""
    final_pronoun = ""

    # remove the surrounding parenthesis (if applicable)
    if "(" in pronoun:
        final_pronoun = pronoun[1:-1]
    # change él, ella, Ud. to "one word"
    elif pronoun == "él, ella, Ud.":
        final_pronoun = "él/ella/usted"
    # change ellos, ellas, Uds. to "one word"
    elif pronoun == "ellos, ellas, Uds.":
        final_pronoun = "ellos/ellas/ustedes"
    # otherwise, leave it be
    else:
        final_pronoun = pronoun

    return final_pronoun


def get_conjugation(conjugation):
    """Given a conjugation, format it so it can go in the dictionary properly
    formatted."""
    final_conjugation = ""
    splitted = conjugation.split()  # split the conjugation by word

    # if there's more than one word AND "o" is in it, get the first word only
    if len(splitted) > 1 and "o" in conjugation:
        final_conjugation = splitted[0]
    # otherwise, leave it be
    else:
        final_conjugation = conjugation

    # if there's a comma, get everything up to it (the last character)
    if "," in final_conjugation:
        final_conjugation = final_conjugation[:-1]

    return final_conjugation


def scrape_verb(verb):
    """Given a verb, scrape its conjugations from WordReference and return the
    data nicely formatted."""
    # get the page and parse it
    full_url = f"{CONJUGATOR_URL}{verb}"
    page = get(full_url)

    # initiate a BeautifulSoup scraper based on the page
    scraper = BeautifulSoup(page.content, "html.parser")

    # get all the tables on the page
    tables = scraper.find_all("div", class_="aa")
    results = dict()  # will hold the final dictionary at the end

    for table in tables:
        # get the current table name
        table_name = table.find("h4").text

        # get each tense
        tenses = table.find_all("table", class_="neoConj")

        for tense in tenses:
            # get the tense name (for key in results)
            tense_name = get_tense_name(tense.find("th").text)
            if table_name == "Subjuntivo":
                tense_name = f"subjuntivo {tense_name}"

            # get (yo, tú, él, etc.) and conjugations
            pronouns = tense.find_all("th", scope="row")
            conjugations = tense.find_all("td")

            # loop through both
            for pronoun, conjugation in zip(pronouns, conjugations):
                # get the correctly parsed pronoun and conjugation
                actual_pronoun = get_pronoun_name(pronoun.text)
                actual_conjugation = get_conjugation(conjugation.text)

                # add the tense if it doesn't yet exist in results
                if tense_name not in results:
                    results[tense_name] = dict()

                # add the pronoun if it doesn't yet in results[tense]
                if actual_pronoun not in results[tense_name]:
                    results[tense_name][actual_pronoun] = ""

                # save the pronoun and conjugation into results
                results[tense_name][actual_pronoun] = actual_conjugation

    # return the parsed conjugation table
    return results
