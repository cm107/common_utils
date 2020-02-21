from setuptools import setup, find_packages

packages = find_packages(
        where='.',
        include=['common_utils*']
)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='common_utils',
    version='0.1',
    description='Common utilities for convenience.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cm107/common_utils",
    author='Clayton Mork',
    author_email='mork.clayton3@gmail.com',
    license='MIT License',
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'opencv-python>=4.1.1.26',
        'numpy>=1.17.2',
        'requests>=2.22.0',
        'pylint>=2.4.2',
        'tqdm>=4.36.1',
        'scipy>=1.4.1',
        'imgaug>=0.3.0',
        'logger @ https://github.com/cm107/logger/archive/master.zip#egg=logger-0.1'
    ],
    python_requires='>=3.6'
)