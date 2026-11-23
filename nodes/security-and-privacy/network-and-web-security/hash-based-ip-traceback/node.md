---
tag: 3RR23Q
kind: algorithm
slug: hash-based-ip-traceback
name: Hash-based IP traceback
aliases:
- SPIE
- source path isolation engine
area: security-and-privacy/network-and-web-security
level: advanced
summary: Routers keep Bloom filters of digests of recent packets, so a single packet can be traced back by querying routers hop by hop.
solves: [ip-traceback-problem]
model: word-ram
complexity:
  vars: {k: the number of hash functions, V: the number of routers, E: the number of links, m: the bits in one digest table}
  time: {worst: O(k(V + E)), average: O(k(V + E)), best: O(k)}
  space: {extra: O(V)}
properties: {deterministic: true, no_false_negatives: true, single_packet: true}
history:
  year: 2001
  people: [Alex C. Snoeren, Craig Partridge, Luis A. Sanchez, Christine E. Jones, Fabrice Tchakountio, Stephen T. Kent, W. Timothy Strayer]
  note: Snoeren and colleagues at BBN Technologies presented the Source Path Isolation Engine at SIGCOMM 2001, with a journal version in 2002.
prereqs: [ip-traceback-problem, bloom-filter, breadth-first-search]
see_also: [probabilistic-packet-marking, ingress-filtering, false-positive-rate, universal-hashing, counting-bloom-filter, reachability, intrusion-detection-problem]
sources:
  - paper: "Alex C. Snoeren, Craig Partridge, Luis A. Sanchez, Christine E. Jones, Fabrice Tchakountio, Stephen T. Kent and W. Timothy Strayer, Hash-based IP traceback, ACM SIGCOMM 2001, pages 3 to 14, doi:10.1145/964723.383060"
    locator: Section 2 (goals and transformations), Section 4 (digests of the invariant bytes, Bloom filters and hash families), Section 5 (the architecture and the traceback process, with reverse-path flooding in Section 5.4), Section 6 (the prototype) and Section 7 (the analysis of false positives and of storage)
  - paper: "Alex C. Snoeren, Craig Partridge, Luis A. Sanchez, Christine E. Jones, Fabrice Tchakountio, Beverly Schwartz, Stephen T. Kent and W. Timothy Strayer, Single-packet IP traceback, IEEE/ACM Transactions on Networking 10(6), pages 721 to 734, December 2002"
    locator: the journal version of the same system
  - paper: "Burton H. Bloom, Space/time trade-offs in hash coding with allowable errors, Communications of the ACM 13(7), 1970"
    locator: the Bloom filter and its error rate
---

Hash-based IP traceback, built as the Source Path Isolation Engine (SPIE), solves the single-packet version of the [IP traceback problem](/ip-traceback-problem/). Each router stores a [Bloom filter](/bloom-filter/) of digests of the packets it forwarded in a recent time window. To trace one packet, the victim's side asks the nearest router whether it saw the packet, and every router that answers yes asks its own neighbors, in a [breadth-first search](/breadth-first-search/) backward along the path. The answer never misses a router that forwarded the packet, and it may contain a few extra routers because of false positives.

## In plain words

Every post office keeps a small sheet of tick boxes for each hour. For each letter it handles, it ticks a few boxes chosen by a secret rule from the letter's address and first line. It never writes the letter down.

When a harmful letter arrives, an investigator goes to the last office and asks: "are all the boxes for this letter ticked?" If yes, the letter probably passed there, and the investigator asks each office that sends mail to it. Offices that say no stop the search on that branch. An office that handled the letter always says yes. An office that did not may say yes by chance when its sheet is nearly full, so the answer can include a few wrong offices but never miss a right one.

## The problem

Given one packet $x$ that reached a victim $v$, and the time it arrived, output a set of routers that contains every router that forwarded $x$ (Snoeren et al., Section 2). The network is a graph $G$ of routers and links. The attacker chooses the contents of $x$ and of any other traffic, including forged source addresses. The routers on the path are not compromised, and their hash keys are secret. A router cannot store packets: it can afford a few bits per packet for a short time.

## The algorithm

Each router $r$ has a digest table $T_r$: a Bloom filter of $m$ bits with $k$ hash functions $h_{r,1}, \ldots, h_{r,k}$ chosen at random by $r$. The hash input is the part of the packet that routers do not change. When the table holds its capacity of packets, the router saves it with a time stamp and starts an empty one.

