import os
from typing import Optional

from .environment_variable_not_found_error import EnvironmentVariableNotFoundError


def demand_env_var(name: str) -> str:
    if name not in os.environ:
        raise EnvironmentVariableNotFoundError(f"Environment variable ({name}) not found")
    return os.environ[name]


def get_env_var(name: str) -> Optional[str]:
    if name not in os.environ:
        return None
    return os.environ[name]


def demand_env_var_as_int(name: str) -> int:
    return int(demand_env_var(name=name))


def demand_env_var_as_float(name: str) -> float:
    return float(demand_env_var(name=name))


def demand_env_var_as_bool(name: str) -> float:
    return bool(demand_env_var(name=name))
