---
tag: EEYGEK
kind: problem
slug: ip-traceback-problem
name: IP traceback problem
aliases:
- packet traceback
area: security-and-privacy/network-and-web-security
level: core
summary: Find the path of routers that packets with forged source addresses took to reach a victim, using marks in the packets or digests kept by the routers.
prereqs: [ingress-filtering, reachability]
see_also: [probabilistic-packet-marking, hash-based-ip-traceback, ingress-filtering, syn-flooding, coupon-collector-problem, bloom-filter, intrusion-detection-problem]
sources:
  - paper: "Stefan Savage, David Wetherall, Anna Karlin and Tom Anderson, Practical network support for IP traceback, ACM SIGCOMM 2000, pages 295 to 306, doi:10.1145/347059.347560"
    locator: Section 2 (ingress filtering, link testing, logging and ICMP traceback, with Table 1), Section 3.1 (exact and approximate traceback, the valid suffix, robustness and convergence time) and Section 3.2 (the assumptions)
  - paper: "Alex C. Snoeren, Craig Partridge, Luis A. Sanchez, Christine E. Jones, Fabrice Tchakountio, Stephen T. Kent and W. Timothy Strayer, Hash-based IP traceback, ACM SIGCOMM 2001, pages 3 to 14, doi:10.1145/964723.383060"
    locator: Section 2 (the attack graph, the goals of single-packet traceback and the packet transformations) and Section 3 (related work)
  - paper: "Micah Adler, Tradeoffs in probabilistic packet marking for IP traceback, ACM STOC 2002, pages 407 to 418"
    locator: the abstract and the introduction (how many header bits a marking scheme needs, and the trade-off between bits and packets)
---

The IP traceback problem asks a victim of an attack to find the path of routers that the attack packets took, when the source addresses in the packets may be forged. IP gives a router no reason to check the source field, so without [ingress filtering](/ingress-filtering/) everywhere the source address says nothing reliable about the origin. A solution adds information on the path: routers write marks into the packets, as in [probabilistic packet marking](/probabilistic-packet-marking/), or keep digests of the packets they forward, as in [hash-based IP traceback](/hash-based-ip-traceback/). The answer can be trusted only up to the first router that the attacker controls.

## In plain words

Anonymous letters arrive, and the return address on each one is false. The letters still went through real sorting offices on their way. If each office stamped some letters with its name, the person who receives them could read the stamps and find the chain of offices back to the town where the letters were posted. If instead each office kept a short note of every letter it handled, an investigator could ask each office, starting with the nearest, "did you handle this one?", and walk back that way.

Traceback does this for packets. The stamps must fit in a few unused bits of the packet, the notes must be small enough for fast routers, and a liar who writes fake stamps must not be able to hide the real chain near the victim.

## Definition

**The network.** Let $G = (N, E)$ be the graph of routers and hosts, with a victim $V \in N$. Each attack origin $A_i$ sends packets to $V$. Routes are stable during the trace, so each $A_i$ has a single attack path $P_i = (R^i_1, R^i_2, \ldots, R^i_{d_i})$: the unique ordered list of routers between $A_i$ and $V$, with $R^i_{d_i}$ the router next to $V$ (Savage et al., Section 3.1). The union of the paths, as a subgraph of $G$, is the attack graph.

**The adversary** (Savage et al., Section 3.2). Attackers may generate any packet, including any content in the fields that routers use for marks. Several attackers may conspire, and they may know that they are traced. Packets may be lost or reordered. Routers are limited in processor time and memory, so a solution cannot keep state per flow. Routers are not widely compromised: a router that the attacker controls can forge anything a correct router would send.

**Exact traceback.** Given the packets that $V$ receives (and, in some schemes, queries to routers), output each $P_i$ and its origin $A_i$.

**Approximate traceback.** Output a candidate path $C_i$ for each attacker such that $P_i$ is a suffix of $C_i$, that is, $C_i = (Q_1, \ldots, Q_k, R^i_1, \ldots, R^i_{d_i})$ for some $k \ge 0$. The part $P_i$ is the valid suffix. A solution is robust if the attacker cannot prevent $V$ from finding candidate paths that contain the valid suffix. The convergence time of a marking scheme is the number of packets $V$ must receive to rebuild the path.

**Single-packet traceback** (Snoeren et al., Section 2). Given one packet $p$, the victim $V$ and the time of arrival, output a subgraph of $G$ that contains every router that forwarded $p$ on its way to $V$. The output may contain extra routers (false positives) but must not miss a router on the path (no false negatives).

## Variants

- **Flood or single packet.** Marking schemes need many packets from the same path, which a flood provides. Single-packet traceback must work from one packet, which needs state in the routers.
- **Post-mortem or live.** Marking and logging work after the attack ends. Link testing (input debugging, controlled flooding) works only while the attack runs (Savage et al., Section 2.2).
- **One path or many.** A distributed attack has many origins, and the answer is an attack graph. Marks from different paths mix at the victim, which makes reconstruction harder.
- **In-band or out-of-band.** Marks can ride in unused header fields of the packets themselves, or in separate messages such as ICMP traceback messages.
- **Stateless or stateful routers.** Marking keeps no state in routers. Logging and packet digests keep state for a limited time window.
- **Packet transformations.** Routers may change packets on the way (fragmentation, NAT, tunnels). Snoeren et al., Section 2.3, require traceback through valid transformations.

## Examples

