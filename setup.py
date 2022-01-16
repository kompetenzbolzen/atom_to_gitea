from distutils.core import setup
import setuptools

setup(
    name='rsstogitea',
    version='0.0.0-dev',
    author="Jonas Gunz",
    description="Create a Gitea Issue for new RSS entries",
    packages=['rss_to_gitea'],
    entry_points={
        'console_scripts': ['rsstogitea=rss_to_gitea.main:main']
        },
    install_requires=[
        "requests>=2.25.1"
    ],
    license='All rights reserved',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

