import warnings

from flask_caching_json.contrib.uwsgicache import UWSGICache as _UWSGICache


class UWSGICache(_UWSGICache):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "Importing UWSGICache from flask_caching_json.backends is deprecated, "
            "use flask_caching_json.contrib.uwsgicache.UWSGICache instead",
            category=DeprecationWarning,
        )

        super().__init__(*args, **kwargs)
