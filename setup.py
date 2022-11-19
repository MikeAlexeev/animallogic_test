from setuptools import setup


setup(
    name="user-manager",
    version="1.0",
    description="user-manager test application",
    packages=["user_manager"],
    package_dir={"user_manager": "source"},
    entry_points={"console_scripts": ["user-manager=user_manager.cli:main"]},
)
