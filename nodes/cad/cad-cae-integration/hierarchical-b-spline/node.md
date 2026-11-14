---
tag: 4MZ00N
kind: data-structure
slug: hierarchical-b-spline
name: Hierarchical B-spline
aliases:
- HB-spline
area: cad/cad-cae-integration
level: advanced
summary: Forsey and Bartels's spline built from nested levels of B-spline bases chosen by refinement regions, used by Vuong and coauthors for adaptive analysis.
model: real-ram
complexity:
  vars: {N: the number of tensor B-splines of all levels together, p: the degree, k: the number of selected basis functions}
  time: {worst: O(N p^2), average: O(N p^2), best: O(N p^2)}
  space: {extra: O(k)}
properties: {deterministic: true, recursive: false}
history:
  year: 1988
  people: [David R. Forsey, Richard H. Bartels]
  note: Forsey and Bartels introduced hierarchical B-spline refinement for surface editing at SIGGRAPH 1988. Kraft gave the selection rule that makes the functions linearly independent in 1997, and Vuong, Giannelli, Jüttler and Simeon used it for adaptive isogeometric analysis in 2011.
prereqs: [b-spline, tensor-product-surface, knot-refinement, cox-de-boor-recursion]
see_also: [truncated-hierarchical-b-spline, t-spline, lr-b-spline, pht-spline, analysis-suitable-t-spline, isogeometric-analysis, partition-of-unity, boehm-knot-insertion]
sources:
  - paper: doi:10.1145/54852.378512
    title: David R. Forsey and Richard H. Bartels, Hierarchical B-spline refinement, Computer Graphics 22(4) (SIGGRAPH 1988), 205 to 212
    locator: overlays of finer B-spline patches on a coarse surface for local editing (general locator)
  - paper: "Rainer Kraft, Adaptive and linearly independent multilevel B-splines, in A. Le Méhauté, C. Rabut and L. L. Schumaker (editors), Surface Fitting and Multiresolution Methods, Vanderbilt University Press, 1997"
    locator: the selection of B-splines of each level by the nested domains, and its linear independence (general locator)
  - paper: doi:10.1016/j.cma.2011.09.004
    title: A.-V. Vuong, C. Giannelli, B. Jüttler and B. Simeon, A hierarchical approach to adaptive local refinement in isogeometric analysis, Computer Methods in Applied Mechanics and Engineering 200(49-52) (2011), 3554 to 3567
    locator: the definition of the hierarchical basis by Kraft's rule, its linear independence, the nested spaces under refinement, and adaptive isogeometric analysis with it (general locator)
  - paper: doi:10.1016/j.cagd.2012.03.025
    title: Carlotta Giannelli, Bert Jüttler and Hendrik Speleers, THB-splines, the truncated basis for hierarchical splines, Computer Aided Geometric Design 29(7) (2012), 485 to 498
    locator: the comparison of the hierarchical basis with the truncated basis, which spans the same space (general locator)
---

A hierarchical B-spline space is built from a sequence of nested tensor product [B-spline](/b-spline/) spaces, one per level, each finer than the last, and a nested sequence of domains $\Omega^0 \supseteq \Omega^1 \supseteq \cdots$. The basis takes, from each level $\ell$, the B-splines whose support lies inside $\Omega^\ell$ but not inside $\Omega^{\ell+1}$. So the functions are coarse where the domains stop and fine where they go on. Forsey and Bartels introduced hierarchical refinement in 1988 to edit surfaces locally. Kraft's selection rule of 1997 makes the functions linearly independent, and Vuong, Giannelli, Jüttler and Simeon used it in 2011 for adaptive [isogeometric analysis](/isogeometric-analysis/).

## In plain words

Start with a coarse grid of smooth bumps that covers the whole surface. In the places where you need more detail, mark a region and lay a second grid of bumps there, with half the spacing. Inside a smaller region you can lay a third grid, and so on.

You cannot keep every bump of every grid, because a coarse bump that sits inside a fine region is then just a sum of fine bumps. So the rule is: keep a bump of a grid if it fits inside the region of its own grid, and drop it if it fits inside the region of the next, finer grid.

The bumps that remain are independent, and together they can make every shape that the grids can make. They do not add up to 1.

