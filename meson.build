project('albasheer',
          version: '2.0',
    meson_version: '>= 0.59.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

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

python = import('python')
py_sources = [
    'albasheer/core.py',
    'albasheer/gtkUi.py',
    'albasheer/__init__.py',
    'albasheer/univaruints.py'
]
python.find_installation('python3').install_sources(py_sources,
  subdir: 'albasheer',
)

data_folders = [
                 [join_paths(get_option('datadir'),'albasheer'), ['tilawa_json_files']]
               ]

foreach folder_ : data_folders
  foreach i : folder_[1]
    install_subdir(
      i,
      install_dir : folder_[0]
  )
  endforeach
endforeach

install_data(
    'albasheer-browser',
    install_mode: 'rwxr-xr-x',
    install_dir : get_option('bindir')
)

i18n = import('i18n')
desktop_file = i18n.merge_file(
        input: 'albasheer.desktop.in',
       output: 'albasheer.desktop',
         type: 'desktop',
       po_dir: 'po',
      install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)
  
subdir('po')

