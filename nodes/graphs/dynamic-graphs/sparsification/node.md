---
tag: 2E2VVG
kind: technique
slug: sparsification
name: Graph sparsification (dynamic)
aliases:
- Eppstein sparsification
- sparse certificates for dynamic graphs
area: graphs/dynamic-graphs
level: advanced
summary: Maintains a sparse certificate of a dense graph so each update touches only a smaller structure.
prereqs: [fully-dynamic-graph, minimum-spanning-tree, spanning-forest]
see_also: [eppstein-galil-italiano-nissenzweig, frederickson-topology-trees, nagamochi-ibaraki-certificate, worst-case-update-time, dynamic-minimum-spanning-tree, dynamic-connectivity, dynamic-bipartiteness, sparse-graph]
sources:
  - paper: doi:10.1145/265910.265914
    title: David Eppstein, Zvi Galil, Giuseppe F. Italiano and Amnon Nissenzweig, Sparsification, a technique for speeding up dynamic graph algorithms, Journal of the ACM 44(5), 669 to 696 (1997)
    locator: Section 2 (certificates, strong and stable certificates, the sparsification tree) and the table of results in Section 1
  - paper: doi:10.1007/BF01758778
    title: Hiroshi Nagamochi and Toshihide Ibaraki, A linear-time algorithm for finding a sparse k-connected spanning subgraph of a k-connected graph, Algorithmica 7, 583 to 596 (1992)
    locator: the whole paper (certificates of k-edge and k-vertex connectivity with O(kn) edges)
  - paper: "David Eppstein, Zvi Galil, Giuseppe F. Italiano and Thomas H. Spencer, Separator based sparsification I: planarity testing and minimum spanning trees, Journal of Computer and System Sciences 52(1), 3 to 27 (1996)"
    locator: Section 1 (sparsification for insertions only, with separators instead of the edge partition)
---

Sparsification is a technique that turns a dynamic graph algorithm whose update time depends on the number of edges $m$ into one whose update time depends only on the number of vertices $n$. It splits the edges into groups of about $n$ edges, puts the groups at the leaves of a balanced tree, and keeps at each node a **sparse certificate** with $O(n)$ edges: a small subgraph that has the same answer to the question as the union of the groups below it, also after any later change. An update then changes one group and recomputes only the $O(\log(m/n))$ certificates on the path to the root, each on a graph with $O(n)$ edges. Eppstein, Galil, Italiano and Nissenzweig (1992, journal 1997) introduced it and used it to get, among other results, $O(n^{1/2})$ worst-case time per update for [minimum spanning forests](/eppstein-galil-italiano-nissenzweig/).

## In plain words

Some questions about a graph do not need all of its edges. For example, to know which vertices are connected, one tree per piece of the graph is enough, and a tree has fewer edges than vertices.

So cut the edge list into many small piles. For each pile, keep only a small summary that answers the question for that pile. Join the summaries in pairs, and shrink each pair again to a small summary, and so on, until one summary at the top answers the question for the whole graph.

When one edge changes, only its pile changes. Redo the summaries on the way from that pile to the top. Each of them is small, so each step is fast, even if the whole graph has a huge number of edges.

## When it applies

The question must have **certificates** that combine well. For a graph property $\mathcal{P}$ on a fixed vertex set $V$:

- A **certificate** for a graph $G$ is a graph $C$ on $V$ such that $G$ has $\mathcal{P}$ if and only if $C$ has $\mathcal{P}$.
- It is a **strong certificate** if, for every graph $H$ on $V$, the graph $G \cup H$ has $\mathcal{P}$ if and only if $C \cup H$ has $\mathcal{P}$. A strong certificate must answer correctly for every future set of extra edges, not only today. Strong certificates compose: if $C_1$ and $C_2$ are strong certificates of $G_1$ and $G_2$, then a strong certificate of $C_1 \cup C_2$ is one of $G_1 \cup G_2$, because the graphs can be replaced one at a time.
- It is **sparse** if it has $O(n)$ edges.
- It is **stable** if a single edge change in $G_1$ or $G_2$ changes the computed certificate of $C_1 \cup C_2$ by $O(1)$ edges. Stability lets each node use a dynamic algorithm instead of recomputing from scratch.

