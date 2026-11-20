---
tag: DNA9DW
kind: algorithm
slug: localized-orthogonal-decomposition
name: Localized orthogonal decomposition
area: scientific-computing/multiscale-methods
level: research
summary: Corrects coarse basis functions by local fine-scale problems that decay exponentially, giving optimal coarse rates for rough coefficients.
model: real-ram
complexity:
  vars: {N: the number of fine cells, M: the number of coarse elements, k: the number of patch layers}
  time: {worst: "Θ(k³ N³ / M² + M² N)"}
  space: {extra: "Θ(k² N² / M² + M N)"}
properties: {deterministic: true, no_scale_separation: true, energy_orthogonal: true, exponential_localization: true}
history:
  year: 2014
  people: [Axel Malqvist, Daniel Peterseim]
  note: Malqvist and Peterseim introduced the method in a 2014 paper in Mathematics of Computation and proved that the correctors decay exponentially away from their element.
prereqs: [multiscale-finite-element-method, galerkin-method]
see_also: [variational-multiscale-method, heterogeneous-multiscale-method, periodic-homogenization, domain-decomposition, schur-complement, finite-element-method, model-order-reduction, multiscale-modeling]
sources:
  - paper: doi:10.1090/S0025-5718-2014-02868-8
    title: Axel Malqvist and Daniel Peterseim, Localization of elliptic multiscale problems, Mathematics of Computation 83(290), 2014, 2583-2603
    locator: the quasi-interpolation, the fine-scale space as its kernel, the element correctors on patches and the proof of their exponential decay, with patches of size of order H log(1/H)
  - book: isbn:9781611976441
    title: Axel Malqvist and Daniel Peterseim, Numerical Homogenization by Localized Orthogonal Decomposition, SIAM Spotlights 5, 2020
    locator: the ideal method and its error estimate, the localization of the correctors and the implementation of the patch problems
---

The localized orthogonal decomposition (LOD) is a coarse [finite element method](/finite-element-method/) for elliptic problems whose coefficient varies on a scale much finer than the coarse mesh. It needs no periodicity and no separation of scales. It splits the fine finite element space into a coarse part and a fine-scale part $W$, the kernel of a quasi-interpolation $I_H$, and corrects each coarse basis function so that the coarse space becomes orthogonal to $W$ in the energy inner product. The corrections decay exponentially away from their element, so each one is computed on a patch of a few coarse layers. The result is a Galerkin method on the coarse mesh with error of order $H$ in the energy norm for any bounded coefficient, where the standard coarse method can fail to converge at all.

## In plain words

A coarse mesh cannot see the fine structure of a rough material, so its hat functions are the wrong shape and the coarse answer can be badly wrong. LOD bends each hat function to fit the material. It finds the bend by solving a small fine-mesh problem near the hat function, with a rule that the bend adds nothing that the coarse mesh can see. The ideal bend spreads over the whole domain, but it fades fast, so a patch of two or three coarse elements is enough. The bent hat functions then give an accurate coarse solution with a small number of unknowns.

## The problem

Given a domain $D$, a coefficient $a$ with $0 < \alpha \le a \le \beta$ that may vary arbitrarily on a fine mesh of width $h$, a source $f$, a coarse mesh of width $H$ that the fine mesh refines, and a number of layers $k$, find an approximation of the fine solution $u_h \in V_h$ of

$$a(u_h, v) = \int_D a \nabla u_h \cdot \nabla v = (f, v) \quad \text{for all } v \in V_h,$$

in a space with one unknown per coarse node, with energy error of order $H$ that does not depend on how $a$ oscillates.

Let $V_H \subset V_h$ be the coarse P1 space with hat functions $\lambda_i$. LOD uses a quasi-interpolation $I_H : V_h \to V_H$ that is a projection, local and stable. A common choice, used here, is $I_H = E_H \circ \Pi_H$: $\Pi_H$ is the $L^2$ projection onto piecewise linear functions on each coarse element, and $E_H$ takes the mean of the values at each coarse node. The fine-scale space is $W = \ker I_H$, and $V_h = V_H \oplus W$.

## The algorithm

