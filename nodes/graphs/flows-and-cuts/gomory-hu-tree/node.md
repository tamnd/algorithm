---
tag: 85Y2JY
kind: data-structure
slug: gomory-hu-tree
name: Gomory-Hu tree
aliases:
- Gomory-Hu cut tree
- flow-equivalent tree
area: graphs/flows-and-cuts
level: advanced
summary: A weighted tree encoding all pairwise min cut values of an undirected graph.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, T: the time of one maximum flow computation on the graph}
  time: {worst: O(n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [all-pairs-min-cut-problem, gomory-hu-algorithm, min-cut-problem]
see_also: [global-min-cut-problem, edge-connectivity, stoer-wagner, lowest-common-ancestor, binary-lifting, maximum-spanning-tree, submodular-function]
sources:
  - paper: doi:10.1137/0109047
    title: Ralph E. Gomory and T. C. Hu, Multi-terminal network flows, Journal of the Society for Industrial and Applied Mathematics 9(4), 551 to 570 (1961)
    locator: the whole paper (the cut tree and its construction by condensation)
  - paper: doi:10.1137/0219009
    title: Dan Gusfield, Very simple methods for all pairs network flow analysis, SIAM Journal on Computing 19(1), 143 to 155 (1990)
    locator: the whole paper (the construction of a cut tree with n - 1 flows on the original graph)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition
    locator: Chapter 8, Network Flows, the section on Gomory-Hu trees
---

A Gomory-Hu tree of an undirected graph $G$ with nonnegative edge weights is a weighted tree $T$ on the same vertex set such that, for every pair $u \ne v$, a lightest edge on the $u$-$v$ path of $T$ has weight equal to the minimum $u$-$v$ cut value $\lambda(u, v)$ of $G$, and removing that edge splits the vertices into a minimum $u$-$v$ cut of $G$. It stores the answers of the [all-pairs minimum cut problem](/all-pairs-min-cut-problem/) in $n - 1$ edges. It is built with $n - 1$ maximum flow computations, by the [Gomory-Hu algorithm](/gomory-hu-algorithm/) or, as here, by Gusfield's method, which needs no graph contraction.

## In plain words

Take a road network where each road has a cost for blocking it. For any two towns, you want the cheapest set of roads whose removal cuts them apart. A Gomory-Hu tree is a small map with one link fewer than the number of towns. Each link has a number. To answer a question about two towns, follow the path between them in the small map and take the smallest number on it. Cutting the small map at that link also tells you which towns end up on each side. Building the map takes one flow computation per town, and then every question is a short walk in a tree.

## The abstract type

The structure is built once from an undirected graph with real weights $w(e) \ge 0$ and is then read only. It answers:

- **min-cut-value**$(u, v)$: the value $\lambda(u, v)$ for $u \ne v$.
- **min-cut**$(u, v)$: the value and a vertex set $A$ with $u \in A$, $v \notin A$, whose cut has that value.
- **global-min-cut**: a set $A$, $\emptyset \ne A \ne V$, of least cut value, the [global minimum cut](/global-min-cut-problem/).
- **edges**: the $n - 1$ tree edges with their weights.

The graph is undirected. An undirected edge of weight $w$ goes to the maximum flow routine as two arcs $u \to v$ and $v \to u$ of capacity $w$, each with its own residual pair, so the two directions never share flow. Edges of weight 0 change no cut, and vertices in different components have $\lambda = 0$. A directed graph has no such tree in general: in the path $a \to b \to c$ with unit weights, $\lambda(a, c) = 1$ and $\lambda(c, a) = 0$.

## Representation

The tree is rooted at vertex 0 and stored as two arrays: $parent[v]$ and $weight[v]$ for $v \ne 0$, the edge from $v$ to its parent and its weight. The implementation also keeps $depth[v]$ and the list of children of each vertex, both derived from $parent$. For the edge $(v, parent[v])$, the set of vertices in the subtree of $v$ is the cut it stands for. The space is $\Theta(n)$, against $\Theta(n^2)$ for a table of all values.

## Operations

```pseudo id=main
BUILD(G, w)                                  ▷ Gusfield's method
L1  for each vertex v do parent[v] ← 0;  weight[v] ← 0;  parent[0] ← none
L2  for s ← 1 to n − 1 do
L3      t ← parent[s]
L4      (λ, Z) ← a minimum s-t cut of G with s ∈ Z;  weight[s] ← λ
L5      for each vertex v ≠ s with parent[v] = t do
L6          if v ∈ Z then parent[v] ← s
L7      if parent[t] ≠ none and parent[t] ∈ Z then
L8          parent[s] ← parent[t];  parent[t] ← s;  weight[s] ← weight[t];  weight[t] ← λ
L9  depth[v] ← the number of edges from v up to 0, for each v

LIGHTEST(u, v)                               ▷ u ≠ v
L10 while u ≠ v do                           ▷ first swap u and v if depth[u] < depth[v]
L11     if best is unset or weight[u] < weight[best] then best ← u
L12     u ← parent[u]
    return best

MIN-CUT-VALUE(u, v)
L13 return weight[LIGHTEST(u, v)]

MIN-CUT(u, v)
L14 b ← LIGHTEST(u, v);  A ← the subtree of b;  return (weight[b], A if u ∈ A else V ∖ A)

GLOBAL-MIN-CUT()
L15 b ← a vertex v ≠ 0 of least weight[v];  return MIN-CUT(b, parent[b])
```

Line L4 runs a maximum flow on the whole graph $G$ and takes $Z$ as the set reachable from $s$ in the final residual graph. Lines L5 and L6 move to $s$ every vertex hanging off $t$ that lies on the side of $s$; this includes vertices not yet processed, which join the group of $s$, and processed vertices, whose subtrees move with them. Lines L7 and L8 handle the case where the parent of $t$ lies on the side of $s$: then $s$ takes the place of $t$ in the tree, and $t$ hangs below $s$ with the new weight $\lambda$. Lines L10 to L12 walk the tree path from both ends, always moving the deeper end, so each path edge is seen once.

## Example

Take the vertices $p, q, r, s, u, v$, numbered 0 to 5, and the undirected edges $p q$ 1, $p r$ 7, $q r$ 1, $q s$ 3, $q u$ 2, $r u$ 4, $s u$ 1, $s v$ 6, $u v$ 2.

| step | $s$ | $t$ | $\lambda$ | $Z$ | change | parents of $q, r, s, u, v$ |
|---|---|---|---|---|---|---|
| start | | | | | | $p, p, p, p, p$ |
| 1 | $q$ | $p$ | 6 | $\{q, s, u, v\}$ | $s, u, v$ move to $q$ | $p, p, q, q, q$ |
| 2 | $r$ | $p$ | 8 | $\{q, r, s, u, v\}$ | $q$ moves to $r$ | $r, p, q, q, q$ |
| 3 | $s$ | $q$ | 6 | $\{s, v\}$ | $v$ moves to $s$ | $r, p, q, q, s$ |
| 4 | $u$ | $q$ | 7 | $\{p, r, u\}$ | $r = parent[q] \in Z$: swap | $u, p, q, r, s$ |
| 5 | $v$ | $s$ | 8 | $\{v\}$ | none | $u, p, q, r, s$ |

In step 2 the processed vertex $q$ hangs off $p$ and lies in $Z$, so its whole subtree moves below $r$. In step 4 the cut $\{p, r, u\}$ separates $u$ from $q$ with weight $q r$ 1 $+$ $p q$ 1 $+$ $q u$ 2 $+$ $s u$ 1 $+$ $u v$ 2 $= 7$, and it contains $r$, the parent of $q$, so $u$ takes the place of $q$ below $r$ with the old weight 6, and $q$ hangs below $u$ with weight 7. The final tree has the edges $p r$ 8, $r u$ 6, $u q$ 7, $q s$ 6 and $s v$ 8.

Queries: MIN-CUT-VALUE$(r, u)$ walks the single edge $u r$ and returns 6. MIN-CUT$(r, u)$ removes that edge; the subtree of $u$ is $\{q, s, u, v\}$, so the answer is $(6, \{p, r\})$, and indeed the cut $\{p, r\}$ crosses $p q$, $q r$ and $r u$ for $1 + 1 + 4 = 6$. MIN-CUT-VALUE$(p, v)$ walks $v\,s\,q\,u\,r\,p$ and takes the least of 8, 6, 7, 6, 8, which is 6. GLOBAL-MIN-CUT picks a lightest edge; the implementation takes $s q$ and returns $(6, \{s, v\})$.

**Edge cases.** For the graph on five vertices with edges $0\,1$ of weight 4, $2\,3$ of weight 0 and $3\,4$ of weight 2, there is no path from 0 to 3 of positive weight, the flow is 0, and the tree joins the two parts by an edge of weight 0; MIN-CUT-VALUE$(2, 3)$ is 0, as the edge of weight 0 is never in a residual graph.

## Correctness

The [correctness proof](proofs/correctness.md) shows that BUILD keeps a Gomory-Hu tree whose nodes are groups of vertices, as in the [Gomory-Hu algorithm](/gomory-hu-algorithm/): processed vertices are the nodes, each unprocessed vertex belongs to the node of its parent, and each tree edge $(k, parent[k])$ has $\lambda(k, parent[k]) = weight[k]$ equal to the cut value of the subtree of $k$. The cut $Z$ of line L4 is a minimum cut of the whole graph and may split subtrees, but by uncrossing it can be changed into a minimum $s$-$t$ cut that agrees with $Z$ on the group of $t$ and puts each subtree on the side of its top vertex; that is the rule of lines L6 and L7. At the end every group is a single vertex, and the triangle inequality turns edge values into path minima. The query operations then read the tree: the walk of lines L10 to L12 visits exactly the edges of the tree path.

## Complexity

BUILD runs $n - 1$ maximum flows on $G$ and spends $O(n)$ more per step, so it costs $O(nT + n^2)$ time, where $T$ is the time of one maximum flow. The implementation uses shortest augmenting paths, with $T = O(nm^2)$. Each query walks one tree path, $O(n)$ time; MIN-CUT also lists a side, $O(n)$; GLOBAL-MIN-CUT is $O(n)$. The space is $\Theta(n)$ for the tree, plus the space of the flow routine during BUILD. With [binary lifting](/binary-lifting/) or path-minimum structures on top of the tree, MIN-CUT-VALUE takes $O(\log n)$ or $O(1)$ time after $O(n \log n)$ or $O(n)$ preprocessing.

## Variants

- **Contraction construction.** The original [Gomory-Hu algorithm](/gomory-hu-algorithm/) runs each flow on a contracted graph, which is smaller but needs more code.
- **Equivalent flow tree.** Gusfield's simpler variant, which in lines L5 and L6 moves only unprocessed vertices and skips the swap of lines L7 and L8, gives a tree with the right path minima, but its edges need not give minimum cuts.
- **All values at once.** A search from each vertex that carries the running minimum gives the full $n \times n$ table in $O(n^2)$ time.
- **Fast constructions.** Since 2020 Gomory-Hu trees have been built with far fewer than $n - 1$ maximum flows, reaching almost-linear time for weighted graphs in 2023.
- **Symmetric submodular functions and hypergraphs.** Cut trees exist for any symmetric submodular cut function, with the same construction.

## When to use it

Use it when many minimum cut queries are asked about one undirected graph: network reliability between all pairs of sites, clustering by removing the lightest tree edges, separation of cut constraints in branch and cut, or minimum $k$-cut approximation, where removing the $k - 1$ lightest tree edges gives a $k$-cut within a factor $2 - 2/k$ of the best. For one pair, run one maximum flow. For directed graphs it does not exist.

## Pitfalls

- **Skipping the swap of lines L7 and L8, or moving only unprocessed vertices in line L6.** On small random graphs such trees often have edges whose subtree is not a minimum cut, so MIN-CUT can return a wrong set.
- **Reading the cut from saturated edges.** The set $Z$ must be the set reachable from $s$ in the final residual graph.
- **One arc per undirected edge.** The flow routine then computes directed cuts and the tree is wrong.
- **Assuming the tree is unique.** Different choices of minimum cuts give different trees; only the path minima are fixed.
- **Using it on a directed graph** gives a tree whose path minima are not the directed cut values.

## Implementations

The Python class `GomoryHuTree(n, edges)` takes undirected edges $(u, v, w)$ with weights of type `int`, `Fraction` or `float`, builds the tree by Gusfield's method with a shortest augmenting path flow, and offers `edges()`, `min_cut_value(u, v)`, `min_cut(u, v)` and `global_min_cut()`. The arrays `parent`, `weight` and `depth` are public.

## History

Ralph Gomory and T. C. Hu introduced the cut tree in 1961 and built it by repeated contraction. Dan Gusfield gave in 1990 the construction used here, which runs every flow on the original graph and is the usual one in practice. Recent work by Abboud, Krauthgamer, Li, Panigrahi, Saranurak, Trabelsi and others builds the tree much faster.

## References
