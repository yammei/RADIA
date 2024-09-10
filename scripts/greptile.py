import os
import requests
import urllib.parse
from dotenv import load_dotenv

class API:
    def __init__(self) -> any:
        # Access credentials.
        self.GRP_URL: str = None
        self.API_KEY: str = None
        self.GIT_TKN: str = None

        # Repository information.
        self.clip_user: str = None
        self.clip_remote: str = None
        self.clip_repository: str = None
        self.clip_branch: str = None

    # 0. Access API.
    def connect(self) -> None:
        try:
            # Set repository information via CLI prompts.
            self.clip_user = input("Repository Username (owner of repository): ")
            self.clip_remote = input("Repository Service (e.g., github/gitlab): ")
            self.clip_repository = f"{self.clip_user}/{input("Repository Path (e.g., my-repo-name/): ")}"
            self.clip_branch = input("Repository Branch (e.g., main): ")

            # Access credentials from .env file.
            load_dotenv("../.env")
            self.API_KEY = os.getenv("API_KEY")
            self.GIT_TKN = os.getenv("GIT_TKN")
            self.GRP_URL = os.getenv("GRP_URL")

            # Status.
            print(f"\nRetrieving Credentials...")
            print(f"    ├ {f'GRP_URL found: ..{self.GRP_URL[20:-8]}...' if self.GRP_URL else 'GRP_URL not found'}")
            print(f"    ├ {f'API_KEY found: {self.API_KEY[0]}...{self.API_KEY[-1]}.' if self.API_KEY else 'API_KEY not found'}")
            print(f"    └ {f'GIT_TKN found: {self.GIT_TKN[0]}...{self.GIT_TKN[-1]}.' if self.GIT_TKN else 'GIT_TKN not found'}")

        except Exception as e:
            print(f"Error: {e}")

    # 1. Call Greptile API to index a Github repository.
    def index(self, repo_service: str = "", repo_path: str = "", repo_branch: str = "main", mode: str = "CLI") -> None:
        if mode == "CLI":
            try:
                headers: dict = {
                    'Authorization': f'Bearer {self.API_KEY}',
                    'X-Github-Token': self.GIT_TKN,
                    'Content-Type': 'application/json'
                }
                payload: dict = {
                    "remote": self.clip_remote,
                    "repository": self.clip_repository,
                    "branch": self.clip_branch if self.clip_branch != "" else "main",
                }
                print(f"\nAttempting to index repository...\n   ├ Service: {payload["remote"]}\n   ├ Branch: {payload["branch"]}\n   └ Repository: {payload["repository"]}")

                response = requests.post(self.GRP_URL, json=payload, headers=headers)
                print(f"Response:\n{response.json()}")

            except Exception as e:
                print(f"Error: {e}")

        elif mode == "APP":
            pass

    # 2. Check progress of repo indexing.
    def index_progress(self) -> None:
        try:
            # Encode repository identifier.
            repo_id: str = f"{self.clip_remote}:{self.clip_branch}:{self.clip_repository}"
            repo_id = urllib.parse.quote(repo_id, safe="")
            url: str = f'https://api.greptile.com/v2/repositories/{repo_id}'

            headers: dict = {
                'Authorization': f'Bearer {self.API_KEY}',
                'X-Github-Token': self.GIT_TKN
            }
            print(f"\nChecking indexing progress:\n    └ URL: ...{url[24:]}.")

            response = requests.get(url, headers=headers)
            print(response.json())

        except Exception as e:
            print(f"Error: {e}")

    # 3. Send prompt and retrieve completion.
    def query(self, uid: str = "default-user", prompt: str = "", role: str = 'user') -> None:
        if len(prompt) == 0:
            return
        
        # API Endpoint.
        url = 'https://api.greptile.com/v2/query'
        headers = {
            'Authorization': f'Bearer {self.API_KEY}',
            'X-Github-Token': self.GIT_TKN,
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
            "sessionId": f"{uid}-session-id"
        }
        # Key sessionId retrieves chat history.

        response = requests.post(url, json=payload, headers=headers)
        print(response.json())
        pass
