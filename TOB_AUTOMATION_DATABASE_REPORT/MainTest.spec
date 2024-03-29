# -*- mode: python -*-

block_cipher = None
def get_pandas_path():
    import pandas
    pandas_path = pandas.__path__[0]
    return pandas_path

def get_reportlab_path():
    import reportlab
    reportlab_path = reportlab.__path__[0]
    return reportlab_path


a = Analysis(['MainTest.py'],
             pathex=['E:\\TOB_AUTOMATION_DATABASE_REPORT'],
             binaries=[],
             datas=[],
             hiddenimports=['reportlab','pandas._libs.tslibs.timedeltas'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

dict_tree = Tree(get_pandas_path(), prefix='pandas', excludes=["*.pyc"])
a.datas += dict_tree
a.binaries = filter(lambda x: 'pandas' not in x[0], a.binaries)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='MainTest',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
