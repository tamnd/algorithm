---
tag: XS4YCM
kind: problem
slug: self-avoiding-walk-enumeration
name: Self-avoiding walk enumeration
aliases:
- counting self-avoiding walks
area: combinatorics/exhaustive-search
level: advanced
summary: Enumerate or count walks on a lattice that never revisit a vertex.
prereqs: [generic-backtracking-algorithm, enumeration-problem, counting-problem]
see_also: [polyomino-enumeration, enumerating-simple-paths, transfer-matrix-method, generic-backtracking-algorithm, combinatorial-explosion, counting-problem, redelmeier-algorithm, search-space]
sources:
  - url: https://oeis.org/A001411
    title: OEIS A001411, number of n-step self-avoiding walks on the square lattice
    locator: the table of values and the references to the series work
  - paper: "John M. Hammersley and K. William Morton, Poor man's Monte Carlo, Journal of the Royal Statistical Society, Series B 16(1), 1954, 23 to 38"
    locator: the inequality c(m + n) at most c(m) c(n) and the existence of the connective constant
  - paper: doi:10.4007/annals.2012.175.3.14
    title: Hugo Duminil-Copin and Stanislav Smirnov, The connective constant of the honeycomb lattice equals sqrt(2 + sqrt 2), Annals of Mathematics 175(3), 2012, 1653 to 1665
    locator: the main theorem, the proof of Nienhuis's prediction for the honeycomb lattice
  - book: "Neal Madras and Gordon Slade, The Self-Avoiding Walk, Birkhäuser, 1993"
    locator: Chapter 1 (definitions, the connective constant, the conjectured asymptotic form with the exponent γ) and Chapter 9 (exact enumeration and series analysis)
  - paper: "Jesper L. Jacobsen, Christian R. Scullard and Anthony J. Guttmann, On the growth constant for square-lattice self-avoiding walks, Journal of Physics A 49(49), 2016, 494004"
    locator: the estimate μ = 2.63815853... for the square lattice
  - paper: "Maciej Liśkiewicz, Mitsunori Ogihara and Seinosuke Toda, The complexity of counting self-avoiding walks in subgraphs of two-dimensional grids and hypercubes, Theoretical Computer Science 304, 2003, 129 to 156"
    locator: the #P-completeness of counting self-avoiding walks in subgraphs of the grid
---

A *self-avoiding walk* of $n$ steps on a lattice is a walk that starts at the origin, moves to a neighboring vertex at each step, and never visits a vertex twice. Self-avoiding walk enumeration asks for all such walks, or for their number $c_n$. On the square lattice $c_1, c_2, \ldots = 4, 12, 36, 100, 284, 780, \ldots$, and no formula is known: the numbers come from [backtracking](/generic-backtracking-algorithm/) for small $n$ and from finite-lattice and [transfer-matrix](/transfer-matrix-method/) methods for large $n$. The growth rate $\mu = \lim c_n^{1/n}$, the *connective constant*, is about $2.638$ on the square lattice, and it is known exactly only for the honeycomb lattice, where Duminil-Copin and Smirnov proved $\mu = \sqrt{2 + \sqrt{2}}$.

## In plain words

Stand on a corner of a city grid and take a walk of a fixed number of blocks. At each corner you may go left, right, straight on, or back, but you must never come back to a corner you have already visited.

How many different walks are there? For one block there are 4, for two blocks 12, for three blocks 36. After that the count grows more slowly than tripling each time, because more and more walks run into their own path. Nobody knows a formula. To get the numbers, people list or count the walks with clever searches. The walks are a simple model of a long chain molecule, which also cannot pass through itself.

## Definition

Let $L$ be a lattice graph, such as the square lattice $\mathbb{Z}^2$, with a vertex $0$ as the origin. An *$n$-step self-avoiding walk* is a sequence $w_0 = 0, w_1, \ldots, w_n$ of pairwise distinct vertices in which $w_{i-1}$ and $w_i$ are adjacent for each $i$.

- The *enumeration problem* lists all $n$-step walks.
- The *counting problem* asks for $c_n$, the number of $n$-step walks. Since the input is the number $n$ alone, the interest is in the sequence $c_1, c_2, \ldots$ as far as possible.

On a general graph, a self-avoiding walk is a [simple path](/enumerating-simple-paths/) that starts at a given vertex.

## Variants

