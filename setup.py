from setuptools import setup, find_packages
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="vietnamadminunits",
    version="0.3.0",
    author="Hieu Tran",
    author_email="tnmhieu@gmail.com",
    description="Library of standardization and conversion of Vietnamese administrative units",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tranngocminhhieu/vietnamadminunits",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "vietnamadminunits": ["data/*.json", "data/*.db"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
        "Intended Audience :: Developers",
        "Natural Language :: Vietnamese"
    ],
    python_requires='>=3.7',
    install_requires=[
        "shapely",
        "geopy",
        "unidecode",
    ]
)