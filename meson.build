project('frr', 'c',
  version: '10.7.0-dev',
  meson_version: '>= 1.10.0',
  default_options: {
    'c_std': 'gnu23,gnu2x,gnu17,gnu11,none',
    'warning_level': '2',
    'b_lundef': 'false',
  },
)

pkg_specs = configuration_data()

pkg_specs.set('configure_input',    'version.h generated from lib/version.h.in by meson')
pkg_specs.set('PACKAGE_NAME',       meson.project_name())
pkg_specs.set('PACKAGE_VERSION',    meson.project_version())
pkg_specs.set('PACKAGE_BUGREPORT',  'https://github.com/frrouting/frr/issues')
pkg_specs.set('PACKAGE_URL',        'https://frrouting.org/')
pkg_specs.set('PACKAGE_FULLNAME',   'FRRouting')
pkg_specs.set('CONFIG_ARGS',        '<meson build>')

prefix = get_option('prefix')
frrlibdir = prefix / get_option('libdir') / get_option('frrlibdir')
frrdaemondir = prefix / get_option('frrdaemondir')

pkg_specs.set('e_frr_runstatedir',  prefix / get_option('rundir') / 'frr')
pkg_specs.set('e_frr_libstatedir',  prefix / get_option('sharedstatedir') / 'frr')
pkg_specs.set('e_yangmodelsdir',    prefix / get_option('datadir') / get_option('yangmodelsdir'))
pkg_specs.set('e_moduledir',        frrlibdir / 'modules')
pkg_specs.set('e_scriptdir',        prefix / get_option('sysconfdir') / 'frr' / get_option('scriptdir'))
pkg_specs.set('e_frr_sysconfdir',   prefix / get_option('sysconfdir') / 'frr')
pkg_specs.set('e_vtysh_bin',        prefix / get_option('bindir') / 'vtysh')
pkg_specs.set('e_watchfrr_sh',      frrdaemondir / 'watchfrr.sh')

configure_file(input: 'lib/version.h.in',      build_subdir: 'generated/lib', output: 'version.h',      configuration: pkg_specs)
configure_file(input: 'lib/config_paths.h.in', build_subdir: 'generated/lib', output: 'config_paths.h', configuration: pkg_specs)

add_project_arguments(
  # '-std=gnu23',
  '-fms-extensions',
  '-fno-omit-frame-pointer',
  '-funwind-tables',
  #  '-Wall',
  #  '-Wextra',
  '-Wformat-nonliteral',
  '-Wformat-security',
  '-Wswitch-enum',
  '-Wstrict-prototypes',
  '-Wmissing-prototypes',
  '-Wmissing-declarations',
  '-Wpointer-arith',
  '-Wbad-function-cast',
  '-Wwrite-strings',
  '-Wundef',
  '-Wimplicit-fallthrough',
  '-Wno-unused-parameter',
  '-Wno-missing-field-initializers',
  #  '-Wno-microsoft-anon-tag',
  '-Wno-error=deprecated-declarations',
  language : 'c',
)

add_project_arguments(
  # '-std=gnu23',
  '-fms-extensions',
  '-fno-omit-frame-pointer',
  '-funwind-tables',
  # '-Wall',
  # '-Wextra',
  '-Wformat-nonliteral',
  '-Wformat-security',
  '-Wswitch-enum',
  '-Wstrict-prototypes',
  '-Wmissing-prototypes',
  '-Wmissing-declarations',
  '-Wpointer-arith',
  '-Wbad-function-cast',
  '-Wwrite-strings',
  '-Wundef',
  '-Wimplicit-fallthrough',
  '-Wno-unused-parameter',
  '-Wno-missing-field-initializers',
  #  '-Wno-microsoft-anon-tag',
  '-Wno-error=deprecated-declarations',
  language : 'c',
  native : true,
)

