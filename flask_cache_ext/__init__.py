# -*- coding: utf-8 -*-
import functools

from flask_cache import Cache as _Cache
from flask_cache._compat import PY2

if PY2:
    str = unicode  # noqa


class Cache(_Cache):

    def _memoize_kwargs_to_args(self, f, *args, **kwargs):
        """重写父类方法, 所有参数都转为字符串,
        例如下面的参数, 实际使用中我们期望得到一样的key
        func.make_cache_key(1)
        func.make_cache_key(1L)
        func.make_cache_key('1')
        func.make_cache_key(u'1')
        """
        keyargs, keykwargs = super(Cache, self) \
            ._memoize_kwargs_to_args(f, *args, **kwargs)

        new_args = tuple(map(str, keyargs))

        return new_args, keykwargs