```pseudo id=main
INSERT(T, x)                      ▷ router r forwards x
L1  for i ← 1 to k do
L2      T[h_{r,i}(invariant(x))] ← 1

QUERY(T, x)
L3  return T[h_{r,i}(invariant(x))] = 1 for every i in 1..k

TRACE(G, v, x)                    ▷ reverse-path flooding from the victim
L4  found ← ∅, seen ← {v}, Q ← a queue holding v
L5  while Q is not empty do
L6      u ← the first node of Q, removed
L7      for each neighbor r of u with r not in seen do add r to seen
L8          if QUERY(T_r, x) for the table of the time x passed r then
L9              add r to found and to the end of Q
L10 return found
```

Line L8 uses the table that covered the time when $x$ could have passed $r$. A router that answers no is not searched further, so the search stays close to the true path.

## Example

Take the graph of the [IP traceback problem](/ip-traceback-problem/) page with links $v$-$R_1$, $R_1$-$R_2$, $R_2$-$R_3$, $R_2$-$R_4$, $R_3$-$R_5$, $R_3$-$R_6$ and $R_4$-$R_7$. Each table has $m = 32$ bits and $k = 3$ functions, keyed by a secret of its router. Four background packets enter, two at $R_5$ and two at $R_7$, and then the packet $x$, from 198.51.100.7 to 192.0.2.1, enters at $R_6$ and takes the path $R_6, R_3, R_2, R_1$. Then $v$ traces $x$:

| step | asked by | router | positions of $x$ | bits at those positions | answer |
|---|---|---|---|---|---|
| 1 | $v$ | $R_1$ | 25, 14, 5 | 1, 1, 1 | yes |
| 2 | $R_1$ | $R_2$ | 17, 26, 9 | 1, 1, 1 | yes |
| 3 | $R_2$ | $R_3$ | 7, 16, 18 | 1, 1, 1 | yes |
| 4 | $R_2$ | $R_4$ | 7, 23, 26 | 0, 0, 1 | no |
| 5 | $R_3$ | $R_5$ | 27, 26, 8 | 0, 0, 1 | no |
| 6 | $R_3$ | $R_6$ | 19, 18, 12 | 1, 1, 1 | yes |

The answer is $\{R_1, R_2, R_3, R_6\}$, the true path. $R_7$ is never asked, because $R_4$ said no. $R_4$ holds 2 packets, so its false-positive rate is $(1 - (1 - 1/32)^{6})^3 \approx 0.0052$; $R_1$ holds 5 packets and has 14 of its 32 bits set. With the same graph and 18 background packets in 16-bit tables with $k = 2$, the tables are nearly full, $R_4$ and $R_7$ also answer yes, and the answer grows to six routers.

## Correctness

**Theorem (no false negatives).** Assume that the routers on the path of $x$ are not compromised, that each recorded $x$ with INSERT, that no router changed the invariant fields, and that the query reaches each table before the router discards it. Then TRACE returns a set that contains every router on the path, against an attacker who chooses all packets. With exact sets in place of Bloom filters, TRACE returns exactly the routers that forwarded $x$.

The proof is by induction along the path from $v$: a Bloom filter has no false negatives, so each router on the path answers yes, and each one is a neighbor of the previous one, which also answered yes. With exact sets, only forwarders answer yes. The full proof is in [proofs/correctness.md](proofs/correctness.md).

**Theorem (extra routers; Snoeren et al., Section 7.1.1).** If every router has at most $d$ neighbors and every table has a [false-positive rate](/false-positive-rate/) of at most $P = p/d$, then the expected number of extra routers in the answer for a path of $n$ routers is at most $n p/(1 - p)$. The paper calls its analysis simplistic: it assumes that the sets of neighbors of different nodes are disjoint and that the tables are full, so it is a worst-case bound for their model. For $p = 1/8$ this gives $n/7$, so at most $32/7 \approx 4.6$ extra routers on average for a path of 32. Their simulation on the topology of a tier-one ISP with about 70 backbone routers found far fewer false positives than the bound (measurement, Section 7.1.2).

**Rate of one table** (theorem for ideal hash functions). After $n$ packets in a table of $m$ bits with $k$ functions, a packet that was not inserted passes the query with probability $(1 - (1 - 1/m)^{kn})^k \approx (1 - e^{-kn/m})^k$ (Section 7.2). With $k = 3$ and $m = 5n$ this is 0.092; with 8 functions and $m/n = 12$ it is 0.00314. For $m = 256$, $k = 3$ and $n = 40$ the formula gives 5.3%, and the tests measure 4.8% over 10,000 queries to 25 tables (measurement).

## Complexity

In the [word RAM](/word-ram/) model, with one hash evaluation taken as $O(1)$ for a fixed input length:

- **Per packet at a router.** INSERT costs $O(k)$ time. The table needs $m$ bits for $n$ packets, so the cost is $m/n$ bits per packet, a constant set by the chosen false-positive rate.
- **Per trace.** TRACE asks each router at most once and looks at each link at most twice, so it takes $O(k(V + E))$ time and $O(V)$ extra space. In practice it touches only the routers near the path and their neighbors. The best case is $O(k)$: the router next to $v$ says no.
- **Storage.** Snoeren et al. (Section 7.2) estimate the storage at about 0.5% of the total link capacity of a router per unit of time (heuristic, for their chosen rate); for an OC-3 router with 4 links, about 47 MB per minute.

## Properties

- **One packet suffices.** Unlike [probabilistic packet marking](/probabilistic-packet-marking/), SPIE traces a single packet, such as one that crashed a host.
- **No false negatives.** A router on the path always answers yes, while its table is kept.
- **Privacy.** Routers keep digests, not packets, so a table does not reveal the traffic it saw; it only answers membership questions.
- **Limited time.** The answer depends on the tables still being kept, so a trace must start before the router discards the tables for the time of the packet.
- **State in routers.** Every router needs memory written at line rate, which is the price of single-packet tracing.

## Variants and improvements

- **The digest input.** SPIE hashes the first 28 invariant bytes of a packet: the IP header with the type of service, TTL, checksum and options masked, plus the first 8 bytes of the payload (Section 4). On their traces, 28 bytes gave a rate of identical digests for distinct packets of 0.00092% in a wide-area trace and 0.139% in a local trace (measurement).
- **Hash families.** Section 4.3 uses a [universal hash family](/universal-hashing/), so that two different packets collide with probability $2^{-m'}$ for $m'$-bit outputs, with members chosen independently at each router. The prototype of Section 6 uses MD5 with a random input vector to produce four 32-bit digests, and changes the input vectors each time a table is paged. The code here uses keyed BLAKE2b in the same role, which is a heuristic for independence.
- **Transformations.** Routers that change a packet, for example by fragmentation, tunneling or network address translation, store a transform lookup table entry so that the trace can continue with the original packet (Section 5.3).
- **Architecture.** Data generation agents in the routers compute digests, SPIE collection and reduction agents gather tables for a region, and a SPIE traceback manager runs the query (Section 5.1).
- **Counting filters.** A [counting Bloom filter](/counting-bloom-filter/) allows deletion, so a router could remove old digests one by one instead of paging whole tables, at a cost of several bits per position.

## When to use it

Use hash-based traceback when one packet, or a few, must be traced, and the routers can spend memory written at line rate. Use [probabilistic packet marking](/probabilistic-packet-marking/) when routers cannot keep state and the attack is a flood. Use [ingress filtering](/ingress-filtering/) to stop forged sources at the edge, which makes many traces unnecessary.

## Pitfalls

- **Hashing fields that change.** If lines L2 and L3 hash the whole header, the TTL and checksum that each router changes make the victim's copy hash to different positions than the copy each upstream router stored, and line L3 answers no on the true path. Hash only invariant(x), as in lines L2 and L3.
- **Flooding through every router.** If line L9 adds every neighbor to $Q$, not only those that answered yes, the search visits the whole network and collects every false positive in it. Add $r$ to $Q$ only when line L8 says yes.
- **Full tables.** If a table is not paged when it reaches its capacity, its bits fill up and line L3 answers yes for almost every packet; the example with 18 background packets shows the answer growing. Page the table when it holds $n$ packets, with $m/n$ fixed by the target rate.
- **Shared hash keys.** If all routers use the same functions in line L2, a packet that collides at one router tends to collide at its neighbors that saw the same traffic, and an attacker who learns the functions can craft collisions. Choose the functions at random per router and per table.
- **Asking the wrong table.** If line L8 asks the current table instead of the one that covered the time of $x$, the trace misses routers after a page change. Use the arrival time and the path delay to pick the table.

## Implementations

The code is a synthetic model: packets are tuples with documentation addresses, routers are names in a graph of at most 20 nodes, and nothing is sent. The tests compare TRACE with Bloom filters against TRACE with exact sets on 500 random graphs, check that the Bloom answer always contains the true path, and measure the false-positive rate of a table.

## History

Logging of whole packets for traceback was known to be too costly for fast routers, as Savage et al. noted in 2000. Snoeren, Partridge, Sanchez, Jones, Tchakountio, Kent and Strayer at BBN Technologies replaced logs by Bloom filters of digests and described the Source Path Isolation Engine, with a prototype, at SIGCOMM 2001. The journal version followed in 2002. Bloom described the filter in 1970.

## References
