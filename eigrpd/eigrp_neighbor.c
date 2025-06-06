// SPDX-License-Identifier: GPL-2.0-or-later
/*
 * EIGRP Neighbor Handling.
 * Copyright (C) 2013-2016
 * Authors:
 *   Donnie Savage
 *   Jan Janovic
 *   Matej Perina
 *   Peter Orsag
 *   Peter Paluch
 *   Frantisek Gazo
 *   Tomas Hvorkovy
 *   Martin Kontsek
 *   Lukas Koribsky
 */

#include <zebra.h>

#include "linklist.h"
#include "prefix.h"
#include "memory.h"
#include "command.h"
#include "frrevent.h"
#include "stream.h"
#include "table.h"
#include "log.h"
#include "keychain.h"
#include "vty.h"

#include "eigrpd/eigrp_structs.h"
#include "eigrpd/eigrpd.h"
#include "eigrpd/eigrp_interface.h"
#include "eigrpd/eigrp_neighbor.h"
#include "eigrpd/eigrp_dump.h"
#include "eigrpd/eigrp_packet.h"
#include "eigrpd/eigrp_zebra.h"
#include "eigrpd/eigrp_vty.h"
#include "eigrpd/eigrp_network.h"
#include "eigrpd/eigrp_topology.h"
#include "eigrpd/eigrp_errors.h"

DEFINE_MTYPE_STATIC(EIGRPD, EIGRP_NEIGHBOR, "EIGRP neighbor");

int eigrp_nbr_comp(const struct eigrp_neighbor *a, const struct eigrp_neighbor *b)
{
	if (a->src.s_addr == b->src.s_addr)
		return 0;
	else if (a->src.s_addr < b->src.s_addr)
		return -1;

	return 1;
}

uint32_t eigrp_nbr_hash(const struct eigrp_neighbor *a)
{
	return a->src.s_addr;
}

struct eigrp_neighbor *eigrp_nbr_new(struct eigrp_interface *ei)
{
	struct eigrp_neighbor *nbr;

	/* Allcate new neighbor. */
	nbr = XCALLOC(MTYPE_EIGRP_NEIGHBOR, sizeof(struct eigrp_neighbor));

	/* Relate neighbor to the interface. */
	nbr->ei = ei;

	/* Set default values. */
	eigrp_nbr_state_set(nbr, EIGRP_NEIGHBOR_DOWN);

	return nbr;
}

/**
 *@fn void dissect_eigrp_sw_version (tvbuff_t *tvb, proto_tree *tree,
 *                                   proto_item *ti)
 *
 * @par
 * Create a new neighbor structure and initalize it.
 */
static struct eigrp_neighbor *eigrp_nbr_add(struct eigrp_interface *ei,
					    struct eigrp_header *eigrph,
					    struct ip *iph)
{
	struct eigrp_neighbor *nbr;

	nbr = eigrp_nbr_new(ei);
	nbr->src = iph->ip_src;

	return nbr;
}

struct eigrp_neighbor *eigrp_nbr_get(struct eigrp_interface *ei,
				     struct eigrp_header *eigrph,
				     struct ip *iph)
{
	struct eigrp_neighbor lookup, *nbr;

	lookup.src = iph->ip_src;
	lookup.ei = ei;

	nbr = eigrp_nbr_hash_find(&ei->nbr_hash_head, &lookup);
	if (nbr) {
		return nbr;
	}

	nbr = eigrp_nbr_add(ei, eigrph, iph);
	eigrp_nbr_hash_add(&ei->nbr_hash_head, nbr);

	return nbr;
}

/**
 * @fn eigrp_nbr_lookup_by_addr
 *
 * @param[in]		ei			EIGRP interface
 * @param[in]		nbr_addr 	Address of neighbor
 *
 * @return void
 *
 * @par
 * Function is used for neighbor lookup by address
 * in specified interface.
 */
struct eigrp_neighbor *eigrp_nbr_lookup_by_addr(struct eigrp_interface *ei,
						struct in_addr *addr)
{
	struct eigrp_neighbor lookup, *nbr;

	lookup.src = *addr;
	nbr = eigrp_nbr_hash_find(&ei->nbr_hash_head, &lookup);

	return nbr;
}

/**
 * @fn eigrp_nbr_lookup_by_addr_process
 *
 * @param[in]    eigrp          EIGRP process
 * @param[in]    nbr_addr       Address of neighbor
 *
 * @return void
 *
 * @par
 * Function is used for neighbor lookup by address
 * in whole EIGRP process.
 */
struct eigrp_neighbor *eigrp_nbr_lookup_by_addr_process(struct eigrp *eigrp,
							struct in_addr nbr_addr)
{
	struct eigrp_interface *ei;
	struct eigrp_neighbor lookup, *nbr;

	/* iterate over all eigrp interfaces */
	frr_each (eigrp_interface_hash, &eigrp->eifs, ei) {
		/* iterate over all neighbors on eigrp interface */
		lookup.src = nbr_addr;
		nbr = eigrp_nbr_hash_find(&ei->nbr_hash_head, &lookup);
		if (nbr) {
			return nbr;
		}
	}

	return NULL;
}


/* Delete specified EIGRP neighbor from interface. */
void eigrp_nbr_delete(struct eigrp_neighbor *nbr)
{
	eigrp_nbr_state_set(nbr, EIGRP_NEIGHBOR_DOWN);
	if (nbr->ei)
		eigrp_topology_neighbor_down(nbr->ei->eigrp, nbr);

	/* Cancel all events. */ /* Thread lookup cost would be negligible. */
	event_cancel_event(master, nbr);
	eigrp_fifo_free(nbr->multicast_queue);
	eigrp_fifo_free(nbr->retrans_queue);
	event_cancel(&nbr->t_holddown);

	if (nbr->ei)
		eigrp_nbr_hash_del(&nbr->ei->nbr_hash_head, nbr);
	XFREE(MTYPE_EIGRP_NEIGHBOR, nbr);
}

