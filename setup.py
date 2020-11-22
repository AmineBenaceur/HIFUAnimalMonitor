from setuptools import setup, find_packages

setup(
    name='capstonepi',
    version='0.0.1',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'docopt==0.6.2'
    ],
    entry_points={
        'console_scripts': ['cappi=capstonepi.main:main']
    }
)
