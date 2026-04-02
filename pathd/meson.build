libpath_sources = [
  # pathd/libpath.a
    clippy.process('path_cli.c'),
    'path_debug.c',
    'path_errors.c',
    'path_nb.c',
    'path_nb_config.c',
    'path_nb_state.c',
    clippy.process('path_ted.c'),
    'path_zebra.c',
    'pathd.c',
]

libpath = static_library('path_a',
  sources: libpath_sources,
  c_args: [
    '-DHAVE_CONFIG_H',
  ],
  include_directories: [
    incls,
  ],
  dependencies: [
    libyang,
    libjson,
  ],
  build_by_default: true,
)

pathd_pcep_sources = [
  # pathd/pathd_pcep.la
    'path_pcep.c',
    clippy.process('path_pcep_cli.c'),
    'path_pcep_controller.c',
    'path_pcep_debug.c',
    'path_pcep_lib.c',
    'path_pcep_config.c',
    'path_pcep_pcc.c',
]

    # FIXME: -I./pceplib
pathd_pcep = shared_module('pathd_pcep',
  sources: pathd_pcep_sources,
  c_args: [
    '-DHAVE_CONFIG_H',
  ],
  include_directories: [
    incls,
  ],
  dependencies: [
    libyang,
    libjson,
  ],
  name_prefix: '',
  link_with: [
    libpcep_pcc,
  ],
  build_by_default: true,
)

pathd_sources = [
  # pathd/pathd
    'path_main.c',
    yang_embed.process('../yang/frr-pathd.yang'),
]

pathd_bin = executable('pathd',
  sources: pathd_sources,
  c_args: [
    '-DHAVE_CONFIG_H',
  ],
  include_directories: [
    incls,
  ],
  dependencies: [
    libyang,
    libjson,
    libm,
    libcap,
  ],
  link_with: [
    libpath,
    libfrr,
  ],
  export_dynamic: true,
)
pathd_bin_wrap = custom_target('pathd_bin_wrap',
  output: ['pathd.dep'],
  input: [pathd_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
pathd_xref = xrelfo.process(pathd_bin_wrap)
xrefs += [ pathd_xref ]

