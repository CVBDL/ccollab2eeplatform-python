"""Setup module."""

from setuptools import setup, find_packages


setup(
    name='ccollab2eeplatform',
    version='0.1',
    description='Extract data from CodeCollaborator to EagleEye-Platform',
    url='https://github.com/CVBDL/ccollab2eeplatform-python',
    author='Patrick Zhong',
    license='MIT',
    packages=find_packages(exclude=['tests'])
    #install_requires=['requests>=2.13.0']
)
