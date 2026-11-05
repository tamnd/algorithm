---
tag: C4CRWZ
kind: model
slug: kleinberg-small-world-model
name: Kleinberg small-world model
aliases:
- navigable small world
area: graphs/network-analysis
level: advanced
summary: Lattice with long-range links whose distribution makes greedy routing efficient.
prereqs: [small-world-network, watts-strogatz-model, harmonic-series]
see_also: [six-degrees-of-separation, small-world-network, watts-strogatz-model, navigable-small-world, chord, kademlia, greedy-best-first-search]
sources:
  - paper: doi:10.1145/335305.335325
    title: Jon Kleinberg, The small-world phenomenon, an algorithmic perspective, Proceedings of the 32nd ACM Symposium on Theory of Computing (STOC 2000), 163 to 170
    locator: the model on the n by n lattice with parameters p, q and r, the definition of a decentralized algorithm, Theorem 1 (the lower bound for r = 0), Theorem 2 (greedy routing in O(log^2 n) for r = 2), Theorem 3 (0 ≤ r < 2) and Theorem 4 (r > 2), and the k-dimensional version
  - paper: doi:10.1038/35022643
    title: Jon M. Kleinberg, Navigation in a small world, Nature 406, 845 (2000)
    locator: the short summary of the model and of the theorem that r = 2 is the only exponent in two dimensions for which a decentralized algorithm finds paths of polylogarithmic length
  - paper: doi:10.1038/30918
    title: Duncan J. Watts and Steven H. Strogatz, Collective dynamics of small-world networks, Nature 393, 440 to 442 (1998)
    locator: the rewired ring lattice with high clustering and short paths, the model that Kleinberg's extends with a distance-dependent link law
  - book: isbn:9780521195331
    title: David Easley and Jon Kleinberg, Networks, Crowds, and Markets, Reasoning about a Highly Connected World, Cambridge University Press, 2010
    locator: Chapter 20, The Small-World Phenomenon (decentralized search, the inverse-square law and its proof idea by distance scales, and the evidence from social networks with geography)
---

The Kleinberg small-world model is a grid in which each vertex has edges to its lattice neighbours and one extra long-range edge, whose far end is $v$ with probability proportional to $d(u, v)^{-r}$, a power of the lattice distance. Jon Kleinberg introduced it in 2000 to ask not only whether a social network has short chains between people, as in Milgram's experiment and the [Watts-Strogatz model](/watts-strogatz-model/), but whether people can *find* them using only local information. His answer is sharp: on the two-dimensional grid with $N = n^2$ vertices, the greedy rule "forward to the contact closest to the target" delivers a message in $O(\log^2 n)$ expected steps when $r = 2$, and for every other $r \ge 0$ every decentralized algorithm needs a number of steps polynomial in $n$. In $k$ dimensions the right exponent is $r = k$. Graphs with this property are called *navigable*.

## The machine

**Parameters.** The side length $n$, a local range $p \ge 1$, a number $q \ge 0$ of long-range links per vertex, and an exponent $r \ge 0$. The vertices are the points $(i, j)$ with $1 \le i, j \le n$, and the lattice distance is $d((i, j), (k, l)) = |k - i| + |l - j|$.

**The edges.** Each vertex $u$ has a directed edge to every $v$ with $d(u, v) \le p$, its *local contacts*. Then, independently, $u$ gets $q$ long-range directed edges; each goes to $v \ne u$ with probability

$$\Pr[u \to v] = \frac{d(u, v)^{-r}}{\sum_{w \ne u} d(u, w)^{-r}}.$$

With $r = 0$ the long links are uniform, as in the rewired model of Watts and Strogatz. As $r$ grows, the links become shorter, and for large $r$ they are almost all local. The basic case has $p = q = 1$: four lattice neighbours, fewer on the border, and one long link.

**Decentralized algorithms.** A message starts at $s$ and must reach $t$. At each step, the vertex that holds the message knows the lattice, the position of $t$, its own contacts and the contacts of the vertices that held the message before, but not the long-range links of the other vertices. It passes the message to one of its contacts. The *delivery time* is the number of steps, in expectation over the random links and over a uniform choice of $s$ and $t$.

**Greedy routing.** The vertex that holds the message passes it to the contact, local or long-range, that is closest to $t$ in lattice distance. Some lattice neighbour is always one step closer, so the distance falls by at least 1 at every step, and the message arrives within $2n - 2$ steps. Since no vertex is visited twice, each long link is used at most once and can be drawn when the message first reaches its vertex, which is how a simulation can run on a grid with $10^8$ vertices.

**Generating the links.** For $r = 2$, the normalizer of a vertex is $\sum_{w \ne u} d(u, w)^{-2}$. At most $4j$ vertices lie at distance exactly $j$, so it is at most $\sum_{j=1}^{2n-2} 4j \cdot j^{-2} = 4 H_{2n-2} \le 4 \ln(6n)$, where $H_m$ is the $m$-th [harmonic number](/harmonic-series/). This bound drives the analysis below.

## What it counts

The model measures how long a local search takes, as a function of $n$ and $r$, compared with the length of the shortest paths.

