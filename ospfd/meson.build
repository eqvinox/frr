libfrrospf_sources = [
  # ospfd/libfrrospf.a
    'ospf_abr.c',
    'ospf_api.c',
    'ospf_apiserver.c',
    'ospf_asbr.c',
    'ospf_ase.c',
    'ospf_bfd.c',
    clippy.process('ospf_dump.c'),
    'ospf_dump_api.c',
    'ospf_errors.c',
    'ospf_ext.c',
    'ospf_flood.c',
    clippy.process('ospf_gr.c'),
    'ospf_ia.c',
    'ospf_interface.c',
    'ospf_ism.c',
    clippy.process('ospf_ldp_sync.c'),
    'ospf_lsa.c',
    'ospf_lsdb.c',
    'ospf_memory.c',
    'ospf_neighbor.c',
    'ospf_network.c',
    'ospf_nsm.c',
    'ospf_opaque.c',
    'ospf_packet.c',
    'ospf_ri.c',
    'ospf_route.c',
    'ospf_routemap.c',
    'ospf_routemap_nb.c',
    'ospf_routemap_nb_config.c',
    'ospf_spf.c',
    'ospf_ti_lfa.c',
    'ospf_sr.c',
    'ospf_te.c',
    clippy.process('ospf_vty.c'),
    'ospf_zebra.c',
    'ospfd.c',
    'ospf_gr_helper.c',
    'ospf_auth.c',
]

# FIXME: conds: OSPFD
# FIXME: all conds: OSPFD
libfrrospf = static_library('frrospf_a',
  sources: libfrrospf_sources,
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

libfrrospfclient_sources = [
  # ospfd/libfrrospfclient.a
    'ospf_api.c',
    'ospf_dump_api.c',
]

# FIXME: conds: OSPFD
# FIXME: all conds: OSPFD
libfrrospfclient = static_library('frrospfclient_a',
  sources: libfrrospfclient_sources,
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

ospfd_snmp_sources = [
  # ospfd/ospfd_snmp.la
    'ospf_snmp.c',
]

# FIXME: conds: OSPFD
# FIXME: all conds: OSPFD && SNMP
ospfd_snmp = shared_module('ospfd_snmp',
  sources: ospfd_snmp_sources,
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

ospfd_sources = [
  # ospfd/ospfd
    'ospf_main.c',
    yang_embed.process('../yang/frr-ospf-route-map.yang'),
]

# FIXME: conds: OSPFD
# FIXME: all conds: OSPFD
ospfd_bin = executable('ospfd',
  sources: ospfd_sources,
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
    libfrrospf,
    libfrrospfclient,
    libfrr,
  ],
  export_dynamic: true,
)
ospfd_bin_wrap = custom_target('ospfd_bin_wrap',
  output: ['ospfd.dep'],
  input: [ospfd_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
ospfd_xref = xrelfo.process(ospfd_bin_wrap)
xrefs += [ ospfd_xref ]