**A small attack graph.** Take routers $R_1, \ldots, R_7$ and a victim $V$, with links $A_1$-$R_5$, $A_2$-$R_6$, $A_3$-$R_7$, $R_5$-$R_3$, $R_6$-$R_3$, $R_7$-$R_4$, $R_3$-$R_2$, $R_4$-$R_2$, $R_2$-$R_1$ and $R_1$-$V$. This is the shape of Figure 1 of Savage et al.

| attacker | attack path $P_i$ | $d_i$ |
|---|---|---|
| $A_1$ | $(R_5, R_3, R_2, R_1)$ | 4 |
| $A_2$ | $(R_6, R_3, R_2, R_1)$ | 4 |
| $A_3$ | $(R_7, R_4, R_2, R_1)$ | 4 |

If only $A_2$ attacks, the candidate $(R_5, R_6, R_3, R_2, R_1)$ is a valid answer to approximate traceback, because it ends with $P_2$. The candidate $(R_6, R_4, R_2, R_1)$ is not valid: $R_4$ is not on the path. If all three attack, the attack graph has the 7 routers and the 9 links between them and $V$.

**What a forged mark can and cannot do.** The attacker can put a fake mark in a packet before it leaves, claiming that the packet passed $R_9$ before $R_6$. In edge sampling (see [probabilistic packet marking](/probabilistic-packet-marking/)), every router on the path overwrites the mark with probability $p$, so a fake mark survives to $V$ only in a fraction $(1 - p)^{d}$ of packets. A surviving fake mark has a distance of at least $d$, because each router adds one, so it can only add routers before the true path. The valid suffix of length $d$ is the part that the attacker cannot change.

**Single packet.** A query for one packet that crossed $R_6, R_3, R_2, R_1$ starts at $R_1$, asks each neighbor whether it saw the packet, and moves on from those that say yes. If $R_4$ answers yes because of a false positive in its digest table, the answer graph has one extra router, which the query process tolerates by design. See [hash-based IP traceback](/hash-based-ip-traceback/).

## Known algorithms

| method | state in routers | packets needed | trace after the attack | source |
|---|---|---|---|---|
| [Ingress filtering](/ingress-filtering/) | none | prevents forgery, traces nothing | not applicable | RFC 2827 |
| Input debugging | per query | live flow | no | Savage et al., Section 2.2.1 |
| Controlled flooding | none | live flow, and it floods links | no | Burch and Cheswick, LISA 2000 |
| Logging | full packets | 1 | yes, while logs last | Savage et al., Section 2.3 |
| ICMP traceback | none | many | yes | Bellovin, Internet-Draft, 2000 |
| [Probabilistic packet marking](/probabilistic-packet-marking/) | none | under 1300 expected for 10 hops (8 fragments per edge, $p = 1/25$) | yes | Savage et al., Sections 4 and 5 |
| [Hash-based IP traceback](/hash-based-ip-traceback/) (SPIE) | Bloom filter digests for a time window | 1 | yes, while digests last | Snoeren et al., Sections 4 and 5 |

Song and Perrig (INFOCOM 2001) improved the reconstruction of packet marking and added authentication of marks. Table 1 of Savage et al. compares the older methods on management cost, network cost, router cost, support for distributed attacks and post-mortem use.

## Bounds

- **Compromised routers.** No scheme can trace past the first router on the path that the attacker controls, because that router can produce any output a correct router would. Savage et al. (Section 3.2) and Snoeren et al. (Section 2.2) state this limit. This is why the definition asks for the valid suffix, the part between that router and $V$.
- **Packets for marking.** For edge sampling on a path of $d$ routers with marking probability $p$, the expected number of packets until $V$ has every edge is at most $H_d / (p (1 - p)^{d-1})$, with $H_d$ the $d$-th harmonic number (theorem, proved on the [probabilistic packet marking](/probabilistic-packet-marking/) page). The proof is the [coupon collector](/coupon-collector-problem/) argument with unequal probabilities.
- **Header bits.** Adler (STOC 2002) studied how many bits of the header a marking scheme needs. For one attack path, a single bit per packet is enough, but the number of packets then grows exponentially with the number of bits needed to describe the path. More bits per packet cut the number of packets sharply (theorem, with the exact bounds in the paper).
- **Single packet.** Under the model of Snoeren et al. (Section 7.1.1), if each router's digest table has a false-positive rate of at most $p/d$ where $d$ bounds the degree of its neighbors, the expected number of extra routers in the answer for a path of $n$ routers is at most $n p / (1 - p)$ (theorem, under their assumption that the neighbor sets are disjoint).

## Reductions

- **Approximate traceback to collecting edges.** If $V$ learns each edge $(R_j, R_{j+1})$ of a path together with its distance from $V$, it rebuilds the path by sorting the edges by distance, in $O(d \log d)$ time, or $O(d)$ with distances as array indices. Edge sampling reduces traceback to collecting all $d$ edges, which is a coupon collector problem with unequal probabilities.
- **Single-packet traceback to membership queries and reachability.** If each router answers "did you forward $p$ in this time window?", the attack graph is the set of routers reachable from $V$ in $G$ through routers that answer yes. This is a [reachability](/reachability/) search on $G$ with one [Bloom filter](/bloom-filter/) query per visited router.

## Applications

- Finding the networks that send a flood with forged sources, such as a [SYN flood](/syn-flooding/), so that their operators can filter it.
- Giving evidence of the path of a single harmful packet that an [intrusion detection](/intrusion-detection-problem/) system flagged, for example one that crashed a host.
- Measuring where forged traffic enters a network, which shows where [ingress filtering](/ingress-filtering/) is missing.

## References