## The abstract type

A hierarchical B-spline space of degree $p$ with $L$ levels stores, for each level $\ell$, a tensor product knot vector and a domain $\Omega^\ell$. The operations are:

- BASIS: the list of selected B-splines, as pairs (level, index).
- EVALUATE$(c, x, y)$: the value $\sum c_\beta \beta(x, y)$ of a function given by coefficients on the selected B-splines.
- REFINE$(\ell, R)$: add a region $R$ to $\Omega^\ell$, where $R$ is a union of cells of level $\ell - 1$ inside $\Omega^{\ell-1}$.
- FINEST$(\beta)$: the coefficients of a selected B-spline in the tensor B-splines of the finest level, by the two-scale relation.

## Representation

Level $\ell$ has, in each direction, the open uniform knot vector of degree $p$ on $[0, n_0]$ with spacing $2^{-\ell}$: $p + 1$ copies of 0, the points $a\, 2^{-\ell}$, and $p + 1$ copies of $n_0$. Its knots contain those of level $\ell - 1$, so by [knot refinement](/knot-refinement/) each B-spline of level $\ell$ is a combination of B-splines of level $\ell + 1$, the *two-scale relation*. A cell of level $\ell$ is a square of side $2^{-\ell}$ between grid lines. The B-spline $N^\ell_i$ is nonzero on the cells $\max(i - p, 0), \ldots, \min(i, n_0 2^\ell - 1)$ in each direction.

Each domain $\Omega^\ell$ is a set of cells of level $\ell$, with $\Omega^0$ the whole square, $\Omega^\ell$ a union of cells of level $\ell - 1$, and $\Omega^\ell \subseteq \Omega^{\ell-1}$. Set $\Omega^L = \emptyset$. "The support of $\beta$ lies in $\Omega$" means that every cell of the support is a cell of $\Omega$. The two-scale coefficients are stored as one sparse matrix per level and direction, computed once by [Boehm insertion](/boehm-knot-insertion/) of all the midpoints.

## Operations

```pseudo id=main
BASIS(levels, Ω)                                   ▷ Kraft's selection
L1  for ℓ ← 0 to L − 1 do
L2      for each tensor B-spline β of level ℓ do
L3          if supp β ⊆ Ω^ℓ and not supp β ⊆ Ω^(ℓ+1) then
L4              add (ℓ, β) to H
```

```pseudo id=evaluate
EVALUATE(c, x, y)
L5  s ← 0
L6  for each (ℓ, (i, j)) with coefficient c in the list do
L7      s ← s + c · N^ℓ_i(x) · N^ℓ_j(y)          ▷ Cox-de Boor on the knots of level ℓ
L8  return s
```

REFINE adds the four children of each given cell to $\Omega^\ell$ and checks that the cell is in $\Omega^{\ell-1}$; then BASIS runs again. FINEST applies the two-scale matrices of the levels $\ell, \ldots, L - 2$ to each index and multiplies the two results.

## Example

Take $p = 2$, $n_0 = 4$ and three levels, with $\Omega^1 = [0, 2]^2$ and $\Omega^2 = [0, 1]^2$. Level 0 has $6 \times 6 = 36$ biquadratic B-splines. The four with $i, j \le 1$ have their support inside $[0, 2]^2$, so they are dropped, and 32 remain. Level 1 has $10 \times 10$ B-splines; the 16 with $i, j \le 3$ lie in $\Omega^1$, and 4 of them, with $i, j \le 1$, lie in $\Omega^2$, so 12 are kept. Level 2 keeps the 16 B-splines that lie in $[0, 1]^2$. The basis has $32 + 12 + 16 = 60$ functions, and their expansions in the finest level have rank 60.

The functions are not a partition of unity. At $(\tfrac12, \tfrac12)$ their sum is $\tfrac{127}{64}$, because there the kept functions of all three levels overlap. Far from the refined region, at $(3, 3)$, only level 0 functions are nonzero, and the sum is 1. The constant 1 is still in the space, with other coefficients, because the space contains all the level 0 B-splines.

## Correctness