add_project_arguments('-DHAVE_CONFIG_H', language: 'c')
add_project_arguments('-DHAVE_CONFIG_H', language: 'cpp')
if get_option('dev-build')
  today = run_command('date', '+%Y%m%d', check: true).stdout().strip()
  add_project_arguments('-DCONFDATE=' + today, language: 'c')
  add_project_arguments('-DCONFDATE=' + today, language: 'cpp')
else
  add_project_arguments('-DCONFDATE=0', language: 'c')
  add_project_arguments('-DCONFDATE=0', language: 'cpp')
endif

rt_enabled = []
rt_enabled += ['--enabled', 'babeld']
rt_enabled += ['--enabled', 'bfdd']
rt_enabled += ['--enabled', 'bgpd']
rt_enabled += ['--enabled', 'bgpd-vnc']
rt_enabled += ['--enabled', 'eigrpd']
rt_enabled += ['--enabled', 'isisd']
rt_enabled += ['--enabled', 'fabricd']
rt_enabled += ['--enabled', 'ldpd']
rt_enabled += ['--enabled', 'nhrpd']
rt_enabled += ['--enabled', 'ospfd']
rt_enabled += ['--enabled', 'ospf6d']
rt_enabled += ['--enabled', 'pbrd']
rt_enabled += ['--enabled', 'pimd']
rt_enabled += ['--enabled', 'ripd']
rt_enabled += ['--enabled', 'ripngd']
rt_enabled += ['--enabled', 'sharpd']
rt_enabled += ['--enabled', 'zebra']

vtysh_daemons = []
vtysh_daemons += ['babeld']
vtysh_daemons += ['bfdd']
vtysh_daemons += ['bgpd']
vtysh_daemons += ['eigrpd']
vtysh_daemons += ['isisd']
vtysh_daemons += ['fabricd']
vtysh_daemons += ['ldpd']
vtysh_daemons += ['nhrpd']
vtysh_daemons += ['ospfd']
vtysh_daemons += ['ospf6d']
vtysh_daemons += ['pbrd']
vtysh_daemons += ['pimd']
vtysh_daemons += ['ripd']
vtysh_daemons += ['ripngd']
vtysh_daemons += ['sharpd']
vtysh_daemons += ['zebra']


perl = find_program('perl')
lex = find_program('flex', 'lex')
yacc = find_program('bison', 'yacc', 'byacc')

protoc_c = find_program('protoc-c')

p_incls_noassert = ['.', 'lib', 'include', 'generated']
p_incls = ['lib/assert'] + p_incls_noassert

incls_noassert = include_directories(p_incls_noassert)
incls = include_directories(p_incls)

#yacc_gen = custom_target('-d -Dapi.prefix=@BISON_OPENBRACE@cmd_yy@BISON_CLOSEBRACE@ @BISON_VERBOSE@
#

cc = meson.get_compiler('c')

headers = configuration_data()

libyang = dependency('libyang', version: '>= 2.1.128', required: true)
libjson = dependency('json-c', 'json',                required: true)
#if not libjson.found()
#  libjson = cc.find_library('json-c')
#endif

libunwind = dependency('libunwind',                   required: get_option('libunwind'))
headers.set('HAVE_LIBUNWIND', libunwind.found())

libcares = dependency('libcares',                     disabler: true)
snmp =     dependency('netsnmp-agent',                disabler: true, required: get_option('snmp'))
rtrlib =   dependency('rtrlib', version: '>= 0.8.0',  disabler: true, required: get_option('rpki'))
libdpdk =  dependency('libdpdk',                      disabler: true, required: get_option('dp-dpdk'))

libm = cc.find_library('m')
libcrypt = cc.find_library('crypt')
libreadline = cc.find_library('readline')
libcap = cc.find_library('cap')

protobuf = false

sys_includes = ''
sys_includes += '#define _GNU_SOURCE\n'
sys_includes += '#include <pthread.h>\n'

