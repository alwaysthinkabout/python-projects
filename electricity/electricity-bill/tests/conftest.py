# -*- coding: utf-8 -*-

import pytest

from app import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def client(app):
    """
    用于测试app的客户端模拟.
    """
    return app.test_client()
