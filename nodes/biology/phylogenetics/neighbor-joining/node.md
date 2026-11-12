---
tag: 7JNM0Y
kind: algorithm
slug: neighbor-joining
name: Neighbor-joining
aliases:
- NJ
area: biology/phylogenetics
level: core
summary: Distance method that joins the pair minimizing the Q-criterion until two nodes remain. Exact on tree metrics in O(n^3) time; greedy for balanced minimum evolution.
solves: [additive-tree-reconstruction]
model: word-ram
complexity:
  vars: {n: the number of taxa}
  time: {worst: "O(n^3)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1987
  people: [Naruya Saitou, Masatoshi Nei]
  note: Saitou and Nei introduced the method in 1987. Studier and Keppler gave the Q-criterion form and the O(n^3) running time in 1988.
prereqs: [additive-tree-reconstruction, tree-metric, agglomerative-clustering]
see_also: [bionj, upgma, minimum-evolution, fitch-margoliash, four-point-method, four-point-condition, progressive-alignment, tree-rooting]
sources:
  - paper: doi:10.1093/oxfordjournals.molbev.a040454
    title: Naruya Saitou and Masatoshi Nei, The neighbor-joining method, a new method for reconstructing phylogenetic trees, Molecular Biology and Evolution 4(4), 1987, pages 406 to 425
    locator: the method, the sum-of-branch-length criterion S and its branch length formulas
  - paper: doi:10.1093/oxfordjournals.molbev.a040527
    title: James A. Studier and Karl J. Keppler, A note on the neighbor-joining algorithm of Saitou and Nei, Molecular Biology and Evolution 5(6), 1988, pages 729 to 731
    locator: the equivalent Q-criterion and the O(n^3) form
  - paper: doi:10.1007/PL00008277
    title: Kevin Atteson, The performance of neighbor-joining methods of phylogenetic reconstruction, Algorithmica 25, 1999, pages 251 to 278
    locator: the l-infinity radius 1/2 of neighbor-joining
  - paper: doi:10.1093/molbev/msl072
    title: Olivier Gascuel and Mike Steel, Neighbor-joining revealed, Molecular Biology and Evolution 23(11), 2006, pages 1997 to 2000
    locator: neighbor-joining as a greedy method for balanced minimum evolution
  - book: isbn:9780521629713
    title: Richard Durbin, Sean Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, 1998
    locator: Chapter 7, neighbour-joining and the proof that it reconstructs additive trees
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, 2004
    locator: Chapter 11, Distance matrix methods
---

Neighbor-joining (NJ) is a distance method of [phylogenetic tree reconstruction](/phylogenetic-tree-reconstruction/): from a matrix of pairwise distances between $n$ taxa it builds an unrooted binary [phylogenetic tree](/phylogenetic-tree/) with edge lengths. Like [agglomerative clustering](/agglomerative-clustering/), it joins two nodes at a time, but it picks the pair that minimizes the $Q$-criterion $Q(i, j) = (r - 2) D_{ij} - R_i - R_j$, not the pair at the smallest distance. When the matrix is a [tree metric](/tree-metric/), NJ returns that tree with its edge lengths, and it runs in $O(n^3)$ time. Saitou and Nei published it in 1987; Studier and Keppler gave the $Q$ form in 1988.

## In plain words

Neighbor-joining builds a family tree from a table of distances between species. Two species are neighbors when they hang from the same point of the tree. The closest pair in the table is not always a pair of neighbors: a species on a short branch near the middle of the tree is close to many others. So the method corrects each distance by how far the two species are from all the other species, and joins the pair with the best corrected value. It puts a new node between the two, computes the two branch lengths, and replaces the pair by the new node in the table. It repeats this until two nodes are left, and connects them. When the table comes exactly from a tree, each joined pair is a true pair of neighbors, so the method rebuilds that tree.

## The problem

The input is $n \ge 2$ taxa and a symmetric $n \times n$ matrix $D$ with $D_{ii} = 0$ and $D_{ij} \ge 0$. The entries are distances only: the method does not look at the $m$ sites of an alignment or at the character type. Usually $D$ comes from aligned sequences through a model correction such as the [Jukes-Cantor](/jukes-cantor-model/) distance. The output is an unrooted tree whose leaves are the taxa, whose internal nodes have degree 3, and whose edges have real lengths.

The exact goal is [additive tree reconstruction](/additive-tree-reconstruction/): if $D$ is the leaf metric of a binary tree $T$ with positive edge lengths, return $T$. For any other $D$, NJ is a fast heuristic for [minimum evolution](/minimum-evolution/). It does not search the $(2n-5)!!$ unrooted binary trees; it builds one tree with $n - 2$ greedy choices.

## The algorithm

```pseudo id=main
NEIGHBOR-JOINING(D, n)
L1  A ← {1, ..., n}; r ← n                 ▷ the active nodes
L2  while r > 2 do
L3      for each i ∈ A do R_i ← Σ_{k ∈ A} D_ik
L4      (i, j) ← a pair of A that minimizes Q(i, j) = (r − 2) D_ij − R_i − R_j
L5      create a new node u
L6      δ_iu ← D_ij / 2 + (R_i − R_j) / (2(r − 2)); δ_ju ← D_ij − δ_iu
L7      add the edges (i, u) of length δ_iu and (j, u) of length δ_ju
L8      for each k ∈ A \ {i, j} do D_uk ← D_ku ← (D_ik + D_jk − D_ij) / 2
L9      A ← (A \ {i, j}) ∪ {u}; r ← r − 1
L10 let A = {a, b}; add the edge (a, b) of length D_ab
L11 return the edges
```

Line L3 computes the row sums over the active nodes only. Line L4 is the selection step. The term $(r-2)D_{ij}$ favors close pairs, and $-R_i - R_j$ favors pairs that are far from everything else; together they find a pair of neighbors even when a long branch makes them look far apart. Line L6 splits $D_{ij}$ between the two new edges: the node that is farther from the rest gets the longer edge. Line L8 gives the distance from the new node $u$ to each other node, and line L9 replaces $i$ and $j$ by $u$. Each pass removes one node, so the loop runs $n - 2$ times.

## Example

The five taxa A to E have this distance matrix. It is the tree metric of the tree `((A:2,B:7):1,E:5,(C:3,D:6):2);` in [Newick format](/newick-format/).

| | A | B | C | D | E |
|---|---|---|---|---|---|
| A | 0 | 9 | 8 | 11 | 8 |
| B | 9 | 0 | 13 | 16 | 13 |
| C | 8 | 13 | 0 | 9 | 10 |
| D | 11 | 16 | 9 | 0 | 13 |
| E | 8 | 13 | 10 | 13 | 0 |

The smallest entries are $D_{AC} = D_{AE} = 8$, and neither pair is a pair of neighbors: A sits on a short edge near the middle.

**Pass 1, $r = 5$.** The row sums are $R = (36, 51, 40, 49, 44)$ for A to E. The $Q$ values are:

| pair | AB | AC | AD | AE | BC | BD | BE | CD | CE | DE |
|---|---|---|---|---|---|---|---|---|---|---|
| $Q$ | −60 | −52 | −52 | −56 | −52 | −52 | −56 | **−62** | −54 | −54 |

NJ joins C and D into $u_1$. Line L6 gives $\delta_{C} = 9/2 + (40 - 49)/6 = 3$ and $\delta_{D} = 9 - 3 = 6$. Line L8 gives $D_{u_1 A} = (8 + 11 - 9)/2 = 5$, $D_{u_1 B} = 10$ and $D_{u_1 E} = 7$.

**Pass 2, $r = 4$.** The active nodes are A, B, E, $u_1$, with $R = (22, 32, 28, 22)$. The pairs AB and E$u_1$ tie at $Q = -36$; all other pairs have $Q = -34$. The two tied pairs are the two cherries of a four-leaf tree, so both choices are correct. The scan order picks AB, joined into $u_2$ with $\delta_A = 9/2 + (22 - 32)/4 = 2$ and $\delta_B = 7$. The new row is $D_{u_2 E} = 6$ and $D_{u_2 u_1} = 3$.

**Pass 3, $r = 3$.** For three nodes all $Q$ values are equal (here −16), since $Q(i, j) = -(D_{ij} + D_{ik} + D_{jk})$. NJ joins E and $u_1$ into $u_3$ with $\delta_E = 7/2 + (13 - 10)/2 = 5$ and $\delta_{u_1} = 2$, and $D_{u_3 u_2} = (6 + 3 - 7)/2 = 1$.

**Line L10.** The last edge is $(u_2, u_3)$ of length 1. The output is `((A:2,B:7):1,E:5,(C:3,D:6):2);`, the tree that produced the matrix, with every edge length right.

## Correctness

If $D$ is the leaf metric of a binary tree $T$ with positive edge lengths, NJ returns $T$ with its edge lengths, for every tie rule in line L4. The key step is that every pair that minimizes $Q$ is a cherry of $T$. Write $z(i, j)$ for the length of the path between $i$ and $j$ plus the sum, over all leaves, of the distance from each leaf to that path; then $Q(i, j) = -2 z(i, j)$. For an internal node $v$ on the path, $z(i, j)$ is at most the sum of the distances from $v$ to all leaves, with equality only when $i$ and $j$ are the two leaf neighbors of $v$. A walk down from the node with the smallest such sum then finds, for each non-cherry, a cherry with a larger $z$. Lines L6 and L8 are exact on a cherry, so the reduced matrix is the leaf metric of the tree with the cherry cut off, and induction on $r$ finishes the proof. The full proof is in the proof file.

## Complexity

The model is the word RAM with unit-cost arithmetic on the entries.

- **Line L3.** $O(r^2)$ time per pass.
- **Line L4.** $\binom{r}{2}$ values of $Q$, each in $O(1)$ time once the row sums are known: $O(r^2)$ time.
- **Lines L5 to L9.** $O(r)$ time.

Summed over $r = n, n-1, \ldots, 3$, the time is $\sum_r O(r^2) = O(n^3)$ in the worst case. The matrix takes $O(n^2)$ space, and a new row can reuse the storage of row $i$. Computing the original criterion of Saitou and Nei (below) from its definition costs $O(r^2)$ time per pair, so a direct implementation is slower by a factor of $r^2$; the identity with $Q$ removes that cost.

## Properties

- **Exact on tree metrics.** Proved above. On the example, the matrix and the output tree agree in every entry.
- **Robust to small errors.** Atteson (1999) proved: if $T$ has shortest edge length $\mu$ and every entry of $D$ differs from the tree metric of $T$ by less than $\mu/2$, NJ returns the topology of $T$. He also showed that no distance method can guarantee a larger radius in this sense.
- **Statistically consistent.** If the distance estimates converge to the tree metric as the number $m$ of sites grows, the bound of Atteson holds with probability tending to 1, so the topology is right with probability tending to 1.
- **Greedy for balanced minimum evolution.** Gascuel and Steel (2006) showed that the pair that minimizes $Q$ is the pair whose joining gives the smallest [balanced minimum evolution](/minimum-evolution/) length of the partly resolved tree. NJ is a greedy method for that criterion, so on non-additive data it need not return the tree with the smallest balanced length.
- **Equivalent criterion.** Saitou and Nei chose the pair that minimizes $S_{ij}$, the total edge length of the tree in which $i$ and $j$ are joined and all other nodes hang from one star. With $T_D$ the sum of all $\binom{r}{2}$ entries, $S_{ij} = (Q(i, j) + 2 T_D) / (2(r - 2))$, so both criteria pick the same pairs.
- **Unrooted output.** The last edge of line L10 is not a root. The order of the joins is not a time order.

## Variants and improvements

- **[BIONJ](/bionj/)** (Gascuel 1997) keeps the selection of line L4 but replaces the reduction of line L8 by a weighted average that minimizes the variance of the new distances.
- **Weighted selection.** Weighbor (Bruno, Socci and Halpern 2000) changes the selection criterion to take the larger variance of long distances into account.
- **Faster search for the minimum.** RapidNJ (Simonsen, Mailund and Pedersen 2008) keeps sorted rows and bounds that skip most pairs; the worst case stays $O(n^3)$, but large inputs run much faster in practice.
- **Tree improvement.** FastME (Desper and Gascuel 2002) starts from a tree and improves its [minimum evolution](/minimum-evolution/) length with [nearest neighbor interchanges](/nearest-neighbor-interchange/).

## When to use it

Use NJ when you need a reasonable tree for hundreds or thousands of taxa in seconds, when you have only a distance matrix, or when you need a guide tree for [progressive alignment](/progressive-alignment/), as in [Clustal](/clustal/). It does not need a [molecular clock](/molecular-clock/), unlike [UPGMA](/upgma/). For a final analysis of sequence data, a [maximum likelihood](/maximum-likelihood-phylogeny/) search usually starts from the NJ tree and improves it.

## Pitfalls

- **Joining the closest pair.** The smallest $D_{ij}$ need not be a pair of neighbors, as in the example. Choosing it gives UPGMA-like behavior, which is wrong without a clock.
- **Wrong $r$ or wrong sums.** $R_i$ sums over the active nodes only, and $r$ is the current number of active nodes, not $n$. With the original $n$, the criterion is no longer $Q$ and the exactness proof fails.
- **Negative edge lengths.** On non-additive data line L6 can give a negative length. Programs often set it to zero and add the difference to the sister edge; report this, because it changes the fit to $D$.
- **Uncorrected distances.** The proportion of differing sites saturates for distant sequences and is not additive. Use a model-based correction, and check for undefined values (the Jukes-Cantor distance is infinite when the proportion reaches 3/4).
- **Ties and input order.** With exact ties in line L4 the output depends on the tie rule. On additive data every choice gives the same tree, but on real data a different order of the taxa can give a different topology.
- **Reading a root.** The output is unrooted. Root it with an outgroup or with [midpoint rooting](/midpoint-rooting/) before you read the order of events.

## Implementations

## History

Saitou and Nei (1987) introduced neighbor-joining as a method that joins, at each step, the pair that gives the smallest total edge length of a star-like tree. Studier and Keppler (1988) showed that the same pair minimizes the simpler $Q$-criterion, which gives the $O(n^3)$ form used today. Atteson (1999) proved the robustness radius of 1/2, and Gascuel and Steel (2006) explained the selection rule as a greedy step for balanced minimum evolution.

## References
