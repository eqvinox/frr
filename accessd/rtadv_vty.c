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

#include "lib/zebra.h"

#include "rtadv.h"
#include "rtadv_protocol.h"

#include "accessd_iface.h"
#include "accessd.h"

#include "lib/vty.h"
#include "lib/command.h"

DEFINE_MTYPE_STATIC(ACCESSD, RTADV_PREFIX, "IPv6 RA prefix");

CPP_NOTICE("FIXME: duplicate");
static int rtadv_prefix_cmp(const struct rtadv_prefix *a,
			    const struct rtadv_prefix *b)
{
	return prefix_cmp(&a->prefix, &b->prefix);
}

DECLARE_RBTREE_UNIQ(rtadv_prefixes, struct rtadv_prefix, item,
		    rtadv_prefix_cmp);


#ifndef VTYSH_EXTRACT_PL
#include "rtadv_vty_clippy.c"
#endif

struct rtadv_iface_cfg rtadv_ifp_defaults = {
	.interval_msec = 15000, /* RTADV_MAX_RTR_ADV_INTERVAL, */
	.lifetime_sec = 600,
};

#define VTY_RTADV_CONTEXT(ifp_, rtadv_if_)                                     \
	VTY_DECLVAR_CONTEXT(interface, ifp_);                                  \
	struct rtadv_iface *rtadv_if_ = rtadv_cli_ifp(vty, ifp_);              \
	if (!rtadv_if_)                                                        \
		return CMD_WARNING_CONFIG_FAILED;                              \
	MACRO_REQUIRE_SEMICOLON()

#define VTY_RTADV_FILL_SETTING(field, arg)                                     \
	VTY_RTADV_CONTEXT(ifp, rtadv_if);                                      \
	if (!no)                                                               \
		rtadv_if->cfg.field = arg;                                     \
	else                                                                   \
		rtadv_if->cfg.field = rtadv_ifp_defaults.field;                \
	rtadv_ifp_reconfig(ifp);                                               \
	MACRO_REQUIRE_SEMICOLON()

static struct rtadv_iface *rtadv_cli_ifp(struct vty *vty, struct interface *ifp)
{
	struct accessd_iface *acif;

	assert(ifp->info);

	acif = ifp->info;
	return rtadv_ifp_get(acif);
}

DEFPY (ipv6_nd_ra_hop_limit,
       ipv6_nd_ra_hop_limit_cmd,
       "[no] ipv6 nd ra-hop-limit ![(0-255)$hopcount]",
       NO_STR
       "Interface IPv6 config commands\n"
       "Neighbor discovery\n"
       "Advertisement Hop Limit\n"
       "Advertisement Hop Limit in hops (default:64)\n")
{
	VTY_RTADV_FILL_SETTING(hoplimit, hopcount);
	return CMD_SUCCESS;
}

DEFPY (ipv6_nd_ra_retrans_interval,
       ipv6_nd_ra_retrans_interval_cmd,
       "[no] ipv6 nd ra-retrans-interval ![(0-4294967295)$interval]",
       NO_STR
       "Interface IPv6 config commands\n"
       "Neighbor discovery\n"
       "Advertisement Retransmit Interval\n"
       "Advertisement Retransmit Interval in msec\n")
{
	VTY_RTADV_FILL_SETTING(retrans_ms, interval);
	return CMD_SUCCESS;
}

DEFPY (ipv6_nd_ra_interval_msec,
       ipv6_nd_ra_interval_msec_cmd,
       "[no] ipv6 nd ra-interval msec ![(70-1800000)$interval]",
       NO_STR
       "Interface IPv6 config commands\n"
       "Neighbor discovery\n"
       "Router Advertisement interval\n"
       "Router Advertisement interval in milliseconds\n"
       "Router Advertisement interval in milliseconds\n")
{
	VTY_RTADV_FILL_SETTING(interval_msec, interval);
	return CMD_SUCCESS;
}
#if 0
	struct zebra_if *zif = ifp->info;
	struct zebra_vrf *zvrf;
	struct adv_if *adv_if;

	zvrf = rtadv_interface_get_zvrf(ifp);

	if ((zif->rtadv.AdvDefaultLifetime != -1
	     && interval > (unsigned)zif->rtadv.AdvDefaultLifetime * 1000)) {
		vty_out(vty,
			"This ra-interval would conflict with configured ra-lifetime!\n");
		return CMD_WARNING_CONFIG_FAILED;
	}

	if (zif->rtadv.MaxRtrAdvInterval % 1000) {
		adv_if = adv_msec_if_del(zvrf, ifp->name);
		if (adv_if != NULL)
			adv_if_free(adv_if);
	}

	if (interval % 1000)
		(void)adv_msec_if_add(zvrf, ifp->name);

	SET_FLAG(zif->rtadv.ra_configured, VTY_RA_INTERVAL_CONFIGURED);
	zif->rtadv.MaxRtrAdvInterval = interval;
	zif->rtadv.MinRtrAdvInterval = 0.33 * interval;
	zif->rtadv.AdvIntervalTimer = 0;
