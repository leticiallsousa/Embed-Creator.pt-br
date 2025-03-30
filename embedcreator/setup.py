from setuptools import setup, find_packages

with open("../README.md", "r") as arq:
    readme = arq.read()

setup(name='embedcreator',
    version='0.1.9',
    license='MIT License',
    author='Leticia Sousa',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='leticialimasousa2007@gmail.com',
    packages=find_packages(),
    install_requires=['discord.py'])
