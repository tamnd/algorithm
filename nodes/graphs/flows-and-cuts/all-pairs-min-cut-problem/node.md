---
tag: J1281T
kind: problem
slug: all-pairs-min-cut-problem
name: All-pairs minimum cut problem
aliases:
- all-pairs min cut
- multi-terminal maximum flow
area: graphs/flows-and-cuts
level: advanced
summary: Compute a minimum s-t cut value for every pair of vertices.
prereqs: [min-cut-problem, max-flow-min-cut-theorem, global-min-cut-problem]
see_also: [gomory-hu-tree, gomory-hu-algorithm, directed-global-min-cut-problem, edge-connectivity, menger-theorem, min-cut-problem]
sources:
  - paper: doi:10.1137/0109047
    title: Ralph E. Gomory and T. C. Hu, Multi-terminal network flows, Journal of the Society for Industrial and Applied Mathematics 9(4), 551 to 570 (1961)
    locator: the whole paper (the n - 1 distinct values, the triangle inequality and the cut tree)
  - paper: doi:10.1137/0219009
    title: Dan Gusfield, Very simple methods for all pairs network flow analysis, SIAM Journal on Computing 19(1), 143 to 155 (1990)
    locator: the whole paper (equivalent flow trees and cut trees without contraction)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition
    locator: Chapter 8, Network Flows, the section on Gomory-Hu trees
---

The all-pairs minimum cut problem asks for the value $\lambda(u, v)$ of a [minimum cut](/min-cut-problem/) between every pair of vertices of a graph, often together with a cut that achieves it. For undirected graphs the answer has a surprising structure: the $\binom{n}{2}$ values take at most $n - 1$ distinct values, and a single weighted tree on the vertices, the [Gomory-Hu tree](/gomory-hu-tree/), encodes all of them, with $\lambda(u, v)$ the lightest edge on the tree path from $u$ to $v$. The tree is built with only $n - 1$ maximum flow computations, instead of one per pair. For directed graphs no such tree exists in general.

## In plain words

In a network of pipes, how much can flow between any two places? There are many pairs, and checking each one with a separate flow computation is slow.

For pipes that work in both directions there is a shortcut. The answers repeat a lot: among all pairs there are fewer different answers than places. Even better, you can draw a tree on the places, with a number on each link, so that the answer for two places is the smallest number on the path between them in the tree. Building that tree needs only one flow computation per place, and after that any pair is answered by looking at the tree.

## Definition

**Input.** A graph $G = (V, E)$ with $n$ vertices and $m$ edges, and capacities $c(e) \ge 0$, real numbers. The main case is undirected; for a directed graph the pairs are ordered.

**Output.** For each pair $u \ne v$, the value $\lambda(u, v) = \min \{ c(\delta(S)) : u \in S,\ v \notin S \}$, and optionally a set $S$ achieving it. In the undirected case $\lambda(u, v) = \lambda(v, u)$.

**Structure (undirected).** Gomory and Hu proved:

- **Triangle inequality.** $\lambda(u, w) \ge \min(\lambda(u, v), \lambda(v, w))$ for any three vertices. Indeed a minimum $u$-$w$ cut puts $v$ on the side of $w$ or of $u$, so it also separates $u$ from $v$ or $v$ from $w$.
- **At most $n - 1$ distinct values.** Applying the inequality repeatedly, $\lambda$ is determined by a maximum spanning tree of the complete graph weighted by $\lambda$, which has $n - 1$ edges.
- **Cut tree.** There is a tree $T$ on $V$ with edge weights such that for each pair, $\lambda(u, v)$ is the least weight on the $u$-$v$ path of $T$, and removing that edge from $T$ splits $V$ into a minimum $u$-$v$ cut of $G$. This is the [Gomory-Hu tree](/gomory-hu-tree/).

Antiparallel edges do not arise in the undirected case. When a directed maximum flow code is used, each undirected edge becomes two antiparallel arcs of the same capacity, kept as separate arcs.

## Variants

- **Values only: equivalent flow trees.** A tree whose path minima give all values, without the promise that its edges give minimum cuts. Gusfield's simple method builds one with $n - 1$ flows on the original graph.
- **Cut trees.** The full Gomory-Hu tree, which also gives a minimum cut for each pair.
- **Unit capacities.** All-pairs edge connectivity of a simple graph; special methods use the small values.
- **Directed graphs.** The values $\lambda(u, v)$ and $\lambda(v, u)$ differ, no tree represents them in general, and the straightforward method is $n(n - 1)$ maximum flows. With unit capacities, algebraic methods based on network coding and fast matrix multiplication are faster for dense graphs.
- **Vertex connectivity for all pairs.** The same question for vertex cuts has no tree structure either.
- **Element connectivity and Steiner versions** ask for cuts separating given terminal sets.

