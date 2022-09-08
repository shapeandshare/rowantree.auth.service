""" Helper functions for environment variables. """

import os
from typing import Optional

from .environment_variable_not_found_error import EnvironmentVariableNotFoundError


def demand_env_var(name: str) -> str:
    """
    Returns an environment variable as a string, or throws an exception.

    Parameters
    ----------
    name: str
        The name of the environment variable.

    Returns
    -------
    variable_value: str
        The environment variables value as a string.
    """

    if name not in os.environ:
        raise EnvironmentVariableNotFoundError(f"Environment variable ({name}) not found")
    return os.environ[name]


def get_env_var(name: str) -> Optional[str]:
    """
    Returns an environment variable as a string, otherwise `None` if it does not exist.

    Parameters
    ----------
    name: str
        The name of the environment variable.

    Returns
    -------
    variable_value: Optional[str]
        The environment variables value as a string, or `None` if it does not exist.
    """

    if name not in os.environ:
        return None
    return os.environ[name]


def demand_env_var_as_int(name: str) -> int:
    """
    Returns an environment variable as an int, or throws an exception.

    Parameters
    ----------
    name: str
        The name of the environment variable.

    Returns
    -------
    variable_value: int
        The environment variables value as an int.
    """

    return int(demand_env_var(name=name))


def demand_env_var_as_float(name: str) -> float:
    """
    Returns an environment variable as a float, or throws an exception.

    Parameters
    ----------
    name: str
        The name of the environment variable.

    Returns
    -------
    variable_value: float
        The environment variables value as a float.
    """

    return float(demand_env_var(name=name))


def demand_env_var_as_bool(name: str) -> bool:
    """
    Returns an environment variable as a bool, or throws an exception.

    Parameters
    ----------
    name: str
        The name of the environment variable.

    Returns
    -------
    variable_value: bool
        The environment variables value as a bool.
    """

    return bool(demand_env_var(name=name))
