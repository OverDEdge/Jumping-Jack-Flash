try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Platformer',
    'author': 'Niklas Moberg',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'niklasm85@gmail.com',
    'version': '0.1',
    'install_requires': ['nose', 'pygame', 'pytest'],
    'packages': ['Jumping_Jack_Flash'],
    'scripts': [],
    'name': 'Jumping_Jack_Flash'
}


setup(**config)
