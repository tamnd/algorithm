---
tag: 0GG3SN
kind: problem
slug: minimum-evolution
name: Minimum evolution
aliases:
- balanced minimum evolution
- minimum evolution principle
area: biology/phylogenetics
level: advanced
summary: Find the tree topology whose total edge length, with lengths estimated from the distance matrix, is smallest. The balanced version is NP-hard; neighbor-joining is its greedy algorithm.
prereqs: [least-squares-phylogeny, tree-metric]
see_also: [neighbor-joining, bionj, fitch-margoliash, nearest-neighbor-interchange, subtree-prune-and-regraft, stepwise-addition, four-point-method, additive-tree-reconstruction]
sources:
  - paper: "Andrey Rzhetsky and Masatoshi Nei, A simple method for estimating and testing minimum-evolution trees, Molecular Biology and Evolution 9(5), 1992, pages 945 to 967"
    title: Rzhetsky and Nei 1992
    locator: the minimum evolution criterion with ordinary least squares edge lengths and a test of the interior edges
  - paper: "Andrey Rzhetsky and Masatoshi Nei, Theoretical foundation of the minimum-evolution method of phylogenetic inference, Molecular Biology and Evolution 10(5), 1993, pages 1073 to 1095"
    title: Rzhetsky and Nei 1993
    locator: the statistical consistency of ordinary least squares minimum evolution
  - paper: "Yves Pauplin, Direct calculation of a tree length using a distance matrix, Journal of Molecular Evolution 51(1), 2000, pages 41 to 47"
    title: Pauplin 2000
    locator: the balanced tree length formula with weights 2 to the power 1 minus the path size
  - paper: "Richard Desper and Olivier Gascuel, Fast and accurate phylogeny reconstruction algorithms based on the minimum-evolution principle, Journal of Computational Biology 9(5), 2002, pages 687 to 705"
    title: Desper and Gascuel 2002
    locator: the balanced minimum evolution criterion, greedy addition and NNI under it, and the FastME program
  - paper: "Richard Desper and Olivier Gascuel, Theoretical foundation of the balanced minimum evolution method of phylogenetic inference and its relationship to weighted least-squares tree fitting, Molecular Biology and Evolution 21(3), 2004, pages 587 to 598"
    title: Desper and Gascuel 2004
    locator: the statistical consistency of balanced minimum evolution
  - paper: "Olivier Gascuel and Mike Steel, Neighbor-joining revealed, Molecular Biology and Evolution 23(11), 2006, pages 1997 to 2000"
    title: Gascuel and Steel 2006
    locator: neighbor-joining as a greedy algorithm for balanced minimum evolution
  - paper: "Samuel Fiorini and Gwenaël Joret, Approximating the balanced minimum evolution problem, Operations Research Letters 40(1), 2012, pages 31 to 35"
    title: Fiorini and Joret 2012
    locator: NP-hardness and inapproximability of balanced minimum evolution
  - paper: "K. K. Kidd and L. A. Sgaramella-Zonta, Phylogenetic analysis: concepts and methods, American Journal of Human Genetics 23(3), 1971, pages 235 to 252"
    title: Kidd and Sgaramella-Zonta 1971
    locator: the early proposal of choosing the tree of smallest total length fitted to distances
---

Minimum evolution is the problem of choosing, from a matrix of distances between $n$ taxa, the unrooted tree topology whose total edge length is smallest when the edge lengths are estimated from the matrix. With ordinary least squares lengths it is the criterion of Rzhetsky and Nei (1992); with the balanced lengths of Pauplin (2000) it is balanced minimum evolution (BME), the criterion of the FastME program (Desper and Gascuel 2002). BME is NP-hard (Fiorini and Joret 2012), and [neighbor-joining](/neighbor-joining/) is a greedy algorithm for it (Gascuel and Steel 2006).

## In plain words

