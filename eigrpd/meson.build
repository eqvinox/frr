eigrpd_sources = [
  # eigrpd/eigrpd
    clippy.process('eigrp_cli.c'),
    'eigrp_dump.c',
    'eigrp_errors.c',
    'eigrp_filter.c',
    'eigrp_fsm.c',
    'eigrp_hello.c',
    'eigrp_interface.c',
    'eigrp_main.c',
    'eigrp_metric.c',
    'eigrp_neighbor.c',
    'eigrp_network.c',
    'eigrp_northbound.c',
    'eigrp_packet.c',
    'eigrp_query.c',
    'eigrp_reply.c',
    'eigrp_siaquery.c',
    'eigrp_siareply.c',
    'eigrp_snmp.c',
    'eigrp_topology.c',
    'eigrp_update.c',
    'eigrp_vrf.c',
    clippy.process('eigrp_vty.c'),
    'eigrp_zebra.c',
    'eigrpd.c',
    yang_embed.process('../yang/frr-eigrpd.yang'),
]

# FIXME: conds: EIGRPD
# FIXME: all conds: EIGRPD
eigrpd_bin = executable('eigrpd',
  sources: eigrpd_sources,
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
eigrpd_bin_wrap = custom_target('eigrpd_bin_wrap',
  output: ['eigrpd.dep'],
  input: [eigrpd_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
eigrpd_xref = xrelfo.process(eigrpd_bin_wrap)
xrefs += [ eigrpd_xref ]

