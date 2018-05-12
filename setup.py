from setuptools import setup, find_packages

setup(
    name = 'sv2',
    packages = find_packages(),
    platform=['any'],
	entry_points = {
        'console_scripts': ['sv2=sv2.command_line:main'],
    },
    version = '0.0.1',
    author = 'David Roman',
    author_email = 'davidroman96@gmail.com',
    url = 'https://github.com/OSPG/sv2'
)
