from setuptools import setup, find_packages

setup(
    name='csvpipe',
    version='0.1.0',
    url='https://github.com/hanKo91/csvpipe',
    author='Dominik Hanko',
    author_email='dominik.hanko91@gmail.com',
    description='Simple csv data pipeline creation',
    packages=find_packages(
      include=
      [
        "csvpipe", "csvpipe.*",
        "test", "test.*"
      ]
    ),
    data_files=[('reference', ['data/ref.csv'])]
)