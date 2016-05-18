from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(
    name='dms',
    version=version,
    description='Doc Mgmt System',
    author='xyz',
    author_email='gsn@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
