---
tag: FSQG1T
kind: technique
slug: ecmp-hashing
name: ECMP hashing
aliases:
- equal-cost multi-path hashing
- flow hashing
- hash-threshold next-hop selection
area: systems/load-balancing-and-hashing
level: advanced
summary: A router hashes the header fields of each packet to choose one of N equal-cost next hops, so all packets of a flow take one path. Modulo-N, hash-threshold and HRW differ in how many flows move.
prereqs: [hash-function, link-state-routing]
see_also: [rendezvous-hashing, maglev-hashing, consistent-hashing, monotonicity-property, source-ip-hash, layer-4-load-balancing, oblivious-routing, load-skew]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc2991
    title: D. Thaler and C. Hopps, Multipath Issues in Unicast and Multicast Next-Hop Selection, RFC 2991, November 2000
    locator: Section 2 (path MTU, latency, TCP reordering and debugging with several paths), Section 3 (keep the packets of a flow on one path), Section 4 (modulo-N, hash-threshold and HRW, with the disruptions (N-1)/N, 1/4 to 1/2 and 1/N, and the recommendations), Section 4.2 (multicast)
  - url: https://www.rfc-editor.org/rfc/rfc2992
    title: C. Hopps, Analysis of an Equal-Cost Multi-Path Algorithm, RFC 2992, November 2000
    locator: Section 2.1 (regions of a 16-bit key space), Section 2.2 (the disruption ((K-1)K + (N-K)(N-K+1)) / (2N(N-1)) for the removal of region K, the range (1/4, 1/2], and the advice to add new regions in the middle), Section 3 (comparison with modulo-N and HRW)
  - url: https://www.rfc-editor.org/rfc/rfc7424
    title: R. Krishnan, L. Yong, A. Ghanwani, N. So and B. Khasnabish, Mechanisms for Optimizing Link Aggregation Group (LAG) and Equal-Cost Multipath (ECMP) Component Link Utilization in Networks, RFC 7424, January 2015
    locator: Section 3 (imbalance of hash-based distribution under unfavorable flow sizes), Section 4.3.1 (the header fields that identify a flow), Section 4.1 (rebalancing ECMP changes traffic at downstream routers)
  - paper: doi:10.1109/90.663936
    title: David G. Thaler and Chinya V. Ravishankar, Using name-based mappings to increase hit rates, IEEE/ACM Transactions on Networking 6(1), 1998, pages 1 to 14
    locator: the highest random weight mapping that RFC 2991 recommends
---

ECMP hashing is how a router spreads traffic over several next hops that a routing protocol finds to be of equal cost. The router computes a [hash](/hash-function/) of the fields that identify a flow, usually the source and destination addresses, the protocol and the two ports, and maps the hash to one next hop. All packets of a flow then take the same path, which avoids reordering inside a TCP connection. RFC 2991 and RFC 2992 compare three maps from the hash to a next hop: modulo-N, hash-threshold and [highest random weight](/rendezvous-hashing/). When one of $N$ next hops is added or removed, they move a fraction $(N-1)/N$, between $1/4$ and $1/2$, and exactly $1/N$ of the flows.

## In plain words

A router often has several equally good ways to reach a destination. Sending each packet down a different way would use all of them, but the packets of one connection would arrive out of order, and TCP would read that as loss and slow down.

So the router looks at the addresses and ports in each packet, which are the same for every packet of a connection, and turns them into a number. The number picks the way. One connection always takes one way, and many connections spread over all of them.

The open question is what happens when a way appears or disappears. The simplest rule, the number modulo the count of ways, then sends most connections down a new way. Better rules move only a quarter to a half of them, or only those that must move.

## When it applies

- The routing protocol gives $N \ge 2$ next hops of equal cost for a destination, for example from [link-state routing](/link-state-routing/) in OSPF or IS-IS, or several links between two switches bundled as one group.
- The traffic is many flows, each much smaller than one path. RFC 2991 (Section 5) says that the hash spreads load well only with many flows.
- Packets of one flow must stay in order, so the choice is per flow, not per packet.
- The forwarder must decide at line rate. Per-flow state may or may not be affordable, and the choice of map depends on it.

The model on this page: a flow is a key $x$ from a key space, the hash of the flow is uniform on the key space, and the question is the fraction of flows that change next hop when the set of next hops changes. This fraction is the *disruption* of RFC 2992. The bounds count flows, not bytes.

