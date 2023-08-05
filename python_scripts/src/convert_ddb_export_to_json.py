#! /usr/bin/env python3

import json
import argparse
from threading import Thread
from dynamodb_json import json_util
from glob import glob
import logging
from typing import Optional, List, Iterable

DEFAULT_THREADS = 8

logger = logging.getLogger(__name__)


"""
A CLI for converting DDB exports to something usable into pandas. DDB exports will be a set
of json files with type information. Pointing this CLI at that set of files will process all records
and convert them into a single json file

convert_ddb_export_to_json.py --files ./EndpointData/*.json --output Endpoints.json
"""


def parse_args(
    argv: Optional[List[str]] = None,
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="A CLI tool for processing DDB exports"
    )
    parser.add_argument("--files", required=True, type=str)
    parser.add_argument("--output", required=True, type=str)
    parser.add_argument("--threads", required=False, default=DEFAULT_THREADS, type=int)
    return parser.parse_args(argv)


def split(a: Iterable, n: int) -> List[List]:
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n))


def process_file(files: List[str], records, thread_no: int):
    for file in files:
        with open(file, 'r') as fh:
            for i, line in enumerate(fh.readlines()):
                if line == "":
                    continue

                if i % 10000 == 0:
                    print(f"Thread {thread_no} has processed {i} records in {file}")

                try:
                    item = json_util.loads(line)["Item"]
                    records.append(item)
                except Exception as e:
                    logger.exception("Error processing record")


def write_output(records, path):
    with open(path, "w") as fh:
        json.dump(records, fh, indent=4)


def main(argv: Optional[List[str]] = None):
    args = parse_args(argv)
    records = []

    threads = []

    files = glob(args.files)

    for i, lst in enumerate(split(files, args.threads)):
        thread = Thread(target=process_file, args=(lst, records, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    with open(args.output, "w") as fh:
        json.dump(records, fh, indent=4)


if __name__ == "__main__":
    main()
