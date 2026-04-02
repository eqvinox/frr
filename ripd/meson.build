ripd_snmp_sources = [
  # ripd/ripd_snmp.la
    'rip_snmp.c',
]

ripd_snmp = shared_module('ripd_snmp',
  sources: ripd_snmp_sources,
  c_args: [
    '-DHAVE_CONFIG_H',
    '-std=gnu11',
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
    libfrrsnmp,
  ],
  build_by_default: true,
)

ripd_sources = [
  # ripd/ripd
    clippy.process('rip_bfd.c'),
    'rip_debug.c',
    'rip_errors.c',
    'rip_interface.c',
    'rip_offset.c',
    'rip_main.c',
    'rip_nb.c',
    'rip_nb_config.c',
    'rip_nb_rpcs.c',
    'rip_nb_notifications.c',
    'rip_nb_state.c',
    'rip_peer.c',
    'rip_routemap.c',
    'rip_zebra.c',
    'ripd.c',
    yang_embed.process('../yang/frr-ripd.yang'),
    yang_embed.process('../yang/frr-bfdd.yang'),
]

ripd_bin = executable('ripd',
  sources: ripd_sources,
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
ripd_bin_wrap = custom_target('ripd_bin_wrap',
  output: ['ripd.dep'],
  input: [ripd_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
ripd_xref = xrelfo.process(ripd_bin_wrap)
xrefs += [ ripd_xref ]

