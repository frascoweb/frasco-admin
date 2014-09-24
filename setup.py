from setuptools import setup, find_packages


def desc():
    with open("README.md") as f:
        return f.read()

def reqs():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='frasco-admin',
    version='0.1',
    url='http://github.com/frascoweb/frasco-admin',
    license='MIT',
    author='Maxime Bouroumeau-Fuseau',
    author_email='maxime.bouroumeau@gmail.com',
    description="Admin interface for Frasco",
    long_description=desc(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=reqs() + [
        'frasco',
        'frasco-bootstrap',
        'frasco-users',
        'frasco-users-acl'
    ]
)