libmgmt_be_nb_sources = [
  'mgmt_be_nb.c',
  clippy.process('../zebra/zebra_cli.c'),
]

mgmtd_sources = [
  yang_embed.process('../yang/frr-zebra.yang'),
  yang_embed.process('../yang/frr-zebra-route-map.yang'),
  yang_embed.process('../yang/ietf/ietf-netconf.yang'),
  yang_embed.process('../yang/ietf/ietf-netconf-with-defaults.yang'),

  'mgmt.c',
  'mgmt_ds.c',
  'mgmt_be_adapter.c',
  'mgmt_fe_adapter.c',
  'mgmt_history.c',
  'mgmt_memory.c',
  'mgmt_txn.c',
  'mgmt_txn_cfg.c',
  clippy.process('mgmt_vty.c'),
  'mgmt_vty_frontend.c',

  'mgmt_main.c',
]

libmgmt_be_nb = library('mgmt_be_nb',
  sources: libmgmt_be_nb_sources,
  c_args : ['-DHAVE_CONFIG_H', '-DINCLUDE_MGMTD_CMDDEFS_ONLY'],
  include_directories : incls,
  link_with: [
    libfrr,
  ],
  dependencies : [
    libyang,
  ],
)

mgmtd_bin = executable('mgmtd',
  sources : mgmtd_sources, 
  c_args : ['-DHAVE_CONFIG_H'],
  include_directories: incls,
  link_with: [
    libmgmt_be_nb,
    libfrr,
  ],
  dependencies : [
    libyang,
    libjson,
  ],
)

mgmtd_bin_wrap = custom_target('mgmtd_bin_wrap',
  output: ['mgmtd.dep'],
  input: [mgmtd_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
mgmtd_xref = xrelfo.process(mgmtd_bin_wrap)