#endif

#if 0
DEFPY (ipv6_nd_ra_interval,
       ipv6_nd_ra_interval_cmd,
       "[no] ipv6 nd ra-interval ![(1-1800)]",
       NO_STR
       "Interface IPv6 config commands\n"
       "Neighbor discovery\n"
       "Router Advertisement interval\n"
       "Router Advertisement interval in seconds\n")
{
	VTY_RTADV_CONTEXT(ifp, rtadv_if);
#if 0
	int idx_number = 3;
	VTY_DECLVAR_CONTEXT(interface, ifp);
	unsigned interval;
	struct zebra_if *zif = ifp->info;
	struct zebra_vrf *zvrf;
	struct adv_if *adv_if;

	zvrf = rtadv_interface_get_zvrf(ifp);

	interval = strtoul(argv[idx_number]->arg, NULL, 10);
	if ((zif->rtadv.AdvDefaultLifetime != -1
	     && interval > (unsigned)zif->rtadv.AdvDefaultLifetime)) {
		vty_out(vty,
			"This ra-interval would conflict with configured ra-lifetime!\n");
		return CMD_WARNING_CONFIG_FAILED;
	}

	if (zif->rtadv.MaxRtrAdvInterval % 1000) {
		adv_if = adv_msec_if_del(zvrf, ifp->name);
		if (adv_if != NULL)
			adv_if_free(adv_if);
	}

	/* convert to milliseconds */
	interval = interval * 1000;

	SET_FLAG(zif->rtadv.ra_configured, VTY_RA_INTERVAL_CONFIGURED);
	zif->rtadv.MaxRtrAdvInterval = interval;
	zif->rtadv.MinRtrAdvInterval = 0.33 * interval;
	zif->rtadv.AdvIntervalTimer = 0;
#endif
	return CMD_SUCCESS;
}
#endif

DEFPY (ipv6_nd_ra_lifetime,
       ipv6_nd_ra_lifetime_cmd,
       "[no] ipv6 nd ra-lifetime ![(0-9000)]",
       NO_STR
       "Interface IPv6 config commands\n"
       "Neighbor discovery\n"
       "Router lifetime\n"
       "Router lifetime in seconds (0 stands for a non-default gw)\n")
{
	VTY_RTADV_FILL_SETTING(lifetime_sec, ra_lifetime);
#if 0
	/* The value to be placed in the Router Lifetime field
	 * of Router Advertisements sent from the interface,
	 * in seconds.  MUST be either zero or between
	 * MaxRtrAdvInterval and 9000 seconds. -- RFC4861, 6.2.1 */
	if ((lifetime != 0 && lifetime * 1000 < zif->rtadv.MaxRtrAdvInterval)) {
		vty_out(vty,
			"This ra-lifetime would conflict with configured ra-interval\n");
		return CMD_WARNING_CONFIG_FAILED;
	}
#endif
	return CMD_SUCCESS;
}

DEFPY (ipv6_nd_reachable_time,
       ipv6_nd_reachable_time_cmd,
       "[no] ipv6 nd reachable-time ![(1-3600000)]",
       NO_STR
       "Interface IPv6 config commands\n"
       "Neighbor discovery\n"
       "Reachable time\n"
       "Reachable time in milliseconds\n")
{
	VTY_RTADV_FILL_SETTING(reachable_ms, reachable_time);
	return CMD_SUCCESS;
}

DEFPY (ipv6_nd_managed_config_flag,
       ipv6_nd_managed_config_flag_cmd,
       "[no] ipv6 nd managed-config-flag",
       NO_STR
       "Interface IPv6 config commands\n"
       "Neighbor discovery\n"
       "Managed address configuration flag\n")
{
	VTY_RTADV_FILL_SETTING(managed_config, true);
	return CMD_SUCCESS;
}

