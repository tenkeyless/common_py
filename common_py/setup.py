import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="common_py",
    version="0.0.1",
    author="TenKeyLess",
    author_email="blivme84@naver.com",
    description="The fundamental package needed for common purpose with Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tenkeyless/common_py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "License :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Unix",
    ],
    python_requires=">=3.7",
)
