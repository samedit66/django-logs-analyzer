from argparse import ArgumentParser
from pathlib import Path
from typing import Iterable

from django_logs_analyzer.reports import handlers_report


def argument_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Analyze Django logs.")
    parser.add_argument(
        "files",
        nargs="+",
        type=str,
        help="Log files to analyze.",
    )
    parser.add_argument(
        "-r",
        "--report",
        type=str,
        default="handlers",
        choices=["handlers"],
        help="Type of report.",
    )
    return parser


def find_nonexistent_files(files: list[str]) -> Iterable[str]:
    return [file for file in files if not Path(file).exists()]


if __name__ == "__main__":
    parser = argument_parser()
    args = parser.parse_args()

    if files := find_nonexistent_files(args.files):
        parser.error(f"File(s) not found: {', '.join(files)}")
    
    match args.report:
        case "handlers":
            print(handlers_report(args.files))