The two-scale relation writes a B-spline of level $\ell$ as a nonnegative combination of B-splines of level $\ell + 1$ whose supports lie inside its own. From this, by induction from the finest level down, every B-spline of level $\ell$ whose support lies in $\Omega^\ell$ is in the span of the selected functions: either the rule selects it, or its support lies in $\Omega^{\ell+1}$ and its children do. Two facts follow. The space contains the whole level 0 spline space, and enlarging the domains gives a larger space, so refinement is nested. The selected functions are linearly independent: on a cell of $\Omega^\ell$ outside $\Omega^{\ell+1}$ only functions of levels up to $\ell$ are nonzero, and B-splines of one level are linearly independent on each cell. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

Let $N$ be the number of tensor B-splines of all levels together and $k$ the number of selected ones. BASIS tests each of the $N$ B-splines against $(p + 1)^2$ cells of its support, with a hash set of cells, so it takes $O(N p^2)$ time. EVALUATE as written takes $O(k p^2)$ time, since each B-spline costs $O(p^2)$ by Cox-de Boor; with a cell index that lists the functions nonzero on each cell, only $O(L p^2)$ functions are touched. FINEST on level $\ell$ costs $O(2^{2(L - \ell)} p^2)$ for the output. The extra space is $O(k)$ for the basis, besides the domains.

## Variants

- **Truncated hierarchical B-splines.** Giannelli, Jüttler and Speleers cut from each coarse function its part in the finer B-splines that are inside the next domain. The [truncated basis](/truncated-hierarchical-b-spline/) spans the same space, is a partition of unity and has smaller supports.
- **Other refinements between levels.** The construction needs only nested spaces of the same degree, so the levels may use nonuniform knots and different knot insertions in each direction.
- **Forsey and Bartels's overlays.** The original hierarchical editing adds offsets on finer patches to the coarse surface. It is a representation for modelling, not a basis selection.
- **Admissible meshes.** For analysis, the domains are often restricted so that only a bounded number of levels have functions that are nonzero on a cell.

## When to use it

Use hierarchical B-splines for adaptive [isogeometric analysis](/isogeometric-analysis/) and local surface fitting when you want a simple data structure, the tensor product structure of each level, and nested spaces under refinement. If the method needs partition of unity or the overlap of supports matters, use the [truncated](/truncated-hierarchical-b-spline/) form. For local refinement that is not dyadic, compare [T-splines](/t-spline/), [LR B-splines](/lr-b-spline/) and [PHT-splines](/pht-spline/).

## Pitfalls

- **Keeping functions that lie in the finer domain.** Without the second test of line L3, a coarse function inside $\Omega^{\ell+1}$ is a combination of fine ones, and the set is dependent.
- **Assuming partition of unity.** The sum of the selected functions is not 1 near the refined regions. A rational form or a convex hull argument that needs it fails.
- **Domains that are not aligned.** $\Omega^\ell$ must be a union of cells of level $\ell - 1$. A domain that cuts a cell gives supports that are partly inside, and the rule is then ambiguous.
- **Overlap of many levels.** A coarse function can stay in the basis while its whole interior is covered by fine functions, so the number of functions nonzero at a point grows with the number of levels.

## Implementations

The Python module builds the open uniform knot vectors of the levels, the two-scale matrices by Boehm insertion of all midpoints, the domains as sets of cells, Kraft's selection of lines L1 to L4, EVALUATE by Cox-de Boor, the expansion in the finest level, and an exact sparse rank. The tests check that one level gives the tensor B-splines of a separate Cox-de Boor table, that the two-scale relation holds at random points with positive coefficients, the counts of the example, that the selected functions of random hierarchies of degree 2 and 3 are independent and contain every B-spline of level $\ell$ that lies in $\Omega^\ell$, that enlarging the domains keeps the old space inside the new one, and that the sum of the functions is not 1 while the constant 1 is in the space.

## History

Forsey and Bartels introduced hierarchical B-spline refinement for interactive surface editing at SIGGRAPH 1988. Kraft defined the selection by nested domains and proved the functions linearly independent in 1997. Vuong, Giannelli, Jüttler and Simeon applied it to adaptive isogeometric analysis in 2011. Giannelli, Jüttler and Speleers introduced the truncated basis in 2012 and proved its stability in 2014.

## References
