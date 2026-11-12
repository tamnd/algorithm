---
tag: WDM8Q2
kind: algorithm
slug: day-algorithm
name: Day's algorithm
aliases:
- linear-time Robinson-Foulds comparison
- Day's cluster table
area: biology/phylogenetics
level: advanced
summary: Computes the Robinson-Foulds distance of two trees on n taxa in O(n) time. Leaves are numbered so each cluster is an interval, and a table answers each lookup in O(1) time.
solves: [tree-comparison]
model: word-ram
complexity:
  vars: {n: the number of taxa}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1985
  people: [William H. E. Day]
  note: Day gave linear-time algorithms for comparing trees with labeled leaves in the Journal of Classification in 1985, among them the cluster table for the symmetric difference distance of Robinson and Foulds.
prereqs: [robinson-foulds-distance, postorder-traversal, rooted-and-unrooted-trees]
see_also: [splits-of-a-tree, split-system, tree-comparison, consensus-tree, preorder-traversal, subtree-sizes]
sources:
  - paper: doi:10.1007/BF01908061
    title: William H. E. Day, Optimal algorithms for comparing trees with labeled leaves, Journal of Classification 2(1), 1985, 7-28
    locator: the cluster table, built from a postorder numbering of the leaves of one tree, and its use for the symmetric difference distance in O(n) time
  - paper: doi:10.1016/0025-5564(81)90043-2
    title: D. F. Robinson and L. R. Foulds, Comparison of phylogenetic trees, Mathematical Biosciences 53(1-2), 1981, 131-147
    locator: the definition of the distance that the algorithm computes
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 30, Consensus trees and distances between trees
---

Day's algorithm computes the [Robinson-Foulds distance](/robinson-foulds-distance/) between two phylogenetic trees on the same $n$ taxa in $O(n)$ time and space. It numbers the leaves of the first tree in [postorder](/postorder-traversal/), so that the set of taxa below each vertex is an interval of numbers, and it stores these intervals in a table with one row per leaf. A vertex of the second tree then has a shared cluster exactly when its leaf numbers form an interval that is in the table, which takes $O(1)$ time to test. Day published it in 1985, and since every algorithm must read both trees, it is optimal.

## In plain words

Two trees on the same species each claim some groups: for each branch point, the species below it. The distance counts the groups that only one tree claims.

Comparing group lists directly is slow, because a group can hold many species. The trick is to number the species by walking around the first tree from left to right. Then every group of the first tree is a run of consecutive numbers, given by its first and last number. We keep these pairs in a table with one row for each species.

Now walk the second tree. For each of its groups, find the smallest number, the largest number and the count of species. The group is a run if the count matches the gap between the ends. If it is a run and the table holds that pair, both trees have the group. Each check is quick.

## The problem

**Input.** Two rooted phylogenetic trees $T_1$ and $T_2$ on the same set $X$ of $n$ taxa, in which each inner vertex has at least two children. For unrooted trees, see the variant below.

**Output.** The rooted Robinson-Foulds distance
$$d_{RF}(T_1, T_2) = |\mathcal{C}(T_1) \,\triangle\, \mathcal{C}(T_2)|,$$
where $\mathcal{C}(T)$ is the set of clusters of the inner vertices of $T$: the cluster of a vertex is the set of taxa below it. The singleton clusters of the leaves are in both trees and are left out; the root cluster $X$ is in both trees and adds 0.

## The algorithm

```pseudo id=main
DAY-RF(T1, T2)                     ▷ rooted trees on the same n taxa
L1  number the leaves of T1 0, 1, ..., n − 1 in postorder; num[x] ← the number of leaf x
L2  X[0 .. n − 1] ← none; c1 ← 0; for each leaf x of T1: lo[x] ← hi[x] ← num[x]
L3  for each inner vertex v of T1, in postorder do
L4      lo[v] ← lo[first child of v]; hi[v] ← hi[last child of v]; c1 ← c1 + 1
L5      if v is the root or the last child of its parent then X[lo[v]] ← (lo[v], hi[v])
L6      else X[hi[v]] ← (lo[v], hi[v])
L7  s ← 0; c2 ← 0; for each leaf x of T2: lo[x] ← hi[x] ← num[x]; size[x] ← 1
L8  for each inner vertex v of T2, in postorder do
L9      lo[v] ← min of lo over the children; hi[v] ← max of hi over the children; size[v] ← sum of size over the children; c2 ← c2 + 1
L10     if hi[v] − lo[v] + 1 = size[v] and (X[lo[v]] = (lo[v], hi[v]) or X[hi[v]] = (lo[v], hi[v])) then s ← s + 1
L11 return (c1 − s) + (c2 − s)
```

