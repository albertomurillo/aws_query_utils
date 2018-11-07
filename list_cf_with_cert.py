#!/usr/bin/env python3

import boto3
from prettytable import PrettyTable

ACCOUNT = "default"


def main():
    session = boto3.Session(profile_name=ACCOUNT)
    cf_client = session.client('cloudfront')
    acm_client = session.client('acm')

    resp = cf_client.list_distributions()
    distributions = resp['DistributionList']['Items']

    table = PrettyTable()
    table.field_names = ["ID", "Certificate", "issuer", "expires"]
    for dist in distributions:
        dist_id = dist['Id']
        cert = dist['ViewerCertificate'].get('Certificate', None)
        source = dist['ViewerCertificate'].get('CertificateSource', None)
        if source == 'acm':
            cert_description = acm_client.describe_certificate(
                CertificateArn=cert)['Certificate']

            issuer = cert_description['Issuer']
            expire_date = cert_description['NotAfter']
            table.add_row([dist_id, cert, issuer, expire_date])

    print(table.get_string(sortby="expires"))


if __name__ == "__main__":
    main()