- **Other lattices.** The triangular, honeycomb and cubic lattices, and $\mathbb{Z}^d$ in higher dimensions.
- **Self-avoiding polygons.** Walks that end next to the origin and close into a cycle. Their count $p_n$ grows at the same rate $\mu$.
- **Walks with interactions.** Each pair of non-consecutive visited neighbors gives an energy, as in models of polymer collapse; the count becomes a polynomial in a weight.
- **Restricted walks.** Walks confined to a strip or a half-plane, or bridges and directed walks, which often have known generating functions.
- **Walks in a finite graph.** Count the self-avoiding walks in a given subgraph of the grid. This is the form for which hardness is proven.
- **Sampling.** Draw walks at random from the uniform distribution on $n$-step walks, by Monte Carlo methods such as the pivot algorithm, when $c_n$ is too large to list.

## Examples

Counts on the square lattice (OEIS A001411):

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $c_n$ | 4 | 12 | 36 | 100 | 284 | 780 | 2,172 | 5,916 | 16,268 | 44,100 |

For $n \le 3$ every walk that never steps straight back is self-avoiding, so $c_n = 4 \cdot 3^{n-1}$. At $n = 4$, the 8 walks that go around a unit square and return to the origin are excluded, so $c_4 = 108 - 8 = 100$.

On the honeycomb lattice, where each vertex has 3 neighbors, the counts are $3, 6, 12, 24, 48, 90, 174, 336, \ldots$. The first exclusion comes at $n = 6$, when a walk closes a hexagon: $96 - 6 = 90$.

**A non-example.** The walk right, up, left, down returns to the origin at step 4, so it is not self-avoiding, although every step goes to a new vertex except the last one.

## Known algorithms

- **Backtracking.** Extend the walk one step at a time and undo the step after the recursion, with a set or an array of visited vertices. The time is $O(c_1 + \cdots + c_n)$, about $O(c_n)$, with $O(n)$ memory. Symmetry cuts the work by a factor near 8: fix the first step to the right and the first turn upward, and multiply.
- **Finite-lattice method.** Count the walks that fit in each rectangle of the lattice by a [transfer-matrix](/transfer-matrix-method/) computation that moves a boundary across the rectangle and stores the states of the boundary, and combine the rectangles. The time grows exponentially in $n$ but with a base well below $\mu$, so it reaches much larger $n$ than any listing method.
- **Lace expansion and length doubling.** Other exact methods count walks by combining shorter walks with corrections for their intersections.
- **Monte Carlo sampling.** The pivot algorithm samples long walks at random. It does not count, but it estimates $\mu$ and the exponents of the asymptotic form.

## Bounds

**Simple bounds.** A walk that only goes right or up is self-avoiding, so $c_n \ge 2^n$. A self-avoiding walk never steps straight back, so $c_n \le 4 \cdot 3^{n-1}$.

**Connective constant.** If a walk of $m + n$ steps is cut at step $m$, both parts are self-avoiding walks, so $c_{m+n} \le c_m c_n$. By Fekete's lemma,

$$\mu = \lim_{n \to \infty} c_n^{1/n} = \inf_n c_n^{1/n}$$

exists, and $c_n \ge \mu^n$ for all $n$. So $2 \le \mu \le 3$ on the square lattice. Series analysis gives $\mu \approx 2.63815853$. On the honeycomb lattice, Nienhuis predicted in 1982, and Duminil-Copin and Smirnov proved in 2012, that $\mu = \sqrt{2 + \sqrt{2}} \approx 1.84776$.

**Asymptotic form.** It is conjectured that $c_n \sim A \mu^n n^{\gamma - 1}$, with $\gamma = 43/32$ in two dimensions. This form is supported by the exact counts and by Monte Carlo data, but it is not proven.

**Hardness.** Counting the self-avoiding walks in a given subgraph of the grid is #P-complete. For the full lattice, where the only input is $n$, no hardness result of this kind applies, but no polynomial-time method is known either.

## Reductions

- **To simple paths.** On any graph, the self-avoiding walks from a vertex are its simple paths, so methods for [enumerating simple paths](/enumerating-simple-paths/) apply.
- **To polyominoes.** The set of cells visited by a self-avoiding walk on the square lattice, viewed as squares, is a [polyomino](/polyomino-enumeration/). Both counts use the same finite-lattice methods.
- **To transfer matrices.** On a strip of fixed width, the number of walks satisfies a linear recurrence whose matrix comes from the [transfer-matrix method](/transfer-matrix-method/).

## Applications

- **Polymer physics.** Flory and later workers model long chain molecules in a good solvent by self-avoiding walks. The exponents of the asymptotic form predict how the size of a polymer grows with its length.
- **Statistical mechanics.** The walk is the limit $N \to 0$ of the $O(N)$ spin model, which links its exponents to conformal field theory and to SLE in the plane.
- **Benchmarks.** Exact counts test new enumeration methods, parallel search and series-analysis techniques.
- **Combinatorics.** The connective constant and its bounds are standard examples of the use of submultiplicative sequences.

## References
