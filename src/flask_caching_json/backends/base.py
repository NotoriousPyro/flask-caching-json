"""
    flask_caching_json.backends.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains the BaseCache that other caching
    backends have to implement.

    :copyright: (c) 2018 by Peter Justin.
    :copyright: (c) 2010 by Thadeus Burgess.
    :license: BSD, see LICENSE for more details.
"""
import warnings

from cachelib import BaseCache as CachelibBaseCache

from flask_caching_json.serialization import json
from flask_caching_json.serialization import pickle
from flask_caching_json.serialization import PickleError


def iteritems_wrapper(mappingorseq):
    """Wrapper for efficient iteration over mappings represented by dicts
    or sequences::

        >>> for k, v in iteritems_wrapper((i, i*i) for i in xrange(5)):
        ...    assert k*k == v

        >>> for k, v in iteritems_wrapper(dict((i, i*i) for i in xrange(5))):
        ...    assert k*k == v

    """
    if hasattr(mappingorseq, "items"):
        return mappingorseq.items()
    return mappingorseq


def extract_serializer_args(data):
    result = dict()
    serializer_prefix = "serializer_"
    for key in tuple(data.keys()):
        if key.startswith(serializer_prefix):
            result[key] = data.pop(key)
    return result


class BaseCache(CachelibBaseCache):
    """Baseclass for the cache systems.  All the cache systems implement this
    API or a superset of it.

    :param default_timeout: The default timeout (in seconds) that is used if
                            no timeout is specified on :meth:`set`. A timeout
                            of 0 indicates that the cache never expires.
    :param serializer_impl: Pickle-like serialization implementation. It should
                            support load(-s) and dump(-s) methods and binary
                            strings/files.
    :param serializer_error: Deserialization exception - for specified
                             implementation.
    """

    def __init__(
        self, default_timeout=300, serializer_impl=json, serializer_error=PickleError
    ):
        CachelibBaseCache.__init__(self, default_timeout=default_timeout)

        self.default_timeout = default_timeout
        self.ignore_errors = False

        if serializer_impl is pickle:
            warnings.warn(
                "Pickle serializer is not secure and may "
                "lead to remote code execution. "
                "Consider using another serializer (eg. JSON)."
            )
        self._serializer = serializer_impl
        self._serialization_error = serializer_error

    @classmethod
    def factory(cls, app, config, args, kwargs):
        return cls()

    def delete_many(self, *keys):
        """Deletes multiple keys at once.

        :param keys: The function accepts multiple keys as positional
                        arguments.
        :returns: A list containing all sucessfuly deleted keys
        :rtype: boolean
        """
        deleted_keys = []
        for key in keys:
            if self.delete(key):
                deleted_keys.append(key)
            else:
                if not self.ignore_errors:
                    break
        return deleted_keys