For each possible tree shape, you fit lengths to its branches from the measured distances and add them up. That sum is how much evolution the tree claims happened. The minimum evolution rule picks the shape that needs the least total evolution. If the distances come exactly from a tree, that tree wins. There are two common ways to fit the lengths, and they can pick different shapes. Trying every shape is impossible for many species, so programs grow a tree step by step and then improve it by small rearrangements; the popular neighbor-joining method is exactly such a greedy procedure.

## Definition

Let $D$ be a symmetric distance matrix on a set $X$ of $n \ge 3$ taxa. For an unrooted binary tree $T$ with leaf set $X$:

**OLS tree length.** Let $\hat b(T)$ be the ordinary least squares edge lengths of $T$, the solution of $A^\top A\, b = A^\top d$ for the path matrix $A$ of $T$ (see [least-squares phylogeny](/least-squares-phylogeny/)). The length is
$$L_{\text{OLS}}(T) = \sum_{e} \hat b_e(T) = \mathbf{1}^\top (A^\top A)^{-1} A^\top d.$$

**Balanced tree length.** Let $\tau_{xy}$ be the number of edges on the path from $x$ to $y$ in $T$. Pauplin's formula is
$$L_{\text{BME}}(T) = \sum_{x<y} 2^{1 - \tau_{xy}}\, D_{xy}.$$
It is the sum of the balanced edge lengths, which weight the subtrees at each vertex equally instead of by their numbers of taxa.

**Problem.** Find $T$ minimizing $L_{\text{OLS}}(T)$ (OLS minimum evolution) or $L_{\text{BME}}(T)$ (balanced minimum evolution). Both lengths are linear in $D$ for a fixed $T$, and if $D$ is the [tree metric](/tree-metric/) of a binary tree $T_0$ with positive edge lengths, both equal the true total length on $T_0$.

**Identity on tree metrics.** For BME this can be checked from the weights: for every edge $e$ of $T_0$, $\sum_{x<y,\ e \in P_{xy}} 2^{1 - \tau_{xy}} = 1$, so the formula counts each edge length once.

## Variants

- **OLS minimum evolution** (Rzhetsky and Nei 1992): consistent when the distances converge to a tree metric (Rzhetsky and Nei 1993).
- **Balanced minimum evolution** (Desper and Gascuel 2002): also consistent (Desper and Gascuel 2004), and it is the criterion behind neighbor-joining.
- **Weighted versions:** lengths from weighted least squares instead of OLS.
- **Nonnegative lengths:** reject topologies whose fitted lengths are negative, or refit them with $b \ge 0$.
- **Interior edge tests:** Rzhetsky and Nei test whether each interior OLS length is significantly greater than 0.

## Examples

**Four taxa.** On the quartet AB|CD, the OLS lengths give $\hat a + \hat b = D_{AB}$ and $\hat c + \hat d = D_{CD}$, so
$$L_{\text{OLS}}(AB|CD) = \tfrac{1}{2}(D_{AB} + D_{CD}) + \tfrac{1}{4}(D_{AC} + D_{AD} + D_{BC} + D_{BD}),$$
which is also Pauplin's sum, since $\tau = 2$ for AB and CD and $\tau = 3$ for the other pairs. With $S_1 = D_{AB} + D_{CD}$ and $S$ the sum of all six entries, this is $\frac{1}{4}(S_1 + S)$, so minimum evolution picks the split with the smallest pair sum, the same rule as the [four-point method](/four-point-method/). For $D_{AB} = 2$, $D_{AC} = D_{AD} = D_{BC} = 6$, $D_{BD} = 9$ and $D_{CD} = 4$ the three lengths are $39/4$, $12$ and $45/4$.

**OLS and BME agree for $n \le 5$.** For every topology on 4 or 5 taxa, $L_{\text{OLS}}$ and $L_{\text{BME}}$ are the same linear function of $D$. For 6 taxa they agree only on the 15 topologies with three cherries, out of 105.

**Six taxa, where the two criteria differ.** Take

| | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| A | 0 | 14 | 15 | 17 | 15 | 7 |
| B | 14 | 0 | 8 | 9 | 9 | 14 |
| C | 15 | 8 | 0 | 12 | 14 | 12 |
| D | 17 | 9 | 12 | 0 | 7 | 16 |
| E | 15 | 9 | 14 | 7 | 0 | 11 |
| F | 7 | 14 | 12 | 16 | 11 | 0 |

