---
tag: EZNZ9R
kind: algorithm
slug: probabilistic-packet-marking
name: Probabilistic packet marking
aliases:
- PPM traceback
- Savage packet marking
area: security-and-privacy/network-and-web-security
level: core
summary: Each router overwrites a mark in a packet with a small probability, and the next router completes it into an edge with a distance. The victim rebuilds the attack path from many packets.
solves: [ip-traceback-problem]
model: word-ram
complexity:
  vars: {d: the number of routers on the attack path, p: the marking probability, m: the number of packets received, e: the number of distinct edges received}
  time: {worst: O(1), average: O(1), best: O(1)}
  space: {extra: O(e)}
properties: {deterministic: false, stateless_routers: true, online: true}
history:
  year: 2000
  people: [Stefan Savage, David Wetherall, Anna Karlin, Tom Anderson]
  note: Savage, Wetherall, Karlin and Anderson presented edge sampling and its encoding in the IP identification field at SIGCOMM 2000. Burch and Cheswick had suggested the idea of marking.
prereqs: [ip-traceback-problem, coupon-collector-problem, geometric-distribution]
see_also: [hash-based-ip-traceback, ingress-filtering, syn-flooding, coupon-collector-problem, inclusion-exclusion-principle, harmonic-series, union-bound]
sources:
  - paper: "Stefan Savage, David Wetherall, Anna Karlin and Tom Anderson, Practical network support for IP traceback, ACM SIGCOMM 2000, pages 295 to 306, doi:10.1145/347059.347560"
    locator: Section 3 (definitions and assumptions), Section 4.2 (node sampling), Section 4.3 and Figure 4 (edge sampling and its expected number of packets), Section 5.1 (compressed edge fragments) and Section 5.2 (the encoding in the IP identification field)
  - paper: "Stefan Savage, David Wetherall, Anna Karlin and Tom Anderson, Network support for IP traceback, IEEE/ACM Transactions on Networking 9(3), pages 226 to 237, 2001"
    locator: the journal version of the same algorithms and analysis
  - paper: "Micah Adler, Tradeoffs in probabilistic packet marking for IP traceback, ACM STOC 2002, pages 407 to 418"
    locator: the abstract and the introduction (the trade-off between header bits and packets)
---

Probabilistic packet marking (PPM) is a solution to the [IP traceback problem](/ip-traceback-problem/) in which routers write parts of the path into the packets they forward. In edge sampling, the version of Savage, Wetherall, Karlin and Anderson, each router overwrites a mark field with its own address with a small probability $p$, the next router writes its address as the other end of the edge, and every router adds one to a distance field. A victim of a flood collects the marks and rebuilds the attack path, router by router, from the edges and their distances. Routers keep no state, and the part of the path between the victim and the attacker cannot be faked.

## In plain words

Think of a long line of people who pass a bucket of notes from a stranger to you. Each person, with a small chance, throws out the note in the bucket and writes a new one: "I am Ann". The next person in line adds "and after me came Bob", and every person after that adds a tally mark. When the bucket arrives, the note says who wrote it, who came next, and how many people passed it after that.

One bucket tells you about one pair of neighbors in the line. After many buckets you have a note for every pair, and the tally marks tell you how to put the pairs in order. A fake note from the stranger may be thrown out by anyone, and if it survives, its tally shows that it started beyond the whole line.

## The problem

The setting is the approximate traceback problem of the [IP traceback problem](/ip-traceback-problem/) page. An attacker sends many packets to a victim $v$ along a stable path of routers $R_1, \ldots, R_d$, where $R_1$ is the first router after the attacker and $R_d$ is next to $v$. Each packet has a mark with three fields: start, end and distance. The attacker can write any value into these fields. Routers have no memory per flow. From the marks it receives, $v$ must output a path that ends with $(R_1, \ldots, R_d, v)$. The threat model is that of Savage et al., Section 3.2: no router on the path is compromised.

## The algorithm

Each router runs MARK on each packet it forwards, with a fresh uniform draw $u$. The victim runs RECONSTRUCT on the marks of the packets it received. The distance field saturates at its largest value, 31 for the 5-bit field of the IP encoding.

```pseudo id=main
MARK(w, R, p)                    ▷ router R forwards a packet with mark w
L1  u ← a uniform draw from [0, 1)
L2  if u < p then
L3      return (R, nil, 0)       ▷ start, end, distance
L4  if w.distance = 0 then
L5      w.end ← R
L6  return (w.start, w.end, min(w.distance + 1, 31))

RECONSTRUCT(W, v)                ▷ W: the marks the victim received
L7  E ← the empty set of edges (x, y, k)
L8  for each mark w in W with w.start ≠ nil do
L9      if w.distance = 0 then add (w.start, v, 0) to E
L10     else add (w.start, w.end, w.distance) to E
L11 keep (x, y, k) only if y = v and k = 0, or (y, z, k - 1) is kept, for k = 0, 1, 2, ...
L12 return the kept edges and the paths they form toward v
```

