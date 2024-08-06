from qpyconf.config import settings
import qpyconf


def test_simple_kv():
    assert settings.key == "value"

def test_nested_settings():
    assert isinstance(settings.databases,dict)

def test_nested_kv():
    assert settings.databases.default.url == "postgresql+psycopg://postgres:changeit@127.0.0.1:5432/workspace"


def test_switch_env_variables():
    qpyconf.ensure_env_settings(env_name="test")
    assert qpyconf.settings.databases.default.url == "postgresql+psycopg_async://postgres:changeit@127.0.0.1:5432/workspace"

def test_env_settings():
    print(settings.env_example)
    assert settings.env_example=="ENV_EXAMPLE"

## test settings to nested model 