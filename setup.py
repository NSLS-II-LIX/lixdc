__author__ = 'hhslepicka'
import setuptools
import versioneer
import os


setuptools.setup(
    name='lixdc',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license="BSD 3-Clause",
    url="https://github.com/NSLS-II-LIX/lixdc.git",
    packages=setuptools.find_packages(),
    install_package_data = True,
    install_requires=[],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Development Status :: 3 - Alpha",
        'Programming Language :: Python :: 3',
    ],
)
