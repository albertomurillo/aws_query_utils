#!/usr/bin/env python3

import boto3
import time
import datetime
from prettytable import PrettyTable

ACCOUNTS = [
    "default",
]


def get_users(client):
    resp = client.list_users()
    return resp['Users']


def get_keys(client, users):
    keys = []
    for user in users:
        resp = client.list_access_keys(UserName=user['UserName'])
        keys += resp['AccessKeyMetadata']

    # Get last_used field
    for key in keys:
        resp = client.get_access_key_last_used(
            AccessKeyId=key['AccessKeyId']
        )
        try:
            last_used = resp['AccessKeyLastUsed']['LastUsedDate']
        except KeyError:
            last_used = None
        key.update({'LastUsedDate': last_used})
    return keys


def print_keys(keys):
    x = PrettyTable()
    x.field_names = ["Profile", "Username",
                     "Access Key", "Status", "Created", "LastUsed", "Key Age"]
    for key in keys:
        profile = key["Profile"]
        user = key['UserName']
        key_id = key['AccessKeyId']
        status = key['Status']
        created = f"{key['CreateDate']: %Y-%m-%d %H:%M}"
        last_used = key['LastUsedDate']
        if last_used:
            last_used = f"{last_used: %Y-%m-%d %H:%M}"
        age = (
            datetime.datetime.now(datetime.timezone.utc) - key['CreateDate']
        ).days
        x.add_row([profile, user, key_id, status, created, last_used, age])
    print(x.get_string(sortby="Created"))


def main():
    keys = []

    for profile in ACCOUNTS:
        session = boto3.Session(profile_name=profile)
        client = session.client('iam')
        users = get_users(client)
        profile_keys = get_keys(client, users)

        # Add profile field to keys
        [k.update({"Profile": profile}) for k in profile_keys]
        keys += profile_keys

    print_keys(keys)


if __name__ == "__main__":
    main()
