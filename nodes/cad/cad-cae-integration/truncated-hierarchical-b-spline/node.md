---
tag: EY36RH
kind: data-structure
slug: truncated-hierarchical-b-spline
name: Truncated hierarchical B-spline
aliases:
- THB-spline
area: cad/cad-cae-integration
level: research
summary: Giannelli, Juttler and Speleers's hierarchical spline whose coarse functions are truncated by finer ones, restoring partition of unity and reducing overlap.
model: real-ram
complexity:
  vars: {N: the number of tensor B-splines of all levels together, p: the degree, k: the number of selected basis functions, L: the number of levels, m: the number of tensor B-splines of the finest level}
  time: {worst: O(N p^2 + k L m p^2), average: O(N p^2 + k L m p^2), best: O(N p^2 + k L m p^2)}
  space: {extra: O(k m)}
properties: {deterministic: true, recursive: false}
history:
  year: 2012
  people: [Carlotta Giannelli, Bert Jüttler, Hendrik Speleers]
  note: Giannelli, Jüttler and Speleers defined the truncated basis for hierarchical splines in 2012 and proved its partition of unity, its linear independence and that it spans the hierarchical space. In 2014 they proved that it is strongly stable.
prereqs: [hierarchical-b-spline, b-spline, knot-refinement, partition-of-unity]
see_also: [isogeometric-analysis, t-spline, lr-b-spline, pht-spline, analysis-suitable-t-spline, boehm-knot-insertion, convex-hull-property, tensor-product-surface]
sources:
  - paper: doi:10.1016/j.cagd.2012.03.025
    title: Carlotta Giannelli, Bert Jüttler and Hendrik Speleers, THB-splines, the truncated basis for hierarchical splines, Computer Aided Geometric Design 29(7) (2012), 485 to 498
    locator: the truncation operator, the definition of the truncated basis, and the proofs of nonnegativity, partition of unity, linear independence, equal span and nested spaces (general locator)
  - paper: doi:10.1007/s10444-013-9315-2
    title: Carlotta Giannelli, Bert Jüttler and Hendrik Speleers, Strongly stable bases for adaptively refined multilevel spline spaces, Advances in Computational Mathematics 40(2) (2014), 459 to 490
    locator: the strong stability of the truncated basis and the preservation of coefficients (general locator)
  - paper: doi:10.1016/j.cma.2011.09.004
    title: A.-V. Vuong, C. Giannelli, B. Jüttler and B. Simeon, A hierarchical approach to adaptive local refinement in isogeometric analysis, Computer Methods in Applied Mechanics and Engineering 200(49-52) (2011), 3554 to 3567
    locator: the hierarchical basis by Kraft's rule that the truncation starts from, and its use in adaptive isogeometric analysis (general locator)
  - paper: "Rainer Kraft, Adaptive and linearly independent multilevel B-splines, in A. Le Méhauté, C. Rabut and L. L. Schumaker (editors), Surface Fitting and Multiresolution Methods, Vanderbilt University Press, 1997"
    locator: the selection of B-splines of each level by the nested domains (general locator)
---

A truncated hierarchical B-spline basis takes the functions of the [hierarchical B-spline](/hierarchical-b-spline/) basis and cuts each coarse function down. A function of level $\ell$ is written in the B-splines of level $\ell + 1$, and the terms whose support lies in the next domain $\Omega^{\ell+1}$ are dropped. This is repeated for each finer level. The truncated functions span the same space as the hierarchical basis and are linearly independent, but they are also nonnegative, they sum to 1, and their supports are smaller. Giannelli, Jüttler and Speleers introduced the basis in 2012, and it is the usual choice for adaptive [isogeometric analysis](/isogeometric-analysis/) with hierarchical splines.

## In plain words

A hierarchical spline has a coarse grid of bumps, and finer grids of bumps in the regions that need detail. A coarse bump that reaches into a fine region overlaps the fine bumps there. Its shape in that region adds nothing new, because the fine bumps can already make it.

So cut it. Write the coarse bump as a sum of fine bumps, and throw away the fine bumps that sit inside the fine region. What remains is the coarse bump with a hole where the fine region is. Do this for each finer level in turn.

After the cuts, at each point only a few bumps are active, every bump is still nonnegative, and all the bumps add up to exactly 1. The set of shapes you can make does not change.

## The abstract type

A truncated hierarchical B-spline space of degree $p$ with $L$ levels stores the same data as a hierarchical one: a tensor product knot vector per level and nested domains $\Omega^0 \supseteq \Omega^1 \supseteq \cdots \supseteq \Omega^{L-1}$, with $\Omega^L = \emptyset$. The operations are:

