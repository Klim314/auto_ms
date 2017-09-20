from setuptools import setup, find_packages

setup(name='auto_ms',
      packages=find_packages(),
      version='0.0.2',
      author='klim314',
      description='Tools for processing MS output',
      author_email='klim314@gmail.com',
      entry_points={"console_scripts": [
          "ms_split_temp=auto_ms.main:tempsplit_entry",
      ]},
      zip_safe=False,
      url='https://github.com/klim314/auto_ms',
      classifiers=['Development Status :: 3 - Alpha',
                   # Indicate who your project is intended for
                   'Intended Audience :: Science/Research',
                   # Pick your license as you wish (should match "license" above)
                   'License :: OSI Approved :: MIT License',
                   # Specify the Python versions you support here. In particular, ensure
                   # that you indicate whether you support Python 2, Python 3 or both.
                   'Programming Language :: Python :: 3'],
      install_requires=['pandas'])
