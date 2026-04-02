isis_sources_sources = [
    'isis_bpf.c',
    'isis_dlpi.c',
    'isis_main.c',
    'isis_pfpacket.c',
]

libisis_sources_sources = [
    'isis_affinitymap.c',
    'isis_adjacency.c',
    'isis_bfd.c',
    'isis_circuit.c',
    'isis_csm.c',
    'isis_dr.c',
    'isis_dynhn.c',
    'isis_errors.c',
    'isis_events.c',
    'isis_flags.c',
    'isis_ldp_sync.c',
    'isis_lfa.c',
    'isis_lsp.c',
    'isis_misc.c',
    'isis_mt.c',
    'isis_pdu.c',
    'isis_pdu_counter.c',
    'isis_redist.c',
    'isis_route.c',
    'isis_routemap.c',
    'isis_spf.c',
    'isis_sr.c',
    'isis_flex_algo.c',
    'isis_srv6.c',
    'isis_te.c',
    'isis_tlvs.c',
    'isis_tx_queue.c',
    'isis_zebra.c',
    'isisd.c',
    'iso_checksum.c',
    'fabricd.c',
]

libisis_sources = [
  # isisd/libisis.a
    libisis_sources_sources,
    'isis_nb.c',
    'isis_nb_config.c',
    'isis_nb_notifications.c',
    'isis_nb_state.c',
    clippy.process('isis_cli.c'),
]

# FIXME: conds: ISISD
# FIXME: all conds: ISISD
libisis = static_library('isis_a',
  sources: libisis_sources,
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

libfabric_sources = [
  # isisd/libfabric.a
    libisis_sources_sources,
    'isis_vty_fabricd.c',
]

# FIXME: conds: FABRICD
# FIXME: all conds: FABRICD
libfabric = static_library('fabric_a',
  sources: libfabric_sources,
  c_args: [
    '-DHAVE_CONFIG_H',
    '-DFABRICD=1',
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

isisd_snmp_sources = [
  # isisd/isisd_snmp.la
    'isis_snmp.c',
]

# FIXME: conds: ISISD
# FIXME: all conds: ISISD && SNMP
isisd_snmp = shared_module('isisd_snmp',
  sources: isisd_snmp_sources,
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

isisd_sources = [
  # isisd/isisd
    isis_sources_sources,
    yang_embed.process('../yang/frr-isisd.yang'),
]

# FIXME: conds: ISISD
# FIXME: all conds: ISISD
isisd_bin = executable('isisd',
  sources: isisd_sources,
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
    libisis,
    libfrr,
  ],
  export_dynamic: true,
)
isisd_bin_wrap = custom_target('isisd_bin_wrap',
  output: ['isisd.dep'],
  input: [isisd_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
isisd_xref = xrelfo.process(isisd_bin_wrap)
xrefs += [ isisd_xref ]

fabricd_sources = [
  # isisd/fabricd
    isis_sources_sources,
]

# FIXME: conds: FABRICD
# FIXME: all conds: FABRICD
fabricd_bin = executable('fabricd',
  sources: fabricd_sources,
  c_args: [
    '-DHAVE_CONFIG_H',
    '-DFABRICD=1',
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
    libfabric,
    libfrr,
  ],
  export_dynamic: true,
)
fabricd_bin_wrap = custom_target('fabricd_bin_wrap',
  output: ['fabricd.dep'],
  input: [fabricd_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
fabricd_xref = xrelfo.process(fabricd_bin_wrap)
xrefs += [ fabricd_xref ]

