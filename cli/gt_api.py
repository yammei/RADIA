import os
import json
import time
import aiohttp
import requests
import urllib.parse
from dotenv import load_dotenv

class API:
    def __init__(self) -> any:
        # Access credentials from .env file.
        load_dotenv(".env")
        self.API_KEY: str = os.getenv("API_KEY")
        self.GIT_TOK: str = os.getenv("GIT_TOK")

        # Repository information.
        self.clip_user: str = None
        self.clip_remote: str = None
        self.clip_repository: str = None
        self.clip_branch: str = None

        # API endpoints.
        self.url_index: str = "https://api.greptile.com/v2/repositories"
        self.url_progress: str = "https://api.greptile.com/v2/repositories/" # Call connect() to complete URL.
        self.url_query: str = "https://api.greptile.com/v2/query"

    # -3. Save current repository access configuration.
    def save(self) -> None:
        # Assign config values to kv pairs.
        with open("config.json", "r") as file:
            config = json.load(file)

        config["username"]      = self.clip_user
        config["service"]       = self.clip_remote
        config["repository"]    = self.clip_repository
        config["branch"]        = self.clip_branch

        # Update config.json with current values.
        print(f"\nMy configurations:\n{json.dumps(config, indent=4)}\n\n[-] Saving configurations...")
        with open("config.json", "w") as file2:
            json.dump(config, file2, indent=4)
            print(f"[✔] Configurations saved.\n")


    # -2. Check for previous repository access configuration.
    def check(self, config_path: str = "config.json", source: str = "cli") -> bool:
        # Change config path if Discord bot access.
        if source == "discord":
            config_path = "../cli/config.json"

        if not os.path.exists(config_path):
            print(f"\nFile {config_path} not found.\n    ├ [-] Generating {config_path}...")

            rac: dict = {
                "username": "",
                "service": "",
                "repository": "",
                "branch": ""
            }

            with open("config.json", "w") as config_file:
                json.dump(rac, config_file, indent=4)
                print(f"    └ [✔] Generated {config_path}.\n")

        with open(config_path, "r") as file:
            config = json.load(file)

        valid_saved_config: bool = True if config.get("username") != "" and config.get("service") != "" and config.get("repository") != "" and config.get("branch") != "" else False
        return valid_saved_config

    # -1. Load repository access configuration.
    def load(self, source: str = "cli") -> None:
        config_path: str = "config.json"

        # Change config path for Discord bot access.
        if source == "discord":
            config_path = "../cli/config.json"

        with open(config_path, "r") as file:
            config = json.load(file)

        # Check for placeholders and alert the user
        self.clip_user = config.get("username")
        self.clip_remote = config.get("service")
        self.clip_repository = config.get("repository")
        self.clip_branch = config.get("branch")

        """
        # Load and validate the configuration
        config = load_config('config.json')

        # Access the configuration values
        discord_token = config["discord_token"]
        database_url = config["database_url"]
        debug_mode = config["debug"]
        """

        print(f"\nLoading Configurations...\n    ├ Username: {self.clip_user}\n    ├ Service: {self.clip_remote}\n    ├ Repository: {self.clip_repository}\n    └ Branch: {self.clip_branch}")

        return

    # 0. Access API.
    def connect(self, mode: str = "manual") -> str:
        try:
            # Set repository information via CLI prompts.
            self.clip_user = input("Repository Username (owner of repository): ")
            self.clip_remote = input("Repository Service (e.g., github/gitlab): ")
            self.clip_repository = f"{self.clip_user}/{input('Repository Path (e.g., my-repo-name/): ')}"
            self.clip_branch = input("Repository Branch (e.g., main): ")

            # Status.
            print(f"\nRetrieving Credentials...")
            print(f"    ├ {f'API_KEY found: {self.API_KEY[0]}...{self.API_KEY[-1]}.' if self.API_KEY else 'API_KEY not found'}")
            print(f"    └ {f'GIT_TOK found: {self.GIT_TOK[0]}...{self.GIT_TOK[-1]}.' if self.GIT_TOK else 'GIT_TOK not found'}")


            # If entries are not empty, return True.
            valid_entries: bool = self.clip_user != "" and self.clip_remote != "" and self.clip_repository != "" and self.clip_branch != ""
            return "save" if valid_entries else "dont save"

        except Exception as e:
            print(f"Error: {e}")

    # 1. Index a Github repository.
    def index(self, mode: str = "CLI") -> None:
        if mode == "CLI":
            try:
                headers: dict = {
                    'Authorization': f'Bearer {self.API_KEY}',
                    'X-Github-Token': self.GIT_TOK,
                    'Content-Type': 'application/json'
                }
                payload: dict = {
                    "remote": self.clip_remote,
                    "repository": self.clip_repository,
                    "branch": self.clip_branch if self.clip_branch != "" else "main",
                }
                print(f"\nAttempting to index repository...\n   ├ Service: {payload['remote']}\n   ├ Branch: {payload['branch']}\n   └ Repository: {payload['repository']}")

                response = requests.post(self.url_index, json=payload, headers=headers)
                print(f"\nResponse:\n{json.dumps(response.json(), indent=4)}")

            except Exception as e:
                print(f"Error: {e}")

        elif mode == "APP":
            # For UI implementation.
            pass

    # 2. Check progress of repo indexing.
    def index_progress(self) -> None:
        try:
            # Encode and append repository identifier for indexing progress endpoint URL.
            repo_id: str = f"{self.clip_remote}:{self.clip_branch}:{self.clip_repository}"
            repo_id = urllib.parse.quote(repo_id, safe="")
            self.url_progress += repo_id

            headers: dict = {
                'Authorization': f'Bearer {self.API_KEY}',
                'X-Github-Token': self.GIT_TOK
            }
            print(f"\nChecking indexing progress:\n    └ URL: ...{self.url_progress[24:]}.")

            response = requests.get(self.url_progress, headers=headers)
            print(f"\nResponse:\n{json.dumps(response.json(), indent=4)}")

        except Exception as e:
            print(f"Error: {e}")

    # 3. Send prompt and retrieve completion.
    def query(self, uid: str = "default-user", prompt: str = "", role: str = "user") -> None:
        print(f"query() reached. Passing prompt of type {type(prompt)} and length {len(prompt)}.")
        if len(prompt) == 0:
            return
        else:
            try:
                headers = {
                    'Authorization': f'Bearer {self.API_KEY}',
                    'X-Github-Token': self.GIT_TOK,
                    'Content-Type': 'application/json'
                }
                payload = {
                    "messages": [
                        {
                            "id": uid,
                            "content": prompt,
                            "role": role
                        }
                    ],
                    "repositories": [
                        {
                            "remote": self.clip_remote,
                            "repository": self.clip_repository,
                            "branch": self.clip_branch
                        }
                    ],
                    "sessionId": f"{uid}-session-id" # Key sessionId retrieves chat history.
                }
                print(f"\nRequesting completion to prompt...\n   ├ Prompt: {payload['messages'][0]['content']}\n   ├ Remote: {payload['repositories'][0]['remote']}\n   ├ Branch: {payload['repositories'][0]['branch']}\n   └ Repository: {payload['repositories'][0]['repository']}")

                response = requests.post(self.url_query, json=payload, headers=headers)
                completion: str = response.json()["message"]
                # print(f"\nResponse:\n{json.dumps(response.json(), indent=4)}")
                print(f"\nMessage:\n{completion}")

                return completion

            except Exception as e:
                print(f"Error: {e}")

    # 3.1 [Discord Ver.] Send prompt and retrieve completion.
    async def discordQuery(self, uid: str = "default-user", prompt: str = "", role: str = "user") -> None:
        if len(prompt) == 0:
            return
        else:
            try:
                headers = {
                    'Authorization': f'Bearer {self.API_KEY}',
                    'X-Github-Token': self.GIT_TOK,
                    'Content-Type': 'application/json'
                }
                payload = {
                    "messages": [
                        {
                            "id": uid,
                            "content": prompt,
                            "role": role
                        }
                    ],
                    "repositories": [
                        {
                            "remote": self.clip_remote,
                            "repository": self.clip_repository,
                            "branch": self.clip_branch
                        }
                    ],
                    "sessionId": f"{uid}-session-id" # Key sessionId retrieves chat history.
                }
                print(f"\nRequesting completion to prompt...\n   ├ Prompt: {payload['messages'][0]['content']}\n   ├ Remote: {payload['repositories'][0]['remote']}\n   ├ Branch: {payload['repositories'][0]['branch']}\n   └ Repository: {payload['repositories'][0]['repository']}")

                async with aiohttp.ClientSession() as session:
                    async with session.post(self.url_query, json=payload, headers=headers) as response:
                        result = await response.json()
                        completion = result.get("message", "No completion.")
                        print(f"\nMessage:\n{completion}")
                        return completion

            except Exception as e:
                print(f"Error: {e}")
