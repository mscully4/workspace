#! /usr/bin/env python3

import argparse
import boto3
import os
from config import Config
from logging_setup import get_logger, add_handler

logger = get_logger(__name__)

module = __file__.split('/')[-1].split('.')[0]

logging_path = Config.LOGS_DIR + "/" + module + "/"
if not os.path.exists(logging_path):
    os.mkdir(logging_path)

add_handler(logger, logging_path)

def parse_args():
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('-b', '--bucket-name', type=str,
	                    required=True, help='The bucket to be deleted')
	parser.add_argument('-p', '--profile', type=str, default="default")
	args = vars(parser.parse_args())
	return args


def create_session(profile_name="default"):
    return boto3.session.Session(profile_name=profile_name)


def delete_bucket(session, bucket_name):
	s3 = session.resource('s3')
	bucket = s3.Bucket(bucket_name)
	logger.info(f"Emptying Bucket: {bucket_name}")
	bucket.objects.delete()
	bucket.object_versions.delete()
	logger.info(f'Deleting Bucket: {bucket_name}')
	bucket.delete()
	logger.info(f"Successfully Deleted Bucket: {bucket_name}")

if __name__ == "__main__":
	args = parse_args()
	session = create_session(args['profile'])
	delete_bucket(session=session, bucket_name=args['bucket_name'])
