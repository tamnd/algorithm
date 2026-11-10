---
tag: 4ZVTP9
kind: problem
slug: bin-packing
name: Bin packing problem
aliases:
- bin packing
- one-dimensional bin packing
area: approximation/covering-and-packing
level: intro
summary: Pack items of given sizes into the fewest unit-capacity bins.
prereqs: [np-hard, approximation-ratio]
see_also: [bin-packing-lower-bound, bin-packing-np-hardness, first-fit-bin-packing, first-fit-decreasing, bin-packing-aptas, karmarkar-karp-bin-packing, cutting-stock-problem, bin-covering]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Appendix A4.1, problem SR1 (Bin packing)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 3.3 (bin packing, the asymptotic scheme) and Chapter 4 (the Karmarkar and Karp algorithm)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 9 (Bin packing)
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems
    locator: Chapter 2, E. G. Coffman, M. R. Garey and D. S. Johnson, Approximation algorithms for bin packing, a survey
  - paper: "D. S. Johnson, A. Demers, J. D. Ullman, M. R. Garey and R. L. Graham, Worst-case performance bounds for simple one-dimensional packing algorithms, SIAM Journal on Computing 3, 1974"
    title: Johnson, Demers, Ullman, Garey and Graham 1974
    locator: the bounds for next fit, first fit, best fit and first fit decreasing
---

The bin packing problem asks for a partition of a list of items, each with a size in $(0, 1]$, into the fewest groups (bins) whose sizes sum to at most 1. It is [NP-hard](/np-hard/), and in the strong sense, so no exact polynomial-time algorithm is expected. It is also the standard example of a problem where the absolute [approximation ratio](/approximation-ratio/) and the asymptotic ratio differ: no polynomial algorithm can promise fewer than $\frac{3}{2}\,\mathrm{OPT}$ bins on all inputs unless P = NP, but there are algorithms that use $\mathrm{OPT} + O(\log \mathrm{OPT})$ bins. The simple greedy rules ([next fit](/next-fit-bin-packing/), [first fit](/first-fit-bin-packing/), [best fit](/best-fit-bin-packing/), [first fit decreasing](/first-fit-decreasing/)) were among the first approximation algorithms that were analysed.

## In plain words

You have boxes that all have the same size, and a pile of objects of different sizes. You want to put all the objects into boxes and use as few boxes as you can. Each box can hold any set of objects whose sizes add up to at most the size of the box. Shapes do not matter here, only sizes.

The question sounds easy, but no fast method is known that always finds the best answer. So people use fast rules that are close to the best. A typical rule takes the objects one by one and puts each one into the first box where it still fits. Such rules never use much more than one and a half to two times the best number of boxes, and some rules are much closer than that.

## Definition

The input is a list of $n$ item sizes $s_1, \ldots, s_n$ with $0 < s_i \le 1$. The bins have capacity 1. A packing with $k$ bins is a map $\beta : \{1, \ldots, n\} \to \{1, \ldots, k\}$ such that

$$\sum_{i \,:\, \beta(i) = j} s_i \le 1 \qquad \text{for each bin } j = 1, \ldots, k.$$

The sum on the left is the *load* of bin $j$. The goal is a packing with the least $k$. This least value is $\mathrm{OPT}$, or $\mathrm{OPT}(L)$ for the list $L$. We write $S = \sum_i s_i$ for the total size and $\mathrm{ALG}$ for the number of bins that an algorithm uses.

Ratio conventions on this page and on the other bin packing pages: bin packing is a minimization problem. An algorithm has *absolute ratio* $\rho$ if $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ for each input. It has *asymptotic ratio* $\rho$ if $\mathrm{ALG} \le \rho \cdot \mathrm{OPT} + c$ for a constant $c$ that does not depend on the input. All bounds below are worst-case bounds over all inputs, not average-case bounds.

