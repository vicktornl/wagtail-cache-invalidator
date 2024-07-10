from setuptools import find_packages, setup

install_requires = ["django>=4", "wagtail>=5"]

test_require = [
    "black",
    "factory_boy",
    "flake8",
    "isort",
    "pytest",
    "pytest-django",
]

docs_require = []

setup(
    name="wagtail-cache-invalidator",
    version="0.6.3",
    description="",
    author="R.Moorman <rob@vicktor.nl>",
    install_requires=install_requires,
    extras_require={"test": test_require},
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Operating System :: Unix",
        "Framework :: Wagtail :: 3",
        "Framework :: Wagtail :: 4",
        "Framework :: Wagtail :: 5",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
