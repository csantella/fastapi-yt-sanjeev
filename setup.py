import os
from setuptools import setup, find_packages
from setuptools_scm.version import get_local_dirty_tag
import tomllib

# major: int = 0
# minor: int = 1
# patch: int = 0
# devtag: str = ""


def get_version() -> str:
    with open("pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)
    base_version = pyproject["project"]["version"]

    build_type = os.environ.get('BUILD_TYPE', 'dev')
    if build_type != 'release':
        vcs_hash = os.environ.get('VCS_VERSION')
        print(f"VCS_VERSION={vcs_hash}")
        vcs_hash = os.environ.get('VCS_VERSION') or "unofficial"
        devtag = f"_{build_type}_{vcs_hash}"
    version = f'{base_version}{devtag}'
    print(f"Building api-{version} ...")


def clean_scheme(version):
    return get_local_dirty_tag(version) if version.dirty else '+clean'


setup(
    name='api',
    use_scm_version={'local_scheme': clean_scheme},
    packages=find_packages()
)