The time column of the front matter is the cost of MARK for one router and one packet. A router that marks (line L3) starts a new edge and sets the distance to 0. The next router sees distance 0 and writes itself as the end of the edge (line L5); every router that does not mark adds one to the distance (line L6). So when the router $j$ hops from $v$ marks a packet and no later router marks it, the victim gets the edge from that router to the next one, with distance $j - 1$. The router next to $v$ produces $(R_d, \text{nil}, 0)$, which line L9 turns into the edge $(R_d, v, 0)$. Line L11 removes edges that do not chain to $v$: it keeps the edges at distance 0 that end at $v$, then the edges at distance 1 that end at the start of a kept edge, and so on.

## Example

Take the path $R_1, R_2, R_3, R_4$ to $v$ and $p = 1/4$. A router marks when its draw is below 0.25. The table shows the first eight packets of a seeded run; when several routers mark one packet, only the last one counts.

| packet | draws at $R_1, R_2, R_3, R_4$ | routers that mark | mark at $v$ | edges known |
|---|---|---|---|---|
| 1 | 0.32, 0.15, 0.65, 0.07 | $R_2$, $R_4$ | $(R_4, \text{nil}, 0)$ | $(R_4, v, 0)$ |
| 2 | 0.54, 0.37, 0.06, 0.51 | $R_3$ | $(R_3, R_4, 1)$ | + $(R_3, R_4, 1)$ |
| 3 | 0.04, 0.43, 0.07, 0.09 | $R_1$, $R_3$, $R_4$ | $(R_4, \text{nil}, 0)$ | no change |
| 4 | 0.42, 0.83, 0.12, 0.22 | $R_3$, $R_4$ | $(R_4, \text{nil}, 0)$ | no change |
| 5 | 0.63, 0.95, 0.58, 0.40 | none | the empty initial mark, now $(\text{nil}, R_1, 4)$ | no change |
| 6 | 0.98, 0.05, 0.86, 0.29 | $R_2$ | $(R_2, R_3, 2)$ | + $(R_2, R_3, 2)$ |
| 7 | 0.14, 0.12, 0.31, 0.82 | $R_1$, $R_2$ | $(R_2, R_3, 2)$ | no change |
| 8 | 0.18, 0.58, 0.64, 0.37 | $R_1$ | $(R_1, R_2, 3)$ | + $(R_1, R_2, 3)$ |

After packet 8 the victim has all four edges, and line L11 keeps them in the order of their distances: $(R_1, R_2, R_3, R_4, v)$. A forged mark such as $(X, Y, 3)$ that survives all four routers arrives as $(X, Y, 7)$; line L11 drops it, because no kept edge at distance 6 starts at $Y$.

The mark of the router $j$ hops from $v$ arrives with probability $q_j = p(1-p)^{j-1}$: here 0.25, 0.1875, 0.1406 and 0.1055, and the attacker's mark survives with probability $(3/4)^4 = 0.3164$. The exact expected number of packets until all four edges arrive is 14.17. For the case $d = 10$ and $p = 1/25$ that Savage et al. use, the exact expectation is 89.57 packets.

## Correctness

**Theorem.** Assume that no router on the path is compromised and the path is fixed. (1) Each packet's mark at $v$ is the edge $(R_{d-j+1}, R_{d-j+2}, j - 1)$ (with $R_{d+1} = v$) with probability $q_j = p(1-p)^{j-1}$ for $j = 1, \ldots, d$, independently across packets, and otherwise it is the attacker's mark with distance at least $d$. (2) If $W$ contains every edge of the path, RECONSTRUCT keeps all of them, and every other kept edge has distance at least $d$, so every path it returns ends with $(R_1, \ldots, R_d, v)$. This solves approximate traceback robustly against an attacker who controls the initial mark. (3) The expected number of packets until every edge has arrived is

$$
E[X] = \sum_{\emptyset \ne S \subseteq \{1, \ldots, d\}} \frac{(-1)^{|S|+1}}{\sum_{j \in S} q_j} \le \frac{H_d}{p(1-p)^{d-1}} .
$$

The key invariant for (1) is that after the router at position $i$ the distance field equals the number of routers since the last marking router, or exceeds the number of routers so far if none marked; the saturation at 31 keeps this a lower bound. Part (3) is [inclusion and exclusion](/inclusion-exclusion-principle/) on the event that some edge is missing, and the bound is the [coupon collector](/coupon-collector-problem/) argument with each missing edge arriving with probability at least $p(1-p)^{d-1}$. The full proof is in [proofs/correctness.md](proofs/correctness.md).

**About the printed bound.** Savage et al. (Section 4.3) write the bound as $E[X] < \ln(d) / (p(1-p)^{d-1})$, from the coupon collector estimate $d(\ln d + O(1))$ with the $O(1)$ term dropped. It is an estimate, not a bound: for $d = 10$ and $p = 1/25$ it gives 83.12, but the exact value is 89.57; for $d = 2$ and $p = 1/25$ it gives 18.05 against an exact 38.29. The bound with the [harmonic number](/harmonic-series/) $H_d$ holds for all $d$ and $p$: it gives 105.73 for $d = 10$ and $p = 1/25$.

