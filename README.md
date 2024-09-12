# ｡ﾟ•꒰ Greptile CLI & Discord Integration ꒱•  ｡ﾟ
<div id="top"/>
Repo Author: <b>Mei Zhang</b> <sup>[<a href="https://www.linkedin.com/in/mei-zh">Linkedin</a>]</sup><br>
Last Updated: <i>Sept 9, 2024</i><br>
Author Notes: Thank you to <b>@Daksh</b> <sup>[<a href="https://www.linkedin.com/in/dakshg/">Linkedin</a>]</sup> for sponsoring API usage.

<h2>Doc Index</h2>


<ul><ul style="list-style-type: none;">
  <li><code><a href="#i">Description</a></code></li>
  <li><code><a href="#ii">Installation: Greptile CLI</a></code></li>
  <li><code><a href="#iii">Installation: Discord Bot</a></code></li>
</ul></ul>

<h2 id="i">I. Description </h2>
This <code>README.md</code> details the step-by-step installation process for the Greptile CLI & Discord integration.<br><br>
This project streamlines API setup into a user-friendly command line interface (CLI), removing the hassle of API integration. Additionally, this repository contains a Discord bot, allowing users to use Greptile AI in a Discord channel and collaborate with other developers.

<h2 id="ii">II. Installation: Greptile CLI</h2>

<h3>Troubleshooting Notes:</h3>
<ul style="list-style-type: none;"><ul>
  <li>You will need an active Greptile API key (<a href="https://www.greptile.com/pricing">Greptile API usage</a>) and a Github permission access token (PAT) (<a href="https://github.com/settings/tokens">Github PAT</a>) to allow Greptile AI to analyse your own repositories.</li>
  <li>If <code>pip</code> and <code>python</code> doesn't work, then use <code>pip3</code> and <code>python3</code>.</li>
  <li>Prefix commands with <code>sudo</code> if you are having permission issues.</li>
</ul></ul>

<br><h3>1. Pull remote repository from Github.</h3>

<ul style="list-style-type: none;">

From the root directory of your choice, initialize a git repository and pull the codebase.

```bash
git init
git remote add origin https://github.com/yammei/greptile-ai.git
git pull origin main
```

</ul>

<br><h3>2. Setup .env file for Greptile API key and Github PAT.</h3>

<ul style="list-style-type: none;">

From the local repository's root directory, move to the <code>cli</code> directory and create a <code>.env</code> file.

```bash
cd cli
touch .env
```

Paste the following into the <code>.env</code> file. Replace and save the placeholder values with your own access credentials.

```bash
API_KEY=greptile_ai_api_key
GIT_TOK=github_personal_access_token
```

</ul>

<br><h3>3. Setup Python virtual environment.</h3>

<ul style="list-style-type: none;">

Setup Python a virtual environment to store Python dependencies (skip if you already have this resolved). Run one of the following series of commands based on your machine's operating system.<br>

For Mac users:
```bash
cd ./cli/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

For Windows users:
```bash
cd ./cli/
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

</ul>

<br><h3>4. Start using Greptile CLI.</h3>

<ul style="list-style-type: none; padding-left: 0;">

Run the following command on a terminal of your choice.

```bash
python gt_cli.py
```

If setup is successful, the main menu will display, which you can navigate using keyboard arrow keys and enter button.

```bash
? Greptile AI CLI - Navigate Menu Options
❯ 1: Check API Usage Credentials
  2: Index Repository
  3: Check Indexing Progress
  4: Post Repository Query
```

Navigate through each option in order 1-4 (repeat any steps necessary to edit or check info).<br>

Note: By using the option, <code>2: Index Repository</code>, Greptile will store summaries regarding your codebase files. <i>Please do not store personal and/or sensitive information you do not want processed, as it may allow unintended users to access that information</i>.
  <ul>
    <li>Step 1: Prompts the user to dictate a repository for Greptile AI to utilize and verifies all access credentials are met.</li>
    <li>Step 2: This will begin the indexing proccess for the repository you've dictated Greptile AI to utilize. This process may take 3 to 5 minutes for small repositories and up to an hour for larger repositories <sup>[<a href="https://docs.greptile.com/quickstart">Source: Greptile API Quickstart</a>]</sup>.</li>
    <li>Step 3: Checks the status of the dictated repository's indexing progress.</li>
    <li>Step 4: You may now prompt Greptile AI model for any questions or statements regarding the processed codebase.</li>
  </ul>

<br>For more information regarding API details. Please refer to <a href="https://docs.greptile.com/api-reference/introduction">Greptile API Reference</a>.

</ul>

<br><h2 id="iii">III. Installation: Discord Bot</h2>

<h3>1. Setup .env file.</h3>

<ul style="list-style-type: none;">
  Instructions coming soon.
</ul>

<br><h3>2. Setup Python virtual environment.</h3>

<ul style="list-style-type: none;">
  Instructions coming soon.
</ul>

<br><h3>3. Execute the Discord bot's run-time.</h3>

<ul style="list-style-type: none;">
  Instructions coming soon.
</ul>

<br><h3>4. Start using Greptile bot.</h3>

<ul style="list-style-type: none;">
    <a href="https://discord.com/oauth2/authorize?client_id=1283119830186070152&permissions=8&integration_type=0&scope=bot">Discord Bot Invite Link</a>
</ul>

<br><h2 id="iv">IV. Features: Greptile CLI</h2>

<h3>Config files are auto-generated if not found.</h3>

<ul style="list-style-type: none;">

```bash
? Greptile AI CLI - Navigate Menu Options 1: Check API Usage Credentials

File config.json not found.
    ├ [-] Generating config.json...
    └ [✔] Generated config.json.

```
</ul>

<h3>Repository access configurations can now be saved.</h3>

<ul style="list-style-type: none;">

```bash
? Would you like to save these repository access configurations?
❯ 1: Yes, save these configurations (checking API credentials in the future will prompt to load the saved configu
2: No, don't save these configurations.

...

? Would you like to save these repository access configurations? 1: Yes, save these configurations (checking API
credentials in the future will prompt to load the saved configurations).

My configurations:
{
    "username": "my_username",
    "service": "github",
    "repository": "my_username/my_repo",
    "branch": "main"
}

[-] Saving configurations...
[✔] Configurations saved.


Automatically returning to menu in 10s...
```
</ul>

<br><a href="#top">Back to Top</a>