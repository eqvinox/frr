nhrpd_sources = [
  # nhrpd/nhrpd
    'linux.c',
    'netlink_arp.c',
    'nhrp_cache.c',
    'nhrp_errors.c',
    'nhrp_event.c',
    'nhrp_interface.c',
    'nhrp_main.c',
    'nhrp_nhs.c',
    'nhrp_packet.c',
    'nhrp_peer.c',
    'nhrp_multicast.c',
    'nhrp_route.c',
    'nhrp_shortcut.c',
    'nhrp_vc.c',
    clippy.process('nhrp_vty.c'),
    'reqid.c',
    'vici.c',
    'zbuf.c',
    'znl.c',
]

# FIXME: conds: NHRPD
# FIXME: all conds: NHRPD
nhrpd_bin = executable('nhrpd',
  sources: nhrpd_sources,
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
    libfrrcares,
  ],
  export_dynamic: true,
)
nhrpd_bin_wrap = custom_target('nhrpd_bin_wrap',
  output: ['nhrpd.dep'],
  input: [nhrpd_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
nhrpd_xref = xrelfo.process(nhrpd_bin_wrap)
xrefs += [ nhrpd_xref ]

