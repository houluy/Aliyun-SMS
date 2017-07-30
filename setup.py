from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='alisms',
    version='1.0.8',
    description='A SDK for Aliyun SMS services in Python3',
    url='https://github.com/houluy/Aliyun-SMS',
    author='Houlu',
    author_email='houlu8674@bupt.edu.cn',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='Aliyun SMS SDK',
    packages=['alisms',],
    install_requires=['requests', 'pyyaml', 'urllib3', 'idna', 'chardet', 'certifi'],
    python_requires='>=3',
)
