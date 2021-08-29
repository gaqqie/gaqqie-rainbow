from pathlib import Path


from setuptools import find_packages, setup


this_directory = Path(__file__).parent

setup(
    name="gaqqie-rainbow",
    version="0.1.0",
    author="Satoyuki Tsukano",
    author_email="tknstyk@gmail.com",
    description="a library for providers to access the quantum computer cloud platform 'gaqqie-sky' in gaqqie suite.",
    long_description=(this_directory / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/gaqqie/gaqqie-rainbow",
    packages=find_packages(),
    license="Apache License 2.0",
    python_requires=">=3.8",
    install_requires=[
        "qiskit",
        "six",
        "urllib3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
