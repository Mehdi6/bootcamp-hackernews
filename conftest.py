import pytest


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
# import pytest
#
#
# @pytest.fixture(scope='session', autouse=True)
# def disable_django_debug_toolbar():
#     """ Disable Django Debug Toolbar error caused by overriding this config """
#     from django.conf import settings
#     #del settings.DEBUG_TOOLBAR_CONFIG["SHOW_TOOLBAR_CALLBACK"]