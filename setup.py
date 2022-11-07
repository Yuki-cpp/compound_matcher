import setuptools


setuptools.setup(
    name="compound_matcher",
    version="1.0.0",
    author="Leo Ghafari",
    author_email="leo.ghafari@gmail.com",
    description="Tool providing matching between compounds depending on their RT values",
    install_requires=["fuzzysearch"],
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "compound_matcher=compound_matcher.find_matches:main",
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
