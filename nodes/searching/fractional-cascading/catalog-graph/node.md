---
tag: XPSWQX
kind: definition
slug: catalog-graph
name: Catalog graph
aliases:
- cascade graph
area: searching/fractional-cascading
level: advanced
summary: A graph whose nodes hold sorted catalogs and whose edges describe which catalogs a search path visits next; the setting for fractional cascading.
prereqs: [multiple-list-search, binary-search]
see_also: [fractional-cascading-bridge, multiple-list-search, dynamic-fractional-cascading, fractional-cascading-lower-bound, hive-graph, segment-tree, layered-range-tree]
sources:
  - paper: doi:10.1007/BF01840440
    title: Bernard Chazelle and Leonidas J. Guibas, Fractional cascading I, A data structuring technique, Algorithmica 1 (1986)
    locator: pages 133 to 162 (catalog graphs, edge ranges, locally bounded degree, and generalized path queries)
  - paper: doi:10.1016/j.jcss.2003.07.003
    title: Bernard Chazelle and Ding Liu, Lower bounds for intersection searching and fractional cascading in higher dimension, Journal of Computer and System Sciences 68(2) (2004)
    locator: Section 1 and Section 4 (the definition of a catalog graph and of a query by a key and a connected subgraph)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Section 5.6 (Fractional Cascading)
---

A catalog graph is a graph in which each vertex holds a sorted list, its catalog, and in which a query moves along edges and asks for the successor of one key in the catalog of each vertex that it visits. It is the setting of the [multiple list search](/multiple-list-search/) problem in the general form of Chazelle and Guibas. When the graph has bounded degree, [fractional cascading](/fractional-cascading-bridge/) answers a query that visits $k$ vertices in $O(\log n + k)$ time with $O(n)$ space, where $n$ is the total size of the catalogs.

## Definition

Let $U$ be a totally ordered set with a largest element $+\infty$.

**Catalog graph.** A catalog graph is a finite undirected graph $G = (V, E)$ together with

- for each vertex $v \in V$, a *catalog* $C_v$: a finite sorted list of elements of $U$;
- for each edge $e \in E$, a *range* $R(e) \subseteq U$, which is an interval of $U$.

The *size* of $G$ is $n = \sum_{v \in V} |C_v|$, the total length of the catalogs. In many uses every range is the whole of $U$, and then the ranges can be left out.

**Successor.** For $x \in U$ and a vertex $v$, the successor of $x$ at $v$ is
$$\operatorname{succ}(x, C_v) = \min \{\, y \in C_v \cup \{+\infty\} : y \ge x \,\}.$$

**Degree.** The graph has *degree* $d$ if each vertex has at most $d$ incident edges. It has *locally bounded degree* $d$ if, for each vertex $v$ and each key $x \in U$, at most $d$ edges $e$ incident to $v$ have $x \in R(e)$. Bounded degree $d$ implies locally bounded degree $d$. The converse fails, as the second example below shows.

**Query.** A query is a key $x \in U$ and a connected subgraph $H$ of $G$ such that $x \in R(e)$ for each edge $e$ of $H$. Its answer is the list of the successors $\operatorname{succ}(x, C_v)$ for all vertices $v$ of $H$. The query size is $k = |V(H)|$. The subgraph need not be given in advance: in most uses it is revealed step by step, and the next vertex depends on the answers found so far. Chazelle and Guibas call such a subgraph a generalized path.

**What fractional cascading gives.** For a catalog graph of locally bounded degree $d$, Chazelle and Guibas build a structure of size $O(n)$ that answers each query in $O(\log n + k \log d)$ time. For constant $d$ this is $O(\log n + k)$, against $O(k \log n)$ for separate [binary searches](/binary-search/).

## Examples and non-examples

**A path.** A path $v_1 v_2 \cdots v_k$ with full ranges has degree 2. A query with the whole path is the list form of [multiple list search](/multiple-list-search/). The [bridge](/fractional-cascading-bridge/) page builds the structure for this case and traces a query on three catalogs of sizes 5, 6 and 7.

**A search tree with ranges.** Let a root $r$ have the key 10 and two children $a$ and $b$. The edge $ra$ has the range $(-\infty, 10]$ and the edge $rb$ has the range $(10, +\infty]$. The catalogs are $C_r = (3, 8, 15)$, $C_a = (1, 4, 9)$ and $C_b = (12, 20)$. For $x = 12$, only the edge $rb$ contains $x$ in its range, so a query from $r$ can visit $\{r, b\}$, and its answer is $15$ at $r$ and $12$ at $b$. The root has degree 2 but locally bounded degree 1. If the root had 100 children with disjoint ranges, as in a [B-tree](/b-tree/) node, its degree would be 100, and its locally bounded degree would still be 1. The ranges are what lets fractional cascading handle a node of high fan-out: each key needs bridges to only a few neighbours.

**A segment tree.** A [segment tree](/segment-tree/) whose nodes store sorted lists is a catalog graph of degree 3 (a parent and two children). A stabbing query walks one root-to-leaf path, so $k = O(\log n)$, and fractional cascading reduces its search cost from $O(\log^2 n)$ to $O(\log n)$. The same holds for the secondary lists of a [layered range tree](/layered-range-tree/).

**Non-example: a star with full ranges.** A star with a centre $c$ and $k$ leaves, where each edge has the range $U$, has degree $k$, and its locally bounded degree is also $k$. The bound $O(\log n + k \log d)$ then becomes $O(\log n + k \log k)$, which is no better than separate searches when $k$ is close to $n$. Fractional cascading needs a degree that does not grow with the input.

**Non-example: planar catalogs.** If each vertex holds a planar subdivision instead of a sorted list, and the query asks for the face that contains a point, the structure is not a catalog graph in the sense above. Chazelle and Liu show that no [pointer machine](/pointer-machine/) structure of near-linear size answers such queries in $O(k + \operatorname{polylog} n)$ time; see the [Chazelle-Liu lower bound](/fractional-cascading-lower-bound/).

**Non-example: a query that is not connected.** A query that asks for successors at two vertices far apart in $G$ is not a query of the catalog graph. It costs two separate searches, because no bridge links the two catalogs.

## Related definitions

- [Multiple list search](/multiple-list-search/): the problem on a catalog graph.
- [Fractional cascading bridge](/fractional-cascading-bridge/): the sampled elements and pointers that the structure adds along each edge.
- [Hive graph](/hive-graph/): an earlier planar structure of Chazelle that uses the same sampling idea for one geometric problem.
- [Dynamic fractional cascading](/dynamic-fractional-cascading/): the version in which the catalogs change.
- [Predecessor problem](/predecessor-problem/): the search in one catalog, which is the first step of each query.

## References
