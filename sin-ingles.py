"""
Sin Inglés - A spaced-reptition flashcard program to learn verbs and words.

This file manages everything from the CLI, grading, and file reading with
help from the utility functions, scraper file, and other files.
"""
from utilities import get_study_verbs_dataset, quiz_verbs, create_analysis
from termcolor import colored


def main():
    """The entire program logic goes here."""
    while True:
        query = colored("¿qué te gustaría hacer? ", "magenta")
        command = input(query)

        if command == "pruebame":
            query_question = "¿qué probarás? (verbos o vocabulario) "
            study_query = colored(query_question, "yellow")
            study_command = input(f"\t{study_query}")

            if study_command == "verbos":
                verbs = get_study_verbs_dataset()
                gotten_wrong = quiz_verbs(verbs)
                create_analysis(gotten_wrong)
            elif study_command == "vocabulario":
                print(colored("\t¡no quiero probar ahora, señor!", "white"))
            else:
                print(colored("\t¡no comprende!", "red"))
        elif command == "q":
            print("¡adiós!\n")
            exit()
        else:
            print(colored("¡no comprende!", "red"))


if __name__ == "__main__":
    # run the contents of this file
    main()
