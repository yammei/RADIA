import os
import json
import requests
import urllib.parse
from dotenv import load_dotenv
class API:
    def __init__(self) -> any:
        # Access credentials.
        self.API_KEY: str = None
        self.GIT_TOK: str = None
        self.credentials: bool = False

        # Repository information.
        self.clip_user: str = None
        self.clip_remote: str = None
        self.clip_repository: str = None
        self.clip_branch: str = None

        # API endpoints.
        self.url_index: str = "https://api.greptile.com/v2/repositories"
        self.url_progress: str = "https://api.greptile.com/v2/repositories/" # Call connect() to complete URL.
        self.url_query: str = "https://api.greptile.com/v2/query"

    # 0. Access API.
    def connect(self) -> None:
        try:
            # Set repository information via CLI prompts.
            self.clip_user = input("Repository Username (owner of repository): ")
            self.clip_remote = input("Repository Service (e.g., github/gitlab): ")
            self.clip_repository = f"{self.clip_user}/{input('Repository Path (e.g., my-repo-name/): ')}"
            self.clip_branch = input("Repository Branch (e.g., main): ")

            # Access credentials from .env file.
            load_dotenv("../.env")
            self.API_KEY = os.getenv("API_KEY")
            self.GIT_TOK = os.getenv("GIT_TOK")

            # Status.
            print(f"\nRetrieving Credentials...")
            print(f"    ├ {f'API_KEY found: {self.API_KEY[0]}...{self.API_KEY[-1]}.' if self.API_KEY else 'API_KEY not found'}")
            print(f"    └ {f'GIT_TOK found: {self.GIT_TOK[0]}...{self.GIT_TOK[-1]}.' if self.GIT_TOK else 'GIT_TOK not found'}")

            # Encode and append repository identifier for indexing progress endpoint URL.
            repo_id: str = f"{self.clip_remote}:{self.clip_branch}:{self.clip_repository}"
            repo_id = urllib.parse.quote(repo_id, safe="")
            self.url_progress += repo_id

        except Exception as e:
            print(f"Error: {e}")

    # 1. Index a Github repository.
    def index(self, repo_service: str = "", repo_path: str = "", repo_branch: str = "main", mode: str = "CLI") -> None:
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
            pass

    # 2. Check progress of repo indexing.
    def index_progress(self) -> None:
        try:
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
                print(f"{payload['messages'][0]['content']}")
                print(f"\Requesting completion to prompt...\n   ├ Prompt: {payload['messages'][0]['content']}\n   ├ Remote: {payload['repositories'][0]['remote']}\n   ├ Branch: {payload['repositories'][0]['branch']}\n   └ Repository: {payload['repositories'][0]['repository']}")

                response = requests.post(self.url_query, json=payload, headers=headers)
                print(f"\nResponse:\n{json.dumps(response.json(), indent=4)}")

                return response

            except Exception as e:
                print(f"Error: {e}")
