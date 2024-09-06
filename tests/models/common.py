"""common functions used across test modules"""

import os


def data_dir() -> str:
    """common function to format location of test folder"""
    # return the test data directory from the current root
    cwd = os.getcwd().replace("\\", "/")
    root = cwd.split("/tests")[0]
    path = root + "/tests/data/"
    return path
