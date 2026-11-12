---
tag: DXB6W7
kind: problem
slug: least-squares-phylogeny
name: Least-squares phylogeny
aliases:
- least squares tree
- least-squares tree fitting
area: biology/phylogenetics
level: advanced
summary: Find the tree and edge lengths whose path distances minimize the weighted sum of squared errors against a distance matrix. Linear for a fixed tree, NP-hard over all trees.
prereqs: [additive-tree-reconstruction, least-squares-problem, normal-equations]
see_also: [fitch-margoliash, minimum-evolution, neighbor-joining, bionj, ordinary-least-squares, tree-metric, nearest-neighbor-interchange, quadratic-programming]
sources:
  - paper: "L. L. Cavalli-Sforza and A. W. F. Edwards, Phylogenetic analysis: models and estimation procedures, American Journal of Human Genetics 19(3), 1967, pages 233 to 257"
    title: Cavalli-Sforza and Edwards 1967
    locator: the unweighted least squares fit of a tree to distances
  - paper: doi:10.1126/science.155.3760.279
    title: Walter M. Fitch and Emanuel Margoliash, Construction of phylogenetic trees, Science 155(3760), 1967, pages 279 to 284
    locator: the weighted least squares criterion with weights 1/D^2
  - paper: doi:10.1007/BF02458863
    title: William H. E. Day, Computational complexity of inferring phylogenies from dissimilarity matrices, Bulletin of Mathematical Biology 49(4), 1987, pages 461 to 467
    locator: NP-hardness of the least squares fit by a tree metric over all topologies
  - paper: "David Bryant and Peter Waddell, Rapid evaluation of least-squares and minimum-evolution criteria on phylogenetic trees, Molecular Biology and Evolution 15(10), 1998, pages 1346 to 1359"
    title: Bryant and Waddell 1998
    locator: the ordinary least squares lengths of a fixed tree in O(n^2) time
  - paper: "M. G. Bulmer, Use of the method of generalized least squares in reconstructing phylogenies from sequence data, Molecular Biology and Evolution 8(6), 1991, pages 868 to 883"
    title: Bulmer 1991
    locator: generalized least squares with the covariances of estimated distances
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, 2004
    locator: Chapter 11, Distance matrix methods, least squares methods, weights, and negative branch lengths
---

Least-squares phylogeny is the problem of finding a tree with edge lengths whose path distances between taxa minimize a weighted sum of squared differences from a given distance matrix. For a fixed topology the best lengths solve a linear system, the [normal equations](/normal-equations/), and they are unique. Over all topologies the problem is NP-hard (Day 1987), so programs such as [Fitch-Margoliash](/fitch-margoliash/) search heuristically. It is the $L_2$ version of [additive tree reconstruction](/additive-tree-reconstruction/).

## In plain words

You have a table of measured distances between species, and the measurements have errors. For a given tree shape, you choose a length for each branch so that the distances you can walk along the tree match the table as well as possible. "As well as possible" means the sum of the squared differences is as small as it can be, the same rule as fitting a straight line through points. For one tree shape this is a standard calculation with one exact answer. To find the best shape, you would have to try them all, and there are far too many, so programs try promising shapes and keep the best one they find.

## Definition

Let $X$ be a set of $n \ge 3$ taxa and $D$ a symmetric matrix of observed distances. Let $T$ be an unrooted binary tree with leaf set $X$ and $k = 2n - 3$ edges. List the $m = n(n-1)/2$ pairs of taxa and the $k$ edges, and let $A$ be the $m \times k$ path matrix: $A_{(x,y), e} = 1$ if the edge $e$ is on the path from $x$ to $y$, and 0 otherwise. For edge lengths $b \in \mathbb{R}^k$, the tree distances are $Ab$. With weights $w_{xy} > 0$ in the diagonal matrix $W$ and $d$ the vector of the entries $D_{xy}$, the score is
$$Q(T, b) = \sum_{x<y} w_{xy} \bigl(D_{xy} - (Ab)_{xy}\bigr)^2 = (d - Ab)^\top W (d - Ab).$$

