import os

from setuptools import find_packages, setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(
    name='snippetto-cli',
    version='0.1.0',
    description='Snippetto command line interface',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Sebastian Opalczynski',
    author_email='sebastian.opalczynski@trurl.it',
    url='https://github.com/opalczynski/snippetto_cli',
    packages=find_packages(),
    license='MIT',
    install_requires=['requests>=2.21.0', 'click>=6.6'],
    # test_suite='tests',
    entry_points="""
        [console_scripts]
        snippetto=snipetto.cli:main
    """
)
