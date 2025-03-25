import os
from importlib.metadata import version


major: int = 0
minor: int = 1
patch: int = 0
devtag: str = ""

__version__ = version('api')

def get_version() -> str:
    print("WARNING: version.get_version() is deprecated and will be removed in 0.2.0 release")
    build_type = os.environ.get('BUILD_TYPE', 'dev')
    if build_type != 'release':
        vcs_hash = os.environ.get('VCS_VERSION')
        print(f"VCS_VERSION={vcs_hash}")
        vcs_hash = os.environ.get('VCS_VERSION') or "unofficial"
        devtag = f"_{build_type}_{vcs_hash}"
    return f'{major}.{minor}.{patch}{devtag}'

def get_api_version() -> str:
    return __version__
