import sys
import requests


class GithubOrganization:
    def __init__(self, organization: str, token: str) -> None:
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        self.session.proxies = {"https": "http://prp04.admin.ch:8080"}
        self.base_url = f"https://api.github.com/orgs/{organization}"

    def __get(self, url) -> any:
        if not url.startswith("http"):
            url = f"{self.base_url}/{url}"
        return self.session.get(url).json()

    def __get_with_details(self, endpoint) -> list[any]:
        return [self.__get(item["url"]) for item in self.__get(endpoint)]

    def get_members(self):
        return self.__get_with_details("members")

    def get_outside_collaborators(self):
        return self.__get_with_details("outside_collaborators")

    def get_repos(self):
        return self.__get(f"{self.base_url}/repos")

    def get_collaborators(self, repo):
        return self.__get(repo["url"] + "/collaborators")


def print_user_info(user):
    print(*[user[key] for key in ["login", "name", "email", "company"]])


def main():
    org = GithubOrganization(*sys.argv[1:])

    print("MEMBERS")
    for member in org.get_members():
        print_user_info(member)
    print()

    print("OUTSIDE COLLABORATORS")
    for collaborator in org.get_outside_collaborators():
        print_user_info(collaborator)
    print()

    print("REPOS")
    for repo in org.get_repos():
        print(repo["name"])
        for collaborator in org.get_collaborators(repo):
            print(
                "\t",
                collaborator["login"],
                [key for key, value in collaborator["permissions"].items() if value],
            )


if __name__ == "__main__":
    main()
