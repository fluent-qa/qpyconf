# qpyconf
![ci](https://github.com/fluent-qa/qpyconf/actions/workflows/ci.yml/badge.svg?event=push&branch=main)
![coverage](coverage.svg)

`qpyconf` is a small configuration helper built on top of:
- `dynaconf` for loading and layering settings from files + environment variables
- `pydantic` for validating and converting settings into typed models

It supports:
- `.env` files (via Dynaconf `load_dotenv`)
- `settings.toml` (and other Dynaconf-supported formats like JSON/YAML/INI)
- Dynaconf environments (e.g. `[default]`, `[test]`) with runtime switching

Docs:
- [Installation](docs/installation.md)
- [Usage](docs/usage.md)

## Install

```sh
uv add qpyconf
```

```sh
pip install qpyconf
```

## Quickstart

Create a `settings.toml`:

```toml
[default]
key = "value"
databases = { default = { url = "postgresql+psycopg://postgres:changeit@127.0.0.1:5432/workspace" } }
pg_url = "postgresql+psycopg://postgres:changeit@127.0.0.1:5432/workspace"
pg_a_url = "postgresql+psycopg_async://postgres:changeit@127.0.0.1:5432/workspace"

[test]
key = "abc"
databases.default.url = "postgresql+psycopg_async://postgres:changeit@127.0.0.1:5432/workspace"
```

Read settings:

```python
from qpyconf import settings

assert settings.key == "value"
```

More examples:
- [docs/usage.md](docs/usage.md)

## Development

```sh
uv sync
uv run ci
```
