#!/usr/bin/env python3

import base64
import hashlib
import hmac
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: %s <AWS_SECRET_ACCESS_KEY>" % sys.argv[0])
        sys.exit(1)

    KEY = sys.argv[1]
    MESSAGE = "SendRawEmail"
    VERSION = bytearray(b'\x02')

    mac = hmac.HMAC(KEY, MESSAGE, hashlib.sha256)
    digest = mac.hexdigest()
    signature = bytearray.fromhex(digest)
    smtp_password = base64.b64encode(VERSION + signature)

    print(smtp_password)


if __name__ == "__main__":
    main()
