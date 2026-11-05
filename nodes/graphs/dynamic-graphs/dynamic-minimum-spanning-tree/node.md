---
tag: KSVJYK
kind: problem
slug: dynamic-minimum-spanning-tree
name: Dynamic minimum spanning tree
aliases:
- dynamic MST
- fully dynamic minimum spanning forest
area: graphs/dynamic-graphs
level: advanced
summary: Maintain a minimum spanning forest under edge insertions and deletions.
prereqs: [minimum-spanning-tree, cut-property, cycle-property, dynamic-connectivity]
see_also: [frederickson-topology-trees, holm-de-lichtenberg-thorup, sparsification, link-cut-tree, top-tree, mst-sensitivity-analysis, kruskal]
sources:
  - paper: doi:10.1137/0214055
    title: Greg N. Frederickson, Data structures for on-line updating of minimum spanning trees, with applications, SIAM Journal on Computing 14(4), 781 to 798 (1985)
    locator: the whole paper (topology trees and O(m^(1/2)) worst-case update time)
  - paper: doi:10.1145/265910.265914
    title: David Eppstein, Zvi Galil, Giuseppe F. Italiano and Amnon Nissenzweig, Sparsification, a technique for speeding up dynamic graph algorithms, Journal of the ACM 44(5), 669 to 696 (1997)
    locator: the results for minimum spanning forests (O(n^(1/2)) worst-case update time)
  - paper: doi:10.1145/502090.502095
    title: Jacob Holm, Kristian de Lichtenberg and Mikkel Thorup, Poly-logarithmic deterministic fully-dynamic algorithms for connectivity, minimum spanning tree, 2-edge, and biconnectivity, Journal of the ACM 48(4), 723 to 760 (2001)
    locator: the sections on decremental and fully dynamic minimum spanning forest (O(log^4 n) amortized per update)
  - paper: doi:10.1109/FOCS.2017.92
    title: Danupon Nanongkai, Thatchaphol Saranurak and Christian Wulff-Nilsen, Dynamic minimum spanning forest with subpolynomial worst-case update time, Proceedings of FOCS 2017, 950 to 961
    locator: the main theorem (n^(o(1)) worst-case update time, Las Vegas)
  - paper: doi:10.1007/978-3-662-48350-3_62
    title: Jacob Holm, Eva Rotenberg and Christian Wulff-Nilsen, Faster fully-dynamic minimum spanning forest, Proceedings of ESA 2015, Lecture Notes in Computer Science 9294, 742 to 753
    locator: the main theorem (O(log^4 n / log log n) amortized update time)
  - paper: doi:10.1016/0022-0000(83)90006-5
    title: Daniel D. Sleator and Robert E. Tarjan, A data structure for dynamic trees, Journal of Computer and System Sciences 26(3), 362 to 391 (1983)
    locator: the path maximum operation and its use for minimum spanning trees under insertions
---

The dynamic minimum spanning tree problem asks to keep a [minimum spanning forest](/minimum-spanning-tree/) of a weighted undirected [dynamic graph](/dynamic-graph/) while edges are inserted and deleted. An insertion is easy: by the [cycle property](/cycle-property/), the new edge either stays out or replaces the heaviest edge on the tree path between its ends. A deletion of a tree edge is hard: by the [cut property](/cut-property/), the forest needs the lightest edge across the cut that the deletion opens, and finding it fast is the core of the problem. The best deterministic amortized bound is polylogarithmic, and the problem is at least as hard as [dynamic connectivity](/dynamic-connectivity/).

## In plain words

A company links its offices with leased lines, and wants the cheapest set of lines that keeps every office connected. Line prices change, new lines appear and old lines go away. After each change, the company wants the cheapest network again, without planning it from zero.

A new line helps only if it is cheaper than the most expensive line on the current route between its two ends. Then it takes the place of that line. When a line in use goes away, the network splits in two parts, and the company needs the cheapest unused line that joins the two parts again. Finding that line quickly, without looking at all unused lines, is the hard part.

## Definition

**Input.** A number $n$ of vertices and an online sequence of operations on an undirected graph $G = (V, E)$ with real edge weights $w : E \to \mathbb{R}$, at first with no edges:

- $\mathrm{insert}(u, v, x)$ adds an edge $\{u, v\}$ of weight $x$,
- $\mathrm{delete}(e)$ removes the edge $e$,
- queries about the forest, for example its total weight, or whether a given edge is in it.

**Output.** After each update, a minimum spanning forest $F$ of the current graph: a spanning forest with one tree per component whose total weight $\sum_{e \in F} w(e)$ is the smallest. The structure reports the changes to $F$, which are at most one edge in and one edge out per update.

**Ties.** With equal weights, the minimum spanning forest need not be unique. Break ties by a fixed order of the edges, for example by insertion time. Then the forest is unique ([uniqueness](/mst-uniqueness/)), and each update changes it by at most one swap.

**Why one swap is enough.** Let $F$ be the unique minimum spanning forest of $G$. After inserting $e = \{u, v\}$: if $u$ and $v$ are in different trees, $F + e$ is the new forest. Otherwise, let $f$ be the heaviest edge on the tree path from $u$ to $v$; the new forest is $F$ if $w(e) > w(f)$ and $F + e - f$ otherwise, by the cycle property applied to the cycle that $e$ closes. After deleting $e$: if $e \notin F$, $F$ stays optimal, because each cycle and cut condition of $F$ still holds. If $e \in F$, removing it splits a tree into parts $A$ and $B$, and the new forest is $F - e + g$, where $g$ is the lightest remaining edge with one end in $A$ and one in $B$, or $F - e$ if there is no such edge. This follows from the cut property for the cut $(A, B)$ and the fact that every other tree edge still passes its own cut test.

