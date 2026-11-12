---
tag: 7VS8ZC
kind: algorithm
slug: midpoint-rooting
name: Midpoint rooting
aliases:
- midpoint root
- midpoint rooting method
area: biology/phylogenetics
level: intro
summary: Roots an unrooted tree at the midpoint of a longest leaf-to-leaf path, found by a double sweep in O(n) time. It is exact for clock-like trees and can be wrong under rate variation.
solves: [tree-rooting]
model: word-ram
complexity:
  vars: {n: the number of taxa}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [rooted-and-unrooted-trees, tree-diameter-double-sweep, depth-first-search]
see_also: [tree-rooting, tree-diameter, tree-center, molecular-clock, ultrametric, upgma, long-branch-attraction, relaxed-molecular-clock]
sources:
  - paper: doi:10.1111/j.1095-8312.2007.00864.x
    title: Pablo N. Hess and Claudia A. de Moraes Russo, An empirical test of the midpoint rooting method, Biological Journal of the Linnean Society 92(4), 2007, 669-674
    locator: the comparison of midpoint roots with outgroup roots on published data sets
  - paper: doi:10.1371/journal.pone.0182238
    title: Uyen Mai, Erfan Sayyari and Siavash Mirarab, Minimum variance rooting of phylogenetic trees and implications for species tree reconstruction, PLoS ONE 12(8), 2017, e0182238
    locator: midpoint rooting as the baseline, its errors under deviations from the clock, and minimum variance rooting
  - paper: doi:10.1038/s41559-017-0193
    title: Fernando D. K. Tria, Giddy Landan and Tal Dagan, Phylogenetic rooting using minimal ancestor deviation, Nature Ecology and Evolution 1, 2017, article 0193
    locator: midpoint rooting compared with MAD rooting under rate variation
---

Midpoint rooting places the root of an unrooted [phylogenetic tree](/phylogenetic-tree/) with branch lengths at the midpoint of a longest path between two leaves. It finds such a path with two traversals, as in the [double sweep](/tree-diameter-double-sweep/) for the [tree diameter](/tree-diameter/), and walks back to the middle, so it takes $O(n)$ time for $n$ taxa. If the tree is ultrametric, that is, if all lineages evolved at the same rate, the midpoint is exactly the true root. Under unequal rates the longest path can run through a single fast lineage, and then the root lands on the wrong edge.

## In plain words

Think of the tree as a set of roads joining towns, where the towns at the dead ends are the species and the road lengths are the amounts of change. Find the two dead-end towns that are farthest apart. Put the root halfway along the road between them.

Why does this work? If all species changed at the same speed, they would all be the same distance from the oldest ancestor. The two species that are farthest apart would then sit on opposite sides of that ancestor, and it would be halfway between them.

To find the farthest pair, start at any species and go to the species farthest from it. From there, go to the species farthest from that one. Those two are a farthest pair. Walk back from the second toward the first, and stop at the halfway point.

## The problem

**Input.** An unrooted phylogenetic tree $U$ on $n \ge 2$ taxa, with branch lengths $\ell(e) \ge 0$. Write $d(x, y)$ for the path length between two points of the tree.

**Output.** The root position $m$: a vertex, or an edge $\{u, v\}$ and a distance $t$ from $u$, such that $m$ is the midpoint of a longest leaf-to-leaf path. With $D$ the length of that path (the *diameter*), $m$ is the point on the path at distance $D/2$ from both ends. The rooted tree is $U$ with a new root vertex at $m$.

## The algorithm

```pseudo id=main
MIDPOINT-ROOT(U)                         ▷ lengths ≥ 0, at least two leaves
L1  a ← any leaf; compute d(a, y) for every vertex y
L2  b ← a leaf with the largest d(a, b)
L3  compute db[y] = d(b, y) and the parent of each vertex y on its path to b
L4  c ← a leaf with the largest db[c]
L5  D ← db[c]; h ← D / 2
L6  x ← c
L7  while db[parent[x]] > h do x ← parent[x]
L8  u ← parent[x]; return the edge {u, x}, the distance t = h − db[u] from u, and D
```

