#! /usr/bin/env python3

from config import Config
import argparse
import boto3
import os
import logging

from logging_setup import get_logger, add_handler
from botocore.exceptions import EndpointConnectionError
from boto3.exceptions import S3UploadFailedError
from mypy_boto3.boto3_session import Session
import yaml

logger = get_logger(__name__)

module = __file__.split('/')[-1].split('.')[0]

logging_path = Config.LOGS_DIR + "/" + module + "/"
if not os.path.exists(logging_path):
    os.mkdir(logging_path)

add_handler(logger, logging_path)

def parse_args() -> dict:
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-l', '--location', type=str, required=True)
    parser.add_argument('-b', '--bucket-name', type=str,
                        required=True, help='The bucket to be deleted')
    parser.add_argument('-o', '--object-name', type=str,
                        required=True, help='The bucket to be deleted')
    parser.add_argument('-p', '--profile', type=str, default="default")
    args = vars(parser.parse_args())
    return args


def create_session(profile_name: str = "default") -> Session:
    return boto3.session.Session(profile_name=profile_name)


def upload_file(session: Session, file_name: str, bucket:str, object_name:str=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    logger.info(f"Writing file at {file_name} to s3://{bucket}/{object_name}")

    # Upload the file
    s3 = session.client('s3')
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


if __name__ == "__main__":
    args = parse_args()
    session = create_session(args['profile'])
    upload_file(session, args['location'], args['bucket_name'], args['object_name'])
