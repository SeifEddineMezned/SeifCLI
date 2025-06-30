from setuptools import setup, find_packages
import os


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


requirements = [r for r in requirements if r and not r.startswith('#')]


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="seifcli",
    version="0.2.0",
    description="AI-powered command-line assistant with browser automation capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="SeifCLI Team",
    author_email="info@seifcli.com",
    url="https://github.com/seifcli/seifcli",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'seif=main:app',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
)