**Lines L1 to L5** find a longest path. Each line L1 and L3 is one traversal with an explicit stack that adds the edge lengths along the way. With lengths $\ge 0$, the leaf $b$ farthest from any leaf $a$ is an end of a longest path, and the leaf $c$ farthest from $b$ is the other end.

**Lines L6 to L8** walk from $c$ toward $b$ along the parent pointers. The distance $db$ falls along the walk, from $D$ at $c$ to 0 at $b$. The loop stops at the first vertex $u$ with $db[u] \le h$; its child $x$ on the path has $db[x] > h$, so the point at distance $h$ from $b$ is on the edge $\{u, x\}$, at distance $h - db[u]$ from $u$. If $t = 0$, the root is the vertex $u$ itself; otherwise the edge is split into parts of lengths $t$ and $\ell(\{u, x\}) - t$, with the new root between them.

For exact answers the lengths are integers or fractions, and $h$ is a fraction; with floating-point lengths $h$ is computed in floating point.

## Example

**Rate variation: a wrong root.** The rooted tree $((A{:}1, B{:}6){:}1, (C{:}1, D{:}1){:}1)$ has a fast lineage $B$. Unrooted, it has inner vertices $P$ (joined to $A$ by 1 and to $B$ by 6) and $Q$ (joined to $C$ and $D$ by 1), and the edge $P - Q$ of length 2. The leaf-to-leaf distances are:

| | $A$ | $B$ | $C$ | $D$ |
|---|---|---|---|---|
| $A$ | 0 | 7 | 4 | 4 |
| $B$ | 7 | 0 | 9 | 9 |
| $C$ | 4 | 9 | 0 | 2 |
| $D$ | 4 | 9 | 2 | 0 |

Start at $a = A$ (line L1). The farthest leaf is $b = B$ at 7 (L2). From $B$, the farthest leaf is $c = C$ at 9 (L4), so $D = 9$ and $h = 9/2$. The walk from $C$ goes $C$ ($db = 9$), $Q$ ($db = 8$), $P$ ($db = 6$), $B$ ($db = 0$). The loop moves $x$ to $Q$ and then to $P$, since $db[P] = 6 > 9/2$, and stops because $db[B] = 0 \le 9/2$. So the root is on the edge $B - P$, at distance $9/2$ from $B$ and $3/2$ from $P$. The rooted tree is $(B, (A, (C, D)))$, with the clusters $\{A, C, D\}$ and $\{C, D\}$. The true tree has the clusters $\{A, B\}$ and $\{C, D\}$: the fast lineage $B$ pulled the root onto its own edge.

**Ultrametric: the right root.** The rooted tree $((A{:}2, B{:}2){:}1, (C{:}1, D{:}1){:}2)$ has every leaf at distance 3 from the root. Unrooted, $P$ is joined to $A$ and $B$ by 2, $Q$ to $C$ and $D$ by 1, and $P - Q$ has length 3. From $a = A$ the farthest leaf is $C$ (or $D$) at 6; say $b = C$. From $C$ the farthest leaf is $A$ (or $B$) at 6, so $D = 6$ and $h = 3$. The walk from $A$ passes $P$ with $db[P] = 4 > 3$ and stops at $Q$ with $db[Q] = 1 \le 3$. So the root is on $P - Q$ at distance $3 - 1 = 2$ from $Q$, that is, 1 from $P$: the true root, with the true lengths 1 and 2.

## Correctness

The full proofs are in the proofs file. The argument has three steps.

1. **The double sweep finds a longest path.** This is the classical result for trees with nonnegative lengths: a vertex farthest from any start vertex is an end of a longest path. A farthest vertex can be taken to be a leaf, since moving away from an inner vertex along an edge never decreases the distance.
2. **All longest paths have the same midpoint.** Let $m$ be the midpoint of the path from $b$ to $c$. Every leaf $y$ has $d(m, y) \le D/2$: the path from $m$ to $y$ leaves the $b$ to $c$ path on one side of $m$, say the side of $c$, and then $d(b, y) = d(b, m) + d(m, y)$, which would exceed $D$. For any other longest path from $b'$ to $c'$, $D = d(b', c') \le d(b', m) + d(m, c') \le D$, so both distances are $D/2$ and, when all lengths are positive, $m$ lies on that path at its middle. So the answer does not depend on which longest path the sweep finds.
3. **On an ultrametric tree the midpoint is the root.** If every leaf is at distance $H$ from the root $\rho$, then $d(x, y) = 2(H - \delta(\operatorname{lca}(x, y)))$, where $\delta(v)$ is the distance from $\rho$ to $v$. With positive lengths $\delta(v) > 0$ for $v \ne \rho$, so the longest paths are exactly the paths between leaves in different subtrees of $\rho$, $D = 2H$, and each such path passes through $\rho$ at distance $H = D/2$ from both ends. By step 2, the algorithm returns $\rho$, at its true position on the edge.