**Why $r = 2$ works, the proof idea.** Take $p = q = 1$ and greedy routing, and say the message is in *phase* $j$ when its distance to $t$ is in $(2^j, 2^{j+1}]$. Let the current holder be $u$ and let $B_j$ be the set of vertices within distance $2^j$ of $t$. The set $B_j$ has at least $2^{2j-1}$ vertices of the grid, and each of them is within distance $2^{j+1} + 2^j < 2^{j+2}$ of $u$. So the long link of $u$ lands in $B_j$ with probability at least

$$2^{2j-1} \cdot \frac{(2^{j+2})^{-2}}{4 \ln(6n)} = \frac{1}{128 \ln(6n)}.$$

The links of the vertices visited are independent and the distance never grows, so phase $j$ lasts at most $128 \ln(6n)$ steps in expectation. There are at most $\log_2 n + 2$ phases, and the delivery time is $O(\log^2 n)$. The point is that $d^{-2}$ in two dimensions gives each distance scale $2^j$ the same total probability, about $1/\log n$, so the long link helps equally at every scale.

**Why other exponents fail.** For $r < 2$, the links are spread too evenly: they are long, but the chance that one lands near $t$ is small. For $r = 0$, a ball of radius $n^{2/3}$ around $t$ holds about $n^{4/3}$ of the $n^2$ vertices, so a link lands in it with probability about $n^{-2/3}$; a search of fewer than $\delta n^{2/3}$ steps probably finds no such link, and without one it must walk the last $n^{2/3}$ steps. For $r > 2$, the links are too short: a link longer than some length $L$ is rare, and without such links the message moves only $L$ per step. Balancing the two gives the bounds of the table below.

**A simulation.** One run of greedy routing with $p = q = 1$, 1000 uniform pairs $s, t$ per cell, links drawn on first visit, and the random seed 2000, gave these average delivery times.

| $n$ (grid $n \times n$) | $r = 0$ | $r = 1$ | $r = 2$ | $r = 3$ |
|---|---|---|---|---|
| 100 | 22.2 | 19.6 | 26.0 | 48.7 |
| 1000 | 103.7 | 65.5 | 72.0 | 400.4 |
| 10000 | 493.3 | 205.7 | 140.2 | 3426.5 |

For $r = 0$ the times grow by a factor of about $4.7$ for each factor 10 in $n$, close to $10^{2/3} \approx 4.6$. For $r = 2$ they grow by $2.8$ and then $1.9$, as a power of $\log n$ does, and at $n = 10^4$, a grid of $10^8$ vertices, $r = 2$ is the best of the four. On the small grids $r = 1$ is faster: the asymptotic advantage of $r = 2$ shows only when $\log n$ is small compared with the polynomial factors.

## Relation to other models

- **[Watts-Strogatz model](/watts-strogatz-model/).** A ring lattice with uniformly rewired edges, which is the case $r = 0$ in one dimension. It has short paths, but Kleinberg's lower bound shows that no local algorithm finds them fast.
- **[Small-world network](/small-world-network/) and [six degrees of separation](/six-degrees-of-separation/).** Kleinberg's model separates the existence of short paths, which many random graphs have, from their discovery, which Milgram's letters showed people can do and which needs links that follow the geometry.
- **The $k$-dimensional and ring versions.** On a $k$-dimensional lattice, the exponent $r = k$ gives $O(\log^2 n)$ greedy routing, and every other exponent forces polynomial time. On a ring of $n$ vertices with links of probability proportional to $1/d$, greedy routing takes $O(\log^2 n)$ steps.
- **Distributed hash tables.** [Chord](/chord/) gives each node links at distances $1, 2, 4, \ldots$ around a ring, a deterministic version of the inverse-distance law, and routes greedily in $O(\log n)$ hops. Symphony draws its links from the harmonic distribution $1/d$, Kleinberg's one-dimensional law. [Kademlia](/kademlia/) uses the XOR distance with one bucket per distance scale.
- **Nearest neighbour search.** [Navigable small-world graphs](/navigable-small-world/) and HNSW build proximity graphs on which greedy search in the data space reaches a query's neighbours quickly, the same idea applied to points in a metric space.

## Known results in the model

| setting, $p = q = 1$, grid $n \times n$ | expected delivery time | who |
|---|---|---|
| $r = 2$, greedy routing | $O(\log^2 n)$ | Kleinberg, Theorem 2 |
| $r = 0$, any decentralized algorithm | $\Omega(n^{2/3})$ | Kleinberg, Theorem 1 |
| $0 \le r < 2$, any decentralized algorithm | $\Omega(n^{(2-r)/3})$ | Kleinberg, Theorem 3 |
| $r > 2$, any decentralized algorithm | $\Omega(n^{(r-2)/(r-1)})$ | Kleinberg, Theorem 4 |
| $k$-dimensional lattice, $r = k$, greedy | $O(\log^2 n)$ | Kleinberg |
| $r = 0$, shortest paths | polylogarithmic in $n$ with high probability, because the uniform links form a random graph of small diameter | random graph results cited by Kleinberg |

The constants in the bounds depend on $p$, $q$ and $r$ but not on $n$. The lower bounds hold for any decentralized algorithm, not just greedy routing, and in expectation over uniform $s$ and $t$. Only $r$ equal to the dimension makes the delivery time polylogarithmic, which is the sense in which navigable networks are rare: the link lengths must be spread evenly over all distance scales. Easley and Kleinberg describe later studies of real social networks with geographic positions, such as LiveJournal, in which the probability of a friendship falls roughly as the inverse of the number of people who live closer, the rank-based form of the same law.

## References
