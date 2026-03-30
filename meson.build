project('frr', 'c')

add_project_arguments(
  '-std=gnu23',
  '-fms-extensions',
  '-fno-omit-frame-pointer',
  '-funwind-tables',
  '-Wall',
  '-Wextra',
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
  '-std=gnu23',
  '-fms-extensions',
  '-fno-omit-frame-pointer',
  '-funwind-tables',
  '-Wall',
  '-Wextra',
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

incls = include_directories('.', 'lib', 'lib/assert')
#yacc_gen = custom_target('-d -Dapi.prefix=@BISON_OPENBRACE@cmd_yy@BISON_CLOSEBRACE@ @BISON_VERBOSE@
#

cc = meson.get_compiler('c')

libyang = dependency('libyang', version: '>= 2.1.128')
libjson = cc.find_library('json-c')
libm = cc.find_library('m')
libcrypt = cc.find_library('crypt')

headers = configuration_data()

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

headers.set('HAVE_OPENAT', cc.has_function('openat', prefix: '#include <fcntl.h>'))
headers.set('HAVE_UNLINKAT', cc.has_function('unlinkat', prefix: '#include <unistd.h>\n#include <fcntl.h>'))
headers.set('HAVE_POSIX_FALLOCATE', cc.has_function('posix_fallocate', prefix: '#include <fcntl.h>'))

headers.set('HAVE_POLLTS', cc.has_function('pollts', prefix: '#include <poll.h>\n#include <signal.h>\n#include<time.h>'))
headers.set('HAVE_PPOLL', cc.has_function('ppoll', prefix: '#define _GNU_SOURCE\n#include <poll.h>'))

headers.set('HAVE_SENDMMSG', cc.has_function('sendmmsg', prefix: '#define _GNU_SOURCE\n#include <sys/socket.h>'))

headers.set('HAVE_SETNS', cc.has_function('setns', prefix: '#define _GNU_SOURCE\n#include <sched.h>'))

headers.set('HAVE_GETGROUPLIST', cc.has_function('getgrouplist', prefix: '#include <grp.h>'))

headers.set('HAVE_CLOCK_NANOSLEEP', cc.has_function('clock_nanosleep', prefix: '#include <time.h>'))
headers.set('HAVE_CLOCK_THREAD_CPUTIME_ID', cc.has_header_symbol('time.h', 'CLOCK_THREAD_CPUTIME_ID'))

headers.set('HAVE_EXPLICIT_BZERO', cc.has_function('explicit_bzero', prefix: '#include <string.h>'))
headers.set('HAVE_STRLCAT', cc.has_function('strlcat', prefix: '#include <string.h>'))
headers.set('HAVE_STRLCPY', cc.has_function('strlcpy', prefix: '#include <string.h>'))

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

#	HAVE_IP_FREEBIND
#	HAVE_IP_PKTINFO
#	HAVE_IP_RECVDSTADDR
#	HAVE_IP_RECVIF
#	HAVE_SO_BINDANY
#	IPV6_MINHOPCOUNT

headers.set('HAVE_OPENPAM_H',           cc.has_header('openpam.h'))
headers.set('HAVE_PAM_MISC_H',          cc.has_header('pam_misc.h'))

headers.set('HAVE_SECTION_SYMS', true)
headers.set('_GNU_SOURCE', true)

headers.set('MULTIPATH_NUM', 64)
headers.set('CONFIGFILE_MASK', 0o640)
headers.set('LOGFILE_MASK', 0o640)
headers.set('DFLT_NAME', '"traditional"')
headers.set('LOG_TIMESTAMP_PRECISION', 6)
headers.set('GNU_LINUX', true)
headers.set('HAVE_NETLINK', true)
headers.set('NETLINK_DEBUG', 1)
headers.set('HAVE_BFDD', 1)
headers.set('LINUX_IPV6', true)

headers.set('HAVE_STRLCPY', true)
headers.set('HAVE_STRLCAT', true)

headers.set('HAVE_DECL_BE32DEC', 0)
headers.set('HAVE_DECL_BE32ENC', 0)
headers.set('HAVE_DECL_TCP_MD5SIG', 1)

headers.set('VTYSH', true)

configure_file(
  output: 'config.h',
  configuration: headers,
)

subdir('lib')

#libfrr = sub_lib.get_variable('libfrr')
#clippy = sub_lib.get_variable('clippy')

subdir('zebra')

frr_xref = custom_target('frr.xref',
  input : [libfrr_xref, zebra_xref],
  output : ['frr.xref', 'vtysh_cmd.c'],
  command : [clippy_bin, '../python/xrelfo.py', '-Werror', '-o', '@OUTPUT0@', '@INPUT@', '-c', '@OUTPUT1@', vtysh_split],
  build_by_default: true,
)
