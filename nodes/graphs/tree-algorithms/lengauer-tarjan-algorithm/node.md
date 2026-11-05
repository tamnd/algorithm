---
tag: 206HCM
kind: algorithm
slug: lengauer-tarjan-algorithm
name: Lengauer-Tarjan algorithm
aliases:
- Lengauer-Tarjan dominators
area: graphs/tree-algorithms
level: research
summary: Compute immediate dominators in near-linear time using DFS and path compression.
solves: [dominators-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(m log n), average: O(m log n), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [dominators-problem, depth-first-search, path-compression, depth-first-orders]
see_also: [dominator-tree, dominators-problem, path-compression, disjoint-set-forest, inverse-ackermann-function, iterative-depth-first-search, tarjan-offline-lca, transpose-graph]
sources:
  - paper: doi:10.1145/357062.357071
    title: "Thomas Lengauer and Robert Endre Tarjan, A fast algorithm for finding dominators in a flowgraph, ACM Transactions on Programming Languages and Systems 1(1) (1979), 121-141"
    locator: Section 2 (Lemmas 1 to 5, Theorems 1 to 4 and Corollary 1 on semidominators and immediate dominators), Section 3 (the algorithm, its four steps and the procedures LINK and EVAL in the simple and the sophisticated versions) and Section 4 (the running time)
  - paper: "Robert Endre Tarjan, Applications of path compression on balanced trees, Journal of the ACM 26(4) (1979), 690-715"
    locator: the analysis of EVAL and LINK with path compression, with and without balancing
  - paper: "Loukas Georgiadis, Robert E. Tarjan and Renato F. Werneck, Finding dominators in practice, Journal of Graph Algorithms and Applications 10(1) (2006), 69-94"
    locator: the experimental comparison of the simple and sophisticated Lengauer-Tarjan versions with the iterative algorithm of Cooper, Harvey and Kennedy
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition
    locator: Chapter 19 (Static single-assignment form), the section on the efficient computation of the dominator tree, with the semidominator theorems and the path-compression forest
---

The Lengauer-Tarjan algorithm solves the [dominators problem](/dominators-problem/): given a directed graph and a start vertex $r$, it finds the immediate dominator of every vertex reachable from $r$, and with it the [dominator tree](/dominator-tree/). It numbers the vertices by a depth-first search, computes for each vertex a *semidominator*, a first approximation of its immediate dominator read off the DFS tree, and then corrects the approximations in one more pass. Both steps need minimum queries along paths of the DFS tree, which a forest with [path compression](/path-compression/) answers. The simple version runs in $O(m \log n)$ time; with balanced linking it runs in $O(m\, \alpha(m, n))$ time, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/). It is the classic near-linear dominator algorithm, and the starting point of the linear-time ones.

## In plain words

Think of a building with one entrance and one-way doors. A room guards another if every way in to the second room passes it. For each room we want the nearest guard.

First, explore the building once, always going deeper when a new door opens, and number the rooms in the order you first reach them. For each room, a first guess at its nearest guard is the earliest-numbered room from which you can sneak in using only rooms with later numbers. The true guard is never closer than this guess.

Then check each guess: look at the rooms on the way down from the guess to the room. If none of them has an earlier sneaky way in, the guess is right. If one does, the room has the same guard as that room. Careful bookkeeping makes all these checks fast.

## The problem

The input is a directed graph $G$ with vertices $0, \ldots, n - 1$ and $m$ edges, given as a list of pairs $(a, b)$ meaning $a \to b$, and a start vertex $r$. The graph is unweighted; self-loops and parallel edges are allowed. The output is $\mathrm{idom}(v)$ for every vertex $v \ne r$ that $r$ can reach, and nothing (here $-1$) for $r$ and for the unreachable vertices. A vertex $d$ dominates $v$ if every path from $r$ to $v$ contains $d$, and $\mathrm{idom}(v)$ is the strict dominator of $v$ that every other strict dominator of $v$ dominates.

Inside the algorithm, the reachable vertices are renamed $0, \ldots, k - 1$ by their preorder number in a depth-first search from $r$, so $r = 0$, and "$u < v$" compares preorder numbers. $T$ is the DFS tree and $parent(w)$ the tree parent of $w$. The **semidominator** of $w \ne r$ is

