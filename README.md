# aws_query_utils

A collection of scripts to query useful information from aws accounts.

### Prerequisites
The scripts are written in python3 and use boto3 and PrettyTable libraries for aws access and pretty printing.
Install with `pip3 install -r requirements.txt`

#### list_cf_with_certs.py
This script list cloudformation distributions and its associated certificates

#### list_elb_with_cert.py
This script list all elb and alb from aws accounts which have ssl certificate and associated instances.

Tip: You can convert the output to csv with the following commands
```
./list_elb_with_cert.py | tee elbs.txt
cat elbs.txt | tr "|" "," | tr -d " " | grep -v ^+ | gsed 's/^,//g' | gsed 's/,$//g' > elbs.csv
```

#### list_iam_keys.py
This script list all the IAM keys and how old they are.
To list only active keys
```
./list_iam_keys.py | grep Active
```

#### derive_ses_smtp_password.py
This script takes a secret key as argument and prints the smtp password that can be used with that iam user.

#### list_iam_keys_from_gitlab.py
Query gitlab and print groups or projects and its associated iam key
Note: Requires a gitlab token

```
export GITLAB_ACCESS_TOKEN=gBbswXrl7kde6FYhSHF9
./list_iam_keys_from_gitlab.py
```

#### copy_dynamo_table.js
Copies a DynamoDB table from one AWS account to another