**Fixed topology.** Find $\hat b = \arg\min_b Q(T, b)$. It is the unique solution of the normal equations
$$A^\top W A\, \hat b = A^\top W d.$$

**Full problem.** Find the topology $T$ that minimizes $Q(T) = Q(T, \hat b_T)$, often with the constraint $b \ge 0$.

**Why the solution is unique.** $A$ has full column rank. For a leaf $x$ on edge $e$, pick leaves $y, z$ in the two subtrees at the other end of $e$; then $b_e = \frac{1}{2}\bigl((Ab)_{xy} + (Ab)_{xz} - (Ab)_{yz}\bigr)$. For an internal edge $e$, pick leaves $a, a'$ from the two subtrees on one side and $c, c'$ from the two on the other; then $b_e = \frac{1}{2}\bigl((Ab)_{ac} + (Ab)_{a'c'} - (Ab)_{aa'} - (Ab)_{cc'}\bigr)$. So $Ab = 0$ forces $b = 0$, $A^\top W A$ is positive definite, and $\hat b$ is unique.

## Variants

- **Ordinary least squares (OLS).** All weights 1 (Cavalli-Sforza and Edwards 1967).
- **Weighted least squares (WLS).** Weights that decrease with the distance, because long distances have larger variance: $w = 1/D^2$ in [Fitch-Margoliash](/fitch-margoliash/), $w = 1/D$ in some programs.
- **Generalized least squares (GLS).** Replace $W$ by the inverse of the full covariance matrix of the estimated distances, since distances that share edges are correlated (Bulmer 1991). The solution is $\hat b = (A^\top V^{-1} A)^{-1} A^\top V^{-1} d$.
- **Nonnegative lengths.** Add $b \ge 0$. For a fixed topology this is a convex [quadratic program](/quadratic-programming/); an edge fitted at 0 merges the topologies that resolve it.
- **Fit as a selection rule.** [Minimum evolution](/minimum-evolution/) fits lengths by OLS on each topology but chooses the topology with the smallest total length instead of the smallest $Q$.

## Examples

**Four taxa in closed form.** For the quartet AB|CD with edges $a, b, e, c, d$ (e internal), the matrix $A^\top A$ has diagonal $(3, 3, 4, 3, 3)$, the entry 2 between $e$ and each pendant edge, and the entry 1 between any two pendant edges. Solving the OLS normal equations gives
$$\hat e = \tfrac{1}{4}(D_{AC} + D_{AD} + D_{BC} + D_{BD}) - \tfrac{1}{2}(D_{AB} + D_{CD}), \qquad \hat a = \tfrac{1}{2} D_{AB} + \tfrac{1}{4}(D_{AC} + D_{AD} - D_{BC} - D_{BD}),$$
and similar formulas for $b, c, d$, with $Q = \frac{1}{4}(D_{AC} + D_{BD} - D_{AD} - D_{BC})^2$. For $D_{AB} = 2$, $D_{AC} = D_{AD} = D_{BC} = 6$, $D_{BD} = 9$, $D_{CD} = 4$, the right side $A^\top d$ is $(14, 17, 27, 16, 19)$ and the solution is $(1/4, 7/4, 15/4, 5/4, 11/4)$. The fitted distances are exact on AB and CD and off by $3/4$ on the other four pairs, so $Q = 9/4$. The other two quartets score $9$ and $81/4$, with internal edges $-3$ and $-3/4$.

**Six taxa, where the best fit is not a tree.** Take

| | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| A | 0 | 14 | 15 | 17 | 15 | 7 |
| B | 14 | 0 | 8 | 9 | 9 | 14 |
| C | 15 | 8 | 0 | 12 | 14 | 12 |
| D | 17 | 9 | 12 | 0 | 7 | 16 |
| E | 15 | 9 | 14 | 7 | 0 | 11 |
| F | 7 | 14 | 12 | 16 | 11 | 0 |

and fit OLS lengths on all 105 topologies.