| topology | $L_{\text{OLS}}$ | $L_{\text{BME}}$ |
|---|---|---|
| `((A,F),(B,C),(D,E));` | $123/4 = 30.75$ | $123/4 = 30.75$ |
| `((A,F),C,(B,(D,E)));` | $1109/36 \approx 30.806$ | $491/16 = 30.6875$ |

OLS minimum evolution picks the first tree, the one with three cherries, where both lengths are equal. BME picks the second, by $1/16$; it is also the tree that [neighbor-joining](/neighbor-joining/) returns. Its OLS lengths are A $9/2$, F $5/2$, C $31/6$, B $41/12$, D $33/8$, E $23/8$ and the internal edges $29/6$, $47/36$ and $25/12$, which add to $1109/36$. The next BME lengths are $503/16$ and $509/16$.

## Known algorithms

| algorithm | criterion | time | notes |
|---|---|---|---|
| exhaustive search | either | $(2n-5)!!$ trees, $O(n^2)$ each | only for small $n$ |
| [Neighbor-joining](/neighbor-joining/) | BME, greedy | $O(n^3)$ | each step joins the pair that most decreases the BME length of the partial tree (Gascuel and Steel 2006) |
| [BIONJ](/bionj/) | BME-like, greedy | $O(n^3)$ | NJ with variance-based reduction |
| greedy addition (FastME) | OLS or BME | heuristic | inserts taxa one at a time at the best edge (Desper and Gascuel 2002) |
| NNI and SPR search (FastME) | OLS or BME | heuristic | [nearest neighbor interchange](/nearest-neighbor-interchange/) and [subtree prune and regraft](/subtree-prune-and-regraft/) moves with fast updates of all lengths |
| [stepwise addition](/stepwise-addition/) with refits | OLS | heuristic | general framework |

## Bounds

- **BME:** NP-hard, and hard to approximate (Fiorini and Joret 2012).
- **Fixed topology:** $L_{\text{BME}}$ takes $O(n^2)$ time by Pauplin's formula after computing all $\tau_{xy}$ by a traversal from each leaf; $L_{\text{OLS}}$ also takes $O(n^2)$ time.
- **Exact data:** on a tree metric of a binary tree with positive edges, the true tree is the unique optimum for both criteria, and neighbor-joining finds it.
- **Search space:** $(2n-5)!!$ topologies.

## Reductions

- **Neighbor-joining as greedy BME.** At a step with $r$ active nodes, let $R_i = \sum_k D_{ik}$ and $S = \sum_{k<l} D_{kl}$. The tree in which $i$ and $j$ form a cherry and all other nodes hang from one central vertex has the length $S_{ij} = \bigl(Q(i, j) + 2S\bigr) / \bigl(2(r - 2)\bigr)$ of Saitou and Nei, with $Q(i, j) = (r - 2) D_{ij} - R_i - R_j$. Gascuel and Steel (2006) show that $S_{ij}$ is the balanced length of this partly resolved tree, so the NJ choice of the smallest $Q$ is the greedy BME choice.
- **From least squares.** $L_{\text{OLS}}$ uses the [least-squares](/least-squares-phylogeny/) lengths of each topology; only the selection rule differs.
- **Quartets.** On four taxa minimum evolution is the four-point rule, so both criteria agree with quartet methods there.

## Applications

- **Distance-based phylogenetics at scale.** FastME and neighbor-joining build trees of thousands of taxa in seconds to minutes, as starting trees for likelihood searches or as final trees.
- **Theory of neighbor-joining.** The BME view explains why NJ is exact on tree metrics and why it works well on noisy data.
- **Pitfall: two criteria.** OLS and BME minimum evolution can pick different trees from the same matrix, as in the example above; state which one is used.
- **Pitfall: negative lengths.** The fitted lengths of the optimal topology may include negative values, which add negatively to the total; programs often set them to 0 after the search.

## References
