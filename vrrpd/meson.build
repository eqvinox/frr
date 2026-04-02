vrrpd_sources = [
  # vrrpd/vrrpd
    'vrrp.c',
    'vrrp_arp.c',
    'vrrp_debug.c',
    'vrrp_main.c',
    'vrrp_ndisc.c',
    'vrrp_northbound.c',
    'vrrp_packet.c',
    clippy.process('vrrp_vty.c'),
    'vrrp_zebra.c',
    yang_embed.process('../yang/frr-vrrpd.yang'),
]

# FIXME: conds: VRRPD
# FIXME: all conds: VRRPD
vrrpd_bin = executable('vrrpd',
  sources: vrrpd_sources,
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
vrrpd_bin_wrap = custom_target('vrrpd_bin_wrap',
  output: ['vrrpd.dep'],
  input: [vrrpd_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
vrrpd_xref = xrelfo.process(vrrpd_bin_wrap)
xrefs += [ vrrpd_xref ]

