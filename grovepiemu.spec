# -*- mode: python -*-

block_cipher = None


a = Analysis(['grovepiemu.py'],
             pathex=['fakegrovepi', 'D:\\jqm\\pi\\grovepi-emulator'],
             binaries=[],
             datas=[('main.ico', '.'), ('testfiles/*', 'testfiles'), ('gpe_utils/pikeys', 'pikeys')],
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
          name='grovepiemu',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='grovepiemu')