- BASIS: for each function $\beta$ of Kraft's hierarchical selection, its truncated form $\tau(\beta)$, as coefficients on the tensor B-splines of the finest level.
- EVALUATE$(c, x, y)$: the value of a function given by coefficients on the finest level.
- REFINE$(\ell, R)$: add a region $R$, a union of cells of level $\ell - 1$ inside $\Omega^{\ell-1}$, to $\Omega^\ell$.

The truncation of level $k$ acts on a spline $s$ of level $k - 1$. Write $s = \sum_\gamma c_\gamma \gamma$ in the B-splines $\gamma$ of level $k$. Then

$$\operatorname{trunc}^{k} s = \sum_{\operatorname{supp} \gamma \not\subseteq \Omega^{k}} c_\gamma \gamma,$$

and for $\beta$ of level $\ell$ in the hierarchical basis $H$,

$$\tau(\beta) = \operatorname{trunc}^{L-1} \cdots \operatorname{trunc}^{\ell+2} \operatorname{trunc}^{\ell+1} \beta.$$

## Representation

The levels, cells and domains are those of the [hierarchical B-spline](/hierarchical-b-spline/) page. Level $\ell$ has, in each direction, the open uniform knot vector of degree $p$ on $[0, n_0]$ with spacing $2^{-\ell}$, and a domain is a set of cells. The two-scale relation between levels $\ell$ and $\ell + 1$ is stored as one sparse matrix per direction, computed by [Boehm insertion](/boehm-knot-insertion/) of all the midpoints. A spline of level $\ell$ is a sparse map from index pairs $(i, j)$ to coefficients; the lift to level $\ell + 1$ multiplies by the two matrices. Each truncated function is stored as a sparse map on the tensor B-splines of the finest level.

## Operations

```pseudo id=main
BASIS(levels, Ω)                                   ▷ Giannelli, Jüttler, Speleers
L1  for each (ℓ, β) in Kraft's selection H do
L2      c ← {β: 1}                                 ▷ coefficients on level ℓ
L3      for k ← ℓ + 1 to L − 1 do
L4          c ← lift of c to level k               ▷ two-scale relation
L5          c ← c without the γ with supp γ ⊆ Ω^k  ▷ trunc^k
L6      τ(β) ← c written in the finest level
```

```pseudo id=evaluate
EVALUATE(c, x, y)
L7  s ← 0
L8  for each finest index (i, j) with coefficient c_ij do
L9      s ← s + c_ij · N_i(x) · N_j(y)             ▷ Cox-de Boor, finest knots
L10 return s
```

Kraft's selection in line L1 keeps the B-splines of level $\ell$ whose support lies in $\Omega^\ell$ but not in $\Omega^{\ell+1}$. REFINE adds the four children of each given cell to $\Omega^\ell$, checks that the cell is in $\Omega^{\ell-1}$, and runs BASIS again.

## Example

Take $p = 2$, $n_0 = 4$ and three levels, with $\Omega^1 = [0, 2]^2$ and $\Omega^2 = [0, 1]^2$, the example of the hierarchical B-spline page. Kraft's selection keeps $32 + 12 + 16 = 60$ functions, and the truncated basis has one function for each of them.

Look at the level 0 B-spline $N^0_2(x) N^0_2(y)$, whose support is $[0, 3]^2$. The truncation of level 1 drops the terms of its level 1 expansion whose support lies in $[0, 2]^2$, so the function is zero near the corner and smaller in the rest of $[0, 2]^2$. At $(\tfrac12, \tfrac12)$ the plain function has the value $\tfrac{1}{64}$ and the truncated function has the value 0. At $(\tfrac32, \tfrac32)$ the values are $\tfrac{9}{16}$ and $\tfrac{27}{64}$, and at $(\tfrac52, \tfrac52)$, outside $\Omega^1$, they are equal. In the finest level the plain function has 100 nonzero coefficients and the truncated one has 84.

The sum of all 60 truncated functions has every finest coefficient equal to 1, so it is the constant 1. The plain hierarchical functions sum to $\tfrac{127}{64}$ at $(\tfrac12, \tfrac12)$. At $(\tfrac34, \tfrac34)$, 14 of the hierarchical functions are nonzero, but only 9 of the truncated ones.

## Correctness

