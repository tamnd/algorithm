---
tag: G6HHDK
kind: algorithm
slug: adi-method
name: Alternating direction implicit method
aliases:
- ADI method
- Peaceman-Rachford method
- Peaceman-Rachford ADI
area: numerical/differential-equations
level: advanced
summary: Advances the 2D heat equation in two half steps, implicit first in x and then in y. Each half step is a set of tridiagonal solves, and the scheme is second order and l2 stable for every Δt.
solves: [heat-equation]
model: real-ram
complexity:
  vars: {p: "the number of intervals in x (m_x on the page)", q: "the number of intervals in y (m_y on the page)", N: "the number of time steps"}
  time: {worst: "Θ(N p q)"}
  space: {extra: "Θ(p q)"}
properties: {deterministic: true, implicit: true, order_space: "2", order_time: "2", unconditionally_stable_l2: true, dimensions: "2"}
history:
  year: 1955
  people: [Donald W. Peaceman, Henry H. Rachford Jr., Jim Douglas Jr.]
  note: Peaceman and Rachford (1955) introduced the method for parabolic and elliptic problems in reservoir simulation. Douglas (1955) and Douglas and Rachford (1956) gave related ADI schemes, including ones for three dimensions.
prereqs: [crank-nicolson-method, thomas-algorithm]
see_also: [heat-equation, operator-splitting, method-of-lines, von-neumann-stability-analysis, backward-euler-method, finite-difference-method, a-stability, courant-friedrichs-lewy-condition]
sources:
  - paper: doi:10.1137/0103003
    title: "D. W. Peaceman and H. H. Rachford, Jr., The numerical solution of parabolic and elliptic differential equations, Journal of the Society for Industrial and Applied Mathematics 3 (1955) 28-41"
    locator: the alternating direction scheme with two half steps, its stability and its use as an iteration for elliptic problems
  - paper: "J. Douglas, Jr. and H. H. Rachford, Jr., On the numerical solution of heat conduction problems in two and three space variables, Transactions of the American Mathematical Society 82 (1956) 421-439"
    locator: the Douglas-Rachford scheme and three space dimensions
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 9 (diffusion in several space dimensions, locally one-dimensional and alternating direction implicit methods)
  - book: isbn:9780898715675
    title: John C. Strikwerda, Finite Difference Schemes and Partial Differential Equations, second edition, SIAM, 2004
    locator: Chapter 7 (alternating direction implicit methods, the Peaceman-Rachford scheme and its stability and accuracy)
---

The alternating direction implicit (ADI) method of Peaceman and Rachford solves the [heat equation](/heat-equation/) in two space dimensions, $u_t = \kappa(u_{xx} + u_{yy})$, on a rectangular grid. A [Crank-Nicolson](/crank-nicolson-method/) step in 2D would need the solution of a large sparse system that couples all grid points. ADI splits the step into two halves. The first half is implicit in $x$ and explicit in $y$, the second is implicit in $y$ and explicit in $x$. Each half is a set of independent tridiagonal systems, one per grid line, solved by the [Thomas algorithm](/thomas-algorithm/). The cost per step is therefore proportional to the number of grid points. The method keeps the second order accuracy and the unconditional $l^2$ stability of Crank-Nicolson. It differs from it only by a term of order $\Delta t^3$ per step.

## In plain words

Picture a heated metal plate whose temperature is known on a grid. An implicit step that treats both directions at once would have to solve for all grid points together, which is slow. ADI does the work in two passes. In the first pass it looks along each row of the grid. It treats heat flow along the row as unknown and heat flow across rows as known from the old values. Each row is then a simple chain of equations. In the second pass it does the same along each column with the roles swapped. Both passes are cheap. Alternating the direction balances the errors, so the combined step is as accurate as the expensive one and stays stable for large time steps.

## The problem

**Notation.** The unknown is $u(x, y, t)$ on $[0, \ell_x] \times [0, \ell_y]$ for $0 \le t \le T$, with $u_t = \kappa(u_{xx} + u_{yy})$, $\kappa \ge 0$, initial data $u_0(x, y)$ and either $u = 0$ on the boundary (Dirichlet) or zero normal derivative (Neumann). The grid is $x_i = i\Delta x$ with $\Delta x = \ell_x/m_x$, $y_j = j\Delta y$ with $\Delta y = \ell_y/m_y$, and $t_n = n\Delta t$. The grid values are $U^n_{ij} \approx u(x_i, y_j, t_n)$. Let $r_x = \kappa\Delta t/\Delta x^2$ and $r_y = \kappa\Delta t/\Delta y^2$. Let $\delta_x^2$ and $\delta_y^2$ be the second differences in each direction. Errors and stability are stated in the discrete $l^2$ norm $\|U\| = (\Delta x\Delta y\sum_{ij}U_{ij}^2)^{1/2}$ or in the max norm, as stated in each claim.

