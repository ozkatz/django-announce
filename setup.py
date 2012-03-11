from setuptools import setup

setup(
    name='django-announce',
    version=__import__('announce').__version__,
    author='Oz Katz',
    author_email='oz.katz@ripplify.com',
    description='an Announce.js client for Django',
    long_description=open('README.md').read(),
    url='http://github.com/ozkatz/django-announce/',
    license='BSD',
    packages=[
        'announce',
        'announce.templatetags'
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Framework :: Django',
    ]
)