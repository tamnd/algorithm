---
tag: Z4ZSZ2
kind: algorithm
slug: eno-scheme
name: ENO schemes
aliases:
- essentially non-oscillatory schemes
area: scientific-computing/conservation-laws-and-shock-capturing
level: advanced
summary: Builds a high order reconstruction from the stencil with the smoothest data, chosen by divided differences, so that shocks cause almost no oscillations.
solves: [riemann-problem, euler-equations-of-gas-dynamics]
model: real-ram
complexity:
  vars: {M: "the number of cells", m: "the number of conserved components", r: "the order of the reconstruction", K: "the number of time steps (O(M) for a fixed end time and Courant number)"}
  time: {worst: "O(r^3 m M K)"}
  space: {extra: "O(m M)"}
properties: {deterministic: true, explicit: true, conservative: true, order: "r on smooth solutions", tvd: "no; overshoots are small", positive: "not guaranteed"}
history:
  year: 1987
  people: [Ami Harten, Bjorn Engquist, Stanley Osher, Sukumar R. Chakravarthy, Chi-Wang Shu]
  note: Harten, Engquist, Osher and Chakravarthy (1987) gave ENO reconstruction with adaptive stencils. Shu and Osher (1988, 1989) gave the efficient finite difference form and the TVD Runge-Kutta time steppers.
prereqs: [divided-differences, finite-volume-method, rusanov-flux, strong-stability-preserving-runge-kutta]
see_also: [weno-scheme, muscl-scheme, piecewise-parabolic-method, newton-interpolation, godunov-order-barrier, total-variation-diminishing, kurganov-tadmor-scheme]
sources:
  - paper: "Ami Harten, Bjorn Engquist, Stanley Osher and Sukumar R. Chakravarthy, Uniformly high order accurate essentially non-oscillatory schemes, III, Journal of Computational Physics 71(2) (1987) 231-303"
    locator: reconstruction from cell averages by the primitive function, with the stencil chosen by divided differences; doi:10.1016/0021-9991(87)90031-3
  - paper: "Chi-Wang Shu and Stanley Osher, Efficient implementation of essentially non-oscillatory shock-capturing schemes, Journal of Computational Physics 77(2) (1988) 439-471"
    locator: the TVD Runge-Kutta methods used for the time steps and the method of lines form of ENO; doi:10.1016/0021-9991(88)90177-5
  - paper: "Chi-Wang Shu and Stanley Osher, Efficient implementation of essentially non-oscillatory shock-capturing schemes, II, Journal of Computational Physics 83(1) (1989) 32-78"
    locator: the continuation of the 1988 paper with further forms and tests of finite difference ENO schemes; doi:10.1016/0021-9991(89)90222-2
---

ENO (essentially non-oscillatory) schemes reach any order $r$ on smooth solutions of [hyperbolic conservation laws](/hyperbolic-conservation-law/) and still capture shocks without large oscillations. A fixed stencil of $r$ cells cannot do this: near a shock its polynomial overshoots, and by the [Godunov order barrier](/godunov-order-barrier/) no linear scheme above first order avoids new extrema. ENO makes the stencil depend on the data. In each cell it grows a stencil of $r$ cells one cell at a time, always toward the side where the [divided differences](/divided-differences/) are smaller, so the stencil stays on the smooth side of a jump. The reconstructed face values then go into a two-point flux, and a strong stability preserving Runge-Kutta method advances the cell averages.

## In plain words

To guess the values at the edges of a cell from the cell averages, fit a polynomial through a few neighbor cells. If the neighbors include a shock, the fit wiggles. So pick the neighbors with care. Start with the cell itself. Then try adding one more cell on the left or on the right, and keep the choice where the data look smoother, measured by how large the differences are. Repeat until there are $r$ cells. Next to a shock, the stencil leans away from the shock. Far from shocks, any choice is accurate.

## The problem

Given cell averages $v_i$ on a uniform grid with width $h$, compute the values $v^-_{i+1/2}$ and $v^+_{i-1/2}$ at the two faces of each cell with error $O(h^r)$ where the data are smooth, without oscillations at isolated jumps. Use them in a conservative scheme for $U_t + F(U)_x = 0$. The page uses scalar laws and the [Euler equations](/euler-equations-of-gas-dynamics/) with $U = (\rho, \rho u, E)$ and $\gamma = 1.4$. The values are cell averages, so errors are measured against exact cell averages.

## The algorithm