One step of the Peaceman-Rachford scheme is
$$\big(I - \tfrac{r_x}{2}\delta_x^2\big)U^* = \big(I + \tfrac{r_y}{2}\delta_y^2\big)U^n, \qquad \big(I - \tfrac{r_y}{2}\delta_y^2\big)U^{n+1} = \big(I + \tfrac{r_x}{2}\delta_x^2\big)U^*.$$
The intermediate value $U^*$ is an approximation at $t_{n+1/2}$. The implementation takes $N = \lceil T/\Delta t\rceil$ equal steps of size $T/N$.

## The algorithm

```pseudo id=main
ADI(u0, κ, ℓx, ℓy, T, mx, my, Δt)
L1  Δx ← ℓx/mx, Δy ← ℓy/my, N ← ⌈T/Δt⌉, Δt ← T/N, rx ← κΔt/Δx², ry ← κΔt/Δy², U ← u0 on the grid
L2  for n ← 0 to N − 1 do
L3      for each grid row j do d_i ← U_ij + (ry/2)·(U_{i,j−1} − 2U_ij + U_{i,j+1}) for the unknown i
L4          solve −(rx/2)·U*_{i−1,j} + (1 + rx)·U*_ij − (rx/2)·U*_{i+1,j} = d_i by the Thomas algorithm
L5      for each grid column i do d_j ← U*_ij + (rx/2)·(U*_{i−1,j} − 2U*_ij + U*_{i+1,j}) for the unknown j
L6          solve −(ry/2)·U_{i,j−1} + (1 + ry)·U_ij − (ry/2)·U_{i,j+1} = d_j by the Thomas algorithm, giving U^{n+1}
L7  return U
```

Lines L3 and L4 are the half step implicit in $x$. Lines L5 and L6 are the half step implicit in $y$. All matrices are tridiagonal, symmetric (after scaling the boundary rows in the Neumann case) and strictly diagonally dominant, so no pivoting is needed. They are the same for every step and could be factored once. For zero-flux boundaries the ghost values are $U_{-1,j} = U_{1,j}$ and so on, exactly as in the one-dimensional Crank-Nicolson code.

## Example

**One step by hand.** Take $\kappa = 1$ on the unit square with $m_x = m_y = 4$, $\Delta t = 1/16$ (so $r_x = r_y = 1$) and $u_0 = \sin\pi x\sin\pi y$. The second difference of $\sin(\pi y_j)$ is $-4s\sin(\pi y_j)$ with $s = \sin^2(\pi/8) = 0.146447$. So the right side of L3 is $(1 - 2s)U^n$, and the row solves divide by $1 + 2s$: $U^* = \tfrac{1 - 2s}{1 + 2s}U^n = 0.546918\,U^n$. The second half step multiplies by the same factor. At the centre, $U^1_{22} = 0.546918^2 = 0.299119$, against the exact $e^{-2\pi^2/16} = 0.291213$.

**Convergence.** With $u_0 = \sin\pi x\sin\pi y$, $T = 0.1$ and $\Delta t = \Delta x/5$, the max-norm error at $T$ is:

| $m_x = m_y$ | $r_x = r_y$ | error | $\log_2$ of the ratio |
|---|---|---|---|
| 8 | 1.6 | $2.1720 \cdot 10^{-3}$ | |
| 16 | 3.2 | $5.3561 \cdot 10^{-4}$ | 2.020 |
| 32 | 6.4 | $1.3344 \cdot 10^{-4}$ | 2.005 |
| 64 | 12.8 | $3.3332 \cdot 10^{-5}$ | 2.001 |

The explicit scheme (forward Euler in time) would need $r_x + r_y \le 1/2$, that is $r \le 1/4$ on a square grid. In the tests it blows up at $r = 0.3$ within 300 steps, while ADI with the same step is fine.

## Correctness

The proofs are in `proofs/correctness.md`. In summary:

1. **Factored form.** Eliminating $U^*$ gives $(I - A)(I - B)U^{n+1} = (I + A)(I + B)U^n$, with $A = \tfrac{r_x}{2}\delta_x^2$ and $B = \tfrac{r_y}{2}\delta_y^2$. This differs from 2D Crank-Nicolson, $(I - A - B)U^{n+1} = (I + A + B)U^n$, by the term $AB(U^{n+1} - U^n)$. That term is $O(\Delta t^3)$ for smooth solutions. This is proved.
2. **Stability.** On the rectangle, $A$ and $B$ are symmetric and commute. Their common eigenvectors are products of sines (Dirichlet) or cosines (Neumann). A product mode is multiplied by $g = \frac{1 - 2r_xs_x}{1 + 2r_xs_x}\cdot\frac{1 - 2r_ys_y}{1 + 2r_ys_y}$, with $|g| \le 1$. So the $l^2$ norm never grows, for every $\Delta t$. This is proved, and the tests check $g$ to rounding error.
3. **Convergence.** Consistency of order $O(\Delta t^2 + \Delta x^2 + \Delta y^2)$ together with this stability gives convergence of the same order in $l^2$. The max-norm order 2 in the table is observed.
4. **Conservation.** With zero-flux boundaries, the trapezoidal total heat is the same after each half step, exactly in exact arithmetic.

