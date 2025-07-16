from __future__ import annotations

import logging
import os

import click
import yaml
from arango import ArangoClient
from arango.database import StandardDatabase

from scripts.paths import CONFIG_DIR

log = logging.getLogger(__name__)


def load_yaml(file, key=None):
    """Loads and parses a YAML file from the CONFIG_DIR.

    Args:
        file (str): The base filename (without extension) of the YAML file to load.
        key (str, optional): Returns only this top-level key from the YAML data.

    Returns:
        dict | Any: Parsed YAML contents, or the sub-dictionary at `key` if specified.
    """
    try:
        path = CONFIG_DIR / f"{file}.yaml"
        with open(path, "r") as f:
            if key:
                return yaml.safe_load(f)[key]
            else:
                return yaml.safe_load(f)
    except Exception as e:
        log.error(f"Error loading {file}: {e}")


def get_arango_client() -> ArangoClient:
    """Initializes and returns an ArangoClient using the ARANGO_HOST env variable.

    Returns:
        ArangoClient: An instance configured to connect to the target host.
    """
    host = os.getenv("ARANGO_HOST")
    return ArangoClient(hosts=host)


def get_system_db() -> StandardDatabase:
    """Returns a handle to the _system database.

    Uses ARANGO_USERNAME and ARANGO_PASSWORD environment variables.
    Useful for administrative tasks like creating or deleting databases.

    Returns:
        StandardDatabase: Authenticated connection to the _system database.
    """
    client = get_arango_client()
    username = os.getenv("ARANGO_USERNAME", "root")
    password = os.getenv("ARANGO_PASSWORD")
    return client.db("_system", username=username, password=password)


def get_arango_db() -> StandardDatabase:
    """Returns a handle to the target ArangoDB database specified in ARANGO_DB.

    This function assumes the database already exists. It does not create or delete databases.

    Returns:
        StandardDatabase: Authenticated connection to the target database.
    """
    client = get_arango_client()
    username = os.getenv("ARANGO_USERNAME", "root")
    password = os.getenv("ARANGO_PASSWORD")
    db_name = os.getenv("ARANGO_DB")
    return client.db(db_name, username=username, password=password)


def confirm_with_timeout(prompt: str, timeout: int = 15, default: bool = True) -> bool:
    """Prompt the user for yes/no input, timing out after `timeout` seconds.

    If the user provides no input within the allotted time, the default value is returned.

    Note:
        Only works on Unix-like systems (e.g. Linux/macOS). Will not work on Windows.

    Args:
        prompt (str): The confirmation message to display.
        timeout (int): Seconds to wait before falling back to the default.
        default (bool): Value to return if the prompt times out.

    Returns:
        bool: True for 'yes', False for 'no', or `default` if time expires.
    """
    import signal

    class TimeoutExpired(Exception):
        pass

    def _timeout_handler(signum, frame):
        raise TimeoutExpired()

    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout)
    try:
        return click.confirm(prompt, default=default)
    except TimeoutExpired:
        click.echo(
            f"\nNo response in {timeout}s — defaulting to {'Yes' if default else 'No'}."
        )
        return default
    finally:
        signal.alarm(0)
