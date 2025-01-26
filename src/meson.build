pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'albasheer'
gnome = import('gnome')

gnome.compile_resources('albasheer',
  'albasheer.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'albasheer.in',
  output: 'albasheer',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

albasheer_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'tafasir_w.py',
  'utl.py',
  'tools_bar.py',
  'tilawa_download.py',
  'tilawa_gui.py',
  'tilawa_settings.py',
  'search_window.py',
  'copy_gui.py',
]


install_data(albasheer_sources, install_dir: moduledir)


python = import('python')
py_sources = [
    'albasheer/core.py',
    'albasheer/__init__.py',
    'albasheer/univaruints.py',
]
python.find_installation('python3').install_sources(py_sources,
  subdir: 'albasheerlib',
)

db_sources = [
    'albasheer-data/ix.db',
    'albasheer-data/quran.db',
]
python.find_installation('python3').install_sources(db_sources,
  subdir: 'albasheerlib/albasheer-data',
)

data_folders = [
                 [join_paths(get_option('datadir'),'albasheer','albasheer'), ['tilawa_json_files']]
               ]

foreach folder_ : data_folders
  foreach i : folder_[1]
    install_subdir(
      i,
      install_dir : folder_[0]
  )
  endforeach
endforeach

document_files = ['README',  'README.md', 'README-ar.txt']
install_data(
    document_files,
    install_dir : join_paths(get_option('datadir'),'doc/albasheer')
)

licenses_files = ['LICENSE-en' , 'LICENSE-ar.txt']
install_data(
    document_files,
    install_dir : join_paths(get_option('datadir'),'licenses/albasheer')
)

data_files = [
              ['icons/hicolor/16x16/apps', ['icons/albasheer-16.png'],['albasheer.png']],
              ['icons/hicolor/22x22/apps', ['icons/albasheer-22.png'],['albasheer.png']],
              ['icons/hicolor/24x24/apps', ['icons/albasheer-24.png'],['albasheer.png']],
              ['icons/hicolor/32x32/apps', ['icons/albasheer-36.png'],['albasheer.png']],
              ['icons/hicolor/36x36/apps', ['icons/albasheer-48.png'],['albasheer.png']],
              ['icons/hicolor/48x48/apps', ['icons/albasheer-64.png'],['albasheer.png']],
              ['icons/hicolor/64x64/apps', ['icons/albasheer-72.png'],['albasheer.png']],
              ['icons/hicolor/72x72/apps', ['icons/albasheer-96.png'],['albasheer.png']],
              ['icons/hicolor/96x96/apps', ['icons/albasheer-128.png'],['albasheer.png']],
              ['icons/hicolor/128x128/apps',['icons/albasheer-256.png'],['albasheer.png']],
              ['icons/hicolor/256x256/apps',['icons/albasheer-512.png'],['albasheer.png']],
              ['icons/hicolor/512x512/apps',['icons/albasheer-16.png'],['albasheer.png']],
              ['icons/hicolor/scalable/apps',['albasheer-data/quran-kareem.svg'],['albasheer.svg']],
              ['pixmaps',['icons/albasheer-128.png'],['albasheer.png']],
              ['albasheer',['albasheer-data/ix.db'],['ix.db']],
              ['albasheer',['albasheer-data/quran.db'],['quran.db']],
              ['albasheer',['albasheer-data/quran-kareem.svg'],['quran-kareem.svg']]
              ]
foreach files_ : data_files
  foreach i : files_[1]
    install_data(
      i,
      install_dir : join_paths(get_option('datadir'),files_[0]),
      rename      : files_[2]
  )
  endforeach
endforeach