**Lines L1 to L6** build the *cluster table* of $T_1$. A postorder walk visits the leaves below a vertex one after another, so the cluster of each inner vertex $v$ is the interval of numbers $[lo[v], hi[v]]$, with its ends taken from the first and the last child. Each interval is stored in one of the two rows at its ends. The row rule of lines L5 and L6 puts no two intervals in the same row, so one table of $n$ rows holds all the clusters of $T_1$.

**Lines L7 to L10** walk $T_2$. With the numbers of $T_1$ on its leaves, a cluster $C$ of $T_2$ is an interval exactly when its largest and smallest numbers are $|C| - 1$ apart. If it is the interval $[a, b]$, it is a cluster of $T_1$ exactly when the table holds $(a, b)$, and the entry can only be in row $a$ or row $b$. So line L10 counts the shared clusters $s$.

**Line L11.** Each tree has its own clusters minus the shared ones, so $d_{RF} = (c_1 - s) + (c_2 - s)$.

**Unrooted trees.** Pick a taxon $r$, root both trees at the neighbour of the leaf $r$, and delete $r$. Each split of the unrooted tree becomes the cluster of its side without $r$, so the rooted distance of the results on $X \setminus \{r\}$ equals the unrooted distance of the original trees. The implementation does this with an explicit stack.

## Example

Let $T_1 = ((a,b),(c,(d,e)))$ and $T_2 = ((a,c),(b,(d,e)))$. Name the inner vertices of $T_1$ $\rho_1$ (the root), $x = (a,b)$, $y = (c,(d,e))$ and $z = (d,e)$.

**The table of $T_1$.** The postorder numbers are $a = 0$, $b = 1$, $c = 2$, $d = 3$, $e = 4$. The inner vertices in postorder are:

| vertex | interval | first child, last child, or root? | row | table after |
|---|---|---|---|---|
| $x = (a,b)$ | $[0, 1]$ | first child of $\rho_1$ | $hi = 1$ | $X[1] = (0, 1)$ |
| $z = (d,e)$ | $[3, 4]$ | last child of $y$ | $lo = 3$ | $X[3] = (3, 4)$ |
| $y = (c,z)$ | $[2, 4]$ | last child of $\rho_1$ | $lo = 2$ | $X[2] = (2, 4)$ |
| $\rho_1$ | $[0, 4]$ | root | $lo = 0$ | $X[0] = (0, 4)$ |

So $X = [(0,4), (0,1), (2,4), (3,4), \text{none}]$ and $c_1 = 4$.

**The walk over $T_2$.**

| vertex of $T_2$ | numbers | lo, hi, size | interval? | in the table? |
|---|---|---|---|---|
| $(a, c)$ | 0, 2 | 0, 2, 2 | no: $2 - 0 + 1 = 3 \ne 2$ | no |
| $(d, e)$ | 3, 4 | 3, 4, 2 | yes | $X[3] = (3, 4)$: yes |
| $(b, (d, e))$ | 1, 3, 4 | 1, 4, 3 | no: $4 \ne 3$ | no |
| root | 0 to 4 | 0, 4, 5 | yes | $X[0] = (0, 4)$: yes |

So $s = 2$, $c_2 = 4$, and $d_{RF} = (4 - 2) + (4 - 2) = 4$: the clusters $ab$ and $cde$ are only in $T_1$, and $ac$ and $bde$ only in $T_2$.

## Correctness

The proof has three parts; the full version is in the proofs file.

1. **Clusters are intervals.** In a postorder walk the leaves below $v$ are visited consecutively, and those below the first child of $v$ come first and those below the last child come last. So the cluster of $v$ is the set of numbers $[lo[v], hi[v]]$ computed by line L4.
2. **No two intervals share a row.** Two clusters of $T_1$ are disjoint or nested. Disjoint intervals use rows inside themselves, so their rows differ. If $w$ is a proper descendant of $v$, its interval is strictly smaller. Suppose they share a row. If $v$ uses row $lo[v]$, then $lo[w] = lo[v]$, and $w$ must also use its low end; so $w$ is the last child of its parent $p$, but then $lo[w] > lo[p] \ge lo[v]$, a contradiction. If $v$ uses row $hi[v]$, then $hi[w] = hi[v]$ and $w$ uses its high end, so $w$ is not the last child of its parent $p$, and $hi[w] < hi[p] \le hi[v]$, again a contradiction. So the table holds every cluster of $T_1$, each in one of the rows at its ends.
3. **The test of line L10.** For an inner vertex $v$ of $T_2$ with cluster $C$, lines L7 and L9 compute the smallest and largest $T_1$-number in $C$ and $|C|$. The numbers are distinct, so $C$ is an interval exactly when $hi - lo + 1 = |C|$. A cluster of $T_1$ equal to $[lo, hi]$ is stored in row $lo$ or row $hi$, and every entry of the table is a cluster of $T_1$, so the test is true exactly when $C \in \mathcal{C}(T_1)$. Distinct inner vertices of $T_2$ have distinct clusters, because each inner vertex has at least two children, so $s = |\mathcal{C}(T_1) \cap \mathcal{C}(T_2)|$.

