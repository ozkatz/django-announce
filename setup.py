from setuptools import setup, find_packages

setup(
    name='django-announce',
    version=__import__('announce').__version__,
    author='Oz Katz',
    author_email='oz.katz@ripplify.com',
    description='an Announce.js client for Django',
    url='http://github.com/ozkatz/django-announce/',
    license='BSD',
    packages=find_packages(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django'
    ]
)
