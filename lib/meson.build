route_types = custom_target('route_types.h',
  input : ['route_types.txt'],
  output : 'route_types.h',
  depend_files: ['route_types.pl'],
  command : [perl, '@CURRENT_SOURCE_DIR@/route_types.pl'] + rt_enabled,
  #+ ['<', '@INPUT0@'],
  feed: true,
  capture : true,
)
vtysh_daemons = custom_target('vtysh_daemons.h',
  input : ['../vtysh/daemons.pl'],
  output : 'vtysh_daemons.h',
  command : [perl, '@INPUT0@'] + vtysh_daemons,
  capture : true,
)

#mgmt_pb = custom_target('mgmt.pb-c.c',
#  input : ['mgmt.proto'],
#  output : ['mgmt.pb-c.c', 'mgmt.pb-c.h'],
#  command : [protoc_c, '-I@SOURCE_ROOT@', '--c_out=@BUILD_ROOT@', '@INPUT@'],
#)

#lex = find_program('flex', 'lex')
#yacc = find_program('bison', 'yacc', 'byacc')

defun_lex = custom_target('defun_lex',
  output: [ 'defun_lex.c' ],
  input: 'defun_lex.l',
  command: [lex, '@INPUT@'],
)

command_lex = custom_target('command_lex',
  output: [ 'command_lex.c', 'command_lex.h' ],
  input: 'command_lex.l',
  command: [lex, '@INPUT@'],
)

command_parse = custom_target('command_parse',
  output: [ 'command_parse.c', 'command_parse.h' ],
  input: 'command_parse.y',
  command: [yacc,
    '-d', '-Dapi.prefix={cmd_yy}', '-Dparse.error=verbose', '-Wno-yacc',
    '@INPUT@'],
)

python = import('python')
py3 = python.find_installation('python3')

yang_embed = generator(py3,
  output: ['@PLAINNAME@.c'],
  arguments: ['../yang/embedmodel.py', '@INPUT@', '@OUTPUT@'],
)

build_cc = meson.get_compiler('c', native : true)
libelf = build_cc.find_library('elf')

clippy_sources = [
  route_types,

  'jhash.c',
  'clippy.c',
  'command_graph.c',
  command_lex,
  command_parse,
  'command_py.c',
  defun_lex,
  'elf_py.c',
  'graph.c',
  'libfrr_trace.c',
  'memory.c',
  'typesafe.c',
  'vector.c',
]

#py3dep = py3.dependency(embed : true)
py3dep = dependency('python3-embed', native: true)
clippy_bin = executable('clippy',
  sources : clippy_sources, 
  include_directories : incls_noassert,
  native : true,
  dependencies : [py3dep, libelf],
  c_args : '-DBUILDING_CLIPPY',
)

#clippymeson = import('clippymeson')
#clippy = clippymeson.setup(clippy_bin)