DEFPY (ipv6_nd_adv_interval_config_option,
       ipv6_nd_adv_interval_config_option_cmd,
       "[no] ipv6 nd adv-interval-option",
       NO_STR
       "Interface IPv6 config commands\n"
       "Neighbor discovery\n"
       "Advertisement Interval Option\n")
{
	VTY_RTADV_FILL_SETTING(managed_config, true);
	return CMD_SUCCESS;
}

DEFPY (ipv6_nd_other_config_flag,
       ipv6_nd_other_config_flag_cmd,
       "[no] ipv6 nd other-config-flag",
       NO_STR
       "Interface IPv6 config commands\n"
       "Neighbor discovery\n"
       "Other statefull configuration flag\n")
{
	VTY_RTADV_FILL_SETTING(other_config, true);
	return CMD_SUCCESS;
}

DEFPY (ipv6_nd_prefix,
       ipv6_nd_prefix_cmd,
       "[no] ipv6 nd prefix X:X::X:X/M [<(0-4294967295)$lifetime|infinite$lt_inf> <(0-4294967295)$preftime|infinite$pref_inf>] [{"
       "   <router-address|no-router-address>$rta"
       "  |<off-link|on-link>$offlink"
       "  |<no-autoconfig|autoconfig>$auton"
       "  |<dad-lladdr|no-dad-lladdr>$makell"
       " }]",
       NO_STR
       "Interface IPv6 config commands\n"
       "Neighbor discovery\n"
       "Prefix information\n"
       "IPv6 prefix\n"
       "Valid lifetime in seconds\n"
       "Infinite valid lifetime\n"
       "Preferred lifetime in seconds\n"
       "Infinite preferred lifetime\n"
       "Set Router Address flag\n"
       "Unset Router Address flag\n"
       "Do not use prefix for onlink determination\n"
       "Use prefix for onlink determination\n"
       "Do not use prefix for autoconfiguration\n"
       "Use prefix for autoconfiguration\n"
       "Create link-local address on router for prefix DAD\n"
       "Do not create link-local address on router for prefix DAD\n")
{
	VTY_RTADV_CONTEXT(ifp, rtadv_if);
	struct rtadv_prefix *ra_prefix, ref = {};

	ref.prefix = *prefix;
	apply_mask_ipv6(&ref.prefix);
	ra_prefix = rtadv_prefixes_find(rtadv_if->prefixes, &ref);

	if (no) {
		if (!ra_prefix) {
			vty_out(vty, "%% prefix %pFX does not exist\n", prefix);
			return CMD_WARNING;
		}

		CPP_NOTICE("cleanup prefix here!");
		rtadv_prefixes_del(rtadv_if->prefixes, ra_prefix);
		XFREE(MTYPE_RTADV_PREFIX, ra_prefix);
		return CMD_SUCCESS;
	}

	if (!ra_prefix) {
		ra_prefix = XCALLOC(MTYPE_RTADV_PREFIX, sizeof(*ra_prefix));
		ra_prefix->prefix = ref.prefix;
		ra_prefix->cfg.valid_sec = RTADV_PREFIX_DFLT_VALID;
		ra_prefix->cfg.preferred_sec = RTADV_PREFIX_DFLT_PREFERRED;
		ra_prefix->cfg.onlink = true;
		ra_prefix->cfg.autonomous = true;
		rtadv_prefixes_add(rtadv_if->prefixes, ra_prefix);
	}

	if (lifetime_str)
		ra_prefix->cfg.valid_sec = lifetime;
	else if (lt_inf)
		ra_prefix->cfg.valid_sec = ~0U;

	if (preftime_str)
		ra_prefix->cfg.preferred_sec = preftime;
	else if (pref_inf)
		ra_prefix->cfg.preferred_sec = ~0U;

	if (rta)
		ra_prefix->cfg.router_addr = !strcmp(rta, "router-addr");
	if (offlink)
		ra_prefix->cfg.onlink = !strcmp(offlink, "on-link");
	if (auton)
		ra_prefix->cfg.autonomous = !strcmp(auton, "autoconfig");
	if (makell)
		ra_prefix->cfg.make_addr = !strcmp(makell, "dad-lladdr");

	if (ra_prefix->cfg.make_addr && !ra_prefix->ll_addr) {
		rtadv_lladdr_addref(ifp->info, ra_prefix);

		zlog_info("LL for %pFX: %pI6", &ra_prefix->prefix,
			  &ra_prefix->ll_addr->ll_addr);
	}

	rtadv_ifp_reconfig(ifp);
	return CMD_SUCCESS;
}

