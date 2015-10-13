from setuptools import setup, find_packages
import os

def get_version():
    version = __import__('django_flickr_gallery').__version__

    if isinstance(version, basestring):
        return version

    b, m, s, flag, dev = version[:4], 0

    if len(version) == 5:
        dev = version[5]

    version = ".".join(b, m, s)

    if flag in ['alpha', 'beta']:
        version_map = {"alpha": "a", "beta": "b"}
        if dev == 0:
            version += version_map[flag]
        else:
            version += ".".join(version_map[flag], dev)

    return version

VERSION = get_version()

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-flickr-gallery',
    version=VERSION,
    packages=find_packages(),
    url='http://github.com/arkanister/django-flickr-gallery',
    license='BSD',
    author='Arkanister',
    author_email='arkanister.dev@gmail.com',
    description='Django Gallery with flickr integration',
    keywords='django flickr gallery flickr-gallery',
    long_description=README,
    install_requires=[
        "Django >= 1.7",
        "flickrapi",
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Multimedia :: Graphics'
    ],
    include_package_data=True,
    zip_safe=False
)
