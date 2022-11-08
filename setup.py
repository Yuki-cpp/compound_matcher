import setuptools


setuptools.setup(
    name="rt_matcher",
    version="1.0.0",
    author="Leo Ghafari",
    author_email="leo.ghafari@gmail.com",
    description="Tool allowing to Fuzzy search a library for a set of features",
    install_requires=["fuzzysearch"],
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "metabolite-finder=rt_matcher.find_metabolites:main",
            "rt-matcher=rt_matcher.find_matches:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires=">3",
)
