#! /usr/bin/env python3

import argparse
import logging
import re
import boto3
from typing import Optional, List

logger = logging.getLogger(__name__)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Empties and deletes an S3 bucket")
    parser.add_argument(
        "-b", "--bucket-name", type=str, required=False, help="The bucket to be deleted"
    )
    parser.add_argument(
        "-p", "--profile", type=str, required=True, help="The AWS Profile to use"
    )
    parser.add_argument(
        "-r",
        "--bucket-regex",
        type=str,
        required=False,
        help="A pattern of bucket names to delete",
    )
    args = parser.parse_args(argv)
    return args


def get_buckets_that_match_regex(session: boto3.Session, regex: str):
    buckets = []
    s3 = session.resource("s3")
    for bucket in s3.buckets.all():
        if re.match(regex, bucket.name):
            buckets.append(bucket)
    return buckets


def delete_bucket(session: boto3.Session, bucket_name: str):
    s3 = session.resource("s3")
    bucket = s3.Bucket(bucket_name)
    logger.info(f"Emptying Bucket: {bucket_name}")
    bucket.objects.delete()
    bucket.object_versions.delete()
    logger.info(f"Deleting Bucket: {bucket_name}")
    bucket.delete()
    logger.info(f"Successfully Deleted Bucket: {bucket_name}")


def main(argv: Optional[List[str]] = None):
    args = parse_args(argv)
    session = boto3.Session(profile_name=args.profile)

    if "bucket_regex" in args:
        buckets = get_buckets_that_match_regex(args.bucket_regex)
        for bucket in buckets:
            delete_bucket(session=session, bucket_name=bucket.name)
    elif "bucket_name" in args:
        delete_bucket(session=session, bucket_name=args.bucket_name)


if __name__ == "__main__":
    main()
