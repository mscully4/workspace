#! /usr/bin/env python3

import argparse
import logging
import boto3
from typing import Optional, List
from urllib.parse import unquote, urlparse


logger = logging.getLogger(__name__)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Retrieves an S3 object using its web url"
    )
    parser.add_argument(
        "-u", "--url", type=str, required=True, help="The url of the object"
    )
    parser.add_argument(
        "-o",
        "--output-file",
        type=str,
        required=False,
        help="A file to write the object to",
    )
    parser.add_argument(
        "-p", "--profile", type=str, required=True, help="The AWS Profile to use"
    )
    args = parser.parse_args(argv)
    return args


def get_bucket_and_key_from_url(url: str):
    parsed = urlparse(unquote(url))

    return parsed.netloc.split(".")[0], parsed.path[1:]


def get_object(session: boto3.Session, bucket_name: str, key: str):
    s3 = session.resource("s3")
    obj = s3.Object(bucket_name, key)
    return obj.get()["Body"].read().decode("utf-8")


def write_object_to_file(filepath, content):
    with open(filepath, "w") as fh:
        fh.write(content)


def main(argv: Optional[List[str]] = None):
    args = parse_args(argv)
    session = boto3.Session(profile_name=args.profile)

    bucket, key = get_bucket_and_key_from_url(args.url)
    obj = get_object(session, bucket, key)

    if args.output_file:
        write_object_to_file(args.output_file, obj)
    else:
        print(obj)


if __name__ == "__main__":
    main()
