import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gspan_mining",
    version="0.2.3",
    author="Qingying Chen",
    author_email="qychen.pku@gmail.com",
    description="Implementation of frequent subgraph mining algorithm gSpan",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/betterenvi/gSpan",
    packages=['gspan_mining'],
    classifiers=(
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
