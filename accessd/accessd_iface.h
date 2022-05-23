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

#ifndef _FRR_ACCESSD_IFACE_H
#define _FRR_ACCESSD_IFACE_H

#include "lib/hook.h"

struct interface;
struct rtadv_iface;

struct accessd_iface {
	struct interface *ifp;

	struct rtadv_iface *rtadv;
};

DECLARE_HOOK(accessd_ifp_up, (struct accessd_iface *acif), (acif));
DECLARE_KOOH(accessd_ifp_down, (struct accessd_iface *acif), (acif));

#endif /* _FRR_ACCESSD_IFACE_H */