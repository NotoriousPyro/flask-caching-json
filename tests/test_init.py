import pytest
from flask import Flask

from flask_caching_json import Cache
from flask_caching_json.backends import FileSystemCache
from flask_caching_json.backends import MemcachedCache
from flask_caching_json.backends import NullCache
from flask_caching_json.backends import RedisCache
from flask_caching_json.backends import RedisSentinelCache
from flask_caching_json.backends import SASLMemcachedCache
from flask_caching_json.backends import SimpleCache
from flask_caching_json.backends import SpreadSASLMemcachedCache


@pytest.fixture
def app():
    app_ = Flask(__name__)

    return app_


@pytest.mark.parametrize(
    "cache_type",
    (
        FileSystemCache,
        MemcachedCache,
        NullCache,
        RedisCache,
        RedisSentinelCache,
        SASLMemcachedCache,
        SimpleCache,
        SpreadSASLMemcachedCache,
    ),
)
def test_init_nullcache(cache_type, app, tmp_path):
    extra_config = {
        FileSystemCache: {
            "CACHE_DIR": tmp_path,
        },
        SASLMemcachedCache: {
            "CACHE_MEMCACHED_USERNAME": "test",
            "CACHE_MEMCACHED_PASSWORD": "test",
        },
    }
    app.config["CACHE_TYPE"] = "flask_caching_json.backends." + cache_type.__name__
    app.config.update(extra_config.get(cache_type, {}))
    cache = Cache(app=app)

    assert isinstance(app.extensions["cache"][cache], cache_type)
