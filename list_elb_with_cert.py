#!/usr/bin/env python3

import boto3
from prettytable import PrettyTable

ACCOUNTS = [
    "default",
]

SSL_CERTS = {}

ELB_CLIENT = None
ELBV2_CLIENT = None
ACM_CLIENT = None
IAM_CLIENT = None


def get_cert_expiration_date(cert):
    try:
        exp_date = SSL_CERTS[cert]
    except KeyError:
        if "iam" in cert:
            exp_date = IAM_CLIENT.get_server_certificate(ServerCertificateName=cert.split('/')[-1])[
                'ServerCertificate']['ServerCertificateMetadata']['Expiration']
        elif "acm" in cert:
            exp_date = ACM_CLIENT.describe_certificate(
                CertificateArn=cert)['Certificate']['NotAfter']
        SSL_CERTS[cert] = exp_date
    return exp_date


def main():
    global ELB_CLIENT
    global ELBV2_CLIENT
    global ACM_CLIENT
    global IAM_CLIENT

    table = PrettyTable()
    table.field_names = ["Account", "LoadBalancerName",
                         "SSLCertificateID", "ExpirationDate"]

    for account in ACCOUNTS:
        session = boto3.Session(profile_name=account)
        ELB_CLIENT = session.client('elb')
        ELBV2_CLIENT = session.client('elbv2')
        ACM_CLIENT = session.client('acm')
        IAM_CLIENT = session.client('iam')

        # Go thru ELB
        elbs = ELB_CLIENT.describe_load_balancers()['LoadBalancerDescriptions']
        for elb in elbs:
            # Skip loadbalancers without instances
            if not elb['Instances']:
                continue
            for listener in elb['ListenerDescriptions']:
                name = elb['LoadBalancerName']
                sslcert = listener['Listener'].get('SSLCertificateId', None)
                if sslcert:
                    exp_date = get_cert_expiration_date(sslcert)
                    table.add_row([account, name, sslcert, exp_date])

        # Go thru ALB
        albs = ELBV2_CLIENT.describe_load_balancers()['LoadBalancers']
        for alb in albs:
            name = alb['LoadBalancerName']
            listeners = ELBV2_CLIENT.describe_listeners(
                LoadBalancerArn=alb['LoadBalancerArn'])['Listeners']
            for listener in listeners:
                if 'Certificates' in listener:
                    sslcerts = listener['Certificates']
                    for sslcert in sslcerts:
                        cert_arn = sslcert['CertificateArn']
                        exp_date = get_cert_expiration_date(cert_arn)
                        table.add_row([account, name, cert_arn, exp_date])

    print(table.get_string(sortby="ExpirationDate"))


if __name__ == "__main__":
    main()
