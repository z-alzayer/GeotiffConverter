from setuptools import setup, find_packages

setup(
    name="GeotiffConverter",
    version="0.1.0",
    author="Zayad",
    description="Basic python implementation that rewrites metadata into a geotiff to make it readable by rio/gdal",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
