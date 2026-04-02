libpcep_pcc_sources = [
  # pceplib/libpcep_pcc.la
    'pcep_msg_messages.c',
    'pcep_msg_objects.c',
    'pcep_msg_tlvs.c',
    'pcep_msg_tools.c',
    'pcep_msg_messages_encoding.c',
    'pcep_msg_objects_encoding.c',
    'pcep_msg_tlvs_encoding.c',
    'pcep_msg_object_error_types.c',
    'pcep_pcc_api.c',
    'pcep_session_logic.c',
    'pcep_session_logic_loop.c',
    'pcep_session_logic_states.c',
    'pcep_session_logic_counters.c',
    'pcep_socket_comm_loop.c',
    'pcep_socket_comm.c',
    'pcep_timers_event_loop.c',
    'pcep_timers.c',
    'pcep_utils_counters.c',
    'pcep_utils_double_linked_list.c',
    'pcep_utils_logging.c',
    'pcep_utils_memory.c',
    'pcep_utils_ordered_list.c',
    'pcep_utils_queue.c',
]

libpcep_pcc = shared_library('pcep_pcc',
  sources: libpcep_pcc_sources,
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
)
libpcep_pcc_wrap = custom_target('libpcep_pcc_wrap',
  output: ['pcep_pcc.dep'],
  input: [libpcep_pcc],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
pcep_pcc_xref = xrelfo.process(libpcep_pcc_wrap)
xrefs += [ pcep_pcc_xref ]

libsocket_comm_mock_sources = [
  # pceplib/libsocket_comm_mock.la
]
if false
  libsocket_comm_mock_sources += [
    'pcep_socket_comm_mock.c',
  ]
endif

libsocket_comm_mock = shared_library('socket_comm_mock',
  sources: libsocket_comm_mock_sources,
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
)
libsocket_comm_mock_wrap = custom_target('libsocket_comm_mock_wrap',
  output: ['socket_comm_mock.dep'],
  input: [libsocket_comm_mock],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
socket_comm_mock_xref = xrelfo.process(libsocket_comm_mock_wrap)
xrefs += [ socket_comm_mock_xref ]

pcep_pcc_sources = [
  # pceplib/pcep_pcc
    'pcep_pcc.c',
]

pcep_pcc_bin = executable('pcep_pcc',
  sources: pcep_pcc_sources,
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
    libpcep_pcc,
    libfrr,
  ],
  export_dynamic: true,
  build_by_default: true,
)

