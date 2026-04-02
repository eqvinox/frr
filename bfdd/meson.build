libbfd_sources = [
  # bfdd/libbfd.a
    'bfd.c',
    'bfdd_nb.c',
    'bfdd_nb_config.c',
    'bfdd_nb_state.c',
    clippy.process('bfdd_vty.c'),
    clippy.process('bfdd_cli.c'),
    'bfd_packet.c',
    'dplane.c',
    'event.c',
    'ptm_adapter.c',
    'bfd_trace.c',
]

# FIXME: conds: BFDD
# FIXME: all conds: BFDD
libbfd = static_library('bfd_a',
  sources: libbfd_sources,
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

bfdd_sources = [
  # bfdd/bfdd
    'bfdd.c',
    yang_embed.process('../yang/frr-bfdd.yang'),
]

# FIXME: conds: BFDD
# FIXME: all conds: BFDD
bfdd_bin = executable('bfdd',
  sources: bfdd_sources,
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
  link_with: [
    libbfd,
    libfrr,
  ],
  export_dynamic: true,
)
bfdd_bin_wrap = custom_target('bfdd_bin_wrap',
  output: ['bfdd.dep'],
  input: [bfdd_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
bfdd_xref = xrelfo.process(bfdd_bin_wrap)
xrefs += [ bfdd_xref ]