## Complexity

Lines L1 and L3 are traversals that visit each of the fewer than $2n$ vertices and edges once. Lines L2 and L4 scan the leaves. The walk of lines L6 and L7 follows at most one path, so it takes at most $2n$ steps. Inserting the root is one more traversal. In all the time is $\Theta(n)$ and the extra space is $\Theta(n)$ for the distances and parent pointers. The traversals use an explicit stack, so a caterpillar with $10^5$ taxa does not overflow the call stack.

## Properties

- **Uses branch lengths only.** It needs no outgroup and no model, and it ignores the sequences.
- **Unique answer.** With positive lengths, every longest path gives the same point, by step 2 of the proof. With zero lengths, several points at distance 0 from each other can qualify, and they give the same rooted tree up to a zero-length edge.
- **The tree center.** The midpoint minimizes the largest distance to a leaf, with value $D/2$. So midpoint rooting places the root at the center of the tree as a metric space, which is the weighted version of the [tree center](/tree-center/).
- **Driven by two leaves.** Only the two ends of a longest path decide the root. A single long branch, from a fast lineage or from an error in the data, moves the root.

## Variants and improvements

- **Minimum variance (MV) rooting** places the root at the point that minimizes the variance of the root-to-tip distances (Mai, Sayyari and Mirarab, 2017). It uses all leaves instead of two and also runs in $O(n)$ time. On the rate-variation example above it chooses the edge $B - P$ at $25/6$ from $B$, also wrong, because the true tree is far from a clock; on trees with milder rate variation it is usually more accurate than the midpoint.
- **MAD rooting** (Tria, Landan and Dagan, 2017) scores each root by the mean deviation of all pairs of leaves from the clock assumption.
- **Rooting by tip dates.** With sampling dates, choose the root at which the root-to-tip distances best fit a linear function of the dates.
- **Outgroup rooting** uses known outside taxa and no branch lengths; see [tree rooting](/tree-rooting/).

## When to use it

Use midpoint rooting when there is no reliable outgroup, the branch lengths are trusted, and the rates are close to equal across lineages, as for a group of closely related strains. Check the result against an outgroup when one exists. Do not use it when one lineage is known to evolve fast, or for gene trees with long branches from paralogs or contamination; there use an outgroup, MV rooting, or a clock model.

## Pitfalls

- **Rate variation.** The method assumes a clock. A fast lineage makes a longest path that ends in that lineage, and the root moves onto its edge, as in the first example.
- **Ties and zero lengths.** With several longest paths and zero-length edges, the points found may differ by a zero-length edge; compare roots as points of the tree, not as vertex names.
- **Inner labels.** Inserting the root on an edge splits that edge in two. Support values stored as labels of vertices in [Newick format](/newick-format/) belong to edges, so they must be moved with care when the root is inserted.
- **Floating point.** With floating-point lengths, the test $db[parent[x]] > h$ in line L7 can go the wrong way when the root is very close to a vertex. Use exact fractions when the result must be exact.
- **Deep trees.** Recursive traversals overflow the stack on trees with tens of thousands of levels. Use explicit stacks, as the implementation does.

## Implementations

## History

Rooting at the midpoint of the longest path follows from the observation that under a molecular clock the root is equally far from all leaves. It has long been a default in tree programs and tree viewers when no outgroup is given. Hess and de Moraes Russo (2007) compared midpoint roots with outgroup roots on published data sets. Later methods, minimum variance rooting (Mai, Sayyari and Mirarab, 2017) and minimal ancestor deviation (Tria, Landan and Dagan, 2017), use all leaves instead of the two ends of one path to reduce the effect of rate variation.

## References
