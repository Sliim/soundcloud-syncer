from distutils.core import setup

setup(
    name="soundcloud-syncer",
    version="0.1",
    description="Synchronize user's favorites tracks from soundcloud'",
    author="Sliim",
    author_email="sliim@mailoo.org",
    url="https://github.com/sliim/soundcloud-syncer",
    license="GPLv3",
    scripts = ["sc-syncer"],
    packages=["ssyncer"]
)
