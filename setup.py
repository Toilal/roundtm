#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# RoundTM - A Round based Tournament Manager
# Copyright (c) 2013 Rémi Alvergnat <toilal.dev@gmail.com>
#
# RoundTM is free software; you can redistribute it and/or modify it under
# the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# RoundTM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from setuptools import setup, find_packages
import os

from roundtm import __version__


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
HISTORY = open(os.path.join(here, 'HISTORY.rst')).read()


install_requires = ['PYAML']

entry_points = {
    'console_scripts': [
        'roundtm = roundtm.__main__:main'
    ],
}


args = dict(name='roundtm',
            version=__version__,
            description='RoundTM - A Round based Tournament Manager.',
            long_description=README + '\n\n' + HISTORY,
            # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
            classifiers=['Development Status :: 2 - Pre-Alpha',
                         'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                         'Operating System :: OS Independent',
                         'Intended Audience :: End Users/Desktop',
                         'Programming Language :: Python :: 2',
                         'Programming Language :: Python :: 3',
                         'Topic :: Games/Entertainment'
                         ],
            keywords='round based tournament manager play players sport game',
            author='Rémi Alvergnat',
            author_email='toilal.dev@gmail.com',
            url='https://github.com/Toilal/roundtm',
            license='LGPLv3',
            packages=find_packages(),
            include_package_data=True,
            install_requires=install_requires,
            entry_points=entry_points,
            test_suite='roundtm.test',
            )

setup(**args)