sys_headers = [
  'endian.h',
  'sys/endian.h',
  'malloc.h',
  'malloc/malloc.h',
  'malloc_np.h',
  'pthread_np.h',
]

foreach hdr : sys_headers
  sym = 'HAVE_' + hdr.to_upper().replace('/', '_').replace('.', '_')
  if cc.has_header(hdr)
    headers.set(sym, true)
    sys_includes += '#include <@0@>\n'.format(hdr)
  else
    headers.set(sym, false)
  endif
endforeach

sys_funcs = [
  'be32enc',
  'be32dec',
  'mallinfo',
  'mallinfo2',
  'malloc_usable_size',
  'malloc_size',
  'pthread_setname_np',
  'pthread_set_name_np',
  'pthread_getthreadid_np',
  'pthread_condattr_setclock',
]

foreach func : sys_funcs
  sym = 'HAVE_' + func.to_upper()
  headers.set(sym, cc.has_function(func, prefix: sys_includes))
endforeach

headers.set('HAVE_DECL_BE32DEC', '(!!defined(HAVE_BE32DEC) - 0)')
headers.set('HAVE_DECL_BE32ENC', '(!!defined(HAVE_BE32ENC) - 0)')

headers.set('HAVE_OPENAT',                  cc.has_function('openat', prefix: '#include <fcntl.h>'))
headers.set('HAVE_UNLINKAT',                cc.has_function('unlinkat', prefix: '#include <unistd.h>\n#include <fcntl.h>'))
headers.set('HAVE_POSIX_FALLOCATE',         cc.has_function('posix_fallocate', prefix: '#include <fcntl.h>'))

headers.set('HAVE_POLLTS',                  cc.has_function('pollts', prefix: '#include <poll.h>\n#include <signal.h>\n#include<time.h>'))
headers.set('HAVE_PPOLL',                   cc.has_function('ppoll', prefix: '#define _GNU_SOURCE\n#include <poll.h>'))

headers.set('HAVE_SENDMMSG',                cc.has_function('sendmmsg', prefix: '#define _GNU_SOURCE\n#include <sys/socket.h>'))

headers.set('HAVE_SETNS',                   cc.has_function('setns', prefix: '#define _GNU_SOURCE\n#include <sched.h>'))

headers.set('HAVE_GETGROUPLIST',            cc.has_function('getgrouplist', prefix: '#include <grp.h>'))

headers.set('HAVE_CLOCK_NANOSLEEP',         cc.has_function('clock_nanosleep', prefix: '#include <time.h>'))
headers.set('HAVE_CLOCK_THREAD_CPUTIME_ID', cc.has_header_symbol('time.h', 'CLOCK_THREAD_CPUTIME_ID'))

headers.set('HAVE_EXPLICIT_BZERO',          cc.has_function('explicit_bzero', prefix: '#include <string.h>'))
headers.set('HAVE_STRLCAT',                 cc.has_function('strlcat', prefix: '#include <string.h>'))
headers.set('HAVE_STRLCPY',                 cc.has_function('strlcpy', prefix: '#include <string.h>'))

headers.set('HAVE_INET_ND_H',           cc.has_header('inet/nd.h'))
headers.set('HAVE_LINUX_MROUTE6_H',     cc.has_header('linux/mroute6.h'))
headers.set('HAVE_LINUX_MROUTE_H',      cc.has_header('linux/mroute.h'))
headers.set('HAVE_NETINET6_IN6_VAR_H',  cc.has_header('netinet6/in6_var.h'))
headers.set('HAVE_NETINET6_ND6_H',      cc.has_header('netinet6/nd6.h'))
headers.set('HAVE_NETINET_IN6_VAR_H',   cc.has_header('netinet/in6_var.h'))
headers.set('HAVE_NETINET_IN_VAR_H',    cc.has_header('netinet/in_var.h'))
headers.set('HAVE_NETINET_IP_MROUTE_H', cc.has_header('netinet/ip_mroute.h'))
headers.set('HAVE_NET_IF_DL_H',         cc.has_header('net/if_dl.h'))
headers.set('HAVE_NET_IF_VAR_H',        cc.has_header('net/if_var.h'))
headers.set('HAVE_NET_NETOPT_H',        cc.has_header('net/netopt.h'))
headers.set('HAVE_STDATOMIC_H',         cc.has_header('stdatomic.h'))
headers.set('HAVE_STROPTS_H',           cc.has_header('stropts.h'))
headers.set('HAVE_SYS_CONF_H',          cc.has_header('sys/conf.h'))
headers.set('HAVE_SYS_KSYM_H',          cc.has_header('sys/ksym.h'))
headers.set('HAVE_SYS_SOCKIO_H',        cc.has_header('sys/sockio.h'))
headers.set('HAVE_SYS_SYSCTL_H',        cc.has_header('sys/sysctl.h'))

