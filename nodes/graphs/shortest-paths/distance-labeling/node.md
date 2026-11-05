---
tag: T7281R
kind: concept
slug: distance-labeling
name: Distance labeling
aliases:
- distance labels
area: graphs/shortest-paths
level: advanced
summary: Assigning each vertex a short label so that the distance between two vertices is computed from their two labels alone.
prereqs: [shortest-path, all-pairs-shortest-paths]
see_also: [hub-labeling, distance-oracle, thorup-zwick-oracle, contraction-hierarchies, lowest-common-ancestor, planar-separator-theorem, treewidth, tree-decomposition]
sources:
  - paper: doi:10.1002/(sici)1097-0118(200003)33:3<167::aid-jgt7>3.0.co;2-5
    title: David Peleg, Proximity-preserving labeling schemes, Journal of Graph Theory 33(3), 167 to 176 (2000)
    locator: the whole paper (the definition of distance labeling schemes and the O(log² n)-bit scheme for trees by separators)
  - paper: doi:10.1016/j.jalgor.2004.05.002
    title: Cyril Gavoille, David Peleg, Stéphane Pérennes and Ran Raz, Distance labeling in graphs, Journal of Algorithms 53(1), 85 to 112 (2004)
    locator: the whole paper (the Θ(n)-bit bound for general graphs, Ω(log² n) for trees, and the bounds for planar graphs and graphs with small separators)
  - paper: doi:10.1137/s0097539702403098
    title: Edith Cohen, Eran Halperin, Haim Kaplan and Uri Zwick, Reachability and distance queries via 2-hop labels, SIAM Journal on Computing 32(5), 1338 to 1355 (2003)
    locator: the whole paper (2-hop covers, and the greedy set-cover construction with an O(log n) approximation of the smallest cover)
  - paper: doi:10.1007/978-3-642-20662-7_20
    title: Ittai Abraham, Daniel Delling, Andrew V. Goldberg and Renato F. Werneck, A hub-based labeling algorithm for shortest paths in road networks, SEA 2011, LNCS 6630, 230 to 241
    locator: the whole paper (hub labels from contraction-hierarchy search spaces and their query times on road networks)
  - paper: doi:10.1145/2463676.2465315
    title: Takuya Akiba, Yoichi Iwata and Yuichi Yoshida, Fast exact shortest-path distance queries on large networks by pruned landmark labeling, SIGMOD 2013, 349 to 360
    locator: the whole paper (pruned breadth-first searches in degree order that build a 2-hop cover)
---

A distance labeling scheme gives every vertex $v$ of a graph a bit string $L(v)$, its *label*, and fixes a decoder $D$ such that $D(L(u), L(v)) = \operatorname{dist}(u, v)$ for every pair, without looking at the graph. The question is how short the labels can be. For general graphs on $n$ vertices, $\Theta(n)$ bits per label are needed and suffice; for trees, $\Theta(\log^2 n)$; for planar graphs, between $\Omega(n^{1/3})$ and $O(\sqrt n \log n)$. The concept was introduced by Peleg (2000), and Gavoille, Peleg, Pérennes and Raz (2004) proved the main bounds. In practice the most used kind is the *2-hop* or [hub label](/hub-labeling/), where $L(v)$ is a list of hubs with distances and the decoder takes a minimum over common hubs; it gives the fastest exact distance queries known on road networks.

## In plain words

Imagine you had to write a short note on each town's sign so that anyone holding the signs of two towns could work out the distance between them, with no map.

On a straight road this is easy: write the kilometre marker on each sign and subtract. On a network of roads it is harder. One way is to choose a few important hub towns and write on each sign the distances to some of them. To find the distance between two towns, look for hubs that appear on both signs and add the two distances; the smallest sum is the answer, as long as every best route passes through some hub shared by both signs.

The question behind distance labeling is how short these notes can be for different kinds of networks.

## The idea

**Definition.** A distance labeling scheme for a family of graphs is an encoder that, given a graph $G$ of the family, assigns a label $L(v)$ to each vertex, and a single decoder $D$, the same for all graphs of the family, with $D(L(u), L(v)) = \operatorname{dist}_G(u, v)$. Its size is the largest label length in bits, as a function of $n$. The decoder sees only the two labels, not the graph and not the names of other vertices.

**Weight assumptions.** The bounds above are for unweighted graphs, or for integer weights with $\log W$ extra bits per stored distance when weights are at most $W$. For [hub labels](/hub-labeling/), weights can be any nonnegative reals, and in fact any reals, as long as the graph has no negative cycle, since the labels just store true distances; with a negative cycle some distances are $-\infty$ and the schemes do not apply. In a directed graph each vertex has an out-label and an in-label. Pairs with no path get $\operatorname{dist}(u, v) = \infty$, and the decoder must report it: with hub labels this is the case where the two labels share no hub.

