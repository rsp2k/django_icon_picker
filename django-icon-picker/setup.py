from setuptools import setup, find_packages

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="django-icon-picker",
    version="1.0.2",
    description="A custom Django model field that allows users to select icons from a predefined set.",
    author="Mohammed CHAHBOUN",
    author_email="m97.chahboun@gmail.com",
    url="https://github.com/bixat/django_icon_picker",
    include_package_data=True,
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    install_requires=[
        "Django>=3.0",
        "requests",
    ],
    package_data={
        "django_icon_picker": ["templates/django_icon_picker/icon_picker.html"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
