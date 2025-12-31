import os

from dynaconf import Dynaconf
from pydantic import BaseModel

settings = Dynaconf(
    settings_file=[
        "configs/settings.toml",
        "configs/.secrets.toml",
        "settings.toml",
        ".secrets.toml",
    ],
    environment=True,
    load_dotenv=True,
    envvar_prefix=False,
    includes=["../config/custom_settings.toml"],
)

settings.validators.validate()


def ensure_env_settings(env_name: str, conf: Dynaconf = settings):
    env_switcher_key = conf.ENV_SWITCHER_FOR_DYNACONF
    os.environ[env_switcher_key] = env_name
    conf.reload()


def setting_to_model(setting: Dynaconf, model_type: type[BaseModel]):
    data = {field_name: getattr(setting, field_name) for field_name in model_type.model_fields}
    return model_type.model_validate(data)
