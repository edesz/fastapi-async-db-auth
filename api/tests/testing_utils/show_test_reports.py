#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Utility function to display test report."""


import argparse
import logging
import subprocess
from pathlib import Path
from shutil import get_terminal_size


def show_test_outputs(show_cov_html=True):
    """Show test code coverage annotated in files."""
    term_dims = get_terminal_size((80, 20))
    n_dashes, n_rem = divmod(term_dims[0], 2)
    smsg = ""  # type: str
    file_print_divider = smsg.join(
        ["=" * (n_dashes + int(n_rem / 2))] * 2
    )  # type: str

    PROJECT_DIR = Path(__file__).parents[1]  # type: Path

    with open(PROJECT_DIR / "test-logs" / "report.md") as f:
        print(f"{f.read()}{file_print_divider}")

    logger = logging.getLogger(__name__)
    logger.info(f"Lauch Coverage HTML in browser = {show_cov_html}")

    if show_cov_html:
        html_file_path = PROJECT_DIR / "test-logs" / "htmlcov" / "index.html"
        _ = subprocess.Popen(["xdg-open", str(html_file_path)])


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--show-cov-html",
        type=str2bool,
        nargs="?",
        const=True,
        dest="show_cov_html",
        default=True,
        help="whether to open Coverage HTML report in browser",
    )
    args = parser.parse_args()
    show_test_outputs(show_cov_html=args.show_cov_html)
