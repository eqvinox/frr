libpbr_sources = [
  # pbrd/libpbr.a
    'pbr_zebra.c',
    clippy.process('pbr_vty.c'),
    'pbr_map.c',
    'pbr_memory.c',
    'pbr_nht.c',
    clippy.process('pbr_debug.c'),
    'pbr_vrf.c',
]

# FIXME: conds: PBRD
# FIXME: all conds: PBRD
libpbr = static_library('pbr_a',
  sources: libpbr_sources,
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

pbrd_sources = [
  # pbrd/pbrd
    'pbr_main.c',
]

# FIXME: conds: PBRD
# FIXME: all conds: PBRD
pbrd_bin = executable('pbrd',
  sources: pbrd_sources,
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
    libpbr,
    libfrr,
  ],
  export_dynamic: true,
)
pbrd_bin_wrap = custom_target('pbrd_bin_wrap',
  output: ['pbrd.dep'],
  input: [pbrd_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
pbrd_xref = xrelfo.process(pbrd_bin_wrap)
xrefs += [ pbrd_xref ]

