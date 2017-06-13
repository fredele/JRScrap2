# -*- mode: python -*-

block_cipher = None


a = Analysis(['C:\\Users\\fredele\\Desktop\\JRScrap2\\src\\main.py'],
             pathex=['C:\\Users\\fredele\\Desktop\\bin'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='JRScrap2',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='C:\\Users\\fredele\\Desktop\\JRScrap2\\res\\icon.ico')
coll = COLLECT(exe,Tree('C:\\Users\\fredele\\Desktop\\JRScrap2\\src\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='JRScrap2')
