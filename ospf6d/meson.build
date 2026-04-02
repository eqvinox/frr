libospf6_sources = [
  # ospf6d/libospf6.a
    clippy.process('ospf6_nssa.c'),
    'ospf6_abr.c',
    clippy.process('ospf6_area.c'),
    clippy.process('ospf6_asbr.c'),
    'ospf6_routemap_nb.c',
    'ospf6_routemap_nb_config.c',
    'ospf6_bfd.c',
    'ospf6_flood.c',
    clippy.process('ospf6_gr.c'),
    clippy.process('ospf6_gr_helper.c'),
    clippy.process('ospf6_interface.c'),
    'ospf6_intra.c',
    clippy.process('ospf6_lsa.c'),
    'ospf6_lsdb.c',
    'ospf6_message.c',
    clippy.process('ospf6_neighbor.c'),
    'ospf6_network.c',
    'ospf6_proto.c',
    clippy.process('ospf6_route.c'),
    'ospf6_spf.c',
    clippy.process('ospf6_top.c'),
    'ospf6_zebra.c',
    clippy.process('ospf6d.c'),
    'ospf6_auth_trailer.c',
]

# FIXME: conds: OSPF6D
# FIXME: all conds: OSPF6D
libospf6 = static_library('ospf6_a',
  sources: libospf6_sources,
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

ospf6d_snmp_sources = [
  # ospf6d/ospf6d_snmp.la
    'ospf6_snmp.c',
]

# FIXME: conds: OSPF6D
# FIXME: all conds: OSPF6D && SNMP
ospf6d_snmp = shared_module('ospf6d_snmp',
  sources: ospf6d_snmp_sources,
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

ospf6d_sources = [
  # ospf6d/ospf6d
    'ospf6_main.c',
    yang_embed.process('../yang/frr-ospf-route-map.yang'),
    yang_embed.process('../yang/frr-ospf6-route-map.yang'),
]

# FIXME: conds: OSPF6D
# FIXME: all conds: OSPF6D
ospf6d_bin = executable('ospf6d',
  sources: ospf6d_sources,
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
    libospf6,
    libfrr,
  ],
  export_dynamic: true,
)
ospf6d_bin_wrap = custom_target('ospf6d_bin_wrap',
  output: ['ospf6d.dep'],
  input: [ospf6d_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
ospf6d_xref = xrelfo.process(ospf6d_bin_wrap)
xrefs += [ ospf6d_xref ]

