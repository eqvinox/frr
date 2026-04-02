libbgp_sources = [
  # bgpd/libbgp.a
    'bgp_addpath.c',
    'bgp_advertise.c',
    'bgp_aspath.c',
    'bgp_attr.c',
    'bgp_attr_evpn.c',
    clippy.process('bgp_bfd.c'),
    'bgp_clist.c',
    'bgp_community.c',
    'bgp_community_alias.c',
    'bgp_conditional_adv.c',
    'bgp_damp.c',
    clippy.process('bgp_debug.c'),
    'bgp_dump.c',
    'bgp_ecommunity.c',
    'bgp_encap_tlv.c',
    'bgp_errors.c',
    'bgp_evpn.c',
    'bgp_evpn_mh.c',
    clippy.process('bgp_evpn_vty.c'),
    'bgp_filter.c',
    'bgp_flowspec.c',
    'bgp_flowspec_util.c',
    'bgp_flowspec_vty.c',
    'bgp_fsm.c',
    'bgp_io.c',
    'bgp_keepalives.c',
    'bgp_label.c',
    clippy.process('bgp_labelpool.c'),
    'bgp_lcommunity.c',
    'bgp_ls.c',
    'bgp_ls_nlri.c',
    'bgp_ls_ted.c',
    'bgp_mac.c',
    'bgp_memory.c',
    'bgp_mpath.c',
    'bgp_mplsvpn.c',
    'bgp_network.c',
    clippy.process('bgp_nexthop.c'),
    'bgp_nht.c',
    'bgp_open.c',
    'bgp_packet.c',
    'bgp_pbr.c',
    'bgp_rd.c',
    'bgp_regex.c',
    clippy.process('bgp_route.c'),
    clippy.process('bgp_routemap.c'),
    'bgp_routemap_nb.c',
    'bgp_routemap_nb_config.c',
    'bgp_script.c',
    'bgp_table.c',
    'bgp_updgrp.c',
    'bgp_updgrp_adv.c',
    'bgp_updgrp_packet.c',
    'bgp_vpn.c',
    clippy.process('bgp_vty.c'),
    'bgp_zebra.c',
    'bgpd.c',
    'bgp_trace.c',
    'bgp_nhg.c',
    'bgp_nhc.c',
    'bgp_srv6.c',
]
  #bgpd/rfapi/vnc_zebra.c ENABLE_BGP_VNC -- FIXME!

# FIXME: conds: BGPD
# FIXME: all conds: BGPD
libbgp = static_library('bgp_a',
  sources: libbgp_sources,
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

bgpd_snmp_sources = [
  # bgpd/bgpd_snmp.la
    'bgp_snmp_bgp4.c',
    'bgp_snmp_bgp4v2.c',
    clippy.process('bgp_snmp.c'),
    'bgp_mplsvpn_snmp.c',
]

# FIXME: conds: BGPD
# FIXME: all conds: BGPD && SNMP
bgpd_snmp = shared_module('bgpd_snmp',
  sources: bgpd_snmp_sources,
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

bgpd_rpki_sources = [
  # bgpd/bgpd_rpki.la
    clippy.process('bgp_rpki.c'),
]

# FIXME: conds: BGPD && RPKI
# FIXME: all conds: BGPD && RPKI
bgpd_rpki = shared_module('bgpd_rpki',
  sources: bgpd_rpki_sources,
  c_args: [
    '-DHAVE_CONFIG_H',
  ],
  include_directories: [
    incls,
  ],
  dependencies: [
    libyang,
    libjson,
    rtrlib,
  ],
  name_prefix: '',
  build_by_default: true,
)

bgpd_bmp_sources = [
  # bgpd/bgpd_bmp.la
    clippy.process('bgp_bmp.c'),
]

# FIXME: conds: BGPD && BGP_BMP
# FIXME: all conds: BGPD && BGP_BMP
bgpd_bmp = shared_module('bgpd_bmp',
  sources: bgpd_bmp_sources,
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
  name_prefix: '',
  link_with: [
    libfrrcares,
  ],
  build_by_default: true,
)

bgp_btoa_sources = [
  # bgpd/bgp_btoa
    'bgp_btoa.c',
]

    # FIXME: bgpd/rfp-example/librfp/librfp.a ENABLE_BGP_VNC
# FIXME: conds: BGPD
# FIXME: all conds: BGPD
bgp_btoa_bin = executable('bgp_btoa',
  sources: bgp_btoa_sources,
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
    libbgp,
    libfrr,
  ],
  export_dynamic: true,
  build_by_default: true,
)

bgpd_sources = [
  # bgpd/bgpd
    'bgp_main.c',
    yang_embed.process('../yang/frr-bgp-types.yang'),
    yang_embed.process('../yang/frr-bgp.yang'),
    yang_embed.process('../yang/frr-bgp-common-structure.yang'),
    yang_embed.process('../yang/frr-bgp-common.yang'),
    yang_embed.process('../yang/frr-bgp-common-multiprotocol.yang'),
    yang_embed.process('../yang/frr-bgp-neighbor.yang'),
    yang_embed.process('../yang/frr-bgp-peer-group.yang'),
    yang_embed.process('../yang/frr-bgp-bmp.yang'),
    yang_embed.process('../yang/frr-bgp-rpki.yang'),
    yang_embed.process('../yang/frr-deviations-bgp-datacenter.yang'),
    yang_embed.process('../yang/frr-bgp-filter.yang'),
    yang_embed.process('../yang/frr-bgp-route-map.yang'),
]

    # FIXME: bgpd/rfp-example/librfp/librfp.a ENABLE_BGP_VNC
# FIXME: conds: BGPD
# FIXME: all conds: BGPD
bgpd_bin = executable('bgpd',
  sources: bgpd_sources,
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
    libbgp,
    libfrr,
  ],
  export_dynamic: true,
)
bgpd_bin_wrap = custom_target('bgpd_bin_wrap',
  output: ['bgpd.dep'],
  input: [bgpd_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
bgpd_xref = xrelfo.process(bgpd_bin_wrap)
xrefs += [ bgpd_xref ]

