libsharp_sources = [
  # sharpd/libsharp.a
    'sharp_nht.c',
    'sharp_zebra.c',
    clippy.process('sharp_vty.c'),
    'sharp_logpump.c',
]

# FIXME: conds: SHARPD
# FIXME: all conds: SHARPD
libsharp = static_library('sharp_a',
  sources: libsharp_sources,
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

sharpd_sources = [
  # sharpd/sharpd
    'sharp_main.c',
]

# FIXME: conds: SHARPD
# FIXME: all conds: SHARPD
sharpd_bin = executable('sharpd',
  sources: sharpd_sources,
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
    libsharp,
    libfrr,
  ],
  export_dynamic: true,
)
sharpd_bin_wrap = custom_target('sharpd_bin_wrap',
  output: ['sharpd.dep'],
  input: [sharpd_bin],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
sharpd_xref = xrelfo.process(sharpd_bin_wrap)
xrefs += [ sharpd_xref ]

