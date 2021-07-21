from setuptools import setup, Extension
from Cython.Build import cythonize
# cython: language_level=3

#extension = [Extension('*', ['*.py'])]

setup(
    name='Test',
    version='1.0.0',
    url='http://www.majjcom.site:12568/',
    author='Majjcom',
    ext_modules=cythonize('secret.py'),
    zip_safe=False,
)
