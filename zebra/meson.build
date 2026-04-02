zebra_snmp_sources = [
  # zebra/zebra_snmp.la
    'zebra_snmp.c',
]

zebra_snmp = shared_module('zebra_snmp',
  sources: zebra_snmp_sources,
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

zebra_fpm_sources = [
  # zebra/zebra_fpm.la
    'zebra_fpm.c',
    'zebra_fpm_netlink.c',
]
if protobuf
  zebra_fpm_sources += [
    'zebra_fpm_protobuf.c',
  ]
endif
if protobuf and get_option('dev-build')
  zebra_fpm_sources += [
    'zebra_fpm_dt.c',
  ]
endif

    # FIXME: fpm/libfrrfpm_pb.la HAVE_PROTOBUF
    # FIXME: qpb/libfrr_pb.la HAVE_PROTOBUF
    # FIXME: ${PROTOBUF_C_LIBS} HAVE_PROTOBUF
if get_option('fpm')
zebra_fpm = shared_module('zebra_fpm',
  sources: zebra_fpm_sources,
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
  build_by_default: true,
)
endif # get_option('fpm')

zebra_cumulus_mlag_sources = [
  # zebra/zebra_cumulus_mlag.la
    'zebra_mlag_private.c',
]

if host_machine.system() == 'linux'
zebra_cumulus_mlag = shared_module('zebra_cumulus_mlag',
  sources: zebra_cumulus_mlag_sources,
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
  build_by_default: true,
)
endif # host_machine.system() == 'linux'

dplane_sample_plugin_sources = [
  # zebra/dplane_sample_plugin.la
    'sample_plugin.c',
]

if get_option('dev-build')
dplane_sample_plugin = shared_module('dplane_sample_plugin',
  sources: dplane_sample_plugin_sources,
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
  build_by_default: true,
)
endif # get_option('dev-build')

dplane_fpm_nl_sources = [
  # zebra/dplane_fpm_nl.la
    clippy.process('dplane_fpm_nl.c'),
]

if host_machine.system() == 'linux'
dplane_fpm_nl = shared_module('dplane_fpm_nl',
  sources: dplane_fpm_nl_sources,
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
  build_by_default: true,
)
endif # host_machine.system() == 'linux'

zebra_dplane_dpdk_sources = [
  # zebra/zebra_dplane_dpdk.la
    'dpdk/zebra_dplane_dpdk.c',
    clippy.process('dpdk/zebra_dplane_dpdk_vty.c'),
]

zebra_dplane_dpdk = shared_module('zebra_dplane_dpdk',
  sources: zebra_dplane_dpdk_sources,
  c_args: [
    '-DHAVE_CONFIG_H',
  ],
  include_directories: [
    incls,
  ],
  dependencies: [
    libyang,
    libjson,
    libdpdk, # FIXME,
  ],
  name_prefix: '',
  build_by_default: true,
)

zebra_sources = [
  # zebra/zebra
    'connected.c',
    clippy.process('debug.c'),
    'if_ioctl.c',
    'if_netlink.c',
    'if_socket.c',
    'if_sysctl.c',
    clippy.process('interface.c'),
    'ioctl.c',
    'ipforward_proc.c',
    'ipforward_sysctl.c',
    'kernel_netlink.c',
    'kernel_socket.c',
    clippy.process('label_manager.c'),
    'main.c',
    'netconf_netlink.c',
    'redistribute.c',
    'router-id.c',
    'rt_netlink.c',
    'ge_netlink.c',
    'rt_socket.c',
    clippy.process('rtadv.c'),
    'rtread_netlink.c',
    'rtread_sysctl.c',
    'rule_netlink.c',
    'rule_socket.c',
    'table_manager.c',
    'tc_netlink.c',
    'tc_socket.c',
    'zapi_msg.c',
    'zebra_affinitymap.c',
    'zebra_dplane.c',
    'zebra_errors.c',
    'zebra_gr.c',
    'zebra_l2.c',
    'zebra_l2_bridge_if.c',
    'zebra_evpn.c',
    'zebra_evpn_mac.c',
    'zebra_evpn_neigh.c',
    'zebra_mlag.c',
    clippy.process('zebra_mlag_vty.c'),
    'zebra_mpls.c',
    'zebra_mpls_netlink.c',
    'zebra_mpls_openbsd.c',
    'zebra_mpls_null.c',
    'zebra_mpls_vty.c',
    'zebra_srv6.c',
    clippy.process('zebra_srv6_vty.c'),
    'zebra_mroute.c',
    'zebra_nb.c',
    'zebra_nb_config.c',
    'zebra_nb_rpcs.c',
    'zebra_nb_state.c',
    'zebra_netns_id.c',
    'zebra_netns_notify.c',
    'zebra_nhg.c',
    'zebra_ns.c',
    'zebra_opaque.c',
    'zebra_pbr.c',
    'zebra_ptm.c',
    'zebra_ptm_redistribute.c',
    'zebra_pw.c',
    'zebra_rib.c',
    'zebra_router.c',
    'zebra_rnh.c',
    clippy.process('zebra_routemap.c'),
    'zebra_routemap_nb.c',
    'zebra_routemap_nb_config.c',
    'zebra_script.c',
    'zebra_srte.c',
    'zebra_tc.c',
    'zebra_trace.c',
    clippy.process('zebra_vrf.c'),
    clippy.process('zebra_vty.c'),
    'zebra_vxlan.c',
    'zebra_vxlan_if.c',
    'zebra_evpn_mh.c',
    'zebra_neigh.c',
    clippy.process('zserv.c'),
    yang_embed.process('../yang/frr-zebra.yang'),
    yang_embed.process('../yang/frr-zebra-route-map.yang'),
]
if get_option('netlink-debug')
  zebra_sources += [
    'debug_nl.c',
  ]
endif

    # FIXME: mlag/libmlag_pb.la HAVE_PROTOBUF3
    # FIXME: ${PROTOBUF_C_LIBS} HAVE_PROTOBUF3
zebra_bin = executable('zebra',
  sources: zebra_sources,
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
zebra_bin_wrap = custom_target('zebra_bin_wrap',
  output: ['zebra.dep'],
  input: [zebra_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
zebra_xref = xrelfo.process(zebra_bin_wrap)
xrefs += [ zebra_xref ]

fpm_listener_sources = [
  # zebra/fpm_listener
    'fpm_listener.c',
]

fpm_listener_bin = executable('fpm_listener',
  sources: fpm_listener_sources,
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
fpm_listener_bin_wrap = custom_target('fpm_listener_bin_wrap',
  output: ['fpm_listener.dep'],
  input: [fpm_listener_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
fpm_listener_xref = xrelfo.process(fpm_listener_bin_wrap)
xrefs += [ fpm_listener_xref ]