$$\mathrm{sdom}(w) = \min \{\, v : \text{there is a path } v = v_0, v_1, \ldots, v_j = w \text{ with } v_i > w \text{ for } 0 < i < j \,\}.$$

The tree edge from $parent(w)$ gives $\mathrm{sdom}(w) \le parent(w) < w$.

## The algorithm

The algorithm rests on two facts, proved in the proof file. **Semidominator formula:** $\mathrm{sdom}(w)$ is the minimum of the predecessors $v < w$ of $w$ and of $\mathrm{sdom}(u)$ over all $u > w$ that are tree ancestors of some predecessor $v$ of $w$. **Immediate dominator rule:** let $u$ have the least $\mathrm{sdom}$ among the tree path vertices strictly below $\mathrm{sdom}(w)$ down to $w$; then $\mathrm{idom}(w) = \mathrm{sdom}(w)$ if $\mathrm{sdom}(u) = \mathrm{sdom}(w)$, and $\mathrm{idom}(w) = \mathrm{idom}(u)$ otherwise.

The vertices are processed in decreasing preorder. A forest, stored in $ancestor[\cdot]$, holds the processed vertices, each linked to its tree parent; EVAL$(v)$ returns a vertex of least $semi$ on the forest path from $v$ up to the root of its forest tree, not counting the root, or $v$ itself if $v$ is a root. Path compression keeps the paths short.

```pseudo id=main
LENGAUER-TARJAN(G, r)
L1  DFS from r with an explicit stack; rename the reachable vertices 0, ..., k − 1 in preorder; record parent
L2  for i ← 0 to k − 1 do semi[i] ← i; label[i] ← i; ancestor[i] ← none; bucket[i] ← ∅
L3  for w ← k − 1 down to 1 do
L4      for each predecessor v of w that r reaches do
L5          u ← EVAL(v); if semi[u] < semi[w] then semi[w] ← semi[u]
L6      add w to bucket[semi[w]]; ancestor[w] ← parent(w)              ▷ LINK
L7      for each v in bucket[parent(w)] do
L8          u ← EVAL(v); idom[v] ← u if semi[u] < semi[v], else parent(w)
L9      bucket[parent(w)] ← ∅
L10 for w ← 1 to k − 1 do                                               ▷ increasing order
L11     if idom[w] ≠ semi[w] then idom[w] ← idom[idom[w]]

EVAL(v)
L12 if ancestor[v] = none then return v
L13 x ← v; P ← empty list
L14 while ancestor[ancestor[x]] ≠ none do append x to P; x ← ancestor[x]
L15 for x in P from last to first do
        if semi[label[ancestor[x]]] < semi[label[x]] then label[x] ← label[ancestor[x]]
        ancestor[x] ← ancestor[ancestor[x]]
    return label[v]
```

Line L5 is the semidominator formula: a predecessor $v < w$ is still unlinked and EVAL returns $v$ with $semi[v] = v$, while for $v > w$ the forest path above $v$ consists of the processed tree ancestors of $v$, all larger than $w$. Lines L7 and L8 apply the rule to the vertices $v$ whose semidominator is $parent(w)$, once the tree path from $w$ down to $v$ is linked: if the minimum is at a vertex $u$ with $semi[u] = semi[v]$, the answer is $parent(w) = \mathrm{sdom}(v)$; otherwise $idom[v]$ temporarily holds $u$, meaning "the same as $\mathrm{idom}(u)$", and line L11 resolves it in increasing order, after $\mathrm{idom}(u)$ is final. The DFS and EVAL use loops, not recursion.

## Example

Take the flow graph on $0, \ldots, 8$ with start 0 and the 11 edges

$$0 \to 1,\; 1 \to 2,\; 2 \to 3,\; 2 \to 4,\; 3 \to 4,\; 3 \to 7,\; 4 \to 5,\; 5 \to 6,\; 6 \to 3,\; 7 \to 8,\; 8 \to 6.$$

With successors tried in this order, the DFS visits $0, 1, \ldots, 8$ in order, so the preorder numbers equal the labels. The DFS tree is the path $0 \to 1 \to 2 \to 3 \to 4 \to 5 \to 6$ with the branch $3 \to 7 \to 8$, so $parent = [-, 0, 1, 2, 3, 4, 5, 3, 7]$. The edges $6 \to 3$, $8 \to 6$, $2 \to 4$ and $3 \to 4$ are not tree edges.

