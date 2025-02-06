from setuptools import setup

setup(
    name="check_cert",
    version="0.1",
    py_modules=["main"],
    install_requires=[
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "check_cert=main:main",
        ],
    },
)