```pseudo id=main
ENO-RATE(v, h, F, SPEED, r)
L1  add r ghost cells on each side (copy for outflow, wrap for periodic)
L2  for each cell i: s <- i                                           ▷ the stencil is {s, ..., s+l-1}
L3      for l = 1 to r-1: if |Δ^l v_{s-1}| < |Δ^l v_s| then s <- s-1   ▷ add the smoother side
L4      v^-_{i+1/2}, v^+_{i-1/2} <- derivative at the two faces of cell i of the Newton interpolant of the primitive on the faces of {s, ..., s+r-1}
L5  for each face: H_{i+1/2} <- (F(v^-) + F(v^+))/2 - (a/2)(v^+ - v^-),  a = max(SPEED(v^-), SPEED(v^+))
L6  return L_i = -(H_{i+1/2} - H_{i-1/2}) / h
L7  advance dv/dt = L(v) with the SSP RK3 of Shu and Osher
```

$\Delta^l v_a$ is the $l$-th undivided difference of the averages over the cells $a, \dots, a + l$, which is a multiple of a divided difference of the primitive function $V(x) = \int^x u$. The primitive is known exactly at the faces from sums of averages, and its derivative is the point value of $u$. So line L4 is an exact linear map from $r$ averages to a face value, with weights that depend only on $r$ and the shift $k = i - s$. For $r = 3$ the right face weights are $(\frac13, \frac56, -\frac16)$, $(-\frac16, \frac56, \frac13)$ and $(\frac13, -\frac76, \frac{11}6)$ for $k = 0, 1, 2$. The code computes the weights once, in `Fraction`. Line L5 is the [Rusanov flux](/rusanov-flux/). For systems the code reconstructs each conserved component separately. The time step is $\Delta t = 0.5\,h/\max_i(|u_i| + c_i)$.

## Example

**One reconstruction by hand.** Take $r = 3$, outflow boundaries and $v = (0, 0, 1, 3, 4, 4)$. In cell 3 (value 1), the first differences are $1$ on the left and $2$ on the right, so the left cell joins: $\{2, 3\}$. The second differences are $1 - 2\cdot 0 + 0 = 1$ over $\{1, 2, 3\}$ and $3 - 2\cdot 1 + 0 = 1$ over $\{2, 3, 4\}$. The test is strict, so the right cell joins and the stencil is $\{2, 3, 4\}$ with $k = 1$. The face values are

$$v^-_{3+1/2} = -\tfrac16\cdot 0 + \tfrac56\cdot 1 + \tfrac13\cdot 3 = \tfrac{11}6, \qquad v^+_{3-1/2} = \tfrac13\cdot 0 + \tfrac56\cdot 1 - \tfrac16\cdot 3 = \tfrac13.$$

In cell 4 the stencil is $\{4, 5, 6\}$ and the face values are $\frac{13}6$ and $\frac{11}3$. Over all cells, from the left ghost cell, the right face values are $(0, 0, 0, \frac{11}6, \frac{11}3, 4, 4, 4)$ and the left face values are $(0, 0, 0, \frac13, \frac{13}6, 4, 4, 4)$. The test checks both lists exactly in `Fraction` arithmetic. The values at the face between cells 3 and 4 differ ($\frac{11}6$ and $\frac{13}6$), and the Rusanov flux handles the jump.

**Smooth advection.** For $u_t + u_x = 0$ with the cell averages of $\sin(2\pi x)$, Courant number 0.5 and one period, these $L^1$ errors are measurements made with the code on this page.

| $r$ | $M = 20$ | $M = 40$ | $M = 80$ | orders |
|---|---|---|---|---|
| 1 | 0.3989069 | 0.2477481 | 0.1391560 | 0.69, 0.83 |
| 2 | 0.1020351 | 0.0452852 | 0.0133387 | 1.17, 1.76 |
| 3 | 0.0107088 | 0.0013658 | 0.0001714 | 2.97, 2.99 |

For $r = 2$ the stencil choice acts like the minmod limiter at the extrema, so the order approaches 2 slowly. For the Euler wave $\rho = 1 + 0.2\sin(2\pi(x - t))$, $u = 1$, $p = 1$ to $t = 0.1$, $r = 3$ gives the errors 0.00022819, 0.0000289 and 0.00000362 at $M = 25, 50, 100$ (orders 2.98 and 3.00).

**Sod's tube.** On $[0, 1]$ with the jump at $x = 0.5$ and outflow boundaries, to $t = 0.2$, the $L^1$ density errors are:

| cells $M$ | steps | $r = 1$ | $r = 2$ | $r = 3$ |
|---|---|---|---|---|
| 100 | 82 to 87 | 0.025915 | 0.009678 | 0.007662 |
| 200 | 170 to 174 | 0.018100 | 0.005508 | 0.004379 |

With $r = 1$ the scheme is the first order Rusanov scheme. The central flux of line L5 smears the contact, so these errors are larger than those of [MUSCL-Hancock](/muscl-scheme/) with HLLC (0.00585 at $M = 100$).

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Theorem: for every stencil the rule can choose, the face values are exact for polynomials of degree $r - 1$, so for smooth data the error is $O(h^r)$, and the stencil choice does not affect the order. For piecewise constant data with jumps at least $r$ cells apart, every chosen stencil lies inside one constant piece, so the face values have no overshoot. The scheme is conservative and consistent, so by the [Lax-Wendroff theorem](/lax-wendroff-theorem/) bounded $L^1$ limits are weak solutions.

ENO is not TVD, and no bound on the growth of the total variation is proved here. On a square wave with $r = 3$, the test measures a new maximum $2.6 \times 10^{-5}$ above the old one after 80 steps.

## Complexity

Theorem, in the [real-RAM](/real-ram/) model: the stencil choice in one cell computes $r - 1$ pairs of undivided differences, and the code computes the $l$-th one from scratch in $O(l^2)$ operations, so a cell costs $O(r^3)$ per component. Keeping a table of all differences once per step lowers this to $O(r^2)$ and the face values cost $O(r)$. One rate evaluation is $O(r^3 mM)$ in the code, and SSP RK3 uses three. A fixed end time at a fixed Courant number needs $K = O(M)$ steps. The weights are computed once for each pair $(r, k)$, at a cost that does not depend on $M$.

## Properties

- **Order $r$ on smooth solutions.** Proved for the reconstruction; measured for the scheme with $r = 3$.
- **Almost no oscillations.** Exactly none for isolated jumps in piecewise constant data, as proved; small overshoots of order $10^{-5}$ in the square wave test.
- **Conservative.** Exact in rational arithmetic; the test checks it in `Fraction` for Burgers' equation.
- **Not TVD.** The total variation can grow by a small amount.
- **Nonsmooth in the data.** The stencil choice switches discretely, so the scheme is not a differentiable function of the averages, and in smooth regions small changes in the data can switch stencils.

## Variants and improvements

- **[WENO](/weno-scheme/).** Instead of one stencil, take a convex combination of all $r$ candidates with weights that depend on smoothness. In smooth regions this gives order $2r - 1$, and the result is a smooth function of the data.
- **Finite difference ENO on fluxes.** Shu and Osher (1988, 1989) reconstruct the flux values at points instead of averages, which is cheaper in several dimensions.
- **Characteristic decomposition.** For systems, reconstructing in characteristic variables gives cleaner shocks than the componentwise reconstruction used here.
- **Upwind fluxes.** Replacing the Rusanov flux of line L5 with an upwind Riemann solver such as HLLC sharpens contacts.

## When to use it

Use ENO with $r = 3$ when smooth parts of the flow need third order accuracy and shocks must stay clean, and the cost of a wider stencil is acceptable. In most new codes WENO has replaced ENO, because it is more accurate for the same stencil and smooth in the data. ENO is still a clear way to learn adaptive stencils, and it is the base of WENO.

## Pitfalls

- **Ties in the test.** With a strict comparison the stencil leans to the right when the two differences are equal. Both choices are valid, but the code and the hand trace must agree.
- **Too few ghost cells.** Order $r$ needs $r$ ghost cells on each side, because the stencil of a boundary face can reach $r - 1$ cells past the end of the grid.
- **Time stepping of low order.** Forward Euler limits the scheme to first order in time. Use SSP RK3 for $r = 3$.
- **Stencil switching on smooth data.** Near zeros of the derivatives of $u$, small changes in the data switch the stencil. Near extrema the choice also cuts the slope, like a limiter, which is why $r = 2$ shows the orders 1.17 and 1.76 in the table above.

## Implementations

## History

Harten, Engquist, Osher and Chakravarthy (1987) gave the reconstruction from cell averages through the primitive function, with the stencil chosen by divided differences. Shu and Osher (1988, 1989) gave a finite difference form on point values of fluxes, which is cheaper in several dimensions, together with the TVD Runge-Kutta methods now known as SSP methods. WENO schemes, which combine the same candidate stencils with smooth weights, followed in the 1990s.

## References
