from setuptools import setup, find_packages

setup(
    name="cs4090-assignment-4-templae",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)

# Run pip install -e . to install in editable mode