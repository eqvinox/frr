/*
 * This file is part of FRR.
 *
 * FRR is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the
 * Free Software Foundation; either version 2, or (at your option) any
 * later version.
 *
 * FRR is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; see the file COPYING; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
 */

#ifndef _FRR_ACCESSD_H
#define _FRR_ACCESSD_H

#include "lib/memory.h"
#include "lib/privs.h"

DECLARE_MGROUP(DHCP6);

struct thread_master;

extern struct thread_master *master;
extern struct zebra_privs_t accessd_privs;

extern void accessd_zebra_init(void);
extern void accessd_vrf_init(void);
extern void accessd_if_init(void);

extern void dhcp6r_if_init(void);
extern void dhcp6r_zebra_init(void);
extern void dhcp6_state_init(void);
extern void dhcp6_upstream_init(void);

#endif /* _FRR_ACCESSD_H */