```pseudo id=main
LOD(a, f, coarse mesh, fine mesh, k)
L1  for each coarse element K do
L2      U ← K and k layers of coarse elements around it
L3      for each vertex i of K find q_{K,i} ∈ W(U) with a(q_{K,i}, w) = a_K(λ_i, w) for all w ∈ W(U)
L4  for each coarse node i do φ_i ← λ_i - Σ_K q_{K,i}
L5  solve the Galerkin equations Σ_j a(φ_j, φ_i) U_j = (f, φ_i) for all i
L6  return u_ms = Σ_i U_i φ_i
```

Here $a_K$ is the energy integral over $K$ alone, and $W(U)$ is the set of functions of $W$ that vanish outside the patch $U$. Line L3 is a fine finite element problem on the patch with the constraints $I_H w = 0$, one per coarse node in $U$. It is solved as a saddle point system with Lagrange multipliers, or in the kernel of the constraints. All right sides of one patch share one matrix. Lines L1 to L4 depend only on $a$ and the meshes, so the basis is reused for any $f$. Lines L5 and L6 are the [Galerkin method](/galerkin-method/) on the coarse mesh with the corrected basis.

If $U$ is the whole domain, the sum $Q = \sum_K q_{K, \cdot}$ is the $a$-orthogonal projection of $V_H$ onto $W$, and the corrected space $(1 - Q) V_H$ is $a$-orthogonal to $W$. This is the ideal method. The patches make it practical.

## Example

Take $(0, 1)$ with $N = 64$ fine cells and $a$ constant on each fine cell, equal to $0.1$, $1$ or $10$ at random and multiplied by a random factor in $[0.5, 1.5]$ (seed 1), so the contrast is about 300 and there is no period. Take $f = 1 + \sin 3x$. The fine solution has energy norm $1.133$. The table lists energy errors against the fine solution.

| $M$ | standard P1 | $k = 1$ | $k = 2$ | $k = 3$ | ideal |
| --- | --- | --- | --- | --- | --- |
| 4 | 1.094 | 0.1666 | 0.1053 | 0.1052 | 0.1052 |
| 8 | 1.043 | 0.1273 | 0.0406 | 0.0372 | 0.0370 |
| 16 | 1.000 | 0.2387 | 0.0334 | 0.0112 | 0.0094 |

The standard coarse method has an error near 90% of the solution and does not improve as $H$ decreases. The ideal LOD error decreases by more than a factor of 2 each time $H$ is halved, as the theorem below requires. For $M = 8$ the energy difference between the localized and the ideal solution for $k = 1, 2, 3, 4, 5$ is $0.120$, $0.0179$, $0.00254$, $4.80 \times 10^{-4}$ and $4.0 \times 10^{-5}$: each extra layer divides it by 5 or more. The column $k = 1$ also shows that a fixed number of layers is not enough: at $M = 16$ one layer is worse than at $M = 8$, because the localization error grows relative to the ideal error as $H$ decreases.

## Correctness

The [proof](proofs/correctness.md) covers the 1D method of the code. The quasi-interpolation is a projection onto $V_H$ and satisfies $\|v - I_H v\|_{L^2} \le C_I H \|v'\|_{L^2}$ with $C_I < 2.53$. The ideal correctors lie in $W$, and the corrected space is $a$-orthogonal to $W$, with $V_h = V_{ms} \oplus W$. Then the error $e = u_h - u_{ms}$ lies in $W$, so $I_H e = 0$ and

$$\|e\|_a^2 = (f, e - I_H e) \le C_I H \|f\| \|e'\| \quad \text{gives} \quad \|e\|_a \le \frac{C_I H}{\sqrt \alpha} \|f\|,$$

with no dependence on the oscillation of $a$ or on $\beta$. For patches of $k$ layers, the Cea lemma bounds the error by the ideal error plus the localization error $\|(Q - Q_k) I_H u_{ms}\|_a$. Malqvist and Peterseim proved that this term decays exponentially in $k$, at a rate that depends on the contrast $\beta / \alpha$. Hence $k$ of order $\log(1/H)$ keeps the order $H$ rate. The proof page cites this decay and does not prove it.

## Complexity

