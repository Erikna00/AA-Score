from setuptools import setup, find_packages
import os

# Read the long description from README.md
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="AA_Score",
    version="0.1.0",
    author="Xundrug",
    author_email="your.email@example.com",  # update with your email
    description="A tool for protein-ligand binding affinity prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Xundrug/AA-Score-Tool",
    packages=find_packages(),
    include_package_data=True,  # include non-code files as specified in MANIFEST.in
    package_data={
        "AA_Score_main": ["models/model-final.npy"],
    },
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        # This creates a command-line executable 'aa-score' that calls the main() function in aascore.py.
        "console_scripts": [
            "aascore=AA_Score_main.aa_score:func",
        ],
    },
)
