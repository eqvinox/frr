libfrrospfapiclient_sources = [
  # ospfclient/libfrrospfapiclient.la
    'ospf_apiclient.c',
]

# FIXME: conds: OSPFCLIENT
# FIXME: all conds: OSPFCLIENT
libfrrospfapiclient = shared_library('frrospfapiclient',
  sources: libfrrospfapiclient_sources,
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
  version: '0.0.0',
  link_with: [
    libfrr,
  ],
)
libfrrospfapiclient_wrap = custom_target('libfrrospfapiclient_wrap',
  output: ['frrospfapiclient.dep'],
  input: [libfrrospfapiclient],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
frrospfapiclient_xref = xrelfo.process(libfrrospfapiclient_wrap)
xrefs += [ frrospfapiclient_xref ]

ospfclient_sources = [
  # ospfclient/ospfclient
    'ospfclient.c',
]

    # FIXME: lib/libfrr.la !STATIC_BIN
# FIXME: conds: OSPFCLIENT
# FIXME: all conds: OSPFCLIENT
ospfclient_bin = executable('ospfclient',
  sources: ospfclient_sources,
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
    libfrrospfapiclient,
    libfrrospfclient,
    libfrr,
  ],
  export_dynamic: true,
  build_by_default: true,
)