Examples of sparse certificates:

| property | sparse certificate | edges |
|---|---|---|
| connectivity (and the components) | a [spanning forest](/spanning-forest/) | $\le n - 1$ |
| minimum spanning forest | the minimum spanning forest itself (distinct weights) | $\le n - 1$ |
| bipartiteness | a spanning forest, plus one edge that closes an odd cycle if there is one | $\le n$ |
| 2-edge connectivity | a spanning forest $F_1$ plus a spanning forest of $G - F_1$ | $\le 2n - 2$ |
| $k$-edge or $k$-vertex connectivity | a [Nagamochi-Ibaraki certificate](/nagamochi-ibaraki-certificate/) of $k$ nested forests | $\le k(n - 1)$ |

Each of these is a strong certificate. The minimum spanning forest is one because of the cycle rule: an edge outside the minimum spanning forest of $G$ is the heaviest edge on some cycle of $G$, so it stays outside the minimum spanning forest of $G \cup H$ for any $H$.

## The template

Let $T(n, m)$ be the time to compute a strong certificate of a graph with $n$ vertices and $m$ edges.

```pseudo id=main
BUILD(G)
L1  split E(G) into g = ⌈m / n⌉ groups E_1, …, E_g of at most n edges
L2  build a balanced binary tree with the groups at the leaves
L3  for each node x, bottom up:                      ▷ hole: CERTIFICATE
        C(x) ← CERTIFICATE(E_i) at the leaf of E_i
        C(x) ← CERTIFICATE(C(left(x)) ∪ C(right(x))) at an internal node

UPDATE(e)
L4  insert e into a group with fewer than n edges (or a new group), or delete e from its group
L5  for each node x on the path from that leaf to the root:
        recompute C(x) as in line L3                ▷ hole: static or dynamic method
L6  answer every query from C(root)                  ▷ hole: QUERY on a graph with O(n) edges
```

The holes are the certificate (line L3), the way to recompute it (line L5) and the query on the root certificate (line L6).

**Why it is correct.** By induction from the leaves, $C(x)$ is a strong certificate of the union of the groups below $x$: at a leaf by definition, and at an internal node because strong certificates compose. So $C(\text{root})$ is a strong certificate of $G$, and with $H$ empty it has $\mathcal{P}$ exactly when $G$ does.

**Cost.** Every node graph has at most $2 \cdot O(n) = O(n)$ edges, and the tree has depth $\lceil \lg g \rceil = O(\log(m/n))$. With static recomputation, an update costs $O(T(n, O(n)) \log(m/n))$. With a stable certificate and a dynamic algorithm with update time $f(n, m)$ at each node, a change at a leaf causes $O(1)$ changes in each certificate on the path, so an update costs $O(f(n, O(n)) \log(m/n))$. Eppstein et al. also showed that with groups of varying sizes the $\log(m/n)$ factor disappears when $f$ grows at least like a power of $n$; this is how $O(m^{1/2})$ becomes $O(n^{1/2})$. The bounds keep the kind of the inner algorithm: worst case stays worst case, amortized stays amortized, and the method itself is deterministic.

**Keeping groups balanced.** Deletions empty groups. Keep at most one group that is not full by moving an edge from the last group into the group that lost an edge, which changes two leaves, and remove a leaf when the last group is empty. Rebuild the tree when $m$ doubles or halves, or use [global rebuilding](/global-rebuilding/) to keep worst-case bounds.

## Classic examples