## Variants

- **Incremental.** Insertions only. The swap rule with a [link-cut tree](/link-cut-tree/) that answers path-maximum queries gives $O(\log n)$ time per insertion, deterministic, amortized with splay-based link-cut trees and worst case with the biased version.
- **Decremental.** Deletions only.
- **Fully dynamic.** Both.
- **Weight changes.** A weight increase is a deletion and an insertion; so is a decrease.
- **Approximate.** Keep a spanning forest within a factor $1 + \varepsilon$ of the minimum weight. With integer weights in a bounded range, this is often easier than the exact problem.
- **Sensitivity.** For a fixed graph, find how much each weight can change before the tree changes; this static question is [MST sensitivity analysis](/mst-sensitivity-analysis/).

## Examples

Take $V = \{0, 1, 2, 3, 4\}$. The table gives the minimum spanning forest and its weight after each update, with weights in brackets.

| update | forest after it | weight | what happened |
|---|---|---|---|
| insert 01 (4) | 01 | 4 | new link |
| insert 12 (2) | 01, 12 | 6 | new link |
| insert 23 (6) | 01, 12, 23 | 12 | new link |
| insert 30 (3) | 01, 12, 30 | 9 | path 3, 2, 1, 0 has max 23 (6) > 3, swap |
| insert 13 (5) | 01, 12, 30 | 9 | path 1, 0, 3 has max 01 (4) < 5, rejected |
| insert 34 (7) | 01, 12, 30, 34 | 16 | new link |
| insert 24 (1) | 01, 12, 24, 30 | 10 | path 2, 1, 0, 3, 4 has max 34 (7) > 1, swap |
| delete 01 | 12, 13, 24, 30 | 11 | cut $\{0, 3\}$ and $\{1, 2, 4\}$, lightest crossing edge 13 (5) |
| delete 12 | 13, 23, 24, 30 | 15 | cut $\{2, 4\}$ and $\{0, 1, 3\}$, lightest crossing edge 23 (6) |

The two deletions each remove a tree edge and bring back an edge that the forest had dropped or rejected earlier. So a dynamic structure must keep the non-tree edges, sorted in a way that makes the lightest edge across any cut easy to find.

## Known algorithms

| algorithm | update time | case | deterministic |
|---|---|---|---|
| recompute with [Kruskal](/kruskal/) after each update | $O(m \log n)$ | worst | yes |
| swap rule with a [link-cut tree](/link-cut-tree/), insertions only | $O(\log n)$ | amortized | yes |
| [Frederickson](/frederickson-topology-trees/) (1985), topology trees | $O(m^{1/2})$ | worst | yes |
| [sparsification](/sparsification/) over Frederickson (1997) | $O(n^{1/2})$ | worst | yes |
| [Holm, de Lichtenberg and Thorup](/holm-de-lichtenberg-thorup/) (2001) | $O(\log^4 n)$ | amortized | yes |
| Nanongkai, Saranurak and Wulff-Nilsen (2017) | $n^{o(1)}$ | worst, with high probability | no, Las Vegas |

**Frederickson.** Split the forest into $O(m/z)$ clusters of $O(z)$ vertices each and keep, for each pair of clusters, the lightest non-tree edge between them. A deletion of a tree edge then repairs $O(z)$ entries inside a cluster and checks $O((m/z)^2)$ cluster pairs for the lightest crossing edge, and $z = m^{2/3}$ balances this to $O(m^{2/3})$ per update. Frederickson's 2-dimensional topology trees organize the cluster pairs hierarchically, which lowers the bound to $O(m^{1/2})$ per update, worst case. Sparsification turns $m$ into $O(n)$, which gives $O(n^{1/2})$.

**Holm, de Lichtenberg and Thorup.** First they build a decremental algorithm with the edge levels of their connectivity algorithm, where the search for a replacement takes non-tree edges in order of weight. Then a general reduction turns a decremental minimum spanning forest algorithm into a fully dynamic one, at the cost of one more logarithmic factor. Holm, Rotenberg and Wulff-Nilsen (2015) lowered the bound to $O(\log^4 n / \log\log n)$ amortized.

## Bounds

**Upper bounds.** $O(\log^4 n / \log\log n)$ amortized deterministic, $n^{o(1)}$ worst case with a Las Vegas algorithm. For insertions only, $O(\log n)$.

**Lower bound.** With unit weights, two vertices are connected exactly when they are in one tree of the forest. So dynamic connectivity reduces to this problem, and the $\Omega(\log n)$ cell-probe bound of the [dynamic connectivity lower bound](/dynamic-connectivity-lower-bound/) holds for it, as long as the structure can answer "same tree?" in the time it reports changes.

## Reductions

- **Connectivity to minimum spanning forest.** As above, with all weights equal.
- **Minimum spanning forest to decremental minimum spanning forest.** The reduction of Holm, de Lichtenberg and Thorup keeps $O(\log n)$ decremental structures on parts of the edge set and rebuilds them as insertions arrive.
- **Bipartiteness.** The structures for fully dynamic minimum spanning forests also give [dynamic bipartiteness](/dynamic-bipartiteness/).

## Applications

- **Network design.** Keep a cheapest backbone of a network while link costs and links change.
- **Clustering.** Single-linkage clustering cuts the heaviest edges of a minimum spanning tree, so a dynamic forest keeps the clusters of a changing point set.
- **Subroutine.** Dynamic algorithms for bipartiteness, for $k$-edge connectivity certificates and for some geometric problems use a dynamic minimum spanning forest.

## References
