#! /usr/bin/python
import sys, os
from distutils.core import setup
from glob import glob

from albasheer import __version__
from albasheer.core import albasheerCore, searchIndexer

# to install type: 
# python setup.py install --root=/

from distutils.command.build import build
from distutils.command.clean import clean

class my_build(build):
  def run(self):
    build.run(self)
    # generate data
    from albasheer.core import albasheerCore, searchIndexer

    if not os.path.isfile('albasheer-data/ix.db'):
      q=albasheerCore(False)
      ix=searchIndexer(True)
      for n,(o,i) in enumerate(q.getAyatIter(1, 6236)):
        for w in i.split(): ix.addWord(w,n+1)
      d=os.path.dirname(sys.argv[0])
      ix.save()

class my_clean(clean):
  def run(self):
    clean.run(self)
    try: os.unlink('albasheer-data/ix.db')
    except OSError: pass

locales=map(lambda i: ('share/'+i,[''+i+'/albasheer.mo',]),glob('locale/*/LC_MESSAGES'))
data_files=[('share/albasheer/',glob('albasheer-data/*')),('share/albasheer/tilawa_json_files',glob('tilawa_json_files/*'))]
data_files.extend(locales)
setup (name='Albasheer', version=__version__,
      description='Albasheer Quran Browser',
      author='Yucef Sourani',
      author_email='youssef.m.sourani@gmail.com',
      url='https://github.com/yucefsourani/albasheer-electronic-quran-browser',
      license='Waqf',
      packages=['albasheer'],
      scripts=['albasheer-browser'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: End Users/Desktop',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          ],
      cmdclass={'build': my_build, 'clean': my_clean},
      data_files=data_files
)
