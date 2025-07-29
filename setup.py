from setuptools import find_packages, setup

install_requires = ["django>=5", "wagtail>=7"]

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
    version="0.8.0",
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
        "Framework :: Django :: 4",
        "Framework :: Django :: 5",
        "Operating System :: Unix",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 6",
        "Framework :: Wagtail :: 7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