The truncation of level $k$ is linear, and it only drops terms of an expansion whose coefficients are nonnegative, so every $\tau(\beta)$ has nonnegative coefficients in the finest level and is nonnegative. Partition of unity comes from an induction over the levels. At level $k$, the constant 1 is the sum of the truncated functions of the levels below $k$ plus the B-splines of level $k$ that lie in $\Omega^k$. Lifting to level $k + 1$ and truncating replaces the B-splines that lie in $\Omega^{k+1}$ by their own children, and the coefficients of 1 in every level are all 1. The same induction shows more: a spline of level 0 has the same coefficients on the truncated basis as on the B-splines of each level, which is the preservation of coefficients. Each $\tau(\beta)$ differs from $\beta$ by functions of finer levels that lie in the finer domains, so the span equals the hierarchical span, and the triangular form of this relation gives linear independence. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

Let $N$ be the number of tensor B-splines of all levels together, $k$ the number of selected functions, $L$ the number of levels and $m$ the number of tensor B-splines of the finest level. Kraft's selection takes $O(N p^2)$ time. Each lift of a sparse map with at most $m$ entries spreads each entry to at most $(p + 2)^2$ children, and the truncation test checks $(p + 1)^2$ cells per term, so one function costs $O(L m p^2)$ and BASIS costs $O(N p^2 + k L m p^2)$ in the worst case. In practice the maps stay local, of size $O(4^{L - \ell} p^2)$ for a function of level $\ell$. Storing all truncated functions on the finest level takes $O(k m)$ space. EVALUATE costs $O(p^2)$ per stored coefficient, or $O(p^2)$ per point with an index of the coefficients by cell.

## Variants

- **Hierarchical basis without truncation.** The [hierarchical B-spline](/hierarchical-b-spline/) basis spans the same space but is not a partition of unity and its supports overlap more.
- **Truncation of each level only.** Storing $\tau(\beta)$ level by level, as $\beta$ minus the dropped parts, avoids the finest level and keeps the maps small. The test against a level by level reference evaluates this form.
- **Admissible meshes.** For error estimates and the condition number in analysis, the domains are often restricted so that only a bounded number of levels have truncated functions that are nonzero on a cell.
- **Other nested spaces.** The construction needs only nested spline spaces whose bases have nonnegative two-scale coefficients and partition of unity, so it extends to nonuniform knots, to different refinements per direction, and to some other spline families.

## When to use it

Use truncated hierarchical B-splines for adaptive [isogeometric analysis](/isogeometric-analysis/), for local fitting, and for any method that needs a partition of unity with local refinement on a tensor product structure, for example a rational form or the [convex hull property](/convex-hull-property/) of a control net. The fewer overlaps give sparser stiffness matrices than the plain hierarchical basis. For local refinement that is not dyadic or not aligned to levels, compare [T-splines](/t-spline/), [LR B-splines](/lr-b-spline/) and [PHT-splines](/pht-spline/).

## Pitfalls

- **Truncating against the wrong domain.** The truncation of level $k$ drops the B-splines whose support lies in $\Omega^k$, not those that merely meet it. Dropping more breaks partition of unity and the span.
- **Skipping intermediate levels.** $\tau(\beta)$ must be truncated at each level from $\ell + 1$ to $L - 1$ in order. Lifting straight to the finest level and truncating once against $\Omega^{L-1}$ gives a different function.
- **Nonnegative two-scale coefficients.** Nonnegativity of the truncated functions needs nonnegative two-scale coefficients, which hold for B-splines but not for every refinable basis.
- **Updating after refinement.** A REFINE of level $\ell$ changes the truncated form of functions of all coarser levels, not only those of level $\ell - 1$.

## Implementations

The Python module builds the open uniform knot vectors of the levels, the two-scale matrices by Boehm insertion of all midpoints, the domains as sets of cells, Kraft's selection, the truncation of lines L1 to L6, EVALUATE by Cox-de Boor on the finest knots, and an exact sparse rank. The tests check that one level gives the tensor B-splines, the counts of the example, that the truncated functions sum to 1 exactly in coefficients and at points, that a random spline of level 0 keeps its coefficients, that the coefficients are positive and lie inside those of the plain functions, that the span equals the hierarchical span and the functions are independent, that refinement gives nested spaces, the values against a level by level reference, and the truncated function of the example.

## History

Forsey and Bartels introduced hierarchical B-spline refinement in 1988, Kraft gave the selection rule for linear independence in 1997, and Vuong, Giannelli, Jüttler and Simeon used the hierarchical basis for adaptive isogeometric analysis in 2011. Giannelli, Jüttler and Speleers defined the truncation in 2012 to restore partition of unity and reduce overlap. In 2014 they proved that the truncated basis is strongly stable, with constants that do not depend on the number of levels.

## References
