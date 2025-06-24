from setuptools import setup, find_packages

setup(
    name='hwscraper',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            'hwscraper=hwscraper.__main__:main',
        ]
    },
    author='Naman',
    description='CLI Proxy Scraper Tool - Hacker Style',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ItzNamanDev/hwscraper',  # Replace with real GitHub repo
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)