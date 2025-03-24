import os


major: int = 0
minor: int = 1
patch: int = 0
devtag: str = ""


def get_version() -> str:
    build_type = os.environ.get('BUILD_TYPE', 'dev')
    if build_type != 'release':
        vcs_hash = os.environ.get('VCS_VERSION')
        print(f"VCS_VERSION={vcs_hash}")
        vcs_hash = os.environ.get('VCS_VERSION') or "unofficial"
        devtag = f"_{build_type}_{vcs_hash}"
    return f'{major}.{minor}.{patch}{devtag}'

