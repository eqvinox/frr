pim_common_sources = [
    'pim_addr.c',
    'pim_assert.c',
    'pim_bfd.c',
    'pim_bsm.c',
    'pim_bsr_rpdb.c',
    'pim_cmd_common.c',
    'pim_errors.c',
    'pim_hello.c',
    'pim_iface.c',
    'pim_ifchannel.c',
    'pim_instance.c',
    'pim_int.c',
    'pim_join.c',
    'pim_jp_agg.c',
    'pim_macro.c',
    'pim_memory.c',
    'pim_mroute.c',
    'pim_msg.c',
    'pim_nb.c',
    'pim_nb_config.c',
    'pim_neighbor.c',
    'pim_nht.c',
    'pim_oil.c',
    'pim_pim.c',
    clippy.process('pim_routemap.c'),
    'pim_rp.c',
    'pim_rpf.c',
    'pim_sock.c',
    'pim_ssm.c',
    'pim_dm.c',
    'pim_state_refresh.c',
    'pim_ssmpingd.c',
    'pim_static.c',
    'pim_tib.c',
    'pim_time.c',
    'pim_tlv.c',
    'pim_upstream.c',
    'pim_util.c',
    'pim_vty.c',
    'pim_zebra.c',
    'pim_zlookup.c',
    'pim_vxlan.c',
    'pim_register.c',
    'pimd.c',
]

mtracebis_sources = [
  # pimd/mtracebis
    'mtracebis.c',
    'mtracebis_netlink.c',
    'mtracebis_routeget.c',
]

# FIXME: conds: PIMD
# FIXME: all conds: PIMD
mtracebis_bin = executable('mtracebis',
  sources: mtracebis_sources,
  c_args: [
    '-DHAVE_CONFIG_H',
    '-DPIM_IPV=4',
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
  build_by_default: true,
)

test_igmpv3_join_sources = [
  # pimd/test_igmpv3_join
    'test_igmpv3_join.c',
]

# FIXME: conds: PIMD
# FIXME: all conds: PIMD
test_igmpv3_join_bin = executable('test_igmpv3_join',
  sources: test_igmpv3_join_sources,
  c_args: [
    '-DHAVE_CONFIG_H',
    '-DPIM_IPV=4',
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
  build_by_default: true,
)

pimd_sources = [
  # pimd/pimd
    pim_common_sources,
    'pim_autorp.c',
    clippy.process('pim_cmd.c'),
    'pim_igmp.c',
    'pim_igmp_mtrace.c',
    'pim_igmp_stats.c',
    'pim_igmpv2.c',
    'pim_igmpv3.c',
    'pim_main.c',
    'pim_mlag.c',
    'pim_msdp.c',
    'pim_msdp_packet.c',
    'pim_msdp_socket.c',
    'pim_signals.c',
    'pim_zpthread.c',
    yang_embed.process('../yang/frr-pim.yang'),
    yang_embed.process('../yang/frr-pim-route-map.yang'),
    yang_embed.process('../yang/frr-pim-rp.yang'),
    yang_embed.process('../yang/frr-pim-candidate.yang'),
    yang_embed.process('../yang/frr-gmp.yang'),
]

# FIXME: conds: PIMD
# FIXME: all conds: PIMD
pimd_bin = executable('pimd',
  sources: pimd_sources,
  c_args: [
    '-DHAVE_CONFIG_H',
    '-DPIM_IPV=4',
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
    libfrr,
  ],
  export_dynamic: true,
)
pimd_bin_wrap = custom_target('pimd_bin_wrap',
  output: ['pimd.dep'],
  input: [pimd_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
pimd_xref = xrelfo.process(pimd_bin_wrap)
xrefs += [ pimd_xref ]

pim6d_sources = [
  # pimd/pim6d
    pim_common_sources,
    'pim6_main.c',
    clippy.process('pim6_mld.c'),
    clippy.process('pim6_cmd.c'),
    yang_embed.process('../yang/frr-pim.yang'),
    yang_embed.process('../yang/frr-pim-route-map.yang'),
    yang_embed.process('../yang/frr-pim-rp.yang'),
    yang_embed.process('../yang/frr-pim-candidate.yang'),
    yang_embed.process('../yang/frr-gmp.yang'),
]

# FIXME: conds: PIM6D
# FIXME: all conds: PIM6D
pim6d_bin = executable('pim6d',
  sources: pim6d_sources,
  c_args: [
    '-DHAVE_CONFIG_H',
    '-DPIM_IPV=6',
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
    libfrr,
  ],
  export_dynamic: true,
)
pim6d_bin_wrap = custom_target('pim6d_bin_wrap',
  output: ['pim6d.dep'],
  input: [pim6d_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
pim6d_xref = xrelfo.process(pim6d_bin_wrap)
xrefs += [ pim6d_xref ]

