from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-flickr-gallery',
    version='0.1.3',
    packages=find_packages(),
    url='http://github.com/arkanister/django-flickr-gallery',
    license='BSD',
    author='Arkanister',
    author_email='arkanister.dev@gmail.com',
    description='Django Gallery with flickr integration',
    keywords='django flickr gallery flickr-gallery',
    long_description=README,
    install_requires=[
        "Django >= 1.4",
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
