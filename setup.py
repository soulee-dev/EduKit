import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EduKit", # Replace with your own username
    version="0.0.1",
    author="Lee Soul",
    author_email="a010393223@gmail.com",
    description="Library for teaching Python to students",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lill74/EduKit",
    packages=setuptools.find_packages(),
    install_requires = [
        'requests==2.24.0',
        'beautifulsoup4==4.9.1',
        'konlpy==0.5.2',
        'matplotlib==3.3.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)