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
import sys
import signal
import locale
import gettext
from pathlib import Path

VERSION = '3.0'
pkgdatadir = str(Path(sys._MEIPASS))
localedir  = str(Path(sys._MEIPASS) / "share" / "locale")

sys.path.insert(1, pkgdatadir)
signal.signal(signal.SIGINT, signal.SIG_DFL)

try:
    sys_lang_code, _ = locale.getdefaultlocale()
    langs = [sys_lang_code] if sys_lang_code else None
    lang = gettext.translation('albasheer', localedir, languages=langs, fallback=True)
    lang.install()
except Exception as e:
    print(f"Warning: Could not load translations: {e}")
    gettext.install('albasheer', localedir)

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


datas.append((str(SRC_DIR / "albasheer-data/ix.db" ), "albasheerlib/albasheer-data"))
datas.append((str(SRC_DIR / "albasheer-data/quran.db" ), "albasheerlib/albasheer-data"))

datas.append((str(SRC_DIR / "tilawa_json_files/*" ), "share/albasheer/albasheer/tilawa_json_files"))
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
]

# Collect all gi submodules
hiddenimports += collect_submodules('gi')
hiddenimports += collect_submodules('sqlite3')

# Platform-specific configurations
if sys.platform == 'win32':
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
            icons_dir = share_path / 'icons'
            datas.append((str(icons_dir  / "Adwaita" ), 'share'))
            
            # Add GStreamer plugins
            gst_plugins_dir = lib_path / 'gstreamer-1.0'
            if gst_plugins_dir.exists():
                for plugin in gst_plugins_dir.glob('*.dll'):
                    datas.append((str(plugin), 'lib/gstreamer-1.0'))
            
            break

elif sys.platform == 'darwin':
    # macOS: use Homebrew paths
    homebrew_prefix = os.environ.get('HOMEBREW_PREFIX', '/opt/homebrew')
    gtk_path = Path(homebrew_prefix)
    
    if gtk_path.exists():
        share_path = gtk_path / 'share'
        
        # Add GLib schemas
        schemas_dir = share_path / 'glib-2.0' / 'schemas'
        install_gschema_xml(schemas_dir)
        datas.append((str(schemas_dir), 'share/glib-2.0/schemas'))

        locale_dir = install_po(share_path)
        datas.append((str(locale_dir), 'share/locale'))
            
        # Add icons
        icons_dir = share_path / 'icons'
        datas.append((str(icons_dir / "Adwaita"), 'share/icons'))


else:
    # Linux: use system paths
    share_paths = ['/usr/share', '/usr/local/share']
    
    for share_base in share_paths:
        share_path = Path(share_base)
        
        # Add GLib schemas
        schemas_dir = share_path / 'glib-2.0' / 'schemas'
        if schemas_dir.exists():
            install_gschema_xml(schemas_dir)
            datas.append((str(schemas_dir), 'share/glib-2.0/schemas'))
            break
    for share_base in share_paths:
        locale_dir = Path(share_base) / 'locale'
        if locale_dir.exists():
            locale_dir = install_po(share_path)
            datas.append((str(locale_dir), 'share/locale'))
            break
        

    
    for share_base in share_paths:
        icons_dir = Path(share_base) / 'icons'
        datas.append((str(icons_dir / "Adwaita"), 'share/icons'))
        break
    
    # Add GStreamer plugins for Linux
    gst_plugin_paths = [
        Path('/usr/lib/x86_64-linux-gnu/gstreamer-1.0'),
        Path('/usr/lib64/gstreamer-1.0'),
        Path('/usr/lib/gstreamer-1.0'),
        Path('/usr/lib/aarch64-linux-gnu/gstreamer-1.0'),
    ]
    for gst_path in gst_plugin_paths:
        if gst_path.exists():
            # Collect essential plugins
            essential_plugins = [
                'libgstcoreelements.so', 'libgstplayback.so', 'libgsttypefindfunctions.so',
                'libgstaudioconvert.so', 'libgstaudioresample.so', 'libgstvideoconvert.so',
                'libgstvideoscale.so', 'libgstvolume.so', 'libgstautodetect.so',
                'libgstapp.so', 'libgstgio.so', 'libgstalsa.so', 'libgstpulseaudio.so',
                'libgstlibav.so', 'libgstisomp4.so', 'libgstmatroska.so', 'libgstavi.so',
                'libgstogg.so', 'libgstvorbis.so', 'libgstopus.so', 'libgstflac.so',
                'libgstmpg123.so', 'libgstjpeg.so', 'libgstpng.so', 'libgstwavparse.so',
                'libgstaudioparsers.so', 'libgstvpx.so', 'libgstwebp.so',
                'libgstgtk.so', 'libgstgtk4.so', 'libgstopengl.so',
            ]
            for plugin_name in essential_plugins:
                plugin_path = gst_path / plugin_name
                if plugin_path.exists():
                    datas.append((str(plugin_path), 'lib/gstreamer-1.0'))
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
        'matplotlib',
        'numpy',
        'scipy',
        'PIL',
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
if sys.platform == 'win32':
    exclude_binaries = [
        # Windows UCRT and API-MS DLLs (system libraries)
        'api-ms-win-',
        'ucrtbase',
        # Boost Python (from OpenEXR, not needed)
        'libboost_python',
        # OpenEXR/Imath (not needed for basic media playback)
        'libImath',
        'libOpenEXR',
        'libIex',
        'libIlmThread',
        'libPyImath',
        'libPyIex',
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
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(DATA_DIR / 'com.github.yucefsourani.albasheer-electronic-quran-browser.ico') if sys.platform == 'win32' and (DATA_DIR / 'com.github.yucefsourani.albasheer-electronic-quran-browser.ico').exists() else None,
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

# macOS App Bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name=f'albasheer.app',
        icon=str(DATA_DIR / 'com.github.yucefsourani.albasheer-electronic-quran-browser.icns'),
        bundle_identifier=APP_ID,
        info_plist={
            'CFBundleName': 'albasheer',
            'CFBundleDisplayName': 'albasheer',
            'CFBundleVersion': '3.0',
            'CFBundleShortVersionString': '3.0',
            'NSHighResolutionCapable': True,
        },
    )
