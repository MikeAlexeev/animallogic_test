import setuptools

setuptools.setup(
    name="user-manager",
    version="1.0",
    description="user-manager test application",
    package_dir={"": "source"},
    packages=setuptools.find_packages(
        where="source",
    ),
    entry_points={"console_scripts": ["user-manager=user_manager.cli:main"]},
)
