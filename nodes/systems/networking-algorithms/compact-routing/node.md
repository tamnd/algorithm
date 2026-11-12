---
tag: CZ5P8G
kind: technique
slug: compact-routing
name: Compact routing
aliases:
- compact routing schemes
- Thorup-Zwick routing
area: systems/networking-algorithms
level: research
summary: "Give each node a routing table much smaller than n entries and each destination a short label, so that every packet still follows a path at most a fixed factor, the stretch, longer than the shortest."
prereqs: [routing-problem, shortest-path-tree, thorup-zwick-oracle]
see_also: [distance-oracle, distance-labeling, low-stretch-spanning-tree, dynamic-spanner, heavy-light-decomposition, longest-prefix-match, link-state-routing, overlay-lookup]
sources:
  - paper: "David Peleg and Eli Upfal, A trade-off between space and efficiency for routing tables, Journal of the ACM 36(3), 1989, pages 510 to 530"
    locator: the definition of stretch, hierarchical schemes with stretch O(k), and a lower bound on total table size for small stretch
  - paper: "Cyril Gavoille and Marc Gengler, Space-efficiency for routing schemes of stretch factor three, Journal of Parallel and Distributed Computing 61(5), 2001, pages 679 to 687 (first in SIROCCO 1997)"
    locator: the lower bound, Omega(n) bits at some node for every scheme of stretch below 3 (citation details not checked)
  - paper: "Mikkel Thorup and Uri Zwick, Compact routing schemes, ACM SPAA 2001, pages 1 to 10"
    locator: the scheme for trees, the stretch-3 scheme with tables of size O(sqrt(n log n)) words, and the schemes of stretch 4k - 5, or 2k - 1 with handshaking, with tables of size about n^(1/k) (page numbers not checked)
  - paper: "Lenore J. Cowen, Compact routing with minimum stretch, Journal of Algorithms 38(1), 2001, pages 170 to 183 (first in SODA 1999)"
    locator: the first stretch-3 scheme with sublinear tables, about n^(2/3) entries, built on landmarks (citation details not checked)
  - paper: "Ittai Abraham, Cyril Gavoille, Dahlia Malkhi, Noam Nisan and Mikkel Thorup, Compact name-independent routing with minimum stretch, ACM Transactions on Algorithms 4(3), 2008 (first in SPAA 2004)"
    locator: stretch 3 with tables of about sqrt(n) entries when destinations keep their original names
---

Compact routing is the design of routing schemes in which each node keeps a table much smaller than one entry per destination, and each destination has a short label, while every packet still travels a path at most a fixed factor longer than the shortest. That factor is the *stretch*. A full shortest-path table, as built by [link-state](/link-state-routing/) or [distance-vector](/distance-vector-routing/) routing, has $n$ entries at every node and stretch 1. Compact routing trades a little stretch for much less space. The central result is the stretch-3 scheme of Thorup and Zwick (2001): each node keeps $O(\sqrt{n \log n})$ words, each label has $O(\log^2 n)$ bits in its simple form, and every route is at most 3 times the shortest. Stretch 3 is the least possible with sublinear tables: Gavoille and Gengler showed that any scheme of stretch below 3 needs $\Omega(n)$ bits at some node in some graphs.

## In plain words

A full routing table is like a signpost at every crossroads that lists every town in the country. That is a huge sign. Compact routing uses small signs. Each crossroads lists only the towns near it, plus the way to a few big hub towns. The address of a town says which hub is near it and how to go from that hub to the town.

To send a letter, a crossroads checks its own list first. If the town is there, it sends the letter the short way. If not, it sends the letter toward the hub named in the address, and the hub's map leads it on. The letter may go a bit out of its way, but never more than three times the shortest distance.

## When it applies

- The network is large, so a table with an entry for every destination is too big for fast memory, or too costly to keep up to date.
- The designer may choose the labels (addresses) of the nodes, as in *labeled* schemes; or the destinations keep their own names, as in *name-independent* schemes, which are harder.
- Some stretch is acceptable. Stretch is a worst case, and the average is often near 1.
- A central step, or a slow distributed one, can compute the tables from the whole graph. Dynamic graphs are much harder.

## The template

Most schemes combine two parts: routing on trees with tiny tables, and a choice of a few landmarks (hubs) such that every destination is either near the source or near a landmark.

```pseudo
PREPROCESS(G)                          ▷ the Thorup and Zwick stretch-3 scheme
    A ← CENTER(G, s)                     ▷ landmarks: sample, then sample again among vertices with big clusters
    for each landmark ℓ in A do build the shortest-path tree T(ℓ) and its tree-routing records
    for each vertex v do ℓ(v) ← the landmark nearest to v
    for each vertex u do
        C(u) ← {v : d(u, v) < d(v, A)}   ▷ the cluster of u: destinations closer to u than to their landmark
        table(u) ← u's record in each T(ℓ), and the next hop from u toward each v in C(u)
    for each vertex v do label(v) ← (v, ℓ(v), the tree label of v in T(ℓ(v)))

ROUTE(u, label(v))
    if v ∈ C(u) then forward along the stored next hops to v
    else forward in the tree T(ℓ(v)), using the tree label of v in the header
```

**Why every route has stretch at most 3.** If $v \in C(u)$, the stored next hops give a shortest path, and every vertex $x$ on it also has $v \in C(x)$, because $d(x, v) \le d(u, v) < d(v, A)$; so each hop finds an entry. Otherwise $d(v, \ell(v)) = d(v, A) \le d(u, v)$, and the path in the shortest-path tree $T(\ell(v))$ has length at most

$$d(u, \ell(v)) + d(\ell(v), v) \le \bigl(d(u, v) + d(v, \ell(v))\bigr) + d(v, \ell(v)) \le 3\, d(u, v).$$

