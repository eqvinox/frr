vtysh_sources = [
  clippy.process('vtysh.c'),

  'vtysh_main.c',
  'vtysh_user.c',
  'vtysh_config.c',

  frr_xref,
]

vtysh_bin = executable('vtysh',
  sources : vtysh_sources, 
  c_args : ['-DHAVE_CONFIG_H', '-DVTYSH_PAGER="less"'],
  include_directories: incls,
  link_with: [
    libfrr,
  ],
  dependencies : [
    libreadline,
  ],
  build_by_default: false,
)
