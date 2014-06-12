import os
from setuptools import setup, find_packages
from imp import load_source

version = load_source("version", os.path.join("crawtext", "version.py"))

CLASSIFIERS = [
    'Development Status :: 2 - Beta',
    'Environment :: Other Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Internet',
    'Topic :: Utilities',
    'Topic :: Software Development :: Libraries :: Python Modules']

description = "Crawler"

# read long description
try:
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
        long_description = f.read()
except:
    long_description = description

setup(name='crawtext',
    version=version.__version__,
    description=description,
    long_description=long_description,
    keywords='crawler, scrapping, extractor, web scrapping',
    classifiers=CLASSIFIERS,
    author='Constance de Quatrebarbes',
    author_email='4barbes@gmail.com',
    url='https://github.com/c24b/crawtext',
    license='Apache',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['lxml', 'cssselect', 'jieba', 'beautifulsoup4', 'nltk', 'docopt', 'docstring', 'pymongo', 'requests', 'six','tld', 'wsgiref'],
    test_suite="tests"
)