## Examples

**A six-vertex network.** Take the undirected edges $p q$ 1, $p r$ 7, $q r$ 1, $q s$ 3, $q u$ 2, $r u$ 4, $s u$ 1, $s v$ 6, $u v$ 2. The 15 values are:

| | $p$ | $q$ | $r$ | $s$ | $u$ | $v$ |
|---|---|---|---|---|---|---|
| $p$ | | 6 | 8 | 6 | 6 | 6 |
| $q$ | 6 | | 6 | 6 | 7 | 6 |
| $r$ | 8 | 6 | | 6 | 6 | 6 |
| $s$ | 6 | 6 | 6 | | 6 | 8 |
| $u$ | 6 | 7 | 6 | 6 | | 6 |
| $v$ | 6 | 6 | 6 | 8 | 6 | |

Only three distinct values occur: 6, 7 and 8, fewer than $n - 1 = 5$. The tree with edges $p r$ 8, $p q$ 6, $q u$ 7, $q s$ 6, $s v$ 8 reproduces every entry as a path minimum; for example the path from $r$ to $u$ is $r\,p\,q\,u$ with weights 8, 6, 7, whose minimum 6 is $\lambda(r, u)$. The value 8 between $p$ and $r$ is achieved by the cut $\{p\}$, of capacity $1 + 7 = 8$; the cut $\{r\}$ costs $7 + 1 + 4 = 12$. The cut $\{p, r\}$, of capacity $1 + 1 + 4 = 6$, separates $p$ from $q$ but not $p$ from $r$.

**The running network, undirected.** For $s a$ 10, $s c$ 10, $a b$ 4, $a c$ 2, $a d$ 8, $c d$ 9, $d b$ 6, $b t$ 10, $d t$ 10 taken as undirected, every value is 20 except $\lambda(a, c) = \lambda(a, d) = \lambda(c, d) = 21$. The global minimum cut 20 is the smallest value, as always.

**Disconnected graphs and zero capacities.** If $u$ and $v$ lie in different components, $\lambda(u, v) = 0$, there is no path between them, and the cut tree joins the components by edges of weight 0. An edge of capacity 0 is the same as no edge.

**A directed example without a tree.** In the directed path $a \to b \to c$ with unit capacities, $\lambda(a, c) = 1$ but $\lambda(c, a) = 0$, so the values are not symmetric and no undirected tree can hold them.

## Known algorithms

- **One flow per pair.** $\binom{n}{2}$ maximum flows for undirected graphs, $n(n - 1)$ for directed.
- **[Gomory-Hu algorithm](/gomory-hu-algorithm/).** $n - 1$ maximum flows, each in a graph where parts of $V$ are contracted to single vertices; it returns a cut tree.
- **Gusfield's method.** $n - 1$ maximum flows in the original graph, with no contraction, and a simple parent update; it returns a cut tree or, in a simpler form, an equivalent flow tree.
- **Queries.** Once the tree is built, $\lambda(u, v)$ is a path minimum query, answered in $O(n)$ by walking the tree, or in $O(1)$ after preprocessing.
- **Recent progress.** Since 2020 a series of papers built Gomory-Hu trees with far fewer than $n - 1$ full maximum flows, first for unweighted graphs and then, by Abboud, Krauthgamer, Li, Panigrahi, Saranurak and Trabelsi (2023), for weighted graphs in almost-linear randomized time.

## Bounds

For undirected graphs, $n - 1$ maximum flows give all values, so the time is at most $n - 1$ times that of one maximum flow, and the output fits in $O(n)$ space as a tree. For directed graphs, listing all values needs $\Theta(n^2)$ output, and for sparse weighted graphs no known method avoids the work of many maximum flows.

## Reductions

- **To $n - 1$ minimum s-t cuts** (undirected), by the Gomory-Hu construction.
- **[Global minimum cut](/global-min-cut-problem/).** The lightest edge of a cut tree is a global minimum cut.
- **Minimum $k$-cut approximation.** Removing the $k - 1$ lightest tree edges gives a $k$-cut within a factor $2 - 2/k$ of optimal (Saran and Vazirani).
- **Edge connectivity** for all pairs is the unit capacity case.

## Applications

Network design and reliability analysis, where the capacity between every pair of sites matters; clustering by cutting light tree edges; separation of cut constraints in the branch-and-cut solution of network design problems; and the approximation of minimum $k$-cuts and multiway cuts.

## References
