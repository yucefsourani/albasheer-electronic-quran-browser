# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Albasheer
This spec file handles GTK4, libadwaita, and GResource bundling
"""

import os
import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import subprocess
import glob

# Determine paths
SPEC_DIR = Path(SPECPATH)
PROJECT_DIR = SPEC_DIR.parent
SRC_DIR = PROJECT_DIR / "src"
DATA_DIR = PROJECT_DIR / "data"
PO_DIR = PROJECT_DIR / "po"
gschema_xml   = DATA_DIR / "com.github.yucefsourani.albasheer-electronic-quran-browser.gschema.xml"
FONTS_DIR     = PROJECT_DIR / "pyinstaller" /  "fonts"
FONTS_CONFIG  = PROJECT_DIR / "pyinstaller" / "font.conf"

# Application metadata
APP_NAME = "albasheer"
APP_ID = "com.github.yucefsourani.albasheer-electronic-quran-browser"


def install_po(prefix_dir):
    locale_dir = prefix_dir / "locale"
    os.makedirs(str(locale_dir),exist_ok=True)
    for po in glob.glob(f"{PO_DIR}/*.po"):
        mo      = "albasheer.mo"
        mo_file =  os.path.join(str(locale_dir),os.path.basename(po).split(".")[0],"LC_MESSAGES",mo)
        subprocess.run(["msgfmt",po,"-o",mo_file], check=True)
    return locale_dir
        

def install_gschema_xml(schemas_dir):
    os.makedirs(str(schemas_dir),exist_ok=True) 
    if  gschema_xml.exists():
        subprocess.run(["cp",str(gschema_xml),str(schemas_dir)], check=True)
        subprocess.run(["glib-compile-schemas",str(schemas_dir)], check=True)





# Compile GResource if not exists
gresource_file = SRC_DIR / "albasheer.gresource"
gresource_xml  = SRC_DIR / "albasheer.gresource.xml"

if not gresource_file.exists() and gresource_xml.exists():
    print(f"Compiling GResource: {gresource_xml}")
    subprocess.run([
        "glib-compile-resources",
        "--sourcedir", str(SRC_DIR),
        "--target", str(gresource_file),
        str(gresource_xml)
    ], check=True)

hicolor_icon = DATA_DIR / "icons" / "hicolor" 
adwaita_icon = DATA_DIR / "icons" / "Adwaita" 
hicolor_icon.rename(adwaita_icon)



albasheer_out = SRC_DIR / "albasheer.py" 
albasheer_windows_exe = """import os
import signal
import sys
import locale
import gettext
from pathlib import Path
import ctypes

os.environ['FONTCONFIG_PATH'] = os.path.join(sys._MEIPASS, 'etc', 'fonts')
localedir  = str(Path(sys._MEIPASS) / "share" / "locale")
def get_windows_language():
    try:
        windll = ctypes.windll.kernel32
        lang_id = windll.GetUserDefaultUILanguage()
        lang_code = locale.windows_locale.get(lang_id)
        if lang_code:
            return [lang_code.split('_')[0],lang_code  ] 
    except:
        pass
    return ['en','en_US']

try:
    sys_lang_code = get_windows_language()
    lang = gettext.translation('albasherr', localedir, languages=sys_lang_code, fallback=True)
    lang.install()
except Exception as e:
    print(f"Warning: Could not load translations: {e}")
    gettext.install('albasherr', localedir)


VERSION = '3.0'
pkgdatadir = str(Path(sys._MEIPASS))
localedir  = str(Path(sys._MEIPASS) / "share" / "locale")

sys.path.insert(1, pkgdatadir)
signal.signal(signal.SIGINT, signal.SIG_DFL)



if __name__ == '__main__':
    import gi

    from gi.repository import Gio
    resource = Gio.Resource.load(os.path.join(pkgdatadir, 'albasheer.gresource'))
    resource._register()

    from albasheer import main
    sys.exit(main.main(VERSION))

