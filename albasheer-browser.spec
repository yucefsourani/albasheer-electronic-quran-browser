# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
data_files = [("LICENSE-ar.txt","."),("LICENSE-en","."),
              ("albasheer.ico","."),("albasheer-128.png","."),("README","."),("README-ar.txt","."),("locale","./locale"),("tilawa_json_files","./tilawa_json_files")]
binary_files = [("icons","./icons"),("albasheer","./albasheer"),("albasheer-data","./albasheer-data"),("po","./po"),("amiri_font","./amiri_font")]
a = Analysis(['albasheer-browser'],
             pathex=['.'],
             binaries=binary_files,
             datas=data_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=True)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='albasheer-browser',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,icon='albasheer.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='albasheer-browser')
