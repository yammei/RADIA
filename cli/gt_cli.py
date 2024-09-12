import os
import time
import platform
from gt_api import API
from InquirerPy import prompt

api = API()

# Main process.
def main() -> None:
    menu()

# Main menu.
def menu() -> None:
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

# If available, prompt if user wants to use previous configurations.
def load_config() -> bool:
    clear_terminal()
    questions = [
        {
            "type": "list",
            "name": "option",
            "message": "Repository access configurations found. Use previous configurations?",
            "choices": [
                "1: Yes, load with previous configurations.",
                "2: No, don't load previous configurations (manual entry).",
            ]
        }
    ]
    return True if prompt(questions)["option"].startswith("1") else False

# If available, prompt if user wants to save current configurations.
def save_config() -> bool:
    clear_terminal()
    questions = [
        {
            "type": "list",
            "name": "option",
            "message": "Would you like to save these repository access configurations?",
            "choices": [
                "1: Yes, save these configurations (checking API credentials in the future will prompt to load the saved configurations).",
                "2: No, don't save these configurations.",
            ]
        }
    ]

    return True if prompt(questions)["option"].startswith("1") else False

# Menu choice logic.
def choose_menu(option) -> None:
    # Check for repository access credentials and configurations.
    # NO SAVED CONFIG: Manually input config. Saves config input if user agrees.
    # SAVED CONFIG: Automatically load config if user agrees, else manually input config.
    if "1" in option:
        def manual(): api.save() if (save_config() if api.connect(mode="manual") == "save" else False) else None
        def automatic(): api.load() if load_config() else manual()
        # Check for saved config.
        if api.check(source="cli"):
            automatic()
        else:
            manual()
    # Repository indexing.
    elif "2" in option:
        api.index()

    # Indexing progress.
    elif "3" in option:
        api.index_progress()

    # Query user prompts.
    elif "4" in option:
        prompt: str = input("Enter prompt (e.g., 'Help me understand this codebase.'): ")
        api.query(prompt=prompt)
        print(f"\nAutomatically returning to menu in 15s...")
        time.sleep(15)
        return

    # Time out.
    print(f"\nAutomatically returning to menu in 5s...")
    time.sleep(5)

# Windows and Mac compatible terminal clearing.
def clear_terminal() -> None:
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

if __name__ == "__main__":
    main()
