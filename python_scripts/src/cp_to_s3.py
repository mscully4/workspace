#! /usr/bin/env python3

import argparse
import logging
import os
from typing import List, Optional

import boto3
from boto3.exceptions import S3UploadFailedError
from botocore.exceptions import EndpointConnectionError

logger = logging.getLogger(__name__)


def parse_args(
    argv: Optional[List[str]] = None
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Copy a file to S3")
    parser.add_argument("-l", "--location", type=str, required=True)
    parser.add_argument(
        "-b", "--bucket-name", type=str, required=True, help="The bucket to copy to"
    )
    parser.add_argument(
        "-o", "--object-name", type=str, required=True, help="The file to copy to s3"
    )
    parser.add_argument(
        "-p", "--profile", type=str, required=True, help="The AWS Profile to use"
    )
    args = parser.parse_args(argv)
    return args


def upload_file(
    session: boto3.Session, file_name: str, bucket: str, object_name: str = None
):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    logger.info(f"Writing file at {file_name} to s3://{bucket}/{object_name}")

    # Upload the file
    s3 = session.client("s3")
    try:
        s3.upload_file(file_name, bucket, object_name)
        logging.info("File Upload Successful")
    except FileNotFoundError as e:
        logger.exception("File does not exist")
        raise
    except EndpointConnectionError as e:
        logger.exception("Could not connect to bucket.  Do you have permission?")
        raise
    except S3UploadFailedError as e:
        logger.exception("File Upload Failed")
        raise
    except Exception as e:
        logger.exceptions(e)
        raise


def main(argv: Optional[List[str]] = None):
    args = parse_args(argv)
    session = boto3.Session(profile_name=args.profile)
    upload_file(session, args.location, args.bucket_name, args.object_name)


if __name__ == "__main__":
    main()
