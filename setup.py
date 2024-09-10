from setuptools import setup, find_packages

setup(
    name="thermal_heatmap_generator",
    version="0.1",
    description="A thermal heatmap generation package",
    author="Jonas Klotz",
    author_email="j.klotz@tu-berlin.de",
    packages=find_packages(),
    python_requires=">=3.7,<3.13",
    install_requires=[
        "numpy",
        "scipy",
    ],
)