headers.set('HAVE_LINK_H',              cc.has_header('link.h'))
headers.set('HAVE_UCONTEXT_H',          cc.has_header('ucontext.h'))

headers.set('HAVE_STRUCT_IN_PKTINFO',                         cc.has_member('struct in_pktinfo',   'ipi_addr',      prefix: '#include <netinet/in.h>'))
headers.set('HAVE_STRUCT_IFALIASREQ',                         cc.has_member('struct ifaliasreq',   'ifra_name',     prefix: '#include <net/if.h>'))
headers.set('HAVE_STRUCT_IN6_ALIASREQ',                       cc.has_member('struct in6_aliasreq', 'ifra_name',     prefix: '#include <netinet6/in6_var.h>')) # ???
headers.set('HAVE_STRUCT_IF6_ALIASREQ_IFRA_LIFETIME',         cc.has_member('struct if6_aliasreq', 'ifra_lifetime', prefix: '#include <netinet6/in6_var.h>')) # ???
headers.set('HAVE_STRUCT_IP_MREQN_IMR_IFINDEX',               cc.has_member('struct ip_mreqn',     'imr_ifindex',   prefix: '#include <netinet/in.h>'))
headers.set('HAVE_STRUCT_MMSGHDR_MSG_HDR',                    cc.has_member('struct mmsghdr',      'msg_hdr',       prefix: '#include <sys/socket.h>'))
headers.set('HAVE_STRUCT_UTSNAME_DOMAINNAME',                 cc.has_member('struct utsname',      'domainname',    prefix: '#include <sys/utsname.h>'))

headers.set('HAVE_STRUCT_SOCKADDR_DL',                        cc.has_member('struct sockaddr_dl',  'sdl_family',    prefix: '#include <net/if_dl.h>'))
headers.set('HAVE_STRUCT_SOCKADDR_DL_SDL_LEN',                cc.has_member('struct sockaddr_dl',  'sdl_len',       prefix: '#include <net/if_dl.h>'))
headers.set('HAVE_STRUCT_SOCKADDR_IN_SIN_LEN',                cc.has_member('struct sockaddr_in',  'sin_len',       prefix: '#include <netinet/in.h>'))
headers.set('HAVE_STRUCT_SOCKADDR_SA_LEN',                    cc.has_member('struct sockaddr',     'sa_len',        prefix: '#include <sys/socket>'))
headers.set('HAVE_STRUCT_SOCKADDR_UN_SUN_LEN',                cc.has_member('struct sockaddr_un',  'sun_len',       prefix: '#include <sys/un.h>'))

