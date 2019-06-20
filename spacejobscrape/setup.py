import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spacejobscrape",
    version="0.0.1",
    author="Dan Hirst",
    author_email="dan.hirst@seds.org",
    description="Package to import all US space jobs and upload them to central server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danhirst98/jobsitewebscrape",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU AFFERO GENERAL PUBLIC LICENSE v3",
        "Operating System :: OS Independent",
    ],
)