from setuptools import setup, find_packages
import os

APP_NAME = 'django_flickr_gallery'

def get_version(version=None):
    "Returns a PEP 386-compliant version number from VERSION."
    version = version or __import__(APP_NAME).__version__

    assert version[3] in ('alpha', 'beta', 'rc', 'final')

    # Now build the two parts of the version number:
    # main = X.Y[.Z]
    # sub = .devN - for pre-alpha releases
    #     | {a|b|c}N - for alpha, beta and rc releases
    main = '.'.join(str(x) for x in version[:3])

    sub = ''

    if version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[version[3]] + '.dev' + str(version[4])

    return str(main + sub)

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
        "django-ckeditor >= 5.0.2",
        "flickrapi",
        "pytz",
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