## The template

Let $\text{key}(p)$ be the hash of the flow fields of packet $p$, an integer in $\{0, \ldots, S - 1\}$; RFC 2992 uses a 16-bit key space, $S = 65536$. Let $H[0..N-1]$ be the list of next hops.

```pseudo id=main
MODULO-N(p)
L1  return H[key(p) mod N]

HASH-THRESHOLD(p)                       ▷ N equal regions of the key space
L2  return H[⌊key(p) · N / S⌋]

HRW(p)                                  ▷ highest random weight
L3  return the hop g in H with the largest score(flow(p), g)
```

The three maps cost one hash and $O(1)$ work, one hash and $O(1)$ work, and $N$ hashes. Each gives a next hop the share $1/N$ of the key space (up to rounding when $N$ does not divide $S$), so with many flows each next hop gets about $1/N$ of them.

**Disruption of modulo-N.** Remove one hop from $N$ and renumber the others in order. Suppose the keys are uniform over a multiple of $N(N-1)$. Because $N$ and $N - 1$ are coprime, the pair $(x \bmod N, x \bmod (N-1))$ takes each of its $N(N-1)$ values equally often, by the Chinese remainder theorem. A flow keeps its hop only when its old index and its new index belong to the same surviving hop. There are $N - 1$ such pairs, one for each survivor, so a fraction $1/N$ stays and $(N-1)/N$ moves.

**Disruption of hash-threshold.** Scale the key space to $[0, 1)$, so hop $i$ (numbered from 1) owns $[(i-1)/N, i/N)$. Remove hop $K$. A hop $i < K$ now owns $[(i-1)/(N-1), i/(N-1))$, and the overlap with its old region has length $(N - i)/(N(N-1))$. A hop $i > K$ moves down one place and owns $[(i-2)/(N-1), (i-1)/(N-1))$, with an overlap of length $(i - 1)/(N(N-1))$. The flows that stay add up to

$$\frac{1}{N(N-1)}\left(\sum_{i=1}^{K-1} (N - i) + \sum_{i=K+1}^{N} (i - 1)\right) = \frac{(K-1)(N-K)}{N(N-1)} + \frac{1}{2},$$

so the disruption is

$$D(N, K) = \frac{1}{2} - \frac{(K-1)(N-K)}{N(N-1)} = \frac{(K-1)K + (N-K)(N-K+1)}{2N(N-1)},$$

which is the formula of RFC 2992, Section 2.2. It is $1/2$ for an end region ($K = 1$ or $K = N$). It is smallest in the middle: $1/4 + 1/(4N)$ for odd $N$ and $K = (N+1)/2$, and $N/(4(N-1))$ for even $N$ and $K = N/2$ or $N/2 + 1$. So $1/4 < D \le 1/2$. Adding a hop at place $K$ of $N + 1$ is the same change read backwards, so it has the disruption $D(N + 1, K)$. This is why RFC 2992 advises adding new regions in the middle.

**Disruption of HRW.** A flow keeps its hop unless the hop is removed, or an added hop has a higher score. So exactly the flows of the removed hop move, a fraction $1/N$, and an added hop takes about $1/(N+1)$; see the [monotonicity property](/monotonicity-property/). The proofs are on the [rendezvous hashing](/rendezvous-hashing/) page.

## Classic examples

**Six flows, five next hops A to E.** The 16-bit keys below are the low 16 bits of a CRC-32 of the five flow fields of six random TCP flows. With hash-threshold and $N = 5$, the regions are 0 to 13107 for A, 13108 to 26214 for B, 26215 to 39321 for C, 39322 to 52428 for D, and 52429 to 65535 for E. Hop C fails, and the list becomes A, B, D, E, with regions of 16384 keys.

| key | modulo-5 | modulo-4 after C fails | hash-threshold, 5 hops | hash-threshold, 4 hops |
|---|---|---|---|---|
| 31318 | D | D | C | B |
| 45085 | A | B | D | D |
| 15278 | D | D | B | A |
| 57049 | E | B | E | E |
| 4827 | C | E | A | A |
| 24250 | A | D | B | B |

Modulo-N moves four of the six flows, three of them away from hops that did not fail. Hash-threshold moves two: the flow of C, and the flow with key 15278 from B to A, because the region of B slid down.

