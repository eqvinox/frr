libstatic_sources = [
  # staticd/libstatic.a
    'static_bfd.c',
    'static_debug.c',
    'static_nht.c',
    'static_routes.c',
    'static_zebra.c',
    'static_vrf.c',
    clippy.process('static_vty.c'),
    'static_nb.c',
    'static_nb_config.c',
    'static_srv6.c',
]

libstatic = static_library('static_a',
  sources: libstatic_sources,
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

staticd_sources = [
  # staticd/staticd
    'static_main.c',
    yang_embed.process('../yang/frr-bfdd.yang'),
    yang_embed.process('../yang/frr-staticd.yang'),
]

staticd_bin = executable('staticd',
  sources: staticd_sources,
  c_args: [
    '-DHAVE_CONFIG_H',
  ],
  include_directories: [
    incls,
  ],
  dependencies: [
    libyang,
    libjson,
    libcap,
  ],
  link_with: [
    libstatic,
    libfrr,
  ],
  export_dynamic: true,
)
staticd_bin_wrap = custom_target('staticd_bin_wrap',
  output: ['staticd.dep'],
  input: [staticd_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
staticd_xref = xrelfo.process(staticd_bin_wrap)
xrefs += [ staticd_xref ]