| rank by $Q$ | topology | $Q$ | negative edges |
|---|---|---|---|
| 1 | `((A,F),D,(B,(C,E)));` | 1139/72 | 2: $-37/36$ and $-35/12$ |
| 2 | `((A,F),B,(C,(D,E)));` | 1163/72 | 1 |
| 6 | `((A,F),C,(B,(D,E)));` | 1739/72 | 0 |
| 7 | `((A,F),(B,C),(D,E));` | 105/4 | 0 |

The tree with the smallest $Q$ needs two negative edges, which have no meaning as amounts of evolution. The best topology whose fitted lengths are all positive ranks sixth; it is also the [neighbor-joining](/neighbor-joining/) tree, with lengths A $9/2$, F $5/2$, C $31/6$, B $41/12$, D $33/8$, E $23/8$ and internal edges $29/6$, $47/36$ and $25/12$. The seventh tree is the [minimum evolution](/minimum-evolution/) tree, with total length $123/4$.

## Known algorithms

| task | method | time |
|---|---|---|
| OLS lengths on a fixed tree | form $A^\top A$ from subtree sizes, then [Gaussian elimination](/gaussian-elimination/) or [Cholesky](/cholesky-decomposition/) | $O(n^3)$ |
| OLS lengths on a fixed tree | recursive formulas over the tree (Bryant and Waddell 1998) | $O(n^2)$ |
| WLS lengths on a fixed tree | the weighted normal equations | $O(n^3)$ after forming them |
| nonnegative lengths | [quadratic programming](/quadratic-programming/), or set negative edges to 0 and refit | polynomial |
| topology search | [Fitch-Margoliash](/fitch-margoliash/): [stepwise addition](/stepwise-addition/) and [nearest neighbor interchange](/nearest-neighbor-interchange/), refitting each candidate | heuristic |
| starting tree | [neighbor-joining](/neighbor-joining/) or [BIONJ](/bionj/) | $O(n^3)$ |

## Bounds

- **Full problem:** NP-hard over all topologies (Day 1987).
- **Fixed topology:** $O(n^2)$ time for OLS, which is linear in the input.
- **Exact data:** if $D$ is the [tree metric](/tree-metric/) of a binary tree with positive edge lengths, that tree is the only topology with $Q = 0$, so the least squares tree is correct.
- **Search space:** $(2n-5)!!$ topologies, 105 for $n = 6$ and 2,027,025 for $n = 10$.

## Reductions

- **Fixed topology to linear algebra.** The fit is a [least squares problem](/least-squares-problem/) in $2n - 3$ unknowns; see [ordinary least squares](/ordinary-least-squares/).
- **Nonnegative fit to quadratic programming.** With $b \ge 0$, the fit is a convex quadratic program with simple bounds.
- **Day's reduction.** Day (1987) reduces an NP-complete problem to deciding whether a tree metric lies within a given $L_2$ distance of $D$.
- **To minimum evolution.** OLS lengths define the tree length used by minimum evolution; for each topology the total OLS length is a linear function of $D$.

## Applications

- **Distance-based phylogenetics.** Least squares is the classical optimality criterion for distance trees, used in programs such as PHYLIP FITCH and KITSCH (the clock version).
- **Branch lengths for a given tree.** Trees built by any method get edge lengths and a fit score by OLS or WLS.
- **Pitfall: negative lengths.** Unconstrained least squares can prefer a tree with negative edges. In the quartet, the score of AB|CD is $\frac{1}{4}(S_2 - S_3)^2$, where $S_2$ and $S_3$ are the other two pair sums, and it does not depend on $S_1 = D_{AB} + D_{CD}$. If $S_1$ is the largest sum and $S_2 = S_3$, then AB|CD scores 0 with the negative internal edge $\frac{1}{4}(S_2 + S_3) - \frac{1}{2} S_1$. Check the signs, or constrain $b \ge 0$.
- **Pitfall: weights.** OLS, WLS and GLS can choose different trees from the same matrix; the weights should match the variance of the distance estimates.

## References
