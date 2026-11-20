---
tag: 6V214F
kind: algorithm
slug: multiscale-finite-element-method
name: Multiscale finite element method
aliases:
- MsFEM
area: scientific-computing/multiscale-methods
level: advanced
summary: Builds basis functions by solving the fine-scale equation on each coarse element, so a coarse solve captures the fine structure.
model: real-ram
complexity:
  vars: {N: the number of fine cells, M: the number of coarse elements}
  time: {worst: "Θ(N)"}
  space: {extra: "Θ(N)"}
properties: {deterministic: true, conforming: true, exact_at_coarse_nodes_in_1d: true, needs_scale_separation: false}
history:
  year: 1997
  people: [Thomas Y. Hou, Xiao-Hui Wu]
  note: Hou and Wu introduced the method and the oversampling technique in 1997. Hou, Wu and Cai proved convergence in 1999, and Efendiev, Hou and Wu analyzed the nonconforming method with oversampling in 2000.
prereqs: [periodic-homogenization, finite-element-method]
see_also: [localized-orthogonal-decomposition, heterogeneous-multiscale-method, variational-multiscale-method, static-condensation, domain-decomposition, thomas-algorithm, galerkin-method, multiscale-modeling]
sources:
  - paper: doi:10.1006/jcph.1997.5682
    title: Thomas Y. Hou and Xiao-Hui Wu, A multiscale finite element method for elliptic problems in composite materials and porous media, Journal of Computational Physics 134(1), 1997, 169-189
    locator: the multiscale basis functions from local problems on each coarse element, the oversampling technique and the numerical tests for composites and porous media
  - paper: doi:10.1090/S0025-5718-99-01077-7
    title: Thomas Y. Hou, Xiao-Hui Wu and Zhiqiang Cai, Convergence of a multiscale finite element method for elliptic problems with rapidly oscillating coefficients, Mathematics of Computation 68(227), 1999, 913-943
    locator: the error analysis for periodic coefficients, with the resonance error when the coarse mesh size is close to the period
  - paper: doi:10.1137/S0036142997330329
    title: Yalchin R. Efendiev, Thomas Y. Hou and Xiao-Hui Wu, Convergence of a nonconforming multiscale finite element method, SIAM Journal on Numerical Analysis 37(3), 2000, 888-910
    locator: the analysis of the oversampling method, which is nonconforming, and the reduction of the resonance error
---

The multiscale finite element method (MsFEM) solves an elliptic equation with a rough coefficient, such as $-\nabla \cdot (a(x) \nabla u) = f$ with $a$ that varies on a scale $\varepsilon$, on a coarse mesh of size $H \gg \varepsilon$. It does not use the standard linear basis functions. On each coarse element it solves the equation itself, without the source, on a fine local mesh, with the linear hat functions as boundary data. These multiscale basis functions carry the fine oscillations of the solution, so the Galerkin solution in their span is accurate on the coarse mesh. The local problems are independent of each other and of $f$, so they run in parallel and can be reused for many right-hand sides. In 1D the method gives the fine solution exactly at the coarse nodes.

## In plain words

Picture a slab of rock with thin layers that let water through at very different rates. A coarse mesh with standard elements treats each big element as if its rock were uniform, and it gets the flow wrong by a fixed amount however fine the layers become. MsFEM keeps the coarse mesh but changes the shape functions. For each big element, it solves the flow equation on a fine mesh inside that element only, once, with simple values on the border. The result is a shape function that bends exactly where the rock is tight or open. The coarse problem then has few unknowns, but its shape functions know the layers. You pay for the small local problems once and solve a small global problem.

## The problem

Given a domain $\Omega$, a coefficient $a(x)$ with $0 < \alpha \le a \le \beta$ that may vary on a scale $\varepsilon$, a source $f$ and a coarse mesh $\mathcal T_H$ whose elements each carry a fine mesh of size $h \le \varepsilon$, compute $u_{ms}$ in a space of dimension equal to the number of coarse nodes such that $u_{ms}$ approximates the solution of

$$-\nabla \cdot (a \nabla u) = f \text{ in } \Omega, \qquad u = 0 \text{ on } \partial \Omega,$$

with an error that does not grow when $\varepsilon$ is smaller than $H$. The reference is the fine solution $u_h$ on the whole domain, which is the best that the fine mesh allows and costs a solve with all fine unknowns.