clippy = generator(clippy_bin,
  output: ['@BASENAME@.c'],
  #  depends: ['../python/clidef.py'],
  arguments: ['../python/clidef.py', '--meson', '@OUTPUT0@', '-o', '@BASENAME@_clippy.c', '@INPUT@'],
)
#clippy_if_h = custom_target('if_clippy.h',
#  output: [ 'if_clippy.c' ],
#  input: 'if.c',
#  command: [ clippy, '../python/clidef.py', '-o', '@OUTPUT', '@INPUT@' ],
#)
libfrr_sources = [
  route_types,
  vtysh_daemons,

  'admin_group.c',
  'affinitymap.c',
  clippy.process('affinitymap_cli.c'),
  'affinitymap_northbound.c',
  'agg_table.c',
  'asn.c',
  'atomlist.c',
  'base64.c',
  'bfd.c',
  'buffer.c',
  'checksum.c',
  'command.c',
  'command_graph.c',
  command_lex,
  'command_match.c',
  command_parse,
  'cspf.c',
  'csv.c',
  'darr.c',
  'debug.c',
  'defaults.c',
  'distribute.c',
  clippy.process('event.c'),
  'explicit_bzero.c',
  'ferr.c',
  'filter.c',
  clippy.process('filter_cli.c'),
  'filter_nb.c',
  'flex_algo.c',
  'frr_pthread.c',
  'frrcu.c',
  'frrlua.c',
  'frrscript.c',
  'frrstr.c',
  'grammar_sandbox.c',
  'graph.c',
  'hash.c',
  'hook.c',
  clippy.process('host_cli.c'),
  'host_nb.c',
  'id_alloc.c',
  clippy.process('if.c'),
  clippy.process('if_rmap.c'),
  'iso.c',
  'jhash.c',
  'json.c',
  'keychain.c',
  clippy.process('keychain_cli.c'),
  'keychain_nb.c',
  'ldp_sync.c',
  'lib_errors.c',
  'lib_vty.c',
  'libagentx.c',
  'libfrr.c',
  'libfrr_trace.c',
  'link_state.c',
  'linklist.c',
  'log.c',
  'log_nb.c',
  clippy.process('log_cli.c'),
  'log_filter.c',
  clippy.process('log_vty.c'),
  'md5.c',
  'memory.c',
  clippy.process('mgmt_be_client.c'),
  clippy.process('mgmt_fe_client.c'),
  'mgmt_msg.c',
  'mgmt_msg_native.c',
  'mlag.c',
  'module.c',
  'mpls.c',
  'netlink_parser.c',
  'netns_linux.c',
  'netns_other.c',
  'network.c',
  'nexthop.c',
  clippy.process('nexthop_group.c'),
  'northbound.c',
  clippy.process('northbound_cli.c'),
  'northbound_db.c',
  'northbound_notif.c',
  'northbound_oper.c',
  'ntop.c',
  'openbsd-tree.c',
  'pid_output.c',
  clippy.process('plist.c'),
  'prefix.c',
  'printf/glue.c',
  'printf/printf-pos.c',
  'printf/vfprintf.c',
  'privs.c',
  'ptm_lib.c',
  'pullwr.c',
  'qobj.c',
  'ringbuf.c',
  clippy.process('routemap.c'),
  clippy.process('routemap_cli.c'),
  'routemap_northbound.c',
  'routing_nb.c',
  'routing_nb_config.c',
  'sbuf.c',
  'segment_routing.c',
  'seqlock.c',
  'sha256.c',
  'sigevent.c',
  'skiplist.c',
  'sockopt.c',
  'sockunion.c',
  'spf_backoff.c',
  'srcdest_table.c',
  'srv6.c',
  'stream.c',
  'strformat.c',
  'strlcat.c',
  'strlcpy.c',
  'systemd.c',
  'table.c',
  'tc.c',
  'termtable.c',
  'typerb.c',
  'typesafe.c',
  'vector.c',
  'vrf.c',
  clippy.process('vty.c'),
  'wheel.c',
  'workqueue.c',
  'xref.c',
  'yang.c',
  'yang_translator.c',
  'yang_wrappers.c',
  'zclient.c',
  'zlog.c',
  'zlog_5424.c',
  clippy.process('zlog_5424_cli.c'),
  'zlog_live.c',
  'zlog_recirculate.c',
  'zlog_targets.c',

	yang_embed.process('../yang/frr-affinity-map.yang'),
	yang_embed.process('../yang/frr-backend.yang'),
	yang_embed.process('../yang/frr-filter.yang'),
	yang_embed.process('../yang/frr-host.yang'),
	yang_embed.process('../yang/frr-if-rmap.yang'),
	yang_embed.process('../yang/frr-interface.yang'),
	yang_embed.process('../yang/frr-logging.yang'),
	yang_embed.process('../yang/frr-route-map.yang'),
	yang_embed.process('../yang/frr-route-types.yang'),
	yang_embed.process('../yang/frr-vrf.yang'),
	yang_embed.process('../yang/frr-routing.yang'),
	yang_embed.process('../yang/frr-nexthop.yang'),
	yang_embed.process('../yang/ietf/frr-deviations-ietf-key-chain.yang'),
	yang_embed.process('../yang/ietf/ietf-routing-types.yang'),
	yang_embed.process('../yang/ietf/ietf-syslog-types.yang'),
	yang_embed.process('../yang/ietf/ietf-netconf-acm.yang'),
	yang_embed.process('../yang/ietf/ietf-key-chain.yang'),
	yang_embed.process('../yang/ietf/ietf-interfaces.yang'),
	yang_embed.process('../yang/ietf/ietf-bgp-types.yang'),
	yang_embed.process('../yang/frr-module-translator.yang'),
	yang_embed.process('../yang/ietf/ietf-srv6-types.yang'),
]

libfrr = shared_library('frr',
  #mgmt_pb,
  sources : libfrr_sources,
  c_args : ['-DHAVE_CONFIG_H'],
  include_directories : incls,
  dependencies : [
    libyang,
    libjson,
    libm,
    libcrypt,
  ],
  #link_args: ['-Xlinker', '-e_libfrr_version'],
  link_args: ['-Xlinker', '-e_libfrr_start', '../crt_frr.o'],
  soversion: '10_7_0',
  install: true,
  install_dir: frrlibdir,
)

xrelfo = generator(clippy_bin,
  output: ['@PLAINNAME@.xref'],
  #  depends: ['../python/clidef.py'],
  arguments: ['../python/xrelfo.py', '-Werror', '-Wlog-format', '-Wlog-args', '-o', '@OUTPUT0@', '@INPUT@'],
)

libfrr_wrap = custom_target('libfrr_wrap',
  output: ['libfrr.so.dep'],
  input: [libfrr],
  command: ['ln', '-sf', '@PLAINNAME@', '@OUTPUT@'],
)
libfrr_xref = xrelfo.process(libfrr_wrap)

libfrrsnmp_sources = [
  # lib/libfrrsnmp.la
  'agentx.c',
  'snmp.c',
]

libfrrsnmp = shared_library('frrsnmp',
  sources: libfrrsnmp_sources,
  c_args: [
    '-DHAVE_CONFIG_H',
    '-std=gnu11',
  ],
  include_directories: [
    incls,
  ],
  dependencies: [
    snmp,
    libyang,
    libjson,
  ],
  version: '0.0.0'
)

libfrrcares_sources = [
  # lib/libfrrcares.la
  'resolver.c',
]

libfrrcares = shared_library('frrcares',
  sources: libfrrcares_sources,
  c_args: [
    '-DHAVE_CONFIG_H',
  ],
  include_directories: [
    incls,
  ],
  dependencies: [
    libyang,
    libjson,
    libcares,
  ],
  version: '0.0.0'
)
