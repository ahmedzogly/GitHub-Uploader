from setuptools import setup, find_packages

setup(
    name="github-uploader",
    version="2.0.0",
    author="Your Name",
    description="Professional GUI tool to upload files/folders to GitHub",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "github-uploader=src.uploader:main",
        ],
    },
)