| $w$ | predecessors $v$: EVAL$(v)$, its semi | $semi[w]$ | bucket of $parent(w)$: $v$, EVAL$(v)$, $idom[v]$ |
|---|---|---|---|
| 8 | 7: 7, 7 | 7 | bucket[7] = {8}: EVAL(8) = 8, so $idom[8] = 7$ |
| 7 | 3: 3, 3 | 3 | bucket[3] = {7}: $idom[7] = 3$ |
| 6 | 5: 5, 5; 8: 7, 3 | 3 | bucket[5] is empty |
| 5 | 4: 4, 4 | 4 | bucket[4] = {5}: $idom[5] = 4$ |
| 4 | 2: 2, 2; 3: 3, 3 | 2 | bucket[3] = {6}: EVAL(6) = 4 with $semi[4] = 2 < 3$, so $idom[6] = 4$ for now |
| 3 | 2: 2, 2; 6: 4, 2 | 2 | bucket[2] = {4, 3}: $idom[4] = 2$, $idom[3] = 2$ |
| 2 | 1: 1, 1 | 1 | bucket[1] = {2}: $idom[2] = 1$ |
| 1 | 0: 0, 0 | 0 | bucket[0] = {1}: $idom[1] = 0$ |

At $w = 6$, the predecessor 8 is processed, and EVAL(8) looks at the forest path $8, 7$ below the forest root 3: $semi[8] = 7$ and $semi[7] = 3$, so it returns 7. This says that 6 can be reached from 3 through 7 and 8, all numbered above 6, so $\mathrm{sdom}(6) = 3$. Yet 3 does not dominate 6, because of the path $0, 1, 2, 4, 5, 6$. The rule catches this at $w = 4$: on the tree path from 4 down to 6, vertex 4 has $semi[4] = 2 < 3$. So $\mathrm{idom}(6) = \mathrm{idom}(4)$, and line L11 sets $idom[6] = idom[4] = 2$. The other vertices keep their bucket values, and the result is

$$idom = [-, 0, 1, 2, 2, 4, 2, 3, 7], \qquad semi = [-, 0, 1, 2, 2, 4, 3, 3, 7].$$

Simple shapes: on the single vertex graph, $k = 1$ and nothing is done. On a path $0 \to 1 \to \cdots \to n - 1$, every vertex has one predecessor, its parent, so $semi[w] = parent(w) = idom[w] = w - 1$. On a star $0 \to v$, every semidominator and immediate dominator is 0.

## Correctness

The full proof is in the proof file. Its steps:

1. **DFS edges.** For every edge $(v, w)$ with $v < w$, $w$ is a descendant of $v$ in $T$. Hence any path from $v$ to $w$ with $v \le w$ passes through a common tree ancestor of $v$ and $w$ (LT Lemma 3).
2. **Where the dominators are.** $\mathrm{idom}(w)$ and $\mathrm{sdom}(w)$ are proper tree ancestors of $w$, and $\mathrm{idom}(w)$ is an ancestor of $\mathrm{sdom}(w)$: the tree path to $\mathrm{sdom}(w)$ followed by a semidominator path avoids every tree vertex strictly between $\mathrm{sdom}(w)$ and $w$.
3. **Semidominator formula.** Proved by splitting a shortest semidominator path at its first vertex that is a tree ancestor of the last predecessor.
4. **Immediate dominator rule.** If no vertex on the tree path below $\mathrm{sdom}(w)$ has a smaller semidominator, any path that avoided $\mathrm{sdom}(w)$ would give such a vertex; otherwise the same argument shows that $\mathrm{idom}(u)$ dominates $w$, and the nesting of dominator intervals along tree paths gives equality.
5. **The forest.** EVAL returns a minimum of $semi$ on the right tree path, because path compression keeps the invariant that $label[x]$ is a minimum on the tree path from $ancestor[x]$, exclusive, down to $x$.

## Complexity

The DFS and the predecessor lists take $\Theta(n + m)$ time. Line L5 runs once per edge and line L8 once per vertex, so there are at most $m + n$ calls of EVAL and $n - 1$ links. With path compression alone and links in this order, the total cost of these operations is $O(m \log_{2 + m/n} n)$, which is $O(m \log n)$ (Tarjan 1979). With *balanced* linking, as in the sophisticated version of the paper, it drops to $O(m\, \alpha(m, n))$. On a path or a tree the forest paths stay short and the time is $\Theta(n + m)$. The memory is $\Theta(n + m)$ for the graph, its reverse and the arrays.

