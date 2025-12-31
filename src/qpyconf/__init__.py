"""
Simple Configuration for Python
"""

__version__ = "0.0.1"


__all__ = ["__version__", "settings", "setting_to_model", "ensure_env_settings"]

from qpyconf.config import settings, setting_to_model, ensure_env_settings
