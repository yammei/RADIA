import os
import time
import platform
from greptile import API
from InquirerPy import prompt

api = API()

def main():
    menu()

def menu():
    while True:
        clear_terminal()
        questions = [
            {
                "type": "list",
                "name": "option",
                "message": "Greptile AI CLI - Navigate Menu Options",
                "choices": [
                    "1: Check API Usage Credentials",
                    "2: Index Repository",
                    "3: Check Indexing Progress",
                    "4: Post Repository Query"
                ]
            }
        ]
        answer = prompt(questions)["option"]
        choose_menu(answer)

def choose_menu(option):
    if "1" in option:
        print("Checking API Usage Credentials...")
        api.connect()
    elif "2" in option:
        print("Indexing Repository...")
        api.index()
    elif "3" in option:
        print("Checking Indexing Progress...")
        api.index_progress()
    elif "4" in option:
        print("Preparing for Repository Query...")
        prompt: str = input("Enter prompt (e.g., Help me understand this codebase.):")
        api.query(prompt=prompt)
    else:
        print("Invalid option selected.")

    print(f"\nAutomatically returning to menu in 10s...")
    time.sleep(10)

# Windows and Mac compatible terminal clearing.
def clear_terminal():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

if __name__ == "__main__":
    main()
