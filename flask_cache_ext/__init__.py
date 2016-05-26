# -*- coding: utf-8 -*-
import functools
import inspect

from flask_cache import Cache as _Cache
from flask_cache import null_control
from flask_cache._compat import PY2

if PY2:
    str = unicode  # noqa


def function_namespace(f, args=None):
    """
    Attempts to returns unique namespace for function
    """
    m_args = inspect.getargspec(f)[0]
    instance_token = None

    instance_self = getattr(f, '__self__', None)

    if instance_self \
    and not inspect.isclass(instance_self):
        instance_token = repr(f.__self__)
    elif m_args \
    and m_args[0] == 'self' \
    and args:
        instance_token = repr(args[0])

    module = f.__module__

    if hasattr(f, '__qualname__'):
        name = f.__qualname__
    else:
        klass = getattr(f, '__self__', None)

        if klass \
        and not inspect.isclass(klass):
            klass = klass.__class__

        if not klass:
            klass = getattr(f, 'im_class', None)

        if not klass:
            if m_args and args:
                if m_args[0] == 'self':
                    klass = args[0].__class__
                elif m_args[0] == 'cls':
                    klass = args[0]

        if klass:
            name = klass.__name__ + '.' + f.__name__
        else:
            name = f.__name__
            pritn('@' * 20, name)

    ns = '.'.join((module, name))
    ns = ns.translate(*null_control)

    if instance_token:
        # ins = '.'.join((module, name, instance_token))
        ins = '.'.join((module, instance_token))
        print('ins', ins)
    else:
        ins = None

    return ns, ins


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

    
    def _memoize_version(self, f, args=None,
                         reset=False, delete=False, timeout=None):
        """
        Updates the hash version associated with a memoized function or method.
        """
        fname, instance_fname = function_namespace(f, args=args)
        version_key = self._memvname(fname)
        fetch_keys = [version_key]

        if instance_fname:
            instance_version_key = self._memvname(instance_fname)
            fetch_keys.append(instance_version_key)

        # Only delete the per-instance version key or per-function version
        # key but not both.
        if delete:
            self.cache.delete_many(fetch_keys[-1])
            return fname, None

        version_data_list = list(self.cache.get_many(*fetch_keys))
        dirty = False

        if version_data_list[0] is None:
            version_data_list[0] = self._memoize_make_version_hash()
            dirty = True

        if instance_fname and version_data_list[1] is None:
            version_data_list[1] = self._memoize_make_version_hash()
            dirty = True

        # Only reset the per-instance version or the per-function version
        # but not both.
        if reset:
            fetch_keys = fetch_keys[-1:]
            version_data_list = [self._memoize_make_version_hash()]
            dirty = True

        if dirty:
            self.cache.set_many(dict(zip(fetch_keys, version_data_list)),
                                timeout=timeout)

        return fname, ''.join(version_data_list)