"""
with open(str(albasheer_out) ,"w") as myf:
    myf.write(albasheer_windows_exe)
    
# Collect GTK4 and libadwaita data
datas = []
if FONTS_CONFIG.exists():
    datas.append((str(FONTS_CONFIG), "etc/fonts"))

if FONTS_DIR.exists():
    datas.append((str(FONTS_DIR), "shate/fonts"))
datas.append((str(gresource_file ), "."))

datas.append((str(SRC_DIR / "albasheer/core.py" ), "albasheerlib"))
datas.append((str(SRC_DIR / "albasheer/__init__.py" ), "albasheerlib"))
datas.append((str(SRC_DIR / "albasheer/univaruints.py" ), "albasheerlib"))

datas.append((str(SRC_DIR / "__init__.py" ), "albasheer"))
datas.append((str(SRC_DIR / "main.py" ), "albasheer"))
datas.append((str(SRC_DIR / "window.py" ), "albasheer"))
datas.append((str(SRC_DIR / "tafasir_w.py" ), "albasheer"))
datas.append((str(SRC_DIR / "utl.py" ), "albasheer"))
datas.append((str(SRC_DIR / "tilawa_download.py" ), "albasheer"))
datas.append((str(SRC_DIR / "tilawa_gui.py" ), "albasheer"))
datas.append((str(SRC_DIR / "tilawa_settings.py" ), "albasheer"))
datas.append((str(SRC_DIR / "search_window.py" ), "albasheer"))
datas.append((str(SRC_DIR / "copy_gui.py" ), "albasheer"))
datas.append((str(SRC_DIR / "news_window.py" ),  "albasheer"))
datas.append((str(SRC_DIR / "tools_bar.py" ),  "albasheer"))


datas.append((str(SRC_DIR / "albasheer-data/ix.db" ), "albasheer-data"))
datas.append((str(SRC_DIR / "albasheer-data/quran.db" ), "albasheer-data"))

datas.append((str(SRC_DIR / "tilawa_json_files/*" ), "albasheer/tilawa_json_files"))
datas.append((str(SRC_DIR / "LICENSE-en" ), "licenses/albasheer"))
datas.append((str(SRC_DIR / "LICENSE-ar.txt" ), "licenses/albasheer"))

# Hidden imports for GTK4 and libadwaita
hiddenimports = [
    'gi',
    'gi.repository.Gtk',
    'gi.repository.Gdk',
    'gi.repository.GLib',
    'gi.repository.GObject',
    'gi.repository.Gio',
    'gi.repository.GioWin32',
    'gi.repository.Pango',
    'gi.repository.PangoCairo',
    'gi.repository.GdkPixbuf',
    'gi.repository.Adw',
    'gi.repository.cairo',
    # GStreamer imports
    'gi.repository.Gst',
    'gi.repository.GstBase',
    'gi.repository.GstAudio',
    'gi.repository.GstVideo',
    'gi.repository.GstPbutils',
    'gi.repository.GstTag',
    'gi.repository.GstApp',
    'gi.repository.GstPlayer',
    'gi.repository.GstGL',
    'gi.repository.Soup',
]

# Collect all gi submodules
hiddenimports += collect_submodules('gi')
hiddenimports += collect_submodules('sqlite3')
hiddenimports += collect_submodules('zipfile')
hiddenimports += collect_submodules('ctypes')



# Platform-specific configurations
# Windows: collect GTK4 DLLs from MSYS2/mingw64
# Try to find GTK4 installation
gtk_paths = [
    Path(os.environ.get('MSYSTEM_PREFIX', 'C:/msys64/mingw64')),
    Path('C:/msys64/mingw64'),
    Path('C:/gtk'),
]

for gtk_path in gtk_paths:
    if (gtk_path / 'bin').exists():
        # Add GTK4 binaries
        bin_path = gtk_path / 'bin'
        lib_path = gtk_path / 'lib'
        share_path = gtk_path / 'share'
        
        # Add required DLLs
        for dll in bin_path.glob('*.dll'):
            datas.append((str(dll), '.'))
        
        # Add GLib schemas
        schemas_dir = share_path / 'glib-2.0' / 'schemas'
        install_gschema_xml(schemas_dir)
        datas.append((str(schemas_dir), 'share/glib-2.0/schemas'))
        
        locale_dir = install_po(share_path)
        datas.append((str(locale_dir), 'share/locale'))
        
        # Add icons
        hicolor_icons = share_path / 'icons/hicolor'
        if hicolor_icons.exists():
            datas.append((str(hicolor_icons), 'share/icons/hicolor'))
        
        adwaita_icons = share_path / 'icons/Adwaita'
        if adwaita_icons.exists():
            datas.append((str(adwaita_icons), 'share/icons/Adwaita'))

        adwaita_myicon = DATA_DIR / "icons/Adwaita" 
        if adwaita_myicon.exists():
            datas.append((str(adwaita_myicon), "share/icons/Adwaita"))

        hicolor_myicon = DATA_DIR / "icons/hicolor" 
        if hicolor_myicon.exists():
            datas.append((str(hicolor_myicon), "share/icons/hicolor"))

        
        # Add GStreamer plugins
        gst_plugins_dir = lib_path / 'gstreamer-1.0'
        if gst_plugins_dir.exists():
            for plugin in gst_plugins_dir.glob('*.dll'):
                datas.append((str(plugin), 'lib/gstreamer-1.0'))
        
        break


# Analysis configuration
a = Analysis(
    [str(SRC_DIR / 'albasheer.py')],
    pathex=[str(SRC_DIR),str(SRC_DIR / "albasheer")],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[str(SPEC_DIR / 'hooks')],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Filter out Windows system DLLs and unnecessary libraries
exclude_binaries = [
    # Windows UCRT and API-MS DLLs (system libraries)
    'api-ms-win-',
    'ucrtbase',
    # Boost Python (from OpenEXR, not needed)
    'libboost_python',
]
    
filtered_binaries = []
for binary in a.binaries:
    name = binary[0].lower()
    if not any(exclude in name for exclude in exclude_binaries):
        filtered_binaries.append(binary)

a.binaries = filtered_binaries

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(DATA_DIR / 'com.github.yucefsourani.albasheer-electronic-quran-browser.ico') if  (DATA_DIR / 'com.github.yucefsourani.albasheer-electronic-quran-browser.ico').exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=APP_NAME,
)
