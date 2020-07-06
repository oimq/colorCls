from setuptools import setup, find_packages

setup(name='colorCls',
      version=2.0,
      author='oimq',
      url='https://github.com/oimq/colorCls',
      author_email='taep0q@gmail.com',
      description='Labeling, Aggragation and Categorizing about color RGB',
      packages=find_packages(),
      install_requires=['tqdm', 'opencv-python'],
      python_requires='>=3',
      zip_safe=False
      )