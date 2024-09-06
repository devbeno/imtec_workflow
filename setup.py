from setuptools import find_packages, setup

setup(
    name="imtec_workflow",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fabric",
        "invoke",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "imrun=imtec_workflow.scripts.imrun:main",
        ],
    },
)
