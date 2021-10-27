from setuptools import find_packages, setup

setup(
    name="cam-control",
    version="0.0.1",
    py_modules=["cam-control"],
    packages=find_packages(),
    python_requires="~=3.6",
    install_requires=[
        "pytapo",
        "scapy",
    ],
    entry_points={
        "console_scripts": [
            "cam-control=camcontrol.main:main",
        ],
    },
)
