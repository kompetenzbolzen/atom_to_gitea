from distutils.core import setup
import setuptools

setup(
    name='rsstogitea',
    version='0.2.0',
    author="Jonas Gunz",
    description="Create a Gitea Issue for new RSS entries",
    packages=['rss_to_gitea'],
    entry_points={
        'console_scripts': ['rsstogitea=rss_to_gitea.main:main']
        },
    install_requires=[
        "requests>=2.25.1",
        "pyyaml"
    ],
    license='MIT',
    long_description=open('Readme.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