void holddown_timer_expired(struct event *thread)
{
	struct eigrp_neighbor *nbr = EVENT_ARG(thread);
	struct eigrp *eigrp = nbr->ei->eigrp;

	zlog_info("Neighbor %pI4 (%s) is down: holding time expired", &nbr->src,
		  ifindex2ifname(nbr->ei->ifp->ifindex, eigrp->vrf_id));
	nbr->state = EIGRP_NEIGHBOR_DOWN;
	eigrp_nbr_delete(nbr);
}

uint8_t eigrp_nbr_state_get(struct eigrp_neighbor *nbr)
{
	return (nbr->state);
}

void eigrp_nbr_state_set(struct eigrp_neighbor *nbr, uint8_t state)
{
	nbr->state = state;

	if (eigrp_nbr_state_get(nbr) == EIGRP_NEIGHBOR_DOWN) {
		// reset all the seq/ack counters
		nbr->recv_sequence_number = 0;
		nbr->init_sequence_number = 0;
		nbr->retrans_counter = 0;

		// Kvalues
		nbr->K1 = EIGRP_K1_DEFAULT;
		nbr->K2 = EIGRP_K2_DEFAULT;
		nbr->K3 = EIGRP_K3_DEFAULT;
		nbr->K4 = EIGRP_K4_DEFAULT;
		nbr->K5 = EIGRP_K5_DEFAULT;
		nbr->K6 = EIGRP_K6_DEFAULT;

		// hold time..
		nbr->v_holddown = EIGRP_HOLD_INTERVAL_DEFAULT;
		event_cancel(&nbr->t_holddown);

		/* out with the old */
		if (nbr->multicast_queue)
			eigrp_fifo_free(nbr->multicast_queue);
		if (nbr->retrans_queue)
			eigrp_fifo_free(nbr->retrans_queue);

		/* in with the new */
		nbr->retrans_queue = eigrp_fifo_new();
		nbr->multicast_queue = eigrp_fifo_new();

		nbr->crypt_seqnum = 0;
	}
}

const char *eigrp_nbr_state_str(struct eigrp_neighbor *nbr)
{
	const char *state;
	switch (nbr->state) {
	case EIGRP_NEIGHBOR_DOWN:
		state = "Down";
		break;
	case EIGRP_NEIGHBOR_PENDING:
		state = "Waiting for Init";
		break;
	case EIGRP_NEIGHBOR_UP:
		state = "Up";
		break;
	default:
		state = "Unknown";
		break;
	}

	return (state);
}

void eigrp_nbr_state_update(struct eigrp_neighbor *nbr)
{
	switch (nbr->state) {
	case EIGRP_NEIGHBOR_DOWN: {
		/*Start Hold Down Timer for neighbor*/
		//     event_cancel(&nbr->t_holddown);
		//     EVENT_TIMER_ON(master, nbr->t_holddown,
		//     holddown_timer_expired,
		//     nbr, nbr->v_holddown);
		break;
	}
	case EIGRP_NEIGHBOR_PENDING: {
		/*Reset Hold Down Timer for neighbor*/
		event_cancel(&nbr->t_holddown);
		event_add_timer(master, holddown_timer_expired, nbr,
				nbr->v_holddown, &nbr->t_holddown);
		break;
	}
	case EIGRP_NEIGHBOR_UP: {
		/*Reset Hold Down Timer for neighbor*/
		event_cancel(&nbr->t_holddown);
		event_add_timer(master, holddown_timer_expired, nbr,
				nbr->v_holddown, &nbr->t_holddown);
		break;
	}
	}
}

int eigrp_nbr_count_get(struct eigrp *eigrp)
{
	struct eigrp_interface *iface;
	uint32_t counter;

	counter = 0;
	frr_each (eigrp_interface_hash, &eigrp->eifs, iface)
		counter += eigrp_nbr_hash_count(&iface->nbr_hash_head);

	return counter;
}

/**
 * @fn eigrp_nbr_hard_restart
 *
 * @param[in]		nbr	Neighbor who would receive hard restart
 * @param[in]		vty Virtual terminal for log output
 * @return void
 *
 * @par
 * Function used for executing hard restart for neighbor:
 * Send Hello packet with Peer Termination TLV with
 * neighbor's address, set it's state to DOWN and delete the neighbor
 */
void eigrp_nbr_hard_restart(struct eigrp_neighbor *nbr, struct vty *vty)
{
	struct eigrp *eigrp = nbr->ei->eigrp;

	zlog_debug("Neighbor %pI4 (%s) is down: manually cleared", &nbr->src,
		   ifindex2ifname(nbr->ei->ifp->ifindex, eigrp->vrf_id));
	if (vty != NULL) {
		vty_time_print(vty, 0);
		vty_out(vty, "Neighbor %pI4 (%s) is down: manually cleared\n",
			&nbr->src,
			ifindex2ifname(nbr->ei->ifp->ifindex, eigrp->vrf_id));
	}

	/* send Hello with Peer Termination TLV */
	eigrp_hello_send(nbr->ei, EIGRP_HELLO_GRACEFUL_SHUTDOWN_NBR,
			 &(nbr->src));
	/* set neighbor to DOWN */
	nbr->state = EIGRP_NEIGHBOR_DOWN;
	/* delete neighbor */
	eigrp_nbr_delete(nbr);
}

int eigrp_nbr_split_horizon_check(struct eigrp_route_descriptor *ne,
				  struct eigrp_interface *ei)
{
	if (ne->distance == EIGRP_MAX_METRIC)
		return 0;

	return (ne->ei == ei);
}
