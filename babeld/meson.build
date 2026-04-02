babeld_sources = [
  # babeld/babeld
    'babel_errors.c',
    'babel_filter.c',
    clippy.process('babel_interface.c'),
    'babel_main.c',
    'babel_zebra.c',
    clippy.process('babeld.c'),
    'kernel.c',
    'message.c',
    'neighbour.c',
    'net.c',
    'resend.c',
    'route.c',
    'source.c',
    'util.c',
    'xroute.c',
]

# FIXME: conds: BABELD
# FIXME: all conds: BABELD
babeld_bin = executable('babeld',
  sources: babeld_sources,
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
babeld_bin_wrap = custom_target('babeld_bin_wrap',
  output: ['babeld.dep'],
  input: [babeld_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
babeld_xref = xrelfo.process(babeld_bin_wrap)
xrefs += [ babeld_xref ]

