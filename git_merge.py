import requests
import time
import os

# Replace with your GitHub personal access token
token = os.getenv('GITHUB_TOKEN')

# Read the pull request URLs from a file
with open('pull_request_urls.txt', 'r') as file:
    pull_request_urls = [line.strip() for line in file.readlines()]


# Headers with authentication
headers = {
    'Authorization': f'Bearer {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Function to add a review to a pull request
def add_review(pull_url, event):
    parts = pull_url.split('/')
    owner, repo, pull_number = parts[3], parts[4], parts[6]
    review_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/reviews'
    review_data = {
        "event": event,
        "body": "LGTM"
    }
    response = requests.post(review_url, json=review_data, headers=headers)
    return response

# Function to merge a pull request
def merge_pull_request(pull_url, commit_sha, commit_title):
    parts = pull_url.split('/')
    owner, repo, pull_number = parts[3], parts[4], parts[6]
    merge_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/merge'
    merge_data = {
        "commit_title": commit_title,
        "commit_message": commit_sha
    }
    response = requests.put(merge_url, json=merge_data, headers=headers)
    return response

# Iterate over each pull request URL
for pr_url in pull_request_urls:
    try:
        # Add an approval review to the pull request
        review_response = add_review(pr_url, "APPROVE")

        if review_response.status_code != 200:
            print(f"Failed to add review for pull request {pr_url}. Status code: {review_response.status_code}")
            continue

        print(f"Review added for pull request {pr_url}")

        # Wait for the review to be approved
        while True:
            review_details = review_response.json()
            if review_details["state"] == "APPROVED":
                break
            time.sleep(10)  # Wait for 10 seconds before checking again

        # Replace with the actual commit SHA and commit title
        commit_sha = "sha_of_the_head_commit"
        commit_title = "Merge pull request"

        time.sleep(5) 

        # Merge the pull request
        merge_response = merge_pull_request(pr_url, commit_sha, commit_title)

        if merge_response.status_code != 200:
            print(f"Failed to merge pull request {pr_url}. Status code: {merge_response.status_code}")
        else:
            print(f"Pull request {pr_url} merged successfully")
    except Exception as e:
        print(f"An error occurred while processing {pr_url}: {str(e)}")
