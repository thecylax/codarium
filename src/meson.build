pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'codarium'
gnome = import('gnome')

gnome.compile_resources('codarium',
  'codarium.gresource.xml',
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
  input: 'codarium.in',
  output: 'codarium',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

codarium_sources = [
  '__init__.py',
  'main.py',
  'window.py',
]

core_sources = files(
  'core/__init__.py',
  'core/database.py',
  'core/gesture.py'
)

core_blocks = files(
  'core/blocks/block.py',
  'core/blocks/port.py',
)

blocks_resources = files(
  'blocks/sum.json'
)

install_data(codarium_sources, install_dir: moduledir)
install_data(core_sources, install_dir: moduledir / 'core')
install_data(core_blocks, install_dir: moduledir / 'core' / 'blocks')
install_data(blocks_resources, install_dir: moduledir / 'blocks')