#if 0
DEFPY (ipv6_nd_router_preference,
       ipv6_nd_router_preference_cmd,
       "ipv6 nd router-preference <high|medium|low>",
       "Interface IPv6 config commands\n"
       "Neighbor discovery\n"
       "Default router preference\n"
       "High default router preference\n"
       "Medium default router preference (default)\n"
       "Low default router preference\n")
{
	int idx_high_medium_low = 3;
	VTY_DECLVAR_CONTEXT(interface, ifp);
	struct zebra_if *zif = ifp->info;
	int i = 0;

	while (0 != rtadv_pref_strs[i]) {
		if (strncmp(argv[idx_high_medium_low]->arg, rtadv_pref_strs[i],
			    1)
		    == 0) {
			zif->rtadv.DefaultPreference = i;
			return CMD_SUCCESS;
		}
		i++;
	}

	return CMD_ERR_NO_MATCH;
}

DEFPY (no_ipv6_nd_router_preference,
       no_ipv6_nd_router_preference_cmd,
       "no ipv6 nd router-preference [<high|medium|low>]",
       NO_STR
       "Interface IPv6 config commands\n"
       "Neighbor discovery\n"
       "Default router preference\n"
       "High default router preference\n"
       "Medium default router preference (default)\n"
       "Low default router preference\n")
{
	VTY_DECLVAR_CONTEXT(interface, ifp);
	struct zebra_if *zif = ifp->info;

	zif->rtadv.DefaultPreference =
		RTADV_PREF_MEDIUM; /* Default per RFC4191. */

	return CMD_SUCCESS;
}
#endif

DEFPY (ipv6_nd_mtu,
       ipv6_nd_mtu_cmd,
       "[no] ipv6 nd mtu ![(1-65535)]",
       NO_STR
       "Interface IPv6 config commands\n"
       "Neighbor discovery\n"
       "Advertised MTU\n"
       "MTU in bytes\n")
{
	VTY_RTADV_FILL_SETTING(link_mtu, mtu);
	return CMD_SUCCESS;
}

DEFPY (ipv6_nd_suppress_ra,
       ipv6_nd_suppress_ra_cmd,
       "[no] ipv6 nd suppress-ra",
       NO_STR
       "Interface IPv6 config commands\n"
       "Neighbor discovery\n"
       "Suppress Router Advertisement\n")
{
	VTY_RTADV_CONTEXT(ifp, rtadv_if);

	if (no)
		rtadv_if->cfg.enable = true;
	else
		rtadv_if->cfg.enable = false;

	rtadv_ifp_reconfig(ifp);
	return CMD_SUCCESS;
}

void rtadv_cli_init(void)
{
	install_element(INTERFACE_NODE, &ipv6_nd_ra_hop_limit_cmd);
	install_element(INTERFACE_NODE, &ipv6_nd_ra_interval_msec_cmd);
	install_element(INTERFACE_NODE, &ipv6_nd_ra_lifetime_cmd);
	install_element(INTERFACE_NODE, &ipv6_nd_reachable_time_cmd);
	install_element(INTERFACE_NODE, &ipv6_nd_managed_config_flag_cmd);
	install_element(INTERFACE_NODE, &ipv6_nd_other_config_flag_cmd);
	install_element(INTERFACE_NODE, &ipv6_nd_mtu_cmd);
	install_element(INTERFACE_NODE,
			&ipv6_nd_adv_interval_config_option_cmd);
	install_element(INTERFACE_NODE, &ipv6_nd_prefix_cmd);
	//install_element(INTERFACE_NODE, &ipv6_nd_router_preference_cmd);
	//install_element(INTERFACE_NODE, &ipv6_nd_rdnss_cmd);
	//install_element(INTERFACE_NODE, &ipv6_nd_dnssl_cmd);
	install_element(INTERFACE_NODE, &ipv6_nd_suppress_ra_cmd);
}