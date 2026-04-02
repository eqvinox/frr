watchfrr_sources = [
  # watchfrr/watchfrr
    'watchfrr.c',
    'watchfrr_errors.c',
    clippy.process('watchfrr_vty.c'),
]

# FIXME: conds: WATCHFRR
# FIXME: all conds: WATCHFRR
watchfrr_bin = executable('watchfrr',
  sources: watchfrr_sources,
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
watchfrr_bin_wrap = custom_target('watchfrr_bin_wrap',
  output: ['watchfrr.dep'],
  input: [watchfrr_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
watchfrr_xref = xrelfo.process(watchfrr_bin_wrap)
xrefs += [ watchfrr_xref ]

