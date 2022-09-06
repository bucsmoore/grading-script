import json
import csv
import os
import shutil
from github import Github
from dotenv import load_dotenv

import logging as log

class Repository:

    def __init__(self, repo=None, path="./"):
        """
        _summary_

        Args:
            repo (_type_, optional): _description_. Defaults to None.
            path (str, optional): _description_. Defaults to "./".
        """
        self.dir = path
        self.path = f'{path}/{repo.name}'
        self.name = repo.name
        token = os.environ.get('GITHUB_PAT')
        if not os.path.exists(self.path):
            clone_url= f"https://{token}@github.com/{repo.full_name}"
            os.system(f"git clone {clone_url} {self.path}")

class GHOrganization:

    def __init__(self, org=None, token=None, username=None, email=None, name=None):
        """
        _summary_

        Args:
            org (_type_, optional): _description_. Defaults to None.
        """
        self.token = token or os.getenv('GITHUB_PAT')
        self.org = org or os.getenv('GITHUB_ORG')
        self.username = username or os.getenv('GITHUB_USERNAME')
        self.email = email or os.getenv('GITHUB_EMAIL')
        self.commit_name = name or os.getenv('GITHUB_COMMIT_NAME')
        #log.debug(f"{vars(self)}")
        if self.token and self.org:
            self.g = Github(self.token)
            self.org = self.g.get_organization(self.org) if self.org else None
            self.repo_list = self.org.get_repos()
        self.repositories = []

    def get_repos(self, destination = "./repos"):
        """
        _summary_
        """
        shutil.rmtree(destination, ignore_errors=True)
        os.mkdir(destination)
        for repo in self.repo_list:
                self.repositories.append(Repository(repo=repo, path=destination))
        return self.repositories

    def search_repo(self, destination = "./repos", search=""):
        """
        _summary_
        """
        #log.warning(f"searching for: {search}")
        self.repositories += [Repository(repo, destination) for repo in self.repo_list if search in repo.name]
        #log.warning(f"found: {self.repositories[-1].name}")
        return self.repositories

    def search_repos(self, destination = "./repos", search=None):
        """
        _summary_
        """
        if not search:
            return self.get_repos()

        self.repositories += [self.search_repo(destination=destination, search=s) for s in search]
        return self.repositories

    def clear_repos(self, destination = "./repos", search=""):
        """
        _summary_
        """
        shutil.rmtree(destination, ignore_errors=True)
        os.mkdir(destination)
        self.repositories = []

def main():
    load_dotenv() 
    print("Choose your section (example: A51)")
    section = input(": ").upper()
    students = json.load(open("lab_sections.json"))
    section_students = [s for s in students if section in s["section"]]

    fptr = open(f"section_{section}.txt", "w")
    [fptr.write(f"{s['last_name']}, {s['first_name']} \n") for s in section_students]
    fptr.close()
    
    org = GHOrganization()
    org.clear_repos()
    repos = org.search_repos(search=[s['github_username'] for s in section_students])
    print("Your section's portfolios have been downloaded to the 'repo' folder.")


main()