The *decision version* asks, for a list and an integer $k$, whether a packing with $k$ bins exists. With integer data, the input is a capacity $C$ and integer sizes $1 \le a_i \le C$, and $s_i = a_i / C$.

## Variants

- **Online bin packing.** The items arrive one at a time, and each item must go into a bin before the next one is seen. [Next fit](/next-fit-bin-packing/), [first fit](/first-fit-bin-packing/) and [best fit](/best-fit-bin-packing/) are [online algorithms](/online-algorithm/). Yao (1980) proved that no online algorithm has an asymptotic ratio below $3/2$, and later work raised this lower bound.
- **Offline bin packing.** The whole list is known in advance. The algorithm may sort it, as [first fit decreasing](/first-fit-decreasing/) does, or solve an LP, as [Karmarkar and Karp](/karmarkar-karp-bin-packing/) do.
- **High multiplicity bin packing, or cutting stock.** There are $d$ distinct sizes with demands $n_1, \ldots, n_d$, given in binary. This is the [cutting stock problem](/cutting-stock-problem/).
- **Bin covering.** Each bin must be filled to *at least* 1, and the goal is the largest number of bins. See [bin covering](/bin-covering/).
- **Geometric variants.** Rectangles go into unit squares ([rectangle packing](/rectangle-packing/)) or into a strip of width 1 and least height ([strip packing](/strip-packing/)).
- **Other variants.** Vector bin packing has a size vector for each item and a capacity in each coordinate. Cardinality constrained bin packing allows at most $k$ items in a bin. Bin packing with conflicts forbids some pairs of items in the same bin. Variable sized bin packing has bins of several capacities and costs.

## Examples

Take the list $L = (0.2, 0.5, 0.4, 0.7, 0.1, 0.3, 0.8)$. The total size is $S = 3$, so each packing needs at least 3 bins. Three bins are enough: $\{0.8, 0.2\}$, $\{0.7, 0.3\}$ and $\{0.5, 0.4, 0.1\}$ each have load exactly 1. So $\mathrm{OPT} = 3$. The greedy rules on this list give:

| algorithm | bins | count |
|---|---|---|
| next fit | [0.2 0.5] [0.4] [0.7 0.1] [0.3] [0.8] | 5 |
| first fit | [0.2 0.5 0.1] [0.4 0.3] [0.7] [0.8] | 4 |
| best fit | [0.2 0.5 0.1] [0.4] [0.7 0.3] [0.8] | 4 |
| first fit decreasing | [0.8 0.2] [0.7 0.3] [0.5 0.4 0.1] | 3 |

The total size can be far below $\mathrm{OPT}$. Take $2m$ items of size $0.6$. Then $S = 1.2m$, but no two items fit in one bin, so $\mathrm{OPT} = 2m$. The page on [lower bounds](/bin-packing-lower-bound/) gives bounds that handle such cases.

A yes-instance of [partition](/partition-problem/) gives an instance with $\mathrm{OPT} = 2$. The list $(4, 3, 3, 2, 2, 2)$ with capacity 8 splits as $\{4, 2, 2\}$ and $\{3, 3, 2\}$, so $\mathrm{OPT} = 2$, and first fit decreasing uses 3 bins: $[4\ 3]$, $[3\ 2\ 2]$, $[2]$.

## Known algorithms

The ratios are worst case. "Absolute" means $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ for each input.

