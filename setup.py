from distutils.core import setup

setup(
    name="soundcloud-syncer",
    version="0.2",
    description="Synchronize user's favorites tracks from soundcloud'",
    author="Sliim",
    author_email="sliim@mailoo.org",
    url="https://github.com/sliim/soundcloud-syncer",
    license="GPLv3",
    scripts=["scripts/sc-syncer", "scripts/sc-tagger"],
    packages=["ssyncer"],
    install_requires=[
        "stagger",
        "python-dateutil"
    ],
    tests_require=[
        "mock",
        "nose",
        "pep8",
        "coverage"
    ]
)
