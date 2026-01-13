# PyInstaller hook for gi (GObject Introspection)
# Collects GTK4posite and libadwaita typelibs

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs
import os
import sys
from pathlib import Path

# Collect all gi submodules
hiddenimports = collect_submodules('gi')

# Add specific GTK4 and libadwaita modules
hiddenimports += [
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
    'gi.repository.Graphene',
    'gi.repository.Gsk',
    # GStreamer modules
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

# Collect typelib files
datas = []

def find_typelibs():
    """Find GObject Introspection typelib directories."""
    typelib_dirs = []
    
    if sys.platform == 'win32':
        # MSYS2 paths
        msys_paths = [
            Path(os.environ.get('MSYSTEM_PREFIX', 'C:/msys64/mingw64')),
            Path('C:/msys64/mingw64'),
        ]
        for p in msys_paths:
            typelib_dir = p / 'lib' / 'girepository-1.0'
            if typelib_dir.exists():
                typelib_dirs.append(typelib_dir)
                break
    elif sys.platform == 'darwin':
        # Homebrew paths
        homebrew_prefix = Path(os.environ.get('HOMEBREW_PREFIX', '/opt/homebrew'))
        typelib_dir = homebrew_prefix / 'lib' / 'girepository-1.0'
        if typelib_dir.exists():
            typelib_dirs.append(typelib_dir)
    else:
        # Linux paths
        linux_paths = [
            Path('/usr/lib/girepository-1.0'),
            Path('/usr/lib64/girepository-1.0'),
            Path('/usr/lib/x86_64-linux-gnu/girepository-1.0'),
            Path('/usr/lib/aarch64-linux-gnu/girepository-1.0'),
        ]
        for p in linux_paths:
            if p.exists():
                typelib_dirs.append(p)
                break
    
    return typelib_dirs

required_typelibs = [
    'Gtk-4.0',
    'Gdk-4.0',
    'GLib-2.0',
    'GObject-2.0',
    'Gio-2.0',
    'Pango-1.0',
    'PangoCairo-1.0',
    'GdkPixbuf-2.0',
    'Adw-1',
    'cairo-1.0',
    'Graphene-1.0',
    'Gsk-4.0',
    'GModule-2.0',
    'HarfBuzz-0.0',
    'freetype2-2.0',
    # GStreamer typelibs
    'Gst-1.0',
    'GstBase-1.0',
    'GstAudio-1.0',
    'GstVideo-1.0',
    'GstPbutils-1.0',
    'GstTag-1.0',
    'GstApp-1.0',
    'GstPlayer-1.0',
    'GstGL-1.0',
    'GstAllocators-1.0',
    'GstController-1.0',
    'GstNet-1.0',
    'GstRtp-1.0',
    'GstRtsp-1.0',
    'GstSdp-1.0',
]

for typelib_dir in find_typelibs():
    for typelib_name in required_typelibs:
        typelib_file = typelib_dir / f'{typelib_name}.typelib'
        if typelib_file.exists():
            datas.append((str(typelib_file), 'gi_typelibs'))

# Collect dynamic libraries
binaries = collect_dynamic_libs('gi')
