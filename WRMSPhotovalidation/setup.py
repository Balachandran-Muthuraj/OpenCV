from setuptools import setup, find_packages

setup(
    name="WrmsApp",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "opencv-python",
        "numpy",
        "dlib",
        # Other dependencies
    ],
)
