from setuptools import find_packages, setup

setup(
    name="vyper-select",
    description="Manage multiple Vyper compiler versions.",
    url="https://github.com/jeffchen006/vyper-select",
    author="Zhiyang Chen",
    version="0.0.0",
    packages=find_packages(),
    python_requires=">=3.6",
    license="AGPL-3.0",
    # pylint: disable=consider-using-with
    long_description=open("README.md", encoding="utf8").read(),
    entry_points={
        "console_scripts": [
            "vyper-select = vyper_select.__main__:vyper_select",
            "vyper = vyper_select.__main__:vyper",
        ]
    },
    install_requires=["pycryptodome>=3.4.6", "packaging"],
)