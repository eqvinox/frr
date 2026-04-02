libldp_sources = [
  # ldpd/libldp.a
    'accept.c',
    'address.c',
    'adjacency.c',
    'control.c',
    'hello.c',
    'imsg.c',
    'imsg-buffer.c',
    'init.c',
    'interface.c',
    'keepalive.c',
    'l2vpn.c',
    'labelmapping.c',
    'lde.c',
    'lde_lib.c',
    'ldp_debug.c',
    clippy.process('ldp_vty_cmds.c'),
    'ldp_vty_conf.c',
    'ldp_vty_exec.c',
    'ldp_zebra.c',
    'ldpe.c',
    'logmsg.c',
    'neighbor.c',
    'notification.c',
    'packet.c',
    'pfkey.c',
    'rlfa.c',
    'socket.c',
    'util.c',
]

# FIXME: conds: LDPD
# FIXME: all conds: LDPD
libldp = static_library('ldp_a',
  sources: libldp_sources,
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

ldpd_snmp_sources = [
  # ldpd/ldpd_snmp.la
    'ldp_snmp.c',
]

ldpd_snmp = shared_module('ldpd_snmp',
  sources: ldpd_snmp_sources,
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

ldpd_sources = [
  # ldpd/ldpd
    'ldpd.c',
]

# FIXME: conds: LDPD
# FIXME: all conds: LDPD
ldpd_bin = executable('ldpd',
  sources: ldpd_sources,
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
    libldp,
    libfrr,
  ],
  export_dynamic: true,
)
ldpd_bin_wrap = custom_target('ldpd_bin_wrap',
  output: ['ldpd.dep'],
  input: [ldpd_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
ldpd_xref = xrelfo.process(ldpd_bin_wrap)
xrefs += [ ldpd_xref ]