| algorithm | guarantee | type | time |
|---|---|---|---|
| [next fit](/next-fit-bin-packing/) | $2\,\mathrm{OPT} - 1$ | absolute, tight | $O(n)$ |
| [first fit](/first-fit-bin-packing/) | $\lfloor 1.7\,\mathrm{OPT} \rfloor$ | absolute, tight (Dósa and Sgall 2013) | $O(n \log n)$ |
| [best fit](/best-fit-bin-packing/) | $\lfloor 1.7\,\mathrm{OPT} \rfloor$ | absolute, tight (Dósa and Sgall 2014) | $O(n \log n)$ |
| [first fit decreasing](/first-fit-decreasing/) | $\frac{11}{9}\mathrm{OPT} + \frac{6}{9}$, and $\frac{3}{2}\mathrm{OPT}$ | both tight (Dósa 2007) | $O(n \log n)$ |
| [asymptotic scheme](/bin-packing-aptas/) | $(1 + \varepsilon)\mathrm{OPT} + 1$ | asymptotic, each fixed $\varepsilon > 0$ | $n^{O(1/\varepsilon^2)}$ in the simple form |
| [Fernandez de la Vega and Lueker](/fernandez-de-la-vega-lueker-aptas/) | $(1 + \varepsilon)\mathrm{OPT} + 1$ | asymptotic (1981) | linear in $n$ for fixed $\varepsilon$ |
| [Karmarkar and Karp](/karmarkar-karp-bin-packing/) | $\mathrm{OPT} + O(\log^2 \mathrm{OPT})$ | additive (1982) | polynomial |

An [EPTAS](/eptas/) style scheme is on the page [Epstein and Levin](/epstein-levin-eptas-bin-packing/). Hoberg and Rothvoss (2017) improved the additive term to $O(\log \mathrm{OPT})$, with an algorithm based on the [configuration LP](/configuration-lp/).

For exact answers on small inputs, a dynamic program over subsets of items computes $\mathrm{OPT}$ in $O(2^n n)$ time. For each subset it keeps the least number of bins and, among those, the least load of the last bin.

## Bounds

- **Lower bounds on OPT.** $\mathrm{OPT} \ge \lceil S \rceil$, $\mathrm{OPT}$ is at least the number of items larger than $1/2$, and $\mathrm{OPT}$ is at least the value of the configuration LP. Proofs are on [bin packing lower bound](/bin-packing-lower-bound/).
- **Hardness.** The decision version is NP-complete, and strongly NP-complete. For each $\rho < 3/2$, no polynomial-time algorithm has absolute ratio $\rho$ unless P = NP. Proofs are on [bin packing NP-hardness](/bin-packing-np-hardness/), and more results are on [bin packing inapproximability](/bin-packing-inapproximability/). First fit decreasing has absolute ratio exactly $3/2$, so the absolute ratio $3/2$ is tight for the problem.
- **No absolute PTAS, but an asymptotic one.** The $3/2$ bound rules out a [PTAS](/ptas/) in the absolute sense. It does not rule out an [asymptotic PTAS](/asymptotic-ptas/), and one exists.
- **Additive gap.** It is an open question whether a polynomial algorithm with $\mathrm{ALG} \le \mathrm{OPT} + 1$ exists. Hoberg and Rothvoss give $\mathrm{OPT} + O(\log \mathrm{OPT})$.

## Reductions

- **From partition.** [Partition](/partition-problem/) reduces to the question "is $\mathrm{OPT} \le 2$?". This gives NP-hardness and the $3/2$ bound.
- **From 3-partition.** [3-partition](/three-partition/) reduces to the decision version with polynomially bounded numbers. This gives [strong NP-hardness](/strong-np-hardness/).
- **To makespan scheduling.** Bin packing with $k$ bins is the decision version of [makespan minimization](/makespan-minimization/) on $k$ identical machines with deadline 1. The [dual approximation](/dual-approximation/) method of Hochbaum and Shmoys uses this link in the other direction.
- **To set cover.** Each feasible set of items is a set of the cover. The LP relaxation of this [set cover](/set-cover/) instance is the [configuration LP](/configuration-lp/).

## Applications

- Loading trucks, containers or pallets by weight or volume.
- Placing files on disks or tapes of fixed size, and memory allocation. The early analyses of first fit came from memory allocation.
- Assigning virtual machines to physical servers, with one resource (or several, in vector bin packing).
- Cutting pieces of given lengths from stock rolls or bars, which is the [cutting stock problem](/cutting-stock-problem/).
- Scheduling jobs with a common deadline on the fewest machines.

## References
