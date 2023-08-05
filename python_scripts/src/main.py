from . import convert_ddb_export_to_json
from . import cp_to_s3
from . import delete_bucket
from . import get_s3_object_w_url

import logging
import contextlib
import sys
import argparse
from typing import List, Iterator, Optional

logger = logging.getLogger(__name__)

scripts = {
    "cp_to_s3": cp_to_s3.main,
    "delete_bucket": delete_bucket.main,
    "convert_ddb_export_to_json": convert_ddb_export_to_json.main,
    "get_s3_object_w_url": get_s3_object_w_url.main
}


@contextlib.contextmanager
def replace_sys_argv(argv: List[str]) -> Iterator[None]:
    """
    Context manager for replacing the contents of `sys.argv` and restoring them on exit.
    Not thread safe.
    """

    original_argv = sys.argv.copy()
    # use a slice to ensure we reuse the original list object
    sys.argv[:] = argv
    try:
        yield
    finally:
        sys.argv[:] = original_argv


def configure_logger(log_level: int, root_logger: logging.Logger = logging.getLogger()):
    """
    Sets up logging with a single handler which emits logs to stderr.
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] (main) %(name)s:%(lineno)s  %(message)s",
        "%Y-%m-%dT%H:%M:%S",
    )
    stream_handler.setFormatter(formatter)

    root_logger.setLevel(log_level)
    root_logger.handlers = [stream_handler]


def main(argv: Optional[List[str]] = None) -> None:
    """
    Main entry point for Denominator code. Runs other modules after configuring
    logging and any other undifferentiated initialization tasks.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("script", choices=scripts.keys())
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
    )

    args, remaining_args = parser.parse_known_args(argv)
    script_name = args.script

    configure_logger(log_level=logging.DEBUG if args.verbose else logging.INFO)

    match script_name:
        case "cp_to_s3":
            cp_to_s3.main(remaining_args)
            return
        case "delete_bucket":
            delete_bucket.main(remaining_args)
            return
        case "convert_ddb_export_to_json":
            convert_ddb_export_to_json.main(remaining_args)
            return
        case "get_s3_object_w_url":
            get_s3_object_w_url.main(remaining_args)
            return
        case _:
            logger.info(f"Unknown script '{script_name}'")


if __name__ == "__main__":
    main()