## The algorithm

```pseudo id=main
MSFEM(a, f, T_H, fine mesh in each K)
L1  for each coarse element K in T_H do
L2      for each vertex i of K: solve -div(a grad φ_i^K) = 0 in K, φ_i^K = λ_i on ∂K, on the fine mesh of K
L3      A_K[i][j] ← ∫_K a grad φ_j^K · grad φ_i^K and F_K[i] ← ∫_K f φ_i^K
L4      add A_K into A and F_K into F
L5  solve A U = F with U = 0 at the boundary nodes
L6  return U and u_ms = Σ_i U_i φ_i on the fine meshes
```

Here $\lambda_i$ is the standard linear hat function of coarse node $i$, and $\phi_i$ is the function that equals $\phi_i^K$ on each element $K$ next to node $i$. Since the local problems on two elements next to an edge have the same linear boundary data on that edge, $\phi_i$ is continuous and the method is conforming. Lines L1 to L4 are a normal finite element assembly, with the integrals done on the fine mesh; line L5 is a sparse solve with one unknown per coarse node.

In 1D the local problem of line L2 is a tridiagonal system that the [Thomas algorithm](/thomas-algorithm/) solves, and the basis function of the left vertex is $1 - \phi$ when $\phi$ is that of the right vertex. The flux $a \phi'$ is then constant on $K$, so $\phi' = \bar a_K / (H a)$, where $\bar a_K$ is the harmonic mean of $a$ over $K$, and line L3 gives the element stiffness $\bar a_K / H$. In 1D the MsFEM matrix is the linear element matrix with the harmonic means in place of the arithmetic ones.

## Example

Take $a(x) = 2 + \sin(2\pi x / \varepsilon)$ with $\varepsilon = 1/32$, $f = 1$, a fine mesh of $N = 512$ cells with the midpoint value of $a$ on each cell, and coarse meshes of $M$ elements. The fine solution has $u_h(1/2) = 0.0721688$, which agrees with the homogenized value $1/(8\sqrt 3)$ to $10^{-10}$, and the energy norm $\|u_h\|_a = 0.2193$.

| $M$ | $H$ | MsFEM, $\lVert u_h - u_{ms} \rVert_a$ | standard P1, $\lVert u_h - u_H \rVert_a$ | P1 at $x = 1/2$ |
|---|---|---|---|---|
| 4 | 1/4 | 0.0548 | 0.0951 | 0.0625 |
| 8 | 1/8 | 0.0273 | 0.0842 | 0.0625 |
| 16 | 1/16 | 0.0135 | 0.0813 | 0.0625 |
| 32 | 1/32 | 0.0065 | 0.0805 | 0.0625 |

The MsFEM values at the coarse nodes agree with $u_h$ up to rounding, below $10^{-12}$, for every $M$, and the energy error halves with $H$. The standard linear elements use the mean 2 of $a$ on each element, so their midpoint value is $1/16$, which is 13% low, and their energy error stays above 36% of $\|u_h\|_a$.

By hand, take one coarse element of length $H = \tfrac12$ with four fine cells and $a = 1, 4, 1, 4$. The harmonic mean is $1/(\tfrac12 (1 + \tfrac14)) = 1.6$, so the flux $a \phi'$ is $1.6 / H = 3.2$, and $\phi$ rises by $3.2 \cdot \tfrac18 = 0.4$ on the cells with $a = 1$ and by $0.1$ on the cells with $a = 4$: $\phi = 0, 0.4, 0.5, 0.9, 1$.

## Correctness

The [proof](proofs/correctness.md) covers the 1D method. The key fact is that the fine space splits into the multiscale space and the space $B$ of fine functions that vanish at all coarse nodes, and the two are orthogonal in the energy inner product, because each basis function solves the homogeneous equation inside each element. So the MsFEM solution is the multiscale interpolant of the fine solution, which proves the nodal exactness. The error $u_h - u_{ms}$ lies in $B$ and solves local problems with source $f$, and the Poincare inequality on each element gives

$$\|u_h - u_{ms}\|_a \le \frac{H}{\pi \sqrt \alpha} \|f\|_{L^2},$$

a bound that does not depend on how $a$ oscillates.