In the [real RAM](/real-ram/) model with $n = N / M$ fine cells per coarse element and $k \le M$, a patch has $\Theta(k n)$ fine unknowns and $\Theta(k)$ constraints. The code solves each of the at most $M$ distinct patch systems by dense [Gaussian elimination](/gaussian-elimination/), in $\Theta(k^3 n^3)$ time, which is $\Theta(k^3 N^3 / M^2)$ in all. It forms the coarse matrix with fine energy sums over the whole domain in $\Theta(M^2 N)$. The extra space is the dense patch matrix, $\Theta(k^2 N^2 / M^2)$, and the basis, $\Theta(M N)$.

A sparse code solves each patch problem in time nearly linear in its size, and each corrected basis function is nonzero on $\Theta(k^d)$ coarse elements in $d$ dimensions, so the coarse matrix is sparse with $\Theta(k^d)$ entries per row. The patch problems are independent and run in parallel, and they are computed once for all right sides.

## Properties

- **No scale assumption.** The error bound holds for any coefficient between $\alpha$ and $\beta$, with no period and no separation of scales.
- **Energy orthogonal.** In the ideal method, the coarse space is $a$-orthogonal to the fine-scale space, and the Galerkin solution is the part of $u_h$ in it.
- **Exponential localization.** The correctors decay exponentially in units of $H$, at a rate that depends on the contrast.
- **Reusable basis.** The basis depends on $a$ and not on $f$.
- **Conforming.** The basis functions lie in $V_h$, so the method is a Galerkin method in a subspace of $V_h$, and its energy error is never larger than the error of the best function in that subspace.

## Variants and improvements

- **Other quasi-interpolations.** Nodal averages of local $L^2$ projections as here, weighted Clement operators, or $L^2$ projections onto $V_H$; the choice changes $W$ and the constants, not the structure.
- **Element correctors or node correctors.** Correctors can be computed per element and summed, as here, or as one corrector per basis function on a patch around its node. The two choices give different localization errors and patch counts.
- **Other problems.** The same construction applies to linear elasticity, the Helmholtz equation in the regime where a pollution free coarse method is needed, eigenvalue problems, parabolic and wave equations, and problems with high contrast after a change of the interpolation.
- **Petrov-Galerkin LOD.** Test with the plain hat functions and solve with the corrected ones, which gives a sparser coarse matrix that is not symmetric.
- **Operator-adapted wavelets.** Owhadi's gamblets build a hierarchy of localized bases with similar decay properties and connect the method to Gaussian process estimation.

## When to use it

Use LOD when the coefficient is rough on a scale the coarse mesh cannot resolve, there is no period or scale separation to exploit, and the problem must be solved many times with different sources, or a small coarse model is needed for a time loop or an inverse problem. If the coefficient is periodic with a small period, [periodic homogenization](/periodic-homogenization/) or the [heterogeneous multiscale method](/heterogeneous-multiscale-method/) is cheaper. If one solve is all that is needed, a good fine solver such as multigrid or [domain decomposition](/domain-decomposition/) on the fine mesh may cost less than the patch problems.

## Pitfalls

- **A fixed number of layers.** The localization error must fall below the order $H$ error, so $k$ must grow like $\log(1/H)$. The example shows the loss for $k = 1$.
- **High contrast.** The decay rate degrades with $\beta / \alpha$ for the standard interpolation, so more layers are needed, or an interpolation adapted to the high-conductivity channels.
- **Singular patch systems.** Each constraint must act on the patch unknowns; a constraint of a coarse node whose functional is zero on the patch makes the saddle point matrix singular.
- **Cost of the offline phase.** The patch problems together cost more than one fine solve. The method pays off only when the basis is reused.
- **Truncation at the boundary of the patch.** Setting the corrector to zero outside the patch is the source of the localization error; patches that are too small for the contrast give errors near the standard coarse method.

## Implementations

## History

Malqvist and Peterseim introduced the localized orthogonal decomposition in a 2014 paper in Mathematics of Computation. They built on the [variational multiscale method](/variational-multiscale-method/) of Hughes and on the [multiscale finite element method](/multiscale-finite-element-method/) of Hou and Wu, and proved that the ideal fine-scale correctors decay exponentially. Henning, Peterseim and others extended the method to many other problems, and Kornhuber and Yserentant gave an analysis by subspace decomposition. Malqvist and Peterseim collected the theory in a 2020 book.

## References
