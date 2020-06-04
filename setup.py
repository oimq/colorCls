from setuptools import setup

setup(name='colorCls',
      version=1.2,
      author='oimq',
      url='https://github.com/oimq/colorCls',
      author_email='taep0q@gmail.com',
      description='Labeling, Aggragation and Categorizing about color RGB',
      packages=['core'],
      install_requires=['tqdm', 'opencv-python'],
      python_requires='>=3',
      zip_safe=False
      )