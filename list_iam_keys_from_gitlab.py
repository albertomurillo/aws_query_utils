#!/usr/bin/env python3

import json
import os
import requests
from prettytable import PrettyTable


GITLAB_API_URL = "https://gitlab.com/api/v4"
GITLAB_TOKEN = os.environ['GITLAB_ACCESS_TOKEN']
HEADERS = {'Private-Token': GITLAB_TOKEN}


def get_groups():
    url = GITLAB_API_URL + "/groups"
    r = requests.get(url, headers=HEADERS)
    groups = json.loads(r.content)
    return groups


def get_group_variables(group_id):
    url = GITLAB_API_URL + "/groups/" + str(group_id) + "/variables"
    r = requests.get(url, headers=HEADERS)
    group_vars = json.loads(r.content)
    return group_vars


def get_project_variables(project_id):
    url = GITLAB_API_URL + "/projects/" + str(project_id) + "/variables"
    r = requests.get(url, headers=HEADERS)
    project_vars = json.loads(r.content)
    return project_vars


def get_projects(group_id):
    url = GITLAB_API_URL + "/groups/" + str(group_id) + "/projects"
    r = requests.get(url, headers=HEADERS)
    projects = json.loads(r.content)
    return projects


def get_keys(variables):
    # Skip forbidden queries
    if 'message' in variables and variables['message'] == '403 Forbidden':
        return None
    # Return only AWS_ACCESS_KEY_ID and ignore other variables
    keys = [v for v in variables if v['key'] == 'AWS_ACCESS_KEY_ID']
    if keys:
        return keys[0]["value"]


def main():
    x = PrettyTable()
    x.field_names = ["Key", "Location"]
    x.align["Location"] = "l"

    groups = get_groups()
    for group in groups:
        group_vars = get_group_variables(group['id'])
        keys = get_keys(group_vars)
        if keys:
            x.add_row([keys, group['full_path']])

        projects = get_projects(group['id'])
        for project in projects:
            project_vars = get_project_variables(project['id'])
            keys = get_keys(project_vars)
            if keys:
                x.add_row([keys, project['path_with_namespace']])

    print(x)


if __name__ == "__main__":
    main()
