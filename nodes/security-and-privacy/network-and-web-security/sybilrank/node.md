---
tag: S4HXC8
kind: algorithm
slug: sybilrank
name: SybilRank
aliases:
- early-terminated trust propagation
area: security-and-privacy/network-and-web-security
level: research
summary: Ranks accounts by a short power iteration of trust from known honest seeds, which stays mostly inside the honest region.
model: word-ram
complexity:
  vars: {n: the number of accounts, m: the number of friendship edges, w: the number of iterations}
  time: {worst: O((n + m) log n), average: O((n + m) log n), best: O((n + m) log n)}
  space: {extra: O(n)}
properties: {deterministic: true, parallel: true, ranking_not_classification: true}
history:
  year: 2012
  people: [Qiang Cao, Michael Sirivianos, Xiaowei Yang, Tiago Pregueiro]
  note: Cao, Sirivianos, Yang and Pregueiro presented SybilRank at NSDI 2012, with a deployment at the social network Tuenti.
prereqs: [sybil-attack, power-iteration, markov-chain]
see_also: [sybilguard, pagerank, personalized-pagerank, trustrank, mixing-time, louvain-method, stationary-distribution, conductance]
sources:
  - paper: "Qiang Cao, Michael Sirivianos, Xiaowei Yang and Tiago Pregueiro, Aiding the detection of fake accounts in large scale social online services, USENIX NSDI 2012, pages 197 to 210"
    locator: Section 3 (the model and assumptions), Section 4.2 (trust propagation, early termination and Figure 4), Section 4.2.2 (seeds in several communities with the Louvain method), the security analysis, and the evaluation and the deployment at Tuenti
  - paper: "Haifeng Yu, Phillip B. Gibbons, Michael Kaminsky and Feng Xiao, SybilLimit: a near-optimal social network defense against Sybil attacks, IEEE Symposium on Security and Privacy 2008, pages 3 to 17, doi:10.1109/SP.2008.13"
    locator: the social network model with g attack edges and a fast-mixing honest region
  - paper: "Bimal Viswanath, Ansley Post, Krishna P. Gummadi and Alan Mislove, An analysis of social network-based Sybil defenses, ACM SIGCOMM 2010"
    locator: the analysis of social Sybil defenses as ranking by connectivity to trusted nodes
---

SybilRank ranks the accounts of a social network by how likely they are to be fake. It puts trust on a few accounts known to be honest, the seeds, and spreads it along friendships by [power iteration](/power-iteration/) for only about $\log n$ steps. Because fake accounts, the [Sybil](/sybil-attack/) identities, have few friendships with honest users, little trust reaches them in so few steps, and ranking accounts by trust divided by degree puts most of them at the bottom. Cao, Sirivianos, Yang and Pregueiro designed it for the operators of large networks, who then check the lowest-ranked accounts.

## In plain words

Pour water on a few people you trust in a crowd. Each round, everyone passes their water equally to their friends. Real people have many friends among each other, so the water spreads quickly through them. Fake accounts are friends mostly with other fake accounts and have only a few links to real people, so the water reaches them slowly.

Stop pouring after a few rounds, before the water has spread evenly everywhere. Then measure how much water each person holds per friend. The people with the least are most likely fake. If you wait too long, the water evens out across the whole crowd and the test no longer tells anything.

## The problem

**Input.** An undirected social graph $G = (V, E)$ with $n$ nodes and $m$ edges, every node of degree at least 1; a nonempty set of trust seeds $S$ known to be honest; a total trust $T_G > 0$; and a number of iterations $w$.

**Model** (Cao et al., Section 3). The nodes split into honest nodes $H$ and Sybil nodes. The honest region, the subgraph on $H$, is connected, not bipartite, and fast mixing: a random walk in it reaches its [stationary distribution](/stationary-distribution/) in $O(\log n)$ steps. The attacker can create any number of Sybil nodes and any edges among them, but only $g$ attack edges between Sybil and honest nodes, attached to random honest nodes.

**Output.** A ranking of $V$ from most suspect to least suspect.

## The algorithm

