from setuptools import setup,find_packages

with open("README.md","r",encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="multilingual-assistant",
    version="0.1.0",
    author="Haiyang Zeng",
    author_email="oceanzen9@gmail.com",
    description="基于Deepseek API的多语言助手",
    long_description=long_description,
    long_description_content_type="txt/markdown",
    url="https://github.com/oceanzen9/multilingual-assistant",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operation System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "flash>=3.1.0",
        "openai>=1.68.2",
        "python-dotenv>=1.1.0",
        "httpx>=0.28.1"
    ],
)