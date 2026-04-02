libfrrfpm_pb_sources = [
  # fpm/libfrrfpm_pb.la
    'fpm.h',
    'fpm_pb.h',
    'fpm_pb.c',
    'fpm.pb-c.c',
]

if get_option('fpm') and protobuf
libfrrfpm_pb = shared_library('frrfpm_pb',
  sources: libfrrfpm_pb_sources,
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
)
libfrrfpm_pb_wrap = custom_target('libfrrfpm_pb_wrap',
  output: ['frrfpm_pb.dep'],
  input: [libfrrfpm_pb],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
frrfpm_pb_xref = xrelfo.process(libfrrfpm_pb_wrap)
xrefs += [ frrfpm_pb_xref ]
endif # get_option('fpm') and protobuf

