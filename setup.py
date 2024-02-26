from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='embedcreator',
    version='0.0.1',
    license='MIT License',
    author='Leticia Sousa',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='leticialimasousa2007@gmail.com',
    packages=['creator'],
    install_requires=['discord.py'])