## Complexity

| | time | space |
|---|---|---|
| numbering and table, lines L1 to L6 | $\Theta(n)$ | $n$ rows |
| walk over $T_2$, lines L7 to L10 | $\Theta(n)$ | three numbers per vertex |
| total, rooted or unrooted | $\Theta(n)$ | $\Theta(n)$ |

A tree on $n$ taxa has fewer than $2n$ vertices and edges. Each postorder walk visits each vertex once and each edge once (the minimum, maximum and sum over the children in line L9 cost one step per child). Each table access in lines L5, L6 and L10 is one array access with numbers below $n$, which takes $O(1)$ time in the word RAM. Rooting an unrooted tree at a leaf is one more walk. Every algorithm must read both trees, so $\Omega(n)$ time is needed and the algorithm is optimal.

## Properties

- **Deterministic and exact.** It uses no hashing, so its bound is worst case, unlike the expected bound of a hash table of split masks.
- **Asymmetric.** $T_1$ builds the table and $T_2$ is walked. The result is the same if the roles are swapped.
- **Reusable table.** The table of $T_1$ is built once. Comparing $T_1$ with $m$ other trees takes $O(n)$ time for the table and $O(n)$ for each further tree, so $O(mn)$ in all.
- **Shared clusters, not only their number.** Line L10 marks which vertices of $T_2$ have shared clusters, which is what the strict [consensus tree](/consensus-tree/) of two trees needs.
- **Any degree.** Inner vertices may have any number of children at least two; polytomies need no special case.

## Variants and improvements

- **Unrooted trees.** Root both trees at the neighbour of one fixed leaf and drop the leaf, as described above.
- **Strict consensus.** The same table gives the strict consensus tree of two trees in $O(n)$ time: keep the clusters that line L10 accepts and build the tree of these clusters.
- **Many trees.** For $m$ trees and a full matrix of distances, a [hash table](/hash-table/) of split masks over all trees ([split system](/split-system/)) gives all $\binom{m}{2}$ distances with one pass over the splits of each tree. Day's table gives one row of the matrix in $O(mn)$ time.
- **Half distance.** Programs that report $\frac{1}{2} d_{RF}$ return $((c_1 - s) + (c_2 - s))/2$ from line L11.
- **Other row rules.** Any rule that puts each interval in a row at one of its ends and no two intervals in one row works. The rule on this page, low end for the root and for last children and high end for the others, is chosen to make the proof short; Day's paper states its own rule of this kind.

## When to use it

Use Day's algorithm to compare two large trees, or one tree with a stream of others, when the bound must be worst case and the trees may have $10^5$ or more taxa: it needs no masks of $n$ bits and no hashing. For many small trees, masks in a hash table are simpler. For distances that react less to the move of a single taxon, use another distance from [tree comparison](/tree-comparison/).

## Pitfalls

- **Different leaf sets.** The trees must have the same taxa. A leaf of $T_2$ with no number, or a taxon missing from $T_2$, must raise an error, as the implementation does; otherwise the size test of line L10 is wrong.
- **The row rule.** Storing every interval in its low row fails: in $((a,b),c)$ the clusters $[0, 1]$ and $[0, 2]$ both start at 0. The rule must separate nested intervals that share an end.
- **Rooted against unrooted.** Comparing two unrooted trees as if their Newick strings were rooted gives the rooted distance of two arbitrary rootings, which can be larger. Root both at the same leaf first.
- **Vertices with one child.** A vertex with one child has the same cluster as its child, so $c_1$ or $c_2$ counts that cluster twice. Suppress such vertices first; the implementation rejects them.
- **Deep trees.** A caterpillar on $10^5$ taxa is $10^5$ levels deep. Write the postorder walks with an explicit stack, not with recursion.

## Implementations

## History

Robinson and Foulds defined the symmetric difference distance in 1981. In 1985 William H. E. Day gave linear-time algorithms for comparing trees with labeled leaves, based on the observation that a postorder numbering makes every cluster of one tree an interval; the cluster table answered the question of whether the distance could be computed in time proportional to the size of the trees. The same table gives the strict consensus tree of two trees in linear time, and it is still a standard way to compute the distance in phylogenetics software.

## References
