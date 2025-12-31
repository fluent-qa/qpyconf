# Usage

## Quickstart (TOML)

Create a `settings.toml` next to your project:

```toml
[default]
key = "value"
databases = { default = { url = "postgresql+psycopg://postgres:changeit@127.0.0.1:5432/workspace" } }

[test]
key = "abc"
databases.default.url = "postgresql+psycopg_async://postgres:changeit@127.0.0.1:5432/workspace"
```

Read settings:

```python
from qpyconf import settings

assert settings.key == "value"
```

Read nested/structured values:

```python
from qpyconf import settings

assert settings.databases.default.url.startswith("postgresql")
```

## `.env` support

Create a `.env` file:

```sh
ENV_EXAMPLE='ENV_EXAMPLE'
```

Read it:

```python
from qpyconf import settings

assert settings.env_example == "ENV_EXAMPLE"
```

## Switch Dynaconf environment at runtime

```python
import qpyconf

qpyconf.ensure_env_settings(env_name="test")
assert qpyconf.settings.key == "abc"
```

## Convert settings into Pydantic models

`setting_to_model()` converts the current Dynaconf view into a Pydantic model (including nested models).

```python
from pydantic import BaseModel

import qpyconf


class DatabaseConfig(BaseModel):
    url: str


class DatabasesConfig(BaseModel):
    default: DatabaseConfig


class AppConfig(BaseModel):
    key: str
    databases: DatabasesConfig


model = qpyconf.setting_to_model(qpyconf.settings, AppConfig)
assert model.key == "value"
```

## Layered settings (advanced)

Later files override earlier files. Environment variables override files.

```python
from dynaconf import Dynaconf
from pydantic import BaseModel

import qpyconf


class AppConfig(BaseModel):
    key: str


conf = Dynaconf(
    settings_file=["base.json", "override.toml"],
    environment=True,
    load_dotenv=False,
    envvar_prefix="QPYCONF",
)

qpyconf.ensure_env_settings(env_name="default", conf=conf)
model = qpyconf.setting_to_model(conf, AppConfig)
```