- **A small trace.** Take $K_4$ with the weights $w(01) = 1$, $w(12) = 2$, $w(23) = 3$, $w(03) = 4$, $w(02) = 5$, $w(13) = 6$, the minimum spanning forest as certificate, and groups of two edges: $E_1 = \{01, 02\}$, $E_2 = \{03, 12\}$, $E_3 = \{13, 23\}$ and an empty $E_4$. The node $A$ above $E_1, E_2$ keeps $C(A) = \{01, 12, 03\}$, since 02 closes the cycle 0, 1, 2 as its heaviest edge. The node $B$ above $E_3, E_4$ keeps $\{13, 23\}$. The root takes the minimum spanning forest of $\{01, 12, 03, 13, 23\}$, which is $\{01, 12, 23\}$ with weight 6. Now delete 12. Only $E_2$, $A$ and the root are recomputed: $C(A) = \{01, 02, 03\}$, and the root gets $\{01, 23, 03\}$ with weight 8, which is the minimum spanning forest of $K_4 - 12$. The node $B$ is not touched.

- **Minimum spanning forests.** With the minimum spanning forest as certificate, static recomputation by [Kruskal's algorithm](/kruskal/) costs $O(n \log n)$ per node, so $O(n \log n \log(m/n))$ per update. With Frederickson's $O(m^{1/2})$ worst-case structure at each node, the update time becomes $O(n^{1/2})$ in the worst case; see the [Eppstein-Galil-Italiano-Nissenzweig algorithm](/eppstein-galil-italiano-nissenzweig/).
- **Connectivity, 2-edge connectivity and bipartiteness.** The same paper gives $O(n^{1/2})$ worst-case time per update with stable certificates built from forests; see [dynamic connectivity](/dynamic-connectivity/) and [dynamic bipartiteness](/dynamic-bipartiteness/).
- **Higher connectivity.** With Nagamochi-Ibaraki certificates and static algorithms, the paper reports, for example, $O(n^{2/3})$ for 3-edge connectivity and $O(n)$ for 2- and 3-vertex connectivity per update, all deterministic.

## Variations

- **Separator-based sparsification.** For planar graphs, and for insertions only, Eppstein, Galil, Italiano and Spencer (1996) replace the edge partition by a recursive separator decomposition and get polylogarithmic bounds, for example for planarity testing and minimum spanning trees.
- **Certificates with a dynamic inner algorithm.** If the certificate is stable, the nodes keep dynamic structures and feed each other $O(1)$ edge changes per update, instead of recomputing.
- **Batch updates.** A batch of $k$ updates changes at most $k$ leaves; the union of their root paths has $O(k \log(m/n))$ nodes.
- **Other sparsifiers.** Cut sparsifiers, spectral sparsifiers and [dynamic spanners](/dynamic-spanner/) also keep a small subgraph, but they keep an approximate answer, not an exact certificate. The term "sparsification" in this page means the exact certificate method.

## Pitfalls

- **A subgraph that answers today is not enough.** The method needs strong certificates, which keep the answer for every future $H$. For example, a set of edges that only witnesses "connected" is not a certificate for 2-edge connectivity, because after a later deletion the forest edges may have no backup.
- **Ties in weights.** With equal weights, the minimum spanning forest of a node may change by many edges after one update, which breaks stability. Break ties by a fixed order of the edges.
- **Groups growing past $n$.** The bound needs every node graph to have $O(n)$ edges. Do not let a group grow by insertions beyond $n$; open a new group instead.
- **Small graphs.** For $m = O(n)$, the tree has one node, and sparsification gives nothing.

## Exercises

1. Prove that a spanning forest $F_1$ of $G$ together with a spanning forest $F_2$ of $G - F_1$ is a certificate for 2-edge connectivity, but that $F_1$ alone is not.
2. Show that for minimum spanning forests with distinct weights, one edge change in $C_1$ changes the minimum spanning forest of $C_1 \cup C_2$ by at most two edges.
3. Use sparsification and static Kruskal to give a fully dynamic minimum spanning forest with $O(n \log n \log(m/n))$ worst-case time per update, and compare it with recomputation from scratch for $m = n^2 / 4$.

## References