**Why the tables are small.** The procedure CENTER of Thorup and Zwick samples each vertex of a set $W$ (at first all of $V$) with probability $s / |W|$, adds the sample to $A$, and then lets $W$ be the vertices whose clusters still have more than $4n/s$ members. They show that $W$ shrinks fast, so $|A| = O(s \log n)$ in expectation and every cluster ends with at most $4n/s$ vertices. With $s = \sqrt{n / \log n}$, the table of $u$ has $O(|A| + |C(u)|) = O(\sqrt{n \log n})$ words.

**Tree routing.** In one rooted tree, number the vertices in depth-first order, visiting the *heavy* child (the one with the largest subtree) first. A vertex $x$ keeps its number $f(x)$, the last number in its subtree, its heavy child and that child's range, its parent, and its light depth: the number of light edges from the root to $x$. The label of $v$ is $f(v)$ and the ports of the light edges on the path from the root to $v$. Each light edge at least halves the subtree size, so there are at most $\log_2 n$ of them. At $x$, a packet for $v$ goes up if $f(v)$ is outside $x$'s range, to the heavy child if $f(v)$ is in that child's range, and otherwise down the light edge listed in the label at position equal to $x$'s light depth. This is the same heavy and light split as in [heavy-light decomposition](/heavy-light-decomposition/). The packet follows the tree path exactly.

## Classic examples

- **Thorup and Zwick, stretch 3.** The scheme above. Its tables are $\tilde O(\sqrt n)$ and its labels $O(\log^2 n)$ bits in the simple form; Thorup and Zwick also give a tree scheme with shorter labels. In random sparse graphs with $n$ = 100, 400 and 1000 nodes and average degree about 6, the simple form needs about 10 or 11 landmarks, and an average table of about 70, 120 and 190 words, against $2n$ = 200, 800 and 2000 words for a full table of (destination, next hop) pairs.
- **Thorup and Zwick, stretch $4k - 5$.** Use the $k$ levels of landmarks of the [Thorup and Zwick distance oracle](/thorup-zwick-oracle/), with tables of $\tilde O(n^{1/k})$ words. With a handshake, in which the source first learns a little about the destination, the stretch falls to $2k - 1$. Chechik (2013) later lowered the stretch without handshakes to about $3.68 k$.
- **Cowen's landmark scheme.** The first stretch-3 scheme with sublinear tables, about $n^{2/3}$ entries, with landmarks chosen by a greedy cover rather than by sampling.
- **Name-independent routing.** If destinations keep arbitrary names, a node must first find the label. Abraham, Gavoille, Malkhi, Nisan and Thorup reach stretch 3 with $\tilde O(\sqrt n)$ tables in this setting, the best possible, by storing the labels in a distributed dictionary over the landmarks' neighbourhoods, much as an [overlay lookup](/overlay-lookup/) does.
- **Interval routing.** In a tree, each port is labelled with an interval of depth-first numbers, and a packet takes the port whose interval holds its destination. Santoro and Khatib (1985) and van Leeuwen and Tan (1987) studied it; it gives stretch 1 in trees and is the base of the tree scheme above.
- **Hierarchical addressing.** Internet prefixes, areas and autonomous systems are an informal compact scheme: a router far from a destination keeps one entry for a whole prefix, matched by [longest-prefix match](/longest-prefix-match/). It has no worst-case stretch bound.

## Variations

- **Labeled against name-independent.** Labeled schemes choose addresses that encode location; name-independent ones pay a lookup step and usually more stretch for the same space.
- **Designer ports against fixed ports.** In some models the scheme may number the ports of each node; in others the port numbers are given, and labels must spell them out, which costs a little more.
- **Average stretch.** On graphs like the Internet, the average stretch of the Thorup and Zwick scheme is close to 1, even though the bound is 3.
- **Special graphs.** Trees have schemes with stretch 1, and planar graphs and graphs of bounded doubling dimension admit schemes with stretch $1 + \varepsilon$ and polylogarithmic tables.
- **Lower bounds.** Gavoille and Gengler's bound makes stretch 3 the least stretch with $o(n)$ bits at every node. More generally, if Erdős's girth conjecture holds, stretch below $2k + 1$ needs about $n^{1/k}$ bits at some node in some graphs, so the Thorup and Zwick tables are close to optimal for their stretch.
- **Relation to distance oracles and labels.** A routing scheme answers the question "which neighbour next?", a [distance oracle](/distance-oracle/) answers "how far?", and [distance labeling](/distance-labeling/) answers it from two labels alone. They share the landmark and cluster method. Sparse spanners, such as those kept by [dynamic spanner](/dynamic-spanner/) algorithms, and [low-stretch spanning trees](/low-stretch-spanning-tree/) are the subgraph versions of the same trade-off.

## Pitfalls

- **Stretch is multiplicative.** Stretch 3 can triple the delay of a pair of nodes that are close, which is where users notice it most.
- **Preprocessing is global.** The landmarks, clusters and tree numbers depend on the whole graph. A single link change can change many tables and labels, and distributed, dynamic versions are much more complex than the static scheme.
- **Labels change when the graph changes.** In labeled schemes the address of a node encodes its landmark and tree position, so addresses are not stable names. Name-independent schemes fix this at a cost.
- **Ties in the definitions.** The cluster needs the strict inequality $d(u, v) < d(v, A)$, and the next hops must follow one fixed shortest-path tree per destination, so that every node on the way agrees.
- **At least one landmark.** For small $n$ the cluster bound $4n/s$ can exceed $n$, so the sampling may stop with no landmark. The scheme then has no tree for distant destinations, so the set $A$ must hold at least one vertex.

## References
