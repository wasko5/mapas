# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import os
import sys

spec_root = os.path.abspath(SPECPATH)

def get_pandas_path():
    import pandas
    pandas_path = pandas.__path__[0]
    return pandas_path

def get_statsmodels_path():
    import statsmodels
    path = os.path.dirname(statsmodels.__file__)
    return path
   
def get_numpy_path():
    import numpy
    path = os.path.dirname(numpy.__file__)
    return path

def get_scipy_path():
    import scipy
    path = os.path.dirname(scipy.__file__)
    return path

def get_dateutil_path():
    import dateutil
    path = os.path.dirname(dateutil.__file__)
    return path

def get_patsy_path():
    import patsy
    path = os.path.dirname(patsy.__file__)
    return path

def resource_path(relative_path):
     if hasattr(sys, '_MEIPASS'): 
         return os.path.join(sys._MEIPASS, relative_path) # pylint: disable=no-member
     return os.path.join(os.path.abspath("."), relative_path)


a = Analysis(['__ROOT.py'],
             pathex = [spec_root],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['statsmodels'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += Tree(get_statsmodels_path(), prefix="statsmodels", excludes=["*.pyc"])
a.datas += Tree(get_numpy_path(), prefix="numpy", excludes=["*.pyc"])
a.datas += Tree(get_pandas_path(), prefix='pandas', excludes=["*.pyc"])
a.datas += Tree(get_scipy_path(), prefix="scipy", excludes=["*.pyc"])
a.datas += Tree(get_dateutil_path(), prefix="dateutil", excludes=["*.pyc"])
a.datas += Tree(get_patsy_path(), prefix="patsy", excludes=["*.pyc"])

a.datas += [ (os.path.join("Images", "spss_instr3.gif"), resource_path(os.path.join("Images", "spss_instr3.gif")), 'DATA')]
a.datas += [ (os.path.join("Images", "MUFOS_logo_temp.png"), resource_path(os.path.join("Images", "MUFOS_logo_temp.png")), 'DATA')]

a.binaries = filter(lambda x: 'pandas' not in x[0], a.binaries)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)


exe = EXE(pyz,
      a.scripts,
      exclude_binaries=True,
      name='mufos',
      debug=False,
      strip=None,
      upx=True,
      console=False )

coll = COLLECT(exe,
           a.binaries,
           a.zipfiles,
           a.datas,
           strip=None,
           upx=True,
           name='mufos')