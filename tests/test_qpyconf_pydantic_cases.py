import json
from pathlib import Path

import allure
import pytest
from dynaconf import Dynaconf
from pydantic import BaseModel

import qpyconf


class DatabaseConfig(BaseModel):
    url: str


class DatabasesConfig(BaseModel):
    default: DatabaseConfig


class AppConfig(BaseModel):
    key: str
    databases: DatabasesConfig


def make_settings(settings_files: list[Path], *, enable_environments: bool) -> Dynaconf:
    return Dynaconf(
        settings_file=[str(p) for p in settings_files],
        environment=enable_environments,
        load_dotenv=False,
        envvar_prefix="QPYCONF",
    )


@allure.title("convert TOML settings into nested pydantic model")
@allure.tag("pydantic", "formats")
def test_setting_to_model_from_toml(tmp_path: Path):
    settings_toml = tmp_path / "settings.toml"
    settings_toml.write_text(
        "\n".join(
            [
                "[default]",
                'key = "value"',
                'databases = { default = { url = "postgresql://localhost:5432/app" } }',
                "",
            ]
        ),
        encoding="utf-8",
    )

    conf = make_settings([settings_toml], enable_environments=True)
    model = qpyconf.setting_to_model(conf, AppConfig)

    assert model.key == "value"
    assert model.databases.default.url == "postgresql://localhost:5432/app"


@allure.title("convert JSON settings into nested pydantic model")
@allure.tag("pydantic", "formats")
def test_setting_to_model_from_json(tmp_path: Path):
    settings_json = tmp_path / "settings.json"
    settings_json.write_text(
        json.dumps(
            {
                "default": {
                    "key": "value",
                    "databases": {"default": {"url": "postgresql://localhost:5432/app"}},
                }
            }
        ),
        encoding="utf-8",
    )

    conf = make_settings([settings_json], enable_environments=True)
    model = qpyconf.setting_to_model(conf, AppConfig)

    assert model.key == "value"
    assert model.databases.default.url == "postgresql://localhost:5432/app"


@allure.title("layer settings from multiple files (later wins)")
@allure.tag("layering")
def test_layered_settings_files_override(tmp_path: Path):
    base_json = tmp_path / "base.json"
    base_json.write_text(
        json.dumps({"key": "base", "databases": {"default": {"url": "postgresql://base"}}}),
        encoding="utf-8",
    )

    override_toml = tmp_path / "override.toml"
    override_toml.write_text(
        "\n".join(
            [
                'key = "override"',
                'databases = { default = { url = "postgresql://override" } }',
                "",
            ]
        ),
        encoding="utf-8",
    )

    conf = make_settings([base_json, override_toml], enable_environments=False)

    assert conf.key == "override"
    assert conf.databases.default.url == "postgresql://override"


@allure.title("layer settings: environment variables override files")
@allure.tag("layering")
def test_layered_settings_env_overrides_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    base_toml = tmp_path / "base.toml"
    base_toml.write_text(
        "\n".join(
            [
                'key = "file-value"',
                'databases = { default = { url = "postgresql://file" } }',
                "",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("QPYCONF_KEY", "env-value")

    conf = make_settings([base_toml], enable_environments=False)

    assert conf.key == "env-value"


@allure.title("layer settings: switch dynaconf environment at runtime")
@allure.tag("layering", "dynamic")
def test_switch_env_settings_affects_pydantic_model(tmp_path: Path):
    settings_toml = tmp_path / "settings.toml"
    settings_toml.write_text(
        "\n".join(
            [
                "[default]",
                'key = "default-value"',
                'databases = { default = { url = "postgresql://default" } }',
                "",
                "[test]",
                'key = "test-value"',
                'databases = { default = { url = "postgresql://test" } }',
                "",
            ]
        ),
        encoding="utf-8",
    )

    conf = make_settings([settings_toml], enable_environments=True)
    qpyconf.ensure_env_settings(env_name="default", conf=conf)
    default_model = qpyconf.setting_to_model(conf, AppConfig)
    assert default_model.key == "default-value"

    qpyconf.ensure_env_settings(env_name="test", conf=conf)
    test_model = qpyconf.setting_to_model(conf, AppConfig)

    assert test_model.key == "test-value"
    assert test_model.databases.default.url == "postgresql://test"
