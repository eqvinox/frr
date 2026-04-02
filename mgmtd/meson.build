libmgmtd_sources = [
  # mgmtd/libmgmtd.a
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
]

libmgmtd = static_library('mgmtd_a',
  sources: libmgmtd_sources,
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

libmgmt_be_nb_sources = [
  # mgmtd/libmgmt_be_nb.la
    'mgmt_be_nb.c',
    clippy.process('../zebra/zebra_cli.c'),
]
if true
  libmgmt_be_nb_sources += [
    clippy.process('../ripd/rip_cli.c'),
  ]
endif
if true
  libmgmt_be_nb_sources += [
    clippy.process('../ripngd/ripng_cli.c'),
  ]
endif
if true
  libmgmt_be_nb_sources += [
    clippy.process('../staticd/static_vty.c'),
  ]
endif

libmgmt_be_nb = shared_library('mgmt_be_nb',
  sources: libmgmt_be_nb_sources,
  c_args: [
    '-DHAVE_CONFIG_H',
    '-DINCLUDE_MGMTD_CMDDEFS_ONLY',
    '-DINCLUDE_MGMTD_CMDDEFS_ONLY',
  ],
  include_directories: [
    incls,
  ],
  dependencies: [
    libyang,
    libjson,
  ],
  version: '0.0.0',
  build_by_default: true,
)

mgmtd_sources = [
  # mgmtd/mgmtd
    'mgmt_main.c',
    yang_embed.process('../yang/frr-zebra.yang'),
    yang_embed.process('../yang/frr-zebra-route-map.yang'),
    yang_embed.process('../yang/ietf/ietf-netconf.yang'),
    yang_embed.process('../yang/ietf/ietf-netconf-with-defaults.yang'),
]
if true
  mgmtd_sources += [
    yang_embed.process('../yang/frr-bfdd.yang'),
    yang_embed.process('../yang/frr-staticd.yang'),
  ]
endif
if not true
  mgmtd_sources += [
    yang_embed.process('../yang/frr-bfdd.yang'),
  ]
endif
if true
  mgmtd_sources += [
    yang_embed.process('../yang/frr-ripd.yang'),
  ]
endif
if true
  mgmtd_sources += [
    yang_embed.process('../yang/frr-ripngd.yang'),
  ]
endif

mgmtd_bin = executable('mgmtd',
  sources: mgmtd_sources,
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
    libm,
  ],
  link_with: [
    libmgmtd,
    libfrr,
    libmgmt_be_nb,
  ],
  export_dynamic: true,
)
mgmtd_bin_wrap = custom_target('mgmtd_bin_wrap',
  output: ['mgmtd.dep'],
  input: [mgmtd_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
mgmtd_xref = xrelfo.process(mgmtd_bin_wrap)
xrefs += [ mgmtd_xref ]

mgmtd_testc_sources = [
  # mgmtd/mgmtd_testc
    'mgmt_testc.c',
]

# FIXME: conds: MGMTD_TESTC
# FIXME: all conds: MGMTD_TESTC
mgmtd_testc_bin = executable('mgmtd_testc',
  sources: mgmtd_testc_sources,
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
    libfrr,
  ],
  export_dynamic: true,
)
mgmtd_testc_bin_wrap = custom_target('mgmtd_testc_bin_wrap',
  output: ['mgmtd_testc.dep'],
  input: [mgmtd_testc_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
mgmtd_testc_xref = xrelfo.process(mgmtd_testc_bin_wrap)
xrefs += [ mgmtd_testc_xref ]