**100,000 flows.** Hash 100,000 random flows (seed 7) to 16-bit keys with BLAKE2b, on five hops. Hash-threshold gives each hop between 19,882 and 20,094 flows. Then change the hops:

| change | modulo-N | hash-threshold | HRW | theory |
|---|---|---|---|---|
| remove C, the middle hop | 80,175 | 30,023 | 20,255 | 80,000, 30,000, 20,000 |
| remove E, the last hop | | 50,255 | | 50,000 for hash-threshold |
| add F at the end of the list | | 49,957 | | 50,000 for hash-threshold |
| add F as the fourth of six | | 30,172 | | 30,000 for hash-threshold |

**Where it runs.** RFC 2991 recommends HRW for a forwarder that keeps per-flow state, because the hash is computed only when a flow starts or a next hop is deleted, and hash-threshold for a forwarder without flow state. For multicast it recommends HRW to choose the upstream neighbor of each group (Section 4.2). Data center fabrics with many equal paths between racks use ECMP at every tier, and link aggregation groups use the same hashing over the member links of a bundle (RFC 7424).

## Variations

- **Which fields.** RFC 7424 (Section 4.3.1) lists the fields that can identify a flow: MAC addresses and VLAN, the IP protocol and addresses, the IPv6 flow label, the transport ports and MPLS labels. Fewer fields give coarser flows; for example, a hash of the addresses only keeps all connections between two hosts on one path.
- **Weighted ECMP.** Give a hop several regions or several table entries, in proportion to its capacity.
- **Resilient tables.** Fill a table of $B \gg N$ buckets with next hops and index it by the key. When a hop fails, refill only its buckets, so only its flows move, as with HRW, at the cost of one table read. [Maglev hashing](/maglev-hashing/) builds such a table with a permutation per backend. Linux has nexthop groups of type resilient that work this way.
- **Flowlets.** Split a flow at a gap between its packets that is longer than the difference in path delays, and hash each burst on its own. Reordering stays unlikely, and large flows spread over paths.
- **Hashing at a load balancer.** A [layer 4 load balancer](/layer-4-load-balancing/) uses the same per-flow hash to choose a backend, and often sits behind routers that use ECMP to reach the balancer instances.

## Pitfalls

- **Flows are not equal.** The hash balances the number of flows, not the bytes. A few long, fast flows can land on one path while another is idle. RFC 7424 (Section 3) gives such an example and the ways to move large flows. See [load skew](/load-skew/).
- **Modulo-N in a changing network.** A link that fails and recovers moves $(N-1)/N$ of the flows twice. Each moved TCP flow may see reordering, and a stateful firewall on the new path has no state for it and may drop it.
- **The same hash at two tiers.** If a router splits flows by hash-threshold over two next hops, and the next router uses the same hash on the same fields over its own two next hops, every flow that reaches the second router has a key in the lower half of the key space, so it uses only its first next hop. Seed the hash differently in each router. This effect is often called hash polarization.
- **Fragments and tunnels.** A fragment after the first has no ports, so a hash on ports sends it on another path than the first fragment (RFC 2991, Section 3). Tunnels hide the inner flow fields, so all traffic of a tunnel shares one path unless the hash reads the inner header or the outer header carries entropy.
- **Debugging.** Ping and traceroute packets are other flows than the traffic they test, so they may take another path (RFC 2991, Section 2).
- **Per-packet spraying.** Round robin per packet balances perfectly but reorders TCP segments, and the receiver sends duplicate acknowledgments that cause needless fast retransmits (RFC 2991, Section 2).

## Exercises

1. Prove that for even $N$ the smallest hash-threshold disruption is $N/(4(N-1))$, and find all $K$ that reach it.
2. A router has 4 next hops with hash-threshold. Hop 4 (an end region) fails, and later comes back at the end. What fraction of the flows changes path at least once, and what fraction is on its original path at the end?
3. Show that with modulo-N, going from $N$ to $N + 1$ hops moves the fraction $N/(N+1)$ of the flows, for keys uniform over a multiple of $N(N+1)$.
4. Two tiers of routers both use hash-threshold over two next hops with the same hash of the same fields. Show that half of the links of the second tier carry no traffic. What changes if the second tier uses modulo-2?
5. Design weighted hash-threshold for three hops with capacities 1, 1 and 2, and compute the disruption when the hop of capacity 2 fails, if it owns the last region and if it owns the middle one.

## References
