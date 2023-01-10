import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="container-runtime-interface-api",
    packages=setuptools.find_namespace_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["grpcio~=1.39", "protobuf~=4.2"],
    version="1.0.0",
    author="Domino Data Lab",
    author_email="steven.davidovitz@dominodatalab.com",
    description="Python library for interaction with the Kubernetes container runtime interface API.",  # noqa
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dominodatalab/container-runtime-interface-api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
