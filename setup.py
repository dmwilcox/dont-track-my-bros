"""setuptools based setup module"""

import codecs
from os import path
from setuptools import find_packages, setup


current_dir = path.abspath(path.dirname(__file__))


with codecs.open(path.join(current_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='vcardtools',
    version='0.1.1',
    description='Tool to extract encoded URLs from a URL.',
    long_description=long_description,
    url='https://github.com/dmwilcox/dont-track-my-bros',
    author='Yuba Solutions LLC',
    author_email='dmw@yubasoluions.com',
    license='GPL',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
    ],
    keywords='URL cleaner',
    packages = [
        'dont_track_my_bros',
    ],
    entry_points = {
        'console_scripts': [
            'clean_url = dont_track_my_bros.clean_url:dispatch_main',
        ],
    },
    install_requires = ['argparse', ]
)
