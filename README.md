# Approve and merge multiple pull requests
Approve multiple pull request to review and merge

1. Run ```pip3 install requests```
2. Add your personal token from github as environment Variable ```export GITHUB_TOKEN=your_personal_access_token```
3. Add list of pull requests in [pull_request_urls.txt](pull_request_urls.txt) file
4. Run ```python3 git_merge.py```