## Complexity

In the [word RAM](/word-ram/) model, with router addresses as words:

- **Routers.** MARK does one draw, one comparison and at most two writes: $O(1)$ time per packet per router and no memory per flow.
- **Victim.** Lines L7 to L10 take $O(m)$ expected time with a hash set for $m$ marks. Line L11 groups the $e$ distinct edges by distance and checks each against the starts of the previous level, which is $O(e)$ expected time. The space is $O(e)$.
- **Packets.** By the theorem, the expected number of packets is at most $H_d / (p(1-p)^{d-1})$. The function $p(1-p)^{d-1}$ is largest at $p = 1/d$, which is why Savage et al. suggest $p$ near $1/d$; their examples use $p = 1/25$.

## Properties

- **Stateless routers.** No table, no per-flow memory, and no extra packets.
- **Robust suffix.** A forged mark can only add edges at distance $d$ or more, so it cannot change the part of the answer next to the victim.
- **Needs many packets.** Rebuilding a path takes tens to thousands of packets, so PPM fits floods, not single packets.
- **Randomized.** The marks depend on the draws of the routers, so the number of packets is a random variable; the theorem bounds its mean.

## Variants and improvements

- **Node append.** Every router appends its address to the packet (Section 4.1). The path arrives in one packet, but the packet grows with $d$, which IP does not allow.
- **Node sampling.** Each router writes only its address with probability $p$ (Section 4.2). The victim orders routers by how often they appear, which needs very many packets for far routers: Savage et al. report more than 42,000 packets for $d = 15$ and $p = 0.51$. It is also not robust to forged marks.
- **Compressed edge fragments.** To fit in the 16-bit IP identification field, a router stores the XOR of the two addresses of an edge and splits it, with a hash for checking, into $k = 8$ fragments of 8 bits (Sections 5.1 and 5.2: 3 bits of offset, 5 bits of distance, 8 bits of fragment). The victim must collect all $k d$ fragments. Savage et al. give about $k \ln(kd)/(p(1-p)^{d-1})$, slightly under 1300 packets for $k = 8$, $d = 10$ and $p = 1/25$; the exact expectation by inclusion and exclusion over the 80 fragments is 1228.5.
- **Advanced and authenticated marking.** Song and Perrig (INFOCOM 2001) use a map of upstream routers to cut the cost of reconstruction with many attackers, and add authentication of marks against compromised routers.
- **Fewer bits.** Adler (STOC 2002) showed that a single bit per packet suffices for one path, at a cost in packets that grows exponentially with the length of the path's description, and studied the trade-off between bits and packets.

## When to use it

Use PPM when the routers on the path cannot keep state and the attack is a flood of many packets. Use [hash-based IP traceback](/hash-based-ip-traceback/) when a single packet must be traced and the routers can store digests for a time window. Use [ingress filtering](/ingress-filtering/) to prevent forged sources in the first place; PPM exists because ingress filtering is not deployed everywhere. With many attackers on many paths, the victim gets many edges at each distance, and combining fragments becomes expensive; this is the case that Song and Perrig improved.

## Pitfalls

- **Writing the end on every packet.** If the test of line L4 is dropped and line L5 writes $w.end \leftarrow R$ whenever the router does not mark, the end field holds the last router instead of the router after the start, and every edge with distance above 1 is wrong. Write the end only when $w.distance = 0$, as in line L4.
- **Wrapping the distance.** If line L6 uses $w.distance + 1$ modulo 32 instead of saturating at 31, an attacker can set the initial distance so that it wraps to a small value at the victim, and a forged edge then lands inside the valid suffix. Use $\min(w.distance + 1, 31)$.
- **Trusting edges that do not chain.** If line L11 is skipped and every received edge is used, a forged mark adds routers that are not on the path. Keep only edges that chain to $v$ with distances decreasing by one.
- **A large marking probability.** With $p = 1/2$ and $d = 10$, the far router's edge arrives with probability $2^{-10}$, and the expected number of packets is in the thousands. Choose $p$ near $1/d$ for the longest expected path.
- **Using the printed estimate as a bound.** The value $\ln(d)/(p(1-p)^{d-1})$ is below the true expectation for small $d$ and for $d = 10$, $p = 1/25$. Use the exact sum or the bound with $H_d$.

## Implementations

The code runs on synthetic paths and trees of abstract router names; it builds no packet and touches no network. The tests enumerate every marking decision on short paths and compare the distribution of the mark at the victim with $q_j$, rebuild random attack trees, and check the Monte Carlo mean against the exact expectation.

## History

Savage et al. credit Burch and Cheswick with the idea of marking packets with the addresses of routers to trace floods. Savage, Wetherall, Karlin and Anderson worked out node append, node sampling, edge sampling and the compressed encoding, with an implementation and a simulation, at SIGCOMM 2000, and in the journal version in 2001. Song and Perrig improved the reconstruction and added authentication in 2001, and Adler gave the first study of how many header bits a marking scheme needs in 2002.

## References
