# PyInstaller hook for GStreamer
# Collects GStreamer libraries and plugins

import os
import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_dynamic_libs, logger

# GStreamer hidden imports
hiddenimports = [
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

datas = []
binaries = []


def find_gstreamer_paths():
    """Find GStreamer installation paths."""
    gst_paths = {
        'lib': None,
        'plugins': None,
        'typelibs': None,
    }
    
    if sys.platform == 'win32':
        # MSYS2 paths
        msys_paths = [
            Path(os.environ.get('MSYSTEM_PREFIX', 'C:/msys64/mingw64')),
            Path('C:/msys64/mingw64'),
            Path('C:/gstreamer/1.0/mingw_x86_64'),
        ]
        for base in msys_paths:
            if (base / 'lib' / 'gstreamer-1.0').exists():
                gst_paths['lib'] = base / 'lib'
                gst_paths['plugins'] = base / 'lib' / 'gstreamer-1.0'
                gst_paths['typelibs'] = base / 'lib' / 'girepository-1.0'
                break
                
    elif sys.platform == 'darwin':
        # Homebrew paths
        homebrew_prefix = Path(os.environ.get('HOMEBREW_PREFIX', '/opt/homebrew'))
        if (homebrew_prefix / 'lib' / 'gstreamer-1.0').exists():
            gst_paths['lib'] = homebrew_prefix / 'lib'
            gst_paths['plugins'] = homebrew_prefix / 'lib' / 'gstreamer-1.0'
            gst_paths['typelibs'] = homebrew_prefix / 'lib' / 'girepository-1.0'
            
    else:
        # Linux paths
        linux_paths = [
            Path('/usr/lib'),
            Path('/usr/lib64'),
            Path('/usr/lib/x86_64-linux-gnu'),
            Path('/usr/lib/aarch64-linux-gnu'),
        ]
        for base in linux_paths:
            if (base / 'gstreamer-1.0').exists():
                gst_paths['lib'] = base
                gst_paths['plugins'] = base / 'gstreamer-1.0'
                # Typelibs might be in a different location
                for typelib_path in [
                    Path('/usr/lib/girepository-1.0'),
                    Path('/usr/lib64/girepository-1.0'),
                    base / 'girepository-1.0',
                ]:
                    if typelib_path.exists():
                        gst_paths['typelibs'] = typelib_path
                        break
                break
    
    return gst_paths


def collect_gstreamer_plugins(plugins_dir, plugin_categories=None):
    """
    Collect GStreamer plugins.
    
    Args:
        plugins_dir: Path to GStreamer plugins directory
        plugin_categories: List of plugin categories to include, or None for all
                          Categories: 'core', 'base', 'good', 'bad', 'ugly', 'libav'
    """
    collected = []
    
    if not plugins_dir or not plugins_dir.exists():
        logger.warning(f"GStreamer plugins directory not found: {plugins_dir}")
        return collected
    
    # Plugin prefixes by category
    category_prefixes = {
        'core': ['libgstcore', 'libgstcoretracers'],
        'base': ['libgstapp', 'libgstaudioconvert', 'libgstaudioresample', 
                 'libgstplayback', 'libgsttypefindfunctions', 'libgstvideoconvert',
                 'libgstvideoscale', 'libgstvolume', 'libgstogg', 'libgstvorbis',
                 'libgstopus', 'libgsttheora', 'libgstpango', 'libgstopengl',
                 'libgstgio', 'libgstalsa', 'libgstcdparanoia', 'libgstlibvisual',
                 'libgstrawparse', 'libgstsubparse', 'libgsttcp', 'libgstximagesink',
                 'libgstxvimagesink', 'libgstpbtypes', 'libgstencoding',
                 'libgstadder', 'libgstcompositor', 'libgstaudiomixer',
                 'libgstoverlaycomposition', 'libgstaudiorate', 'libgstvideorate',
                 'libgstaudiotestsrc', 'libgstvideotestsrc'],
        'good': ['libgstautodetect', 'libgstavi', 'libgstcairo', 'libgstflac',
                 'libgstgdkpixbuf', 'libgstisomp4', 'libgstjpeg', 'libgstlame',
                 'libgstlevel', 'libgstmatroska', 'libgstmpg123', 'libgstpng',
                 'libgstpulseaudio', 'libgsttaglib', 'libgstwavparse', 'libgstwavenc',
                 'libgstspectrum', 'libgstaudioparsers', 'libgstvpx', 'libgstwebp',
                 'libgstximagesrc', 'libgstgtk', 'libgstdeinterlace',
                 'libgsteffectv', 'libgstequalizer', 'libgstmultifile',
                 'libgstosxaudio', 'libgstosxvideo', 'libgstv4l2'],
        'bad': ['libgstopencv', 'libgstwebrtc', 'libgstdash', 'libgsthls',
                'libgstsrt', 'libgstx265', 'libgstx264', 'libgstopenh264',
                'libgstfdkaac', 'libgstresindvd', 'libgstdtls', 'libgstsctp',
                'libgstwebrtcdsp', 'libgstzbar', 'libgstopenjpeg', 'libgstsvtav1',
                'libgstva', 'libgstuvch264', 'libgstwaylandsink'],
        'ugly': ['libgsta52dec', 'libgstamrnb', 'libgstamrwbdec', 'libgstasf',
                 'libgstdvdread', 'libgstdvdsub', 'libgstmpeg2dec', 'libgstx264',
                 'libgstsid', 'libgsttwolame'],
        'libav': ['libgstlibav'],
    }
    
    # Essential plugins that should always be included
    essential_plugins = [
        'libgstcoreelements', 'libgstcoretracers', 'libgstplayback',
        'libgsttypefindfunctions', 'libgstaudioconvert', 'libgstaudioresample',
        'libgstvideoconvert', 'libgstvideoscale', 'libgstvolume',
        'libgstautodetect', 'libgstapp', 'libgstgio',
    ]
    
    # File extension based on platform
    if sys.platform == 'win32':
        ext = '.dll'
    elif sys.platform == 'darwin':
        ext = '.dylib'
    else:
        ext = '.so'
    
    # Collect plugins
    for plugin_file in plugins_dir.iterdir():
        if not plugin_file.is_file():
            continue
        if not plugin_file.suffix == ext and ext not in plugin_file.name:
            continue
            
        plugin_name = plugin_file.stem
        
        # Check if plugin should be included
        include = False
        
        # Always include essential plugins
        if any(plugin_name.startswith(e) for e in essential_plugins):
            include = True
        elif plugin_categories is None:
            # Include all if no filter specified
            include = True
        else:
            # Check category filter
            for category in plugin_categories:
                if category in category_prefixes:
                    if any(plugin_name.startswith(p) for p in category_prefixes[category]):
                        include = True
                        break
        
        if include:
            collected.append((str(plugin_file), 'lib/gstreamer-1.0'))
    
    return collected


# Find GStreamer paths
gst_paths = find_gstreamer_paths()

# Collect GStreamer plugins
# Set to None to collect ALL plugins, or specify categories like ['core', 'base', 'good']
PLUGIN_CATEGORIES = ['core', 'base', 'good', 'libav']

if gst_paths['plugins']:
    plugin_binaries = collect_gstreamer_plugins(gst_paths['plugins'], PLUGIN_CATEGORIES)
    binaries.extend(plugin_binaries)
    logger.info(f"Collected {len(plugin_binaries)} GStreamer plugins")

# Collect GStreamer typelibs
gst_typelibs = [
    'Gst-1.0',
    'GstBase-1.0',
    'GstAudio-1.0',
    'GstVideo-1.0',
    'GstPbutils-1.0',
    'GstTag-1.0',
    'GstApp-1.0',
    'GstPlayer-1.0',
    'GstGL-1.0',
    'GstGLEGL-1.0',
    'GstGLWayland-1.0',
    'GstGLX11-1.0',
    'GstAllocators-1.0',
    'GstController-1.0',
    'GstNet-1.0',
    'GstRtp-1.0',
    'GstRtsp-1.0',
    'GstSdp-1.0',
    'GstWebRTC-1.0',
]

if gst_paths['typelibs']:
    for typelib_name in gst_typelibs:
        typelib_file = gst_paths['typelibs'] / f'{typelib_name}.typelib'
        if typelib_file.exists():
            datas.append((str(typelib_file), 'gi_typelibs'))

# Collect GStreamer helper binaries
if sys.platform != 'win32':
    gst_helpers = ['gst-plugin-scanner', 'gst-ptp-helper']
    if gst_paths['lib']:
        libexec_dirs = [
            gst_paths['lib'].parent / 'libexec' / 'gstreamer-1.0',
            gst_paths['lib'] / 'gstreamer-1.0',
        ]
        for libexec_dir in libexec_dirs:
            if libexec_dir.exists():
                for helper in gst_helpers:
                    helper_path = libexec_dir / helper
                    if helper_path.exists():
                        binaries.append((str(helper_path), 'lib/gstreamer-1.0'))
