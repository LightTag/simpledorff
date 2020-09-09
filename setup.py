import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simpledorff", # Replace with your own username
    version="0.0.2",
    author="Tal Perry",
    author_email="tal@lighttag.io",
    description="Calculate Krippendorff's Alpha on any DataFrame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lighttag/simpledorff",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # python_requires='>=3.6',
    # setup_requires=["setuptools~=46.0.0"]
)
