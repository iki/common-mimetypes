#!/usr/bin/env python
"""
common-mimetypes
================

Common MIME types not available in standard library mimetypes module

Package:
  http://pypi.python.org/pypi/common-mimetypes
Project:
  https://github.com/iki/common-mimetypes
Issues:
  https://github.com/iki/common-mimetypes/issues
Updates:
  https://github.com/iki/common-mimetypes/commits/master.atom
Install via `pip <http://www.pip-installer.org>`_:
  ``pip install common-mimetypes``
Install via `easy_install <http://peak.telecommunity.com/DevCenter/EasyInstall>`_:
  ``easy_install common-mimetypes``
Sources via `git <http://git-scm.com/>`_:
  ``git clone https://github.com/iki/common-mimetypes``
Sources via `hg-git <https://github.com/schacon/hg-git>`_:
  ``hg clone git://github.com/iki/common-mimetypes``
"""
__docformat__ = 'restructuredtext en'
__version__ = '0.1rc1'
__all__ = 'COMMON_MIMETYPES add test require'.split()

import mimetypes

COMMON_MIMETYPES = dict(
    ttf  = 'font/ttf',
    otf  = 'font/otf',
    woff = 'font/x-woff',
    eot  = 'application/vnd.ms-fontobject',
    ico  = 'image/x-icon',
    jng  = 'image/x-jng',
    svg  = 'image/svg+xml',
    svgz = 'image/svg+xml',
    webp = 'image/webp',
    oga  = 'audio/ogg',
    ogg  = 'audio/ogg',
    ogv  = 'video/ogg',
    m4v  = 'video/m4v',
    webm = 'video/webm',
    rss  = 'text/xml',
    atom = 'application/atom+xml',
    yaml = 'text/yaml',
    json = 'application/json',
    bson = 'application/bson',
    htc  = 'text/x-component',
    xpi  = 'application/x-xpinstall',
    oex  = 'application/x-opera-extension',
    crx  = 'application/x-chrome-extension',
    safariextz = 'application/octet-stream',
    unity3d = 'application/vnd.unity',
    appcache = 'text/cache-manifest',
    manifest = 'text/cache-manifest',
    )

def add(types=None, strict=True, **kwtypes):
    """Adds multiple mappings between standard types and extensions.

    Expects {ext: mimetype} dictionary as a first positional argument,
    or in keyword arguments, or both.

    If no types dictionary or keyword types are specified,
    COMMON_MIMETYPES are used.

    When the extension is already known, the new type will replace
    the old one. When the type is already known, the extension
    will be added to the list of known extensions.

    If strict is true, information will be added to list of standard types,
    else to the list of non-standard types.

    If mimetypes._db is not initialized yet, then mimetypes.types_map (strict),
    or mimetypes.common_types (not strict) are updated,
    instead of calling mimetypes.init() as in original mimetypes.add_type().

    If ext is not starting with '.' (e.g. in keyword argument type),
    the dot is prepended.

    >>> add()
    >>> require()
    """
    if kwtypes:
        types = types and dict(types, **kwtypes) or kwtypes
    elif types is None:
        types = COMMON_MIMETYPES

    if mimetypes._db is None:
        # Mimetypes database is not initialized yet.
        typemap = mimetypes.types_map if strict else mimetypes.common_types
        typemap.update((ext.startswith('.') and ext or '.%s' % ext, types[ext])
            for ext in types)

    else:
        # Mimetypes database is already initialized.
        add_type = mimetypes._db.add_type
        for ext in types:
            add_type(types[ext], ext.startswith('.') and ext or '.%s' % ext, strict)

def test(types=None, strict=True, **kwtypes):
    """Tests if mappings between standard types and extensions are defined.

    Returns True, or dictionary of undefined types.

    If no types dictionary or keyword types are specified,
    COMMON_MIMETYPES are used.

    If strict is true, the types will be checked against list of standard types,
    else agains the list of non-standard types.
    """
    if kwtypes:
        types = types and dict(types, **kwtypes) or kwtypes
    elif types is None:
        types = COMMON_MIMETYPES

    types = dict(('.%s' % ext, types[ext]) for ext in types)
    predef = strict and mimetypes.types_map or mimetypes.common_types
    missing = [ ext for ext in types if ext not in predef ]

    return missing or True

def require(types=None, strict=True, **kwtypes):
    """Tests if mappings between standard types and extensions are defined.

    Raises RuntimeError if any types are undefined.

    If no types dictionary or keyword types are specified,
    COMMON_MIMETYPES are used.

    If strict is true, the types will be checked against list of standard types,
    else agains the list of non-standard types.
    """
    if kwtypes:
        types = types and dict(types, **kwtypes) or kwtypes

    missing = test(types, strict)

    if missing is not True:
        raise RuntimeError((
            "Common MIME types are not enabled.\n"
            "You can work around by updating module '%s'\n"
            "with the following lines after '_default_mime_types()' line:\n\n%s"
            ) % (mimetypes.__file__, '\n'.join("%s['%s'] = '%s'" % (
                strict and 'types_map' or 'common_types', ext, common[ext])
                for ext in sorted(missing))
                ))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