## Complexity

The first half step solves one tridiagonal system of size about $m_x$ for each of about $m_y$ rows. The second solves one of size about $m_y$ for each of about $m_x$ columns. With the right sides, the cost is $\Theta(m_xm_y)$ operations per step and $\Theta(Nm_xm_y)$ in total, with $\Theta(m_xm_y)$ memory for $U$ and $U^*$. There is no Jacobian, since the problem is linear. A direct sparse solve for 2D Crank-Nicolson with nested dissection costs $\Theta((m_xm_y)^{3/2})$ to factor, although that factorization can be reused for every step. The explicit scheme costs $\Theta(m_xm_y)$ per step too, but needs $\Delta t \le \Delta x^2/(4\kappa)$ on a square grid. The rows (and the columns) are independent, so each half step parallelizes well.

## Properties

- **Second order in space and time,** with no restriction on $r_x$ and $r_y$ for $l^2$ stability.
- **Rough modes are damped slowly.** For large $r$ each factor of $g$ is close to $-1$ for high frequencies, so their product is close to $+1$. Modes that are rough in both directions then hardly decay and do not even change sign. In the tests, with zero-flux boundaries and $r = 5$, an initial hot block still shows a spread of $0.028$ at $t = 0.5$, against $0.0023$ with $r = 1$.
- **Exactly two dimensions.** The direct extension of Peaceman-Rachford to three dimensions with three one-third steps is not unconditionally stable. The Douglas-Rachford and Douglas-Gunn schemes are used there.
- **Needs a tensor product grid.** The splitting into lines needs a rectangle (or a union of rectangles) and an operator without mixed derivative terms. On other domains the operators $A$ and $B$ need not commute, and the stability proof fails.

## Variants and improvements

- **Douglas-Rachford.** $(I - 2A)U^* = (I + 2B)U^n$ in a backward Euler style, then $(I - 2B)U^{n+1} = U^* - 2BU^n$. It is first order in time, more strongly damping, and generalizes to three dimensions.
- **Douglas-Gunn and stabilizing corrections.** Approximate factorizations for three dimensions and for time-dependent boundary data.
- **Locally one-dimensional (LOD) splitting.** Apply Crank-Nicolson in $x$ and then in $y$. It is simpler but needs Strang ordering to be second order. See [operator splitting](/operator-splitting/).
- **ADI iteration for elliptic problems.** Peaceman and Rachford's original goal. The steady state of the iteration solves the Poisson equation, and a cycle of well-chosen parameters $r_k$ makes it converge very fast.
- **Boundary data.** For non-zero, time-dependent Dirichlet data the intermediate value $U^*$ needs boundary values that are consistent with the factored form. Taking $u$ at $t_{n+1/2}$ loses accuracy near the boundary.

## When to use it

Use ADI for diffusion problems on rectangular grids in two dimensions, when an explicit scheme would need too many steps and a full sparse solve is too costly or too complicated. Typical cases are heat conduction in plates, reservoir pressure equations, and the two-factor Black-Scholes equation. Use the Douglas-type schemes in three dimensions. With rough initial data and large $r$, start with a few backward Euler steps or keep $r$ moderate.

## Pitfalls

- **Rough data and large $r$.** Rough modes decay very slowly, as in the properties above. This is a property of the scheme, not of the heat equation.
- **Boundary values of $U^*$.** In the code the boundary values are 0, which is consistent. With non-zero data, naive values at $t_{n+1/2}$ reduce the order to 1 near the boundary.
- **Mixed derivatives and variable coefficients.** A term $u_{xy}$ cannot be split into one-dimensional parts. Variable coefficients break the commutation, so the clean stability proof no longer applies.
- **Three dimensions.** Do not extend Peaceman-Rachford naively. Use a Douglas-type scheme.
- **Steps that do not divide $T$.** The implementation shortens all steps slightly so they stay equal, because a change of $\Delta t$ changes all matrices.

## Implementations

## History

Peaceman and Rachford (1955) worked on oil reservoir simulation at the Humble Oil company. They introduced the alternating direction scheme both as a time stepping method and as an iteration for the elliptic pressure equation. Douglas (1955) and Douglas and Rachford (1956) studied related schemes, including the three-dimensional case, and Douglas and Gunn (1964) gave a general framework. In the 1960s, Wachspress and others studied how to choose the iteration parameters for the elliptic case. ADI schemes are still widely used in computational finance and in heat transfer codes.

## References
