#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Utility function to display test report."""


import argparse
import logging
import webbrowser
from pathlib import Path
from shutil import get_terminal_size


def show_test_outputs(show_htmls=True):
    """Show test summary report and code coverage annotated in files."""
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
    logger.info(f"Lauch HTMLs in browser = {show_htmls}")

    if show_htmls:
        test_logs_dir = PROJECT_DIR / "test-logs"
        cov_html_file_path = test_logs_dir / "htmlcov" / "index.html"
        summary_html_file_path = test_logs_dir / "testreport.html"
        for f in [summary_html_file_path, cov_html_file_path]:
            webbrowser.open_new_tab(str(f))


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
        "--show-htmls",
        type=str2bool,
        nargs="?",
        const=True,
        dest="show_htmls",
        default=True,
        help="whether to open Test summary, Coverage HTML reports in browser",
    )
    args = parser.parse_args()
    show_test_outputs(args.show_htmls)
