# -*- mode: python -*-

block_cipher = None


a = Analysis(['..\\src\\main.py'],
             pathex=['C:\\Users\\fredele\\Desktop\\JR\\windows32'],
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
          console=False , icon='..\\res\\icon.ico')
coll = COLLECT(exe,Tree('..\\src\\'),Tree('C:\\Python27\\share\\sdl2\\bin'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='JRScrap2')