```pseudo id=main
SYBILRANK(G, S, T_G, w)
L1  for each node v: T(v) ← T_G / |S| if v is in S, else 0
L2  repeat w times
L3      T'(v) ← 0 for each node v
L4      for each node u and each neighbor v of u: T'(v) ← T'(v) + T(u) / deg(u)
L5      T ← T'
L6  for each node v: R(v) ← T(v) / deg(v)
L7  return the nodes sorted by R, lowest first (ties by name)
```

Line L4 is one step of the random walk on $G$, applied to the vector of trust: every node splits its trust evenly among its neighbors. The total $T_G$ stays the same. Cao et al. use $w = O(\log n)$; the code uses $w = \lceil \log_2 n \rceil$. Line L6 divides by the degree because, after many steps, trust is proportional to degree, so trust per degree is the quantity that is equal everywhere at the stationary state and lower on nodes that the walk has not reached yet.

## Example

The graph of Figure 4 of Cao et al. has honest nodes $A$ to $E$ and Sybil nodes $F$ to $I$, with edges $A$-$B$, $A$-$C$, $B$-$C$, $B$-$E$, $C$-$D$, $D$-$E$, $E$-$F$, $F$-$G$, $F$-$H$, $G$-$H$, $G$-$I$ and $H$-$I$. The only attack edge is $E$-$F$. The seeds are $C$ and $D$, with $T_G = 648$.

| iteration | $A$ | $B$ | $C$ | $D$ | $E$ | $F$ | $G$ | $H$ | $I$ |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 324 | 324 | 0 | 0 | 0 | 0 | 0 |
| 1 | 108 | 108 | 162 | 108 | 162 | 0 | 0 | 0 | 0 |
| 2 | 90 | 162 | 144 | 108 | 90 | 54 | 0 | 0 | 0 |
| 3 | 102 | 123 | 153 | 78 | 126 | 30 | 18 | 18 | 0 |
| 4 | 92 | 144 | 131 | 93 | 90 | 54 | 16 | 16 | 12 |
| degree | 2 | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 2 |
| $T / \deg$ after 4 | 46 | 48 | 43.67 | 46.5 | 30 | 18 | 5.33 | 5.33 | 6 |

The ranking, lowest first, is $G, H, I, F, E, C, A, D, B$: all four Sybils come before all five honest nodes. With 50 iterations instead of 4, the trust per degree is between 26.79 and 27.19 for every node, close to the stationary value $648 / 24 = 27$, and the ranking says almost nothing.

## Correctness

**Theorem (what is computed).** After line L5 has run $i$ times, $T(v) = T_G \cdot \Pr[X_i = v]$, where $X_0$ is a uniform random seed and $X_0, X_1, \ldots$ is the simple random walk on $G$. The total trust is $T_G$ at every step. If $G$ is connected and not bipartite, $T(v) \to T_G \deg(v) / (2m)$ as $i \to \infty$, so $R(v) \to T_G / (2m)$ for every $v$.

**Lemma (escape bound).** For any $w$, the total trust on Sybil nodes after $w$ iterations is at most the sum, over $i = 0, \ldots, w - 1$, of $\sum T^{(i)}(u) / \deg(u)$ over the attack edges $(u, s)$ with $u$ honest. This holds for every placement of Sybil nodes and edges, since trust enters the Sybil region only along attack edges. If, in addition, every honest node holds at most $\tau$ trust per degree at each step, the Sybil region holds at most $w g \tau$ trust after $w$ steps.

The proofs are in [proofs/correctness.md](proofs/correctness.md).

**Guarantee and its adversary** (Cao et al., security analysis; theorem, not proved here). Under the model above, with the attacker placing $g$ attack edges at random honest nodes and $w = O(\log n)$, the number of Sybil nodes ranked above (as less suspect than) honest nodes is $O(g \log n)$, however many Sybils the attacker creates. Against an attacker who places attack edges close to the seeds, the bound does not apply; Cao et al. study that case by experiment and recommend spreading many seeds.

## Complexity

In the [word RAM](/word-ram/) model, with trust as floating-point words:

- **Time.** Each iteration of lines L3 to L5 touches each node and each edge end once: $O(n + m)$. With $w = O(\log n)$ iterations the total is $O((n + m) \log n)$, and sorting in line L7 adds $O(n \log n)$.
- **Space.** Two vectors of $n$ values, $O(n)$ extra.
- **Parallelism.** Each iteration is a sparse matrix-vector product, which splits over machines; Cao et al. ran it on a cluster for the graph of Tuenti, with about 11 million users.

## Properties

- **A ranking, not a verdict.** The output tells operators which accounts to inspect first; no threshold is part of the algorithm.
- **No jumps.** Unlike [PageRank](/pagerank/) and [TrustRank](/trustrank/), the walk never jumps to random nodes or back to the seeds: random jumps would give Sybils trust in each step, and jumps to the seeds would favor Sybils attached near them.
- **Many seeds.** Trust is split over many seeds, so a wrong seed puts only a small share of the trust in the Sybil region.
- **Deterministic.** The same graph and seeds always give the same ranking.

## Variants and improvements

- **Seeds in every community.** Honest users in a community with few links to the seeds receive little trust and look like Sybils. Cao et al. (Section 4.2.2) find communities with the [Louvain method](/louvain-method/) and seed a few verified accounts in each.
- **Random-route defenses.** [SybilGuard](/sybilguard/) and SybilLimit accept or reject single nodes with random routes under the same model of attack edges and fast mixing. SybilRank replaces many random walks by one deterministic power iteration, which is cheaper on large graphs.
- **Personalized PageRank and TrustRank.** These run [personalized PageRank](/personalized-pagerank/) to convergence with jumps back to the seeds; SybilRank stops early and has no jumps.
- **Community detection.** Viswanath et al. (SIGCOMM 2010) showed that social Sybil defenses effectively rank nodes by how well connected they are to the trusted node, which links them to [community detection](/community-detection/).

## When to use it

Use SybilRank when an operator holds the whole social graph, can verify a few honest seeds per community, and wants a list of accounts to inspect in order. It fits fake accounts made in bulk that have few real friends. It does not fit when attackers can obtain many real friendships, for example by taking over real accounts, or when the honest graph is made of weakly linked groups without seeds in each.

## Pitfalls

- **Running to convergence.** If line L2 repeats until the vector stops changing, trust per degree becomes the same everywhere (the 50-iteration case of the example), and Sybils cannot be told apart. Stop after $w = O(\log n)$ iterations in line L2.
- **Ranking by raw trust.** If line L6 sets $R(v) \leftarrow T(v)$, honest nodes of low degree rank as suspect and a Sybil with many edges to other Sybils can rank as trusted. Divide by the degree, as in line L6.
- **Adding jumps.** If line L4 also sends a fraction of trust back to the seeds or to random nodes, Sybils near the seeds or anywhere gain trust in every step. Keep line L4 a plain walk step.
- **Seeds in one community.** If line L1 seeds only one community, honest communities far from it end up at the bottom of the ranking. Spread the seeds over the communities.
- **Nodes without friends.** A node of degree 0 makes line L4 and line L6 divide by zero. Remove such nodes first, or treat them separately.

## Implementations

The code runs on small synthetic graphs of at most 60 nodes. The tests reproduce Figure 4 exactly, compare the power iteration with an exact dense-matrix computation in fractions on 500 random graphs, check the escape bound, and measure the ranking on graphs with two regions and 2 attack edges: in 40 graphs with 30 honest and 30 Sybil nodes, all 1200 Sybils fell in the bottom 30 places (measurement).

## History

Yu, Kaminsky, Gibbons and Flaxman introduced social-network Sybil defenses with SybilGuard in 2006, followed by SybilLimit in 2008. Viswanath, Post, Gummadi and Mislove analyzed these defenses in 2010. Cao, Sirivianos, Yang and Pregueiro presented SybilRank at NSDI 2012, replacing random routes by early-terminated power iteration, and reported that at Tuenti about 90% of the 200,000 lowest-ranked accounts were fake (measurement).

## References
