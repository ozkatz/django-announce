from setuptools import setup, find_packages

setup(
    name='django-announce',
    version='0.1.5',
    author='Oz Katz',
    author_email='oz.katz@ripplify.com',
    description='an Announce.js client for Django',
    url='http://github.com/ozkatz/django-announce/',
    license='MIT',
    packages=find_packages(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django'
    ]
)
