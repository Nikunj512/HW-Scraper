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
    author_email='your_email@example.com',  # optional
    description='A hacker-style CLI tool to scrape and validate working proxies from multiple sources.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/HW-Scraper',  # replace with your GitHub URL
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/HW-Scraper/issues",
        "Source": "https://github.com/yourusername/HW-Scraper",
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: Proxy Servers',
        'Topic :: Security',
        'Environment :: Console',
    ],
    python_requires='>=3.6',
)