In 2D and 3D this splitting fails, and the analysis of Hou, Wu and Cai for periodic coefficients gives an error of order $H$ plus terms in $\varepsilon$ and a resonance term that grows with $\varepsilon / H$. The resonance comes from the linear boundary data of line L2, which force the basis functions to be linear on the coarse edges, while the true solution oscillates there.

## Complexity

In the [real RAM](/real-ram/) model, line L2 in 1D costs $\Theta(n)$ on an element with $n$ fine cells, and lines L1 to L4 together cost $\Theta(N)$ for $N = M n$ fine cells. Line L5 is a tridiagonal solve in $\Theta(M)$. The total is $\Theta(N)$ time and $\Theta(N)$ space for the basis functions, the same order as the fine solve, but the local work is independent across elements and reusable.

In $d$ dimensions with $n^d$ fine cells per element, each local problem is a sparse solve of size $n^d$ with $d + 1$ or $2^d$ right-hand sides. The coarse problem has $M$ unknowns. For a new source $f$ only lines L3 to L5 are repeated.

## Properties

- **Conforming and symmetric.** With linear boundary data the basis functions are continuous, and the coarse matrix is symmetric positive definite.
- **Local and parallel.** Each element needs only its own fine mesh and coefficient.
- **No periodicity needed.** The method uses the actual coefficient, not a cell problem, so it works for random or channelized media. It still works best when $H$ is well above or well below $\varepsilon$, not near it.
- **Partition of unity.** The basis functions add up to 1, since the constant solves the local problem.

## Variants and improvements

- **Oversampling.** Solve the local problems on a larger patch around $K$ and restrict the result to $K$. The boundary layer of the local solution then lies outside $K$, and the resonance error is much smaller. The basis functions are no longer continuous, so the method is nonconforming; Efendiev, Hou and Wu analyzed it in 2000.
- **Reduced boundary conditions.** Replace the linear edge data by the solution of a 1D problem along each edge, which follows the oscillations of $a$ along the edge.
- **Mixed MsFEM.** Build multiscale velocity basis functions for the Darcy flux. This is common in reservoir simulation, where mass conservation matters.
- **Generalized MsFEM.** Use several local eigenfunctions per element for high-contrast coefficients with channels, which a single basis function per node cannot resolve.
- **[Localized orthogonal decomposition](/localized-orthogonal-decomposition/).** Correct the hat functions by fine-scale problems on patches of a few layers, with a constraint that removes the resonance and gives an error of order $H$ without scale separation.

## When to use it

Use MsFEM when the coefficient is rough on a scale far below any affordable coarse mesh, when the same coefficient is used with many sources or in many time steps, and when the local problems can be solved in parallel: subsurface flow, composites, heat conduction in heterogeneous media. If the coefficient is periodic and only the effective behavior is needed, [periodic homogenization](/periodic-homogenization/) is cheaper. If the macroscopic equation is known but its data are not, the [heterogeneous multiscale method](/heterogeneous-multiscale-method/) samples small micro cells instead of covering each element. If a guaranteed rate without scale separation is needed, use localized orthogonal decomposition.

## Pitfalls

- **Resonance.** When $H$ is a small multiple of $\varepsilon$, the linear boundary data create a boundary layer in each element and the error does not decrease as expected. Oversampling or a smaller $H / \varepsilon$ ratio is needed.
- **An unresolved fine mesh.** The local problems must resolve $a$. A local mesh with $h > \varepsilon$ gives basis functions that are wrong in the same way as standard elements.
- **Inexact integrals.** Line L3 must integrate on the fine mesh. A coarse quadrature rule with one point per element loses the information in the basis functions.
- **High contrast.** If $a$ contains thin channels of high value that cross many elements, one basis function per node is not enough; the error depends on the contrast $\beta / \alpha$.

## Implementations

## History

Hou and Wu introduced the multiscale finite element method in 1997, for elliptic problems in composite materials and porous media, together with the oversampling technique. Babuska and Osborn had used special basis functions from local problems for 1D problems with rough coefficients in 1983. Hou, Wu and Cai proved convergence for periodic coefficients in 1999 and identified the resonance error. Efendiev, Hou and Wu analyzed the nonconforming oversampling method in 2000. Later work produced mixed and generalized versions, and the method became a standard tool of numerical homogenization and reservoir simulation.

## References
