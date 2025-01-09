import json
import subprocess
from datetime import datetime
import email
import os

repo_path = "https://github.com/emilykelt.github.io/me"


POSTS_FILE = "posts.json"

def add_email_posts(posts):
    # Load existing posts
    with open(POSTS_FILE, "r") as file:
        existing_posts = json.load(file)

    for post in posts:
        new_post = {
            "title": post["title"],
            "content": post["content"],
            "date":  datetime.now().strftime("%Y-%m-%d")
        }
        existing_posts.insert(0, new_post)  # Add to the top of the list

    # Save updated posts
    with open(POSTS_FILE, "w") as file:
        json.dump(existing_posts, file, indent=4)

    # Commit and push changes to GitHub
    subprocess.run(["git", "add", POSTS_FILE])
    subprocess.run(["git", "commit", "-m", "Add new posts from email"])
    subprocess.run(["git", "push"])

# Fetch emails and add them to the blog
emails = email.fetch_emails()
add_email_posts(emails)
