"""
Sin Inglés - A spaced-reptition flashcard program to learn verbs and words.

This file manages everything from the CLI, grading, and file reading with
help from the utility functions, scraper file, and other files.
"""
from utilities import get_study_verbs_dataset, start_flashcard, create_analysis
from termcolor import colored


def main():
    """The entire program logic goes here."""
    while True:
        query = colored("¿qué te gustaría hacer? ", "magenta")
        command = input(query)

        if command == "estudia":
            query_question = "¿qué estudiarás? (verbos o vocabulario) "
            study_query = colored(query_question, "yellow")
            study_command = input(f"\t{study_query}")

            if study_command == "verbos":
                verbs = get_study_verbs_dataset()
                gotten_wrong = start_flashcard(verbs)
                create_analysis(gotten_wrong)
            else:
                pass
        elif command == "q":
            print("¡adiós!")
            exit()
        else:
            print("¡no comprende!")


if __name__ == "__main__":
    # run the contents of this file
    main()
