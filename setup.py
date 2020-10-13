import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="covid_india",
    version="1.1.4",
    author="Debdut Goswami",
    author_email="debdutgoswami@gmail.com",
    description="A package to provide information regarding COVID-19 cases in India.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/debdutgoswami/covid-19-India",
    download_url = 'https://github.com/debdutgoswami/covid-19-India/archive/v_1.1.4.tar.gz',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'pandas',
        'lxml'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
