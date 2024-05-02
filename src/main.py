import os

def print_intro():
    """
    Prints the introduction message and menu options.
    """
    print("Welcome to ArchnetAI - NetNode Package!")
    print("This library leverages the Ollama API for generating AI-powered content. Created by UgurkanTech.")
    print("Menu:")
    examples = get_example_files()
    for i, example in enumerate(examples, start=1):
        print(f"{i}. Run {example}")
    print(f"{len(examples) + 1}. Exit")
    process_user_choice(examples)

def get_example_files():
    """
    Retrieves a list of example files from the 'src/examples' directory.
    """
    return [file for file in os.listdir("src/examples") if file.startswith("example_")]

def process_user_choice(examples):
    """
    Processes the user's choice and executes the selected example or exits the program.
    """
    while True:
        choice = input("Enter your choice (1-{}): ".format(len(examples) + 1))
        try:
            choice = int(choice)
            if 1 <= choice <= len(examples):
                example_file = examples[choice - 1]
                execute_example(example_file)
            elif choice == len(examples) + 1:
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid choice. Please try again.")

def execute_example(example_file):
    """
    Executes the selected example file.
    """
    example_path = f"src/examples/{example_file}"
    example_code = open(example_path).read()
    exec(example_code)

# Entry point of the program
if __name__ == "__main__":
    print_intro()
