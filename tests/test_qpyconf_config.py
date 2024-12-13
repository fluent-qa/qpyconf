import allure

import qpyconf
from qpyconf.config import settings

# @allure.title("Test Authentication")
# @allure.description("This test attempts to log into the website using a login and a password. Fails if any error happens.\n\nNote that this test does not test 2-Factor Authentication.")
# @allure.tag("NewUI", "Essentials", "Authentication")
# @allure.severity(allure.severity_level.CRITICAL)
# @allure.label("owner", "John Doe")
# @allure.link("https://dev.example.com/", name="Website")
# @allure.issue("AUTH-123")
# @allure.testcase("TMS-456")
# import allure

# def test_authentication():
#     allure.dynamic.title("Test Authentication")
#     allure.dynamic.description("This test attempts to log into the website using a login and a password. Fails if any error happens.\n\nNote that this test does not test 2-Factor Authentication.")
#     allure.dynamic.tag("NewUI", "Essentials", "Authentication")
#     allure.dynamic.severity(allure.severity_level.CRITICAL)
#     allure.dynamic.label("owner", "John Doe")
#     allure.dynamic.link("https://dev.example.com/", name="Website")
#     allure.dynamic.issue("AUTH-123")
#     allure.dynamic.testcase("TMS-456")
#     ...


@allure.title('test simple kv setting')
@allure.tag('basic function')
def test_simple_kv():
    assert settings.key == 'value'


@allure.title('test nested kv setting for dict object')
@allure.tag('basic function')
def test_nested_settings():
    assert isinstance(settings.databases, dict)


@allure.title('test nested kv setting for string object')
@allure.tag('basic function')
def test_nested_kv():
    assert settings.databases.default.url == 'postgresql+psycopg://postgres:changeit@127.0.0.1:5432/workspace'


@allure.title('test switch env_name variable in runtime')
@allure.tag('dynamic function')
def test_switch_env_variables():
    qpyconf.ensure_env_settings(env_name='test')
    assert (
        qpyconf.settings.databases.default.url
        == 'postgresql+psycopg_async://postgres:changeit@127.0.0.1:5432/workspace'
    )


@allure.title('test after swith env_name the setting changes')
@allure.tag('dynamic function')
def test_env_settings():
    print(settings.env_example)
    assert settings.env_example == 'ENV_EXAMPLE'


## test settings to nested model