**Hub labels and 2-hop covers.** Each vertex $v$ stores a set of pairs $(h, \operatorname{dist}(v, h))$, and the decoder returns
$$D(L(u), L(v)) = \min_{h \in L(u) \cap L(v)} \big(\operatorname{dist}(u, h) + \operatorname{dist}(h, v)\big),$$
or $\infty$ if the intersection is empty. The decoder never underestimates, since each sum is the weight of a real walk. It is exact if and only if the labels have the *cover property*: for every pair $u, v$ with a path, some shortest $u$-$v$ path contains a hub that is in both labels. With labels sorted by hub, decoding is a merge in $O(|L(u)| + |L(v)|)$ time. Cohen, Halperin, Kaplan and Zwick (2003) showed how to build a cover of total size within $O(\log n)$ of the smallest, by greedy [set cover](/set-cover/).

**Size bounds.**

| graph family | label size (bits) |
|---|---|
| paths | $\Theta(\log n)$ |
| trees | $\Theta(\log^2 n)$ |
| graphs with separators of size $O(\sqrt n)$, such as planar graphs | $O(\sqrt n \log n)$ upper, $\Omega(n^{1/3})$ lower for planar |
| graphs of [treewidth](/treewidth/) $k$ | $O(k \log^2 n)$ |
| all graphs | $\Theta(n)$ |

The upper bounds for trees, planar graphs and bounded treewidth all come from separators: a vertex stores its distances to the vertices of the separators on its branch of a recursive decomposition. The $\Omega(n)$ lower bound for general graphs is a counting argument: there are $2^{\Theta(n^2)}$ graphs of diameter 2, each must be told apart by the $n$ labels together, so some label has $\Omega(n)$ bits.

**Approximate labels.** If the decoder may return an estimate within a factor $2k - 1$, the [Thorup-Zwick](/thorup-zwick-oracle/) construction gives labels of $\tilde O(n^{1/k})$ words for any graph, and this is the labeling form of the [approximate distance oracle](/distance-oracle/).

## Examples

**A path.** On the path $v_1, \ldots, v_n$ with unit weights, $L(v_i) = i$ in $\lceil \log_2 (n + 1) \rceil$ bits and $D(i, j) = |i - j|$.

**A tree by centroids, as hub labels.** Take the path $a - b - c - d - e$ with unit weights, a tree. Its centroid is $c$; removing it leaves $\{a, b\}$ with centroid $b$ and $\{d, e\}$ with centroid $d$. Each vertex stores the distances to its chain of centroids:

| vertex | label |
|---|---|
| $a$ | $(c, 2), (b, 1), (a, 0)$ |
| $b$ | $(c, 1), (b, 0)$ |
| $c$ | $(c, 0)$ |
| $d$ | $(c, 1), (d, 0)$ |
| $e$ | $(c, 2), (d, 1), (e, 0)$ |

For $a$ and $e$ the only common hub is $c$, and $2 + 2 = 4$. For $a$ and $b$ the common hubs are $c$ (sum $2 + 1 = 3$) and $b$ (sum $1 + 0 = 1$), and the minimum, 1, is right. Every path between two vertices passes through the first centroid that separates them, which is in both labels, so the cover property holds. The labels have 11 entries in all, against 15 pairs in a full table; on a tree with $n$ vertices each label has at most $\log_2 n + 1$ entries of $O(\log n)$ bits, which is the $O(\log^2 n)$ bound.

**Directed and unreachable.** In the directed path $a \to b \to c$, give out-labels $L_{out}(a) = \{(a, 0), (b, 1)\}$, $L_{out}(b) = \{(b, 0)\}$, $L_{out}(c) = \{(c, 0)\}$ and in-labels $L_{in}(a) = \{(a, 0)\}$, $L_{in}(b) = \{(b, 0)\}$, $L_{in}(c) = \{(b, 1), (c, 0)\}$. Then $\operatorname{dist}(a, c)$ uses the common hub $b$: $1 + 1 = 2$. For $c$ to $a$, $L_{out}(c) \cap L_{in}(a)$ is empty, and the decoder returns $\infty$, correctly, since $a$ is not reachable from $c$.

**General graphs.** Storing a row of the distance matrix gives $n \lceil \log_2 (n + 1) \rceil$ bits, $O(n \log n)$; smarter encodings reach $O(n)$ bits, matching the lower bound up to a constant.

## Where it is used

- **Route planning.** Hub labels built from [contraction hierarchy](/contraction-hierarchies/) search spaces (Abraham, Delling, Goldberg and Werneck 2011) answer exact road-network queries in microseconds, the fastest of all known techniques, at the cost of large labels.
- **Social and web graphs.** Pruned landmark labeling (Akiba, Iwata and Yoshida 2013) runs a breadth-first search from each vertex in decreasing degree order and skips vertices whose distance the labels already give, producing a 2-hop cover of a few hundred hubs per vertex on graphs with millions of edges.
- **Distributed systems.** Labels let a node estimate distances or route messages using only local information, as in compact routing schemes.
- **Trees and ancestry.** Labels for [lowest common ancestors](/lowest-common-ancestor/) and ancestry in XML trees are close relatives of tree distance labels.
- **Lower bounds for data structures.** A labeling scheme is a distance oracle split evenly over the vertices, so label lower bounds limit what [distance oracles](/distance-oracle/) can achieve.

## References
