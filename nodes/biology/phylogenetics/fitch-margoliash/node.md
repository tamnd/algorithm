---
tag: 94EV9J
kind: algorithm
slug: fitch-margoliash
name: Fitch-Margoliash method
area: biology/phylogenetics
level: advanced
summary: Distance method that scores a tree by weighted least squares with weights 1/D^2. It solves the normal equations for each topology and searches topologies by addition and NNI.
solves: [least-squares-phylogeny]
model: word-ram
complexity:
  vars: {n: the number of taxa}
  time: {fit: "O(n^4)", addition: "O(n^6)", step: "O(n^5)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1967
  people: [Walter M. Fitch, Emanuel Margoliash]
  note: Fitch and Margoliash built a tree of cytochrome c sequences by minimizing squared deviations relative to the distances. Cavalli-Sforza and Edwards proposed unweighted least squares in the same year.
prereqs: [least-squares-phylogeny, normal-equations]
see_also: [ordinary-least-squares, minimum-evolution, neighbor-joining, bionj, stepwise-addition, nearest-neighbor-interchange, tree-metric]
sources:
  - paper: doi:10.1126/science.155.3760.279
    title: Walter M. Fitch and Emanuel Margoliash, Construction of phylogenetic trees, Science 155(3760), 1967, pages 279 to 284
    locator: the fit of branch lengths and the comparison of topologies by the percent standard deviation, which weights each squared deviation by 1/D^2
  - paper: "L. L. Cavalli-Sforza and A. W. F. Edwards, Phylogenetic analysis: models and estimation procedures, American Journal of Human Genetics 19(3), 1967, pages 233 to 257"
    title: Cavalli-Sforza and Edwards 1967
    locator: the unweighted least squares fit of a tree to distances
  - paper: doi:10.1007/BF02458863
    title: William H. E. Day, Computational complexity of inferring phylogenies from dissimilarity matrices, Bulletin of Mathematical Biology 49(4), 1987, pages 461 to 467
    locator: NP-hardness of fitting a tree to distances under least squares criteria
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, 2004
    locator: Chapter 11, Distance matrix methods, the sections on least squares, weights and the Fitch-Margoliash method
---

The Fitch-Margoliash method builds an unrooted [phylogenetic tree](/phylogenetic-tree/) from a distance matrix by [weighted least squares](/least-squares-phylogeny/): a tree with edge lengths gets the score $Q = \sum_{i<j} (D_{ij} - d_{ij})^2 / D_{ij}^2$, where $d_{ij}$ is its path length between taxa $i$ and $j$. For a fixed topology the best edge lengths are the solution of a linear system, the [normal equations](/normal-equations/). The topology is chosen by a search, here [stepwise addition](/stepwise-addition/) and [nearest-neighbor interchange](/nearest-neighbor-interchange/), so the method is a heuristic over the $(2n-5)!!$ binary topologies. On an exact [tree metric](/tree-metric/) it returns the true tree.

## In plain words

A distance method compares two things: the distances you measured between species, and the distances that a tree with branch lengths predicts. The Fitch-Margoliash method asks for the tree that makes the differences as small as possible. It does not count all differences the same. A large distance is measured with more error, so the method divides each difference by the measured distance before it squares it. Then an error of one unit on a short distance costs much more than the same error on a long distance. For one tree shape, the best branch lengths come from a set of linear equations. To choose the shape, the method adds species one at a time in the best place, and then tries small swaps of branches while they make the fit better.

## The problem

The input is $n \ge 3$ taxa and a symmetric matrix $D$ with zero diagonal and $D_{ij} > 0$ for $i \ne j$, for example evolutionary distances computed from sequences with a [substitution model](/substitution-model/). The model is an unrooted binary tree on the taxa with real edge lengths; the tree predicts $d_{ij} = \sum_{e \in P_{ij}} b_e$, where $P_{ij}$ is the set of edges on the path. The goal is the tree and lengths that minimize the weighted sum of squares
$$Q = \sum_{i<j} w_{ij} \big(D_{ij} - d_{ij}\big)^2, \qquad w_{ij} = D_{ij}^{-p},$$
with $p = 2$ for Fitch and Margoliash and $p = 0$ for ordinary least squares. This is the [least squares phylogeny](/least-squares-phylogeny/) problem with these weights. Lengths here may have any sign; a variant forces them to be at least 0.

## The algorithm

For a topology $T$ with edge set $E$, let $A$ be the matrix with a row for each pair $i < j$, a column for each edge, and $A_{(ij), e} = 1$ when $e \in P_{ij}$. Let $W$ be the diagonal matrix of the weights and $\mathbf{d}$ the vector of the $D_{ij}$. FIT$(T)$ solves
$$(A^\top W A)\, b = A^\top W \mathbf{d}$$
and returns $b$ and $Q(T) = \sum_{i<j} w_{ij} (D_{ij} - (Ab)_{ij})^2$.

```pseudo id=main
FITCH-MARGOLIASH(D, n, p)          ▷ w_ij = 1 / D_ij^p, p = 2
L1  T ← the star on taxa 1, 2, 3
L2  for x ← 4 to n do
L3      for each edge e of T do T_e ← T with a new node on e and the leaf x attached to it
L4          (b_e, Q_e) ← FIT(T_e)
L5      T ← the T_e with the smallest Q_e
L6  repeat
L7      for each NNI neighbor T' of T do (b', Q') ← FIT(T')
L8      if the smallest Q' is less than Q(T) then T ← the T' with that Q'
L9  until no neighbor has a smaller score
L10 return T, its lengths b and its score Q(T)
```

A nearest-neighbor interchange picks an internal edge $\{u, v\}$, one subtree at $u$ and one subtree at $v$, and swaps them; each internal edge gives two neighbors, so a binary tree has $2(n - 3)$ of them.

## Example

Four taxa A, B, C, D have this matrix. It is not a tree metric: the pair sums are $D_{AB} + D_{CD} = 6$, $D_{AC} + D_{BD} = 15$ and $D_{AD} + D_{BC} = 12$, and the two largest are not equal.

| | A | B | C | D |
|---|---|---|---|---|
| A | 0 | 2 | 6 | 6 |
| B | 2 | 0 | 6 | 9 |
| C | 6 | 6 | 0 | 4 |
| D | 6 | 9 | 4 | 0 |

Line L1 makes the star on A, B, C. Line L3 attaches D to each of its three edges, which gives the three quartet topologies. Their exact scores are $Q = 1/21 \approx 0.048$ for AB|CD, $9/23 \approx 0.391$ for AC|BD and $81/137 \approx 0.591$ for AD|BC, so line L5 keeps AB|CD. Its two NNI neighbors are the other two topologies, which score worse, so the search stops.

For AB|CD with internal edge $e$, the normal equations give the lengths $A = 3/7$, $B = 11/7$, $e = 25/7$, $C = 10/7$ and $D = 18/7$. With ordinary least squares ($p = 0$) the same topology gets $A = 1/4$, $B = 7/4$, $e = 15/4$, $C = 5/4$ and $D = 11/4$. The fitted distances show the effect of the weights:

| pair | $D_{ij}$ | weight | Fitch-Margoliash fit | ordinary fit |
|---|---|---|---|---|
| AB | 2 | 1/4 | 2 | 2 |
| AC | 6 | 1/36 | 38/7 | 21/4 |
| AD | 6 | 1/36 | 46/7 | 27/4 |
| BC | 6 | 1/36 | 46/7 | 27/4 |
| BD | 9 | 1/81 | 54/7 | 33/4 |
| CD | 4 | 1/16 | 4 | 4 |

Ordinary least squares spreads the misfit evenly, with residuals of $\pm 3/4$ on the four long pairs and $Q = 9/4$ in its own units. The weighted fit puts the largest residual, $9/7$, on BD, the longest distance, and residuals of $\pm 4/7$ on the three pairs of length 6. Its score is $3 \cdot (4/7)^2 / 36 + (9/7)^2 / 81 = 1/21$.

## Correctness

**Theorem.** (a) For each topology, FIT returns the unique weighted least squares lengths and score. (b) If $D$ is the leaf metric of a binary tree with positive edge lengths, the method returns that tree with its lengths and $Q = 0$.

For (a), the matrix $A$ has full column rank for every binary topology: the length of a pendant edge is $(d_{ij} + d_{ik} - d_{jk})/2$ and the length of an internal edge is $(d_{ik} + d_{jl} - d_{ij} - d_{kl})/2$ for suitable leaves. With positive weights, $A^\top W A$ is then positive definite, and the expansion $Q(\hat b + h) = Q(\hat b) + h^\top A^\top W A\, h$ shows that the solution of the normal equations is the unique minimizer. For (b), the key fact is that on a tree metric only the true topology has an exact fit, even with lengths of any sign: any binary topology gives equal crossing pair sums on each of its quartets, and the true tree makes the sum of its own quartet split strictly the smallest. So at each step of line L5 the right attachment is the only candidate with score 0, and the NNI phase finds nothing better. The full proof is in the proof file.

The search is a heuristic on other data. It returns a topology with no better NNI neighbor, which need not be the best topology. On random $6 \times 6$ matrices it misses the best of the 105 topologies in some cases.

## Complexity

The model is the word RAM with unit-cost arithmetic. Building the normal equations takes $O(\sum_{i<j} |P_{ij}|^2)$ time, which is $O(n^4)$ for a caterpillar and $O(n^2 \log^2 n)$ for a balanced tree, and dense elimination of the $(2n-3) \times (2n-3)$ system takes $O(n^3)$. So one FIT costs $O(n^4)$ in the worst case. The addition phase calls FIT $\sum_{x=4}^{n} (2x - 5) = O(n^2)$ times, $O(n^6)$ in total. Each NNI pass calls FIT $2(n - 3)$ times, $O(n^5)$; the number of passes has no polynomial bound in general, only the number of topologies. The space is $O(n^2)$ for the system. Faster programs compute least squares lengths for a fixed topology without forming the system, and reuse the work between neighboring topologies.

## Properties

- **Exact on tree metrics.** It returns the true tree and lengths.
- **Relative errors.** With $p = 2$ a residual counts by its size relative to the distance, which matches data whose standard deviation grows in proportion to the distance.
- **Linear fit.** For a fixed topology the lengths are linear in the data, and the score is a quadratic form.
- **Lengths can be negative.** The unconstrained fit can give an edge a negative length when the data do not fit the topology well.
- **Heuristic search.** The result is a local optimum under NNI. Finding the best topology for least squares is NP-hard (Day 1987).
- **Order dependent.** The addition phase depends on the order of the taxa, and ties on line L5 or L8 depend on the scan order.

## Variants and improvements

- **Ordinary least squares,** $p = 0$, as proposed by Cavalli-Sforza and Edwards (1967); see [ordinary least squares](/ordinary-least-squares/). It is the fit behind the score of [minimum evolution](/minimum-evolution/).
- **Other powers.** Programs let the user set $p$; $p = 1$ matches errors whose variance grows in proportion to the distance.
- **Non-negative lengths.** The fit can be constrained to $b \ge 0$, which turns it into a quadratic program; edges that would be negative get length 0.
- **Generalized least squares** uses the full covariance matrix of the distances instead of a diagonal weight matrix.
- **Wider search.** Subtree prune and regraft, several addition orders, or random restarts find better local optima at higher cost.
- **[Neighbor-joining](/neighbor-joining/) and [BIONJ](/bionj/)** give a tree in $O(n^3)$ time without a search; they are common starting trees for a least squares search.

## When to use it

Use it when you have a moderate number of taxa, a distance matrix, and a reason to fit relative errors, for example distances whose error grows with their size. The fitted lengths and the score are a useful check of how well any given tree fits the data. For large data sets, or as a first tree, use [neighbor-joining](/neighbor-joining/) or [BIONJ](/bionj/), which are much faster. When sequence data are available, likelihood methods use more of the information than any fit to distances.

## Pitfalls

- **Zero distances.** With $p = 2$ a pair at distance 0 gets an infinite weight; identical sequences must be merged first or given a small positive distance.
- **Comparing scores across weights.** The score with $p = 2$ and the score with $p = 0$ are in different units, as in the example; compare topologies only under one weighting.
- **Reading negative lengths as data.** A negative length shows misfit, not a reverse branch. Report it, or use the constrained fit.
- **Trusting one search.** A single addition order and NNI can miss the best topology. Try several orders, or a wider rearrangement.
- **Floating point and ties.** On data with symmetries, scores of different topologies can be equal; exact or careful arithmetic is needed to break ties in a stated way.

## Implementations

## History

Fitch and Margoliash (1967) built a tree for cytochrome c from 20 species. They fitted branch lengths to the distances, compared topologies by a percent standard deviation, which squares each deviation relative to the distance, and tried alternative topologies by hand. In the same year Cavalli-Sforza and Edwards (1967) proposed the unweighted least squares fit. Felsenstein's PHYLIP package made the method standard as the program FITCH, which searches topologies by addition and rearrangements. Day (1987) showed that finding the best least squares tree is NP-hard.

## References
