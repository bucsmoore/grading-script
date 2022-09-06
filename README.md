# CS110 Grading Script

The grading script will download portfolios for you section as well as create a test file containing a list of students for your section.

To use the script:

1. Clone repo
2. Change directory into repo
  - `cd grading_script`
3. If this is the first tiem you are suign the script: install dependencies
  - `pip install -r requirements.txt`
4. add a file to the folder called `.env`
5. Add the following to the .env file:
   ```
   GITHUB_PAT=""
   GITHUB_USERNAME=""
   GITHUB_EMAIL=""
   GITHUB_COMMIT_NAME=""

   GITHUB_ORG="bucs110FALL22"
   ```
   For the first 4 , fill in your information. Leave the last one, GITHUB_ORG, as is.
6. Run the grader and select your section
  - `python3 main.py`


