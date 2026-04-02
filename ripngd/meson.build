ripngd_sources = [
  # ripngd/ripngd
    'ripng_debug.c',
    'ripng_interface.c',
    'ripng_nexthop.c',
    'ripng_offset.c',
    'ripng_main.c',
    'ripng_nb.c',
    'ripng_nb_config.c',
    'ripng_nb_rpcs.c',
    'ripng_nb_state.c',
    'ripng_peer.c',
    'ripng_route.c',
    'ripng_routemap.c',
    'ripng_zebra.c',
    'ripngd.c',
    yang_embed.process('../yang/frr-ripngd.yang'),
]

ripngd_bin = executable('ripngd',
  sources: ripngd_sources,
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
    libfrr,
  ],
  export_dynamic: true,
)
ripngd_bin_wrap = custom_target('ripngd_bin_wrap',
  output: ['ripngd.dep'],
  input: [ripngd_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
ripngd_xref = xrelfo.process(ripngd_bin_wrap)
xrefs += [ ripngd_xref ]