| version | time | notes |
|---|---|---|
| simple (this page) | $O(m \log n)$ | path compression only |
| sophisticated | $O(m\, \alpha(m, n))$ | balanced link by subtree sizes |
| linear-time variants (Alstrup et al.; Buchsbaum et al.) | $O(n + m)$ | micro-trees and more machinery |

## Properties

- **Deterministic.** The DFS order depends on the order of the successor lists, and so do the semidominators, but the immediate dominators do not.
- **Non-recursive.** This version uses an explicit DFS stack and an iterative EVAL, so a path of $10^5$ vertices is handled without deep recursion; the version in the paper is recursive.
- **Offline.** The whole graph must be known; edge insertions need a new run or a dynamic algorithm.
- **By-products.** The DFS numbering, the DFS tree and the semidominators are useful elsewhere; for example, the semidominators are what the linear-time algorithms refine.

## Variants and improvements

- **Sophisticated linking.** Link by size, keeping a child pointer chain, so that the forest stays balanced; time $O(m\, \alpha(m, n))$. In experiments by Georgiadis, Tarjan and Werneck, the simple version is often as fast in practice.
- **Semi-NCA.** Compute the semidominators as here, then get $\mathrm{idom}(w)$ as the nearest common ancestor of $parent(w)$ and $\mathrm{sdom}(w)$ in the partially built dominator tree, processing vertices in preorder. Worst case $O(n^2)$, but fast on control-flow graphs.
- **Iterative algorithm of Cooper, Harvey and Kennedy.** No semidominators at all: repeat $\mathrm{idom}(w) \leftarrow$ the intersection of the current dominator chains of the predecessors, in reverse postorder, until stable. Simpler, and often fast on small graphs, but without a near-linear bound.
- **Linear time.** Alstrup, Harel, Lauridsen and Thorup (1999) and Buchsbaum, Georgiadis, Kaplan, Rogers, Tarjan and Westbrook (2008) remove the $\alpha$ factor.
- **Postdominators.** Run on the [transpose graph](/transpose-graph/) from the exit vertex.

## When to use it

Use it when the graphs are large or adversarial, such as huge generated control-flow graphs, heap snapshots or graphs used for connectivity analysis, where a guaranteed near-linear bound matters. On small, structured control-flow graphs, the iterative algorithm of Cooper, Harvey and Kennedy is shorter and competitive, and many compilers use it.

## Pitfalls

- **Comparing labels instead of preorder numbers.** All comparisons in lines L5, L8, L11 and L15 are on DFS numbers. The implementation renames the vertices first for this reason.
- **Unreachable predecessors.** An edge from a vertex that $r$ does not reach must be skipped in line L4; it has no DFS number.
- **Processing the bucket of the wrong vertex.** Line L7 empties the bucket of $parent(w)$, after linking $w$, not the bucket of $w$ or of $semi[w]$.
- **Resolving in the wrong order.** Line L11 must go in increasing preorder, so that $idom[idom[w]]$ is already final.
- **EVAL counting the forest root.** The minimum excludes the root of the forest tree, whose semidominator is not yet known; the check $ancestor[ancestor[x]] \ne$ none in line L14 is what stops at the vertex below the root.
- **Recursion.** The paper's recursive DFS and COMPRESS overflow the Python stack on long paths.

## Implementations

## History

Dominators go back to Prosser (1959) and to Lowry and Medlock (1969), who used them for loop optimization in the FORTRAN H compiler. Purdom and Moore (1972) computed them by deleting each vertex in turn and testing reachability. Lengauer and Tarjan (1979) published the algorithm on this page, with semidominators, the simple $O(m \log n)$ version and the $O(m\, \alpha(m, n))$ version, and analyzed the forest operations with Tarjan's results on path compression from the same year. Harel (1985) announced a linear-time algorithm; complete linear-time algorithms were given by Alstrup, Harel, Lauridsen and Thorup (1999) and by Buchsbaum, Georgiadis, Kaplan, Rogers, Tarjan and Westbrook (2008).

## References
