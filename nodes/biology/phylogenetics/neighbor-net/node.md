---
tag: DQBMCY
kind: algorithm
slug: neighbor-net
name: NeighborNet
aliases:
- neighbor-net
area: biology/phylogenetics
level: research
summary: Builds a circular order of the taxa by neighbor-joining style agglomeration, then fits nonnegative least squares weights to its circular splits.
solves: [split-network-construction]
model: real-ram
complexity:
  vars: {n: the number of taxa, t: the number of active set steps of the least squares fit}
  time: {worst: "O(n^3 + t n^6)"}
  space: {extra: "O(n^4)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2004
  people: [David Bryant, Vincent Moulton]
  note: Bryant and Moulton presented NeighborNet at WABI 2002 and in Molecular Biology and Evolution in 2004. Bryant, Moulton and Spillner proved in 2007 that it recovers every circular metric.
prereqs: [neighbor-joining, split-system, least-squares-problem]
see_also: [split-decomposition, split-network-construction, phylogenetic-network, tree-metric, least-squares-phylogeny, splits-of-a-tree, quadratic-programming, four-point-condition]
sources:
  - paper: doi:10.1093/molbev/msh018
    title: David Bryant and Vincent Moulton, Neighbor-Net, an agglomerative method for the construction of phylogenetic networks, Molecular Biology and Evolution 21(2), 2004
    locator: the agglomeration with clusters of at most two nodes, the reduction of three nodes to two, and the least squares weights for the circular splits
  - paper: doi:10.1186/1748-7188-2-8
    title: David Bryant, Vincent Moulton and Andreas Spillner, Consistency of the Neighbor-Net algorithm, Algorithms for Molecular Biology 2, 2007
    locator: the proof that the agglomeration returns a compatible circular order for every circular metric
  - book: isbn:9780898713565
    title: Charles L. Lawson and Richard J. Hanson, Solving Least Squares Problems, SIAM, 1995
    locator: the active set method for least squares with nonnegativity constraints and its proof of termination
  - paper: doi:10.1093/molbev/msj030
    title: Daniel H. Huson and David Bryant, Application of phylogenetic networks in evolutionary studies, Molecular Biology and Evolution 23(2), 2006
    locator: SplitsTree4, which computes NeighborNet and draws the result as a planar splits graph
---

NeighborNet, by Bryant and Moulton (2004), turns a distance matrix on $n$ taxa into a weighted set of splits that can conflict with each other, and so it shows the signal that a single tree hides. It works in two parts. The first part joins nodes as [neighbor-joining](/neighbor-joining/) does, but it does not join two neighbors into one node at once. It keeps them side by side in a cluster, and later reduces three nodes in a row to two. The result is a *circular order* of the taxa. The second part fits nonnegative weights to all $\binom{n}{2}$ splits whose sides are intervals of that circle, by least squares. The splits with positive weight form a circular [split system](/split-system/), which always has a planar splits graph, so the output is a readable [split network](/split-network-construction/).

## In plain words

Neighbor-joining finds two taxa that look like neighbors and replaces them by one new node. After that, nothing can show that one of the two taxa is also close to a third group. NeighborNet waits. It puts the two taxa next to each other but keeps them both. When a third taxon joins one of them, the middle one has two neighbors, and the three become two new nodes. At the end, undoing these steps gives a ring of all taxa, in which close taxa sit close together.

Then each arc of the ring defines a split: the taxa on the arc against the rest. NeighborNet gives each such split a weight so that the sums of weights match the distances as well as possible, with no negative weights. Splits that get weight zero drop out.

## The problem

The input is a symmetric matrix $d$ with zero diagonal on taxa $X$, usually a [metric](/metric-space/). The output is a circular order $x_0, \ldots, x_{n-1}$ of $X$ and a weight $w_S \ge 0$ for each split $S$ that is *circular* for this order, which means that one side is a set of consecutive taxa around the circle. The weights minimize

$$f(w) = \sum_{p < q} \Big(\sum_S w_S\, \delta_S(p, q) - d(p, q)\Big)^2,$$

where $\delta_S(p, q)$ is 1 if $S$ separates $p$ and $q$ and 0 otherwise. A matrix that is exactly such a sum, $d = \sum_S \lambda_S \delta_S$ with $\lambda \ge 0$ for some circular order, is a *circular metric*. [Tree metrics](/tree-metric/) are circular metrics, because every tree has a circular order in which each of its splits is an interval.

## The algorithm

Let there be $m$ clusters, and let $d(C, D)$ be the mean of the distances between the nodes of $C$ and $D$. Put $R(C) = \sum_{D \ne C} d(C, D)$.

```pseudo id=main
NEIGHBOR-NET(d on n taxa)
L1  make each taxon a cluster of one node
L2  while more than 3 nodes remain do
L3      choose clusters C_i, C_j that minimize Q = (m − 2) d(C_i, C_j) − R(C_i) − R(C_j)
L4      choose x_i ∈ C_i, x_j ∈ C_j by the same Q, with the nodes of C_i and C_j as clusters of one
L5      join the chains C_i and C_j end to end, with x_i next to x_j
L6      while the chain has 3 or more nodes, reduce its first three nodes x, y, z to two new nodes u, v
L7  list the nodes of the last clusters, cluster by cluster
L8  undo the reductions in reverse order, putting x, y, z back in place of u, v
L9  fit w ≥ 0 to all circular splits of the order by least squares
L10 return the order and the splits with w_S > 0
```

**The reduction of line L6.** For three nodes $x, y, z$ in a row and every other node $a$, with $\alpha = \beta = \gamma = \frac{1}{3}$,

$$d(u, a) = (\alpha + \beta)\, d(x, a) + \gamma\, d(y, a), \qquad d(v, a) = \alpha\, d(y, a) + (\beta + \gamma)\, d(z, a),$$
$$d(u, v) = \alpha\, d(x, y) + \beta\, d(x, z) + \gamma\, d(y, z).$$

So $u$ stands for the left end with part of the middle, and $v$ for the right end with the rest of the middle. A cluster never holds more than two nodes after line L6. When two clusters of two are joined, the chain has four nodes, and line L6 reduces twice.

**The least squares fit of line L9.** The design matrix has one row per pair of taxa and one column per circular split, so it is a square matrix of size $\binom{n}{2}$, and it is invertible. The implementation uses the active set method of Lawson and Hanson in exact arithmetic. It starts with all weights zero. It adds the split whose weight most wants to grow, solves the least squares problem on the chosen splits, and, if a weight becomes negative, moves back to the boundary and drops the splits whose weights reach zero. It stops when no weight outside the chosen set can lower $f$.

## Example

Take five taxa with the distances below. They come from a branch of length 1 at each taxon, the split $ab \mid cde$ of weight 3 and the split $bc \mid ade$ of weight 2, the rectangle of the [split network construction](/split-network-construction/) page.

| | a | b | c | d | e |
|---|---|---|---|---|---|
| a | 0 | 4 | 7 | 5 | 5 |
| b | 4 | 0 | 5 | 7 | 7 |
| c | 7 | 5 | 0 | 4 | 4 |
| d | 5 | 7 | 4 | 0 | 2 |
| e | 5 | 7 | 4 | 2 | 0 |

**Round 1.** The row sums are $R = 21, 23, 20, 18, 18$, and $Q(a, b) = 3 \cdot 4 - 21 - 23 = -32$ is the smallest value. The next one is $Q(d, e) = 3 \cdot 2 - 36 = -30$. So $a$ and $b$ form a cluster of two nodes. Nothing is reduced.

**Round 2.** The clusters are $\{a, b\}, c, d, e$, and $d(\{a, b\}, x) = 6$ for $x = c, d, e$. The sums are $R = 18, 14, 12, 12$. The pairs $(\{a, b\}, c)$ and $(d, e)$ tie at $Q = -20$, and the implementation takes the first one. For the nodes, $Q(b, c) = -28$ is smaller than $Q(a, c) = -20$, so $c$ goes next to $b$, and the chain is $a, b, c$. Node $b$ has two neighbors, so line L6 reduces $a, b, c$ to $u, v$ with $d(u, d) = d(u, e) = \frac{2}{3} \cdot 5 + \frac{1}{3} \cdot 7 = \frac{17}{3}$, $d(v, d) = d(v, e) = \frac{1}{3} \cdot 7 + \frac{2}{3} \cdot 4 = 5$ and $d(u, v) = \frac{1}{3}(4 + 7 + 5) = \frac{16}{3}$.

**Rounds 3 and 4.** With three clusters, $Q$ is the same for every pair, so the choice is free, and $d$ and $e$ form a cluster. Then the clusters $\{u, v\}$ and $\{d, e\}$ join into a chain of four nodes, which line L6 reduces twice. Undoing all reductions gives the circle $a, b, c, d, e$.

**The fit.** The circle has $\binom{5}{2} = 10$ circular splits: the five single taxa and the five pairs $ab, bc, cd, de, ea$. The least squares weights are 1 for each single taxon, 3 for $ab \mid cde$, 2 for $bc \mid ade$, and 0 for the other three. They fit $d$ exactly, so NeighborNet returns the seven splits that built $d$. If $d(a, c)$ is raised from 7 to 8, no exact fit exists. The weights become $\frac{13}{4}$ for $ab \mid cde$ and $\frac{9}{4}$ for $bc \mid ade$, and two small splits, $cd \mid abe$ and $bcd \mid ae$, appear with weight $\frac{1}{8}$ each.

## Correctness

The order is a permutation of the taxa. Each cluster stays a block of consecutive nodes, and undoing a reduction replaces the block $u, v$ by $x, y, z$ in the same direction, so by backward induction over the steps each node appears once. The circular splits of an order form a basis: for the split with side $x_i, \ldots, x_j$,

$$2 \lambda_{ij} = D(x_{i-1}, x_j) + D(x_i, x_{j+1}) - D(x_i, x_j) - D(x_{i-1}, x_{j+1}),$$

so the weights of a circular metric can be read off from it, and the design matrix is invertible. Then $f$ is strictly convex, Lawson and Hanson's method stops at a point that satisfies the optimality conditions, and these conditions are enough for a convex problem. If $d$ is a circular metric for the order found, its weights give $f = 0$, and by uniqueness the method returns them. The full proof is in the proof file. The claim that lines L1 to L8 always find a suitable order for a circular metric is the consistency theorem of Bryant, Moulton and Spillner (2007), and the tests check it on random circular and tree metrics.

## Complexity

The agglomeration has $O(n)$ rounds. A cluster holds at most two nodes, so all cluster distances and sums $R$ cost $O(n^2)$ per round, and the choice of nodes and the reductions cost $O(n)$. The least squares part works with $N = \binom{n}{2}$ unknowns.

| part | cost |
|---|---|
| agglomeration, lines L1 to L7 | $O(n^3)$ |
| undoing the reductions, line L8 | $O(n^2)$ |
| the matrix $A^\top A$ | $O(N^3) = O(n^6)$ |
| one active set step, a dense solve | $O(n^6)$ |
| the least squares fit, $t$ steps | $O(t n^6)$ |

The active set method stops after finitely many steps, but no polynomial bound on $t$ is known for general inputs. In practice, $t$ is small compared with $N$. The space is $O(N^2) = O(n^4)$ for $A^\top A$. Fast implementations never build this matrix, as the next sections explain.

## Properties

- **Consistent for circular metrics.** If $d$ is a circular metric, NeighborNet returns an order for which $d$ is circular, and so it recovers the weighted splits exactly. Tree metrics are a special case, and then the result is the tree.
- **Planar output.** The result is a circular split system, so its splits graph can be drawn in the plane, unlike the output of [split decomposition](/split-decomposition/).
- **At most $\binom{n}{2}$ splits.** Every circular split system on $n$ taxa has at most this many splits.
- **Generalizes neighbor-joining.** The cluster choice of line L3 is the [neighbor-joining](/neighbor-joining/) criterion, applied to clusters with mean distances. On a tree metric, the result is the tree that neighbor-joining also finds.
- **Keeps more signal than split decomposition.** The weights come from a global fit, not from a minimum over quartets, so a few noisy quartets do not remove a split.
- **Not canonical.** Ties in lines L3 and L4 can change the order, so the result can depend on the tie rule and on the order of the input. Split decomposition has no such choice.

## Variants and improvements

- **Fast least squares.** Practical programs use the structure of circular splits. The product of the design matrix with a vector costs $O(n^2)$ with prefix sums, so an iterative method, such as conjugate gradients inside the active set loop, avoids the $O(n^6)$ dense solves and the $O(n^4)$ matrix.
- **Other reduction weights.** The values $\alpha, \beta, \gamma$ can be any nonnegative numbers with sum 1. The choice of $\frac{1}{3}$ each is the one in the original paper.
- **Neighbor-joining.** The special case that joins each pair into one node at once.
- **Split decomposition.** [Split decomposition](/split-decomposition/) gives weakly compatible splits with a canonical weight, but it loses most splits on large noisy data.
- **QNet.** A similar agglomeration builds a circular split system from weighted quartets instead of distances.

## When to use it

Use NeighborNet as the first look at a distance matrix when a tree may not fit, for example because of recombination, hybridization, horizontal gene transfer or borrowing between languages. It scales to hundreds or thousands of taxa, and the planar picture shows where the conflicts are. Use [split decomposition](/split-decomposition/) when you want a canonical result on a small and clean data set. Do not read the network as a history of events. Boxes show conflict in the data, not a hybrid ancestor. For explicit events, use a rooted [phylogenetic network](/phylogenetic-network/).

## Pitfalls

- **The wrong count in line L4.** The node criterion treats the nodes of $C_i$ and $C_j$ as separate clusters, so its factor is $\hat m - 2$ with $\hat m = m + |C_i| + |C_j| - 2$, and its sums run over these $\hat m$ parts. Using $m$ and the cluster sums of line L3 picks the wrong nodes.
- **Wrong orientation when undoing.** When line L8 puts $x, y, z$ back, it must keep the direction of the block $u, v$ in the circle. Writing $x, y, z$ the wrong way breaks the adjacency of $z$ with the next node.
- **Negative weights.** Plain least squares can give negative split weights. The nonnegativity constraint is part of the method.
- **Floating point zeros.** Many weights end very close to zero. With floating point arithmetic, a threshold decides which splits are kept, and it changes the picture.
- **Over-reading boxes.** Small boxes often come from noise. Bootstrap or a weight threshold helps to decide which splits to trust.

## Implementations

## History

Bryant and Moulton presented NeighborNet at the WABI workshop in 2002 and published the full method in Molecular Biology and Evolution in 2004. It answered a known weakness of [split decomposition](/split-decomposition/), whose results become nearly star-like on large data sets. Huson and Bryant made NeighborNet the main distance method of SplitsTree4 in 2006. In 2007, Bryant, Moulton and Spillner proved that the agglomeration is consistent, so that NeighborNet returns the right splits for every circular metric. The method is now common in studies of recombining genomes, of plant and bacterial evolution, and of language families.

## References
