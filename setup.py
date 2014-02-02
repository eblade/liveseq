#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup

name_ = 'liveseq'
version_ = '0.0.1'

classifiers = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: POSIX",
    "Programming Language :: Python :: 3",
    "Topic :: Multimedia :: Sound/Audio :: MIDI",
]

setup(
    name=name_,
    version=version_,
    author='Johan Egneblad',
    author_email='johan.egneblad@DELETEMEgmail.com',
    description='Programmable live MIDI sequencer.',
    license = "BSD",
    url='https://github.com/eblade/'+name_,
    download_url='https://github.com/eblade/'+name_+'/archive/v'+version_+'.tar.gz',
    packages=[name_],
    classifiers = classifiers
)