headers.set('HAVE_STRUCT_ND_OPT_ADV_INTERVAL',                cc.has_member('struct nd_opt_adv_interval',   'nd_opt_adv_interval_type', prefix: '#include <netinet/icmp6.h>'))
headers.set('HAVE_STRUCT_ND_OPT_ADV_INTERVAL_ND_OPT_AI_TYPE', cc.has_member('struct nd_opt_adv_interval',   'nd_opt_ai_type',           prefix: '#include <netinet/icmp6.h>'))
headers.set('HAVE_STRUCT_ND_OPT_DNSSL',                       cc.has_member('struct nd_opt_dnssl',          'nd_opt_dnssl_type',        prefix: '#include <netinet/icmp6.h>'))
headers.set('HAVE_STRUCT_ND_OPT_HOMEAGENT_INFO',              cc.has_member('struct nd_opt_homeagent_info', 'nd_opt_hai_type',          prefix: '#include <netinet/icmp6.h>'))
headers.set('HAVE_STRUCT_ND_OPT_RDNSS',                       cc.has_member('struct nd_opt_rdnss',          'nd_opt_rdnss_type',        prefix: '#include <netinet/icmp6.h>'))

headers.set('HAVE_IP_PKTINFO',      cc.has_header_symbol('netdb.h', 'IP_PKTINFO'))
headers.set('HAVE_IP_RECVDSTADDR',  cc.has_header_symbol('netinet/in.h', 'IP_RECVDSTADDR'))
headers.set('HAVE_IP_RECVIF',       cc.has_header_symbol('netinet/in.h', 'IP_RECVDSTADDR'))
headers.set('HAVE_IP_FREEBIND',     cc.has_header_symbol('netinet/in.h', 'IP_FREEBIND'))
headers.set('HAVE_SO_BINDANY',      cc.has_header_symbol('sys/socket.h', 'SO_BINDANY'))

headers.set('HAVE_DECL_TCP_MD5SIG', 1)

if host_machine.system() == 'linux'
  headers.set('GNU_LINUX',    1)
  headers.set('HAVE_NETLINK', 1)
  headers.set('LINUX_IPV6',   1)
  headers.set('IPV6_MINHOPCOUNT', 73)
endif
headers.set('NETLINK_DEBUG', get_option('netlink-debug'))

headers.set('HAVE_OPENPAM_H',           cc.has_header('openpam.h'))
headers.set('HAVE_PAM_MISC_H',          cc.has_header('pam_misc.h'))

headers.set('_GNU_SOURCE', true)
headers.set('HAVE_SECTION_SYMS', true)

headers.set('MULTIPATH_NUM',            get_option('multipath'))
headers.set_quoted('DFLT_NAME',         get_option('defaults'))

headers.set('CONFIGFILE_MASK',          0o640)
headers.set('LOGFILE_MASK',             0o640)
headers.set('LOG_TIMESTAMP_PRECISION',  6)

headers.set('HAVE_BFDD', 1)

headers.set('DISABLE_BGP_ANNOUNCE', 0)

headers.set('DEV_BUILD', get_option('dev-build'))

headers.set('VTYSH', true)

objcopy = find_program('objcopy')
get_interp = run_command('/bin/sh', files('tools/get_interp.sh'), cc.cmd_array(), env: { 'OBJCOPY': ' '.join(objcopy.cmd_array()) }, check: false)
if get_interp.returncode() == 0
  headers.set_quoted('INTERP', get_interp.stdout().strip())
endif

configure_file(
  output: 'config.h',
  configuration: headers,
)

subdir('lib')
subdir('mgmtd')
subdir('zebra')
subdir('bgpd')
subdir('bfdd')
subdir('pimd')
subdir('ripd')
subdir('ripngd')
subdir('staticd')
subdir('watchfrr')

frr_xref = custom_target('frr.xref',
  input : [
    libfrr_xref,
    zebra_xref,
    mgmtd_xref,
    bfdd_xref,
    pimd_xref,
    pim6d_xref,
    ripd_xref,
    ripngd_xref,
    staticd_xref,
  ],
  output : ['frr.xref', 'vtysh_cmd.c'] + vtysh_split,
  command : [clippy_bin, '../python/xrelfo.py', '-Werror', '-o', '@OUTPUT0@', '@INPUT@', '-c', '@OUTPUT1@', vtysh_split],
  build_by_default: true,
)

subdir('vtysh')
