# fluentqa-conf
![ci](https://github.com/fluent-qa/qpyconf/actions/workflows/ci.yml/badge.svg?event=push&branch=main)
![coverage](coverage.svg)

configuration support both:
1. .env file
2. settings.toml file

## 1. How to Use

### 1.1 Settings in Settings.xml

```yaml
[default]
key = "value"
databases = { default = { url = "postgresql+psycopg://postgres:changeit@127.0.0.1:5432/workspace" } }
pg_url = "postgresql+psycopg://postgres:changeit@127.0.0.1:5432/workspace"
pg_a_url = "postgresql+psycopg_async://postgres:changeit@127.0.0.1:5432/workspace"

[test]
key = "abc"
databases.default.url = "postgresql+psycopg_async://postgres:changeit@127.0.0.1:5432/workspace"
```

### 1.2 Getting Key Value

```python
def test_simple_kv():
    assert settings.key == "value"
```

### 1.3 Getting Nested Value or Structured value

```python
def test_nested_settings():
    assert isinstance(settings.databases,dict)
```

### 1.4 Switch Environment

1. swith environment to test
2. the database default url is changed to test environment, not default value anymore

```python
def test_switch_env_variables():
    qpyconf.ensure_env_settings(env_name="test")
    assert qpyconf.settings.databases.default.url == "postgresql+psycopg_async://postgres:changeit@127.0.0.1:5432/workspace"

```

### 1.5. getting value from .env file

- env file
```sh
ENV_EXAMPLE='ENV_EXAMPLE'
```
- Get this value

```python
def test_env_settings():
    print(settings.env_example)
    assert settings.env_example=="ENV_EXAMPLE"
```
