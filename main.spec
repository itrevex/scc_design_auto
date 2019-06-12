# -*- mode: python -*-
import sys
sys.setrecursionlimit(5000)

block_cipher = None
allFiles = [
    ('./src/assests/', 'assests'),
]
hiddenimports = ['numpy.core._dtype_ctypes']
a = Analysis(['src\\main.py'],
             pathex=['E:\\Projects\\ESAI\\PROGRAMMING\\PYTHON\\SSC\\design_auto'],
             binaries=[],
             datas=allFiles,
            hiddenimports=hiddenimports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='trsc',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon='setup/icon_red.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main')
