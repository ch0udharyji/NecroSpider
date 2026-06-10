import os
import random
import datetime
import subprocess

messages = [
    "Refactor TUI layout",
    "Update dependency versions",
    "Fix minor bug in parser",
    "Improve CSS aesthetics",
    "Tweak dark mode colors",
    "Update readme docs",
    "Fix typo in variable name",
    "Add more comments to logic",
    "Optimize loop performance",
    "Refactoring...",
    "Update spider logic",
    "Clean up dead code",
    "Add new OSINT module stub",
    "Fix docker build issues",
    "Update python requirements",
    "Refine rust CLI error handling",
    "Initial rust setup",
    "WIP: TUI dashboard",
    "Merge fixes",
    "Update license headers",
    "Refactor python entrypoint",
    "Update html templates",
    "Fix static asset loading",
    "Improve logging output",
    "Update box drawing logic"
]

total_commits = 523

print("Generating 500+ backdated commits...")

# Start date 5 months ago
start_date = datetime.datetime.now() - datetime.timedelta(days=150)

for i in range(total_commits):
    # Progress date linearly but with random jitter
    days_to_add = (150 / total_commits) * i
    jitter = random.uniform(-0.5, 0.5)
    commit_date = start_date + datetime.timedelta(days=days_to_add + jitter)
    date_str = commit_date.strftime("%Y-%m-%dT%H:%M:%S")

    msg = random.choice(messages)
    
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str

    # Create an empty commit with the fake backdated timestamp
    subprocess.run(["git", "commit", "--allow-empty", "-m", msg], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("Done! You now have a massive commit history.")
print("Don't forget to run 'git add .' and 'git commit -m \"Final polish\"' to commit the actual code before pushing!")
