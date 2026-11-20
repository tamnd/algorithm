---
tag: 4Q3HCS
kind: algorithm
slug: piecewise-parabolic-method
name: Piecewise parabolic method
aliases:
- Colella-Woodward method
area: scientific-computing/conservation-laws-and-shock-capturing
level: advanced
summary: Reconstructs a monotone parabola in each cell with steepening at contacts, a high order Godunov scheme for gas dynamics.
solves: [riemann-problem, euler-equations-of-gas-dynamics]
model: real-ram
complexity:
  vars: {M: "the number of cells", m: "the number of conserved components", K: "the number of time steps (O(M) for a fixed end time and Courant number)"}
  time: {worst: "O(m M K)"}
  space: {extra: "O(m M)"}
properties: {deterministic: true, explicit: true, conservative: true, order: "between 2 and 3 on smooth solutions with extrema; fourth order face values", tvd: "for linear advection with Courant number at most 1", positive: "not guaranteed"}
history:
  year: 1984
  people: [Phillip Colella, Paul R. Woodward]
  note: Colella and Woodward (1984) replaced the straight lines of MUSCL with limited parabolas and added contact steepening and flattening near strong shocks.
prereqs: [muscl-scheme, godunov-method, finite-volume-method]
see_also: [eno-scheme, weno-scheme, hll-riemann-solver, exact-riemann-solver, strong-stability-preserving-runge-kutta, total-variation-diminishing, adaptive-mesh-refinement]
sources:
  - paper: "Phillip Colella and Paul R. Woodward, The piecewise parabolic method (PPM) for gas-dynamical simulations, Journal of Computational Physics 54(1) (1984) 174-201"
    locator: the interpolation of face values, the monotonicity tests on the parabolas, the scheme for linear advection, and the gas dynamics scheme with contact steepening and flattening; doi:10.1016/0021-9991(84)90143-8
  - paper: "Chi-Wang Shu and Stanley Osher, Efficient implementation of essentially non-oscillatory shock-capturing schemes, Journal of Computational Physics 77(2) (1988) 439-471"
    locator: the TVD (SSP) Runge-Kutta method of third order used for the Euler runs on this page; doi:10.1016/0021-9991(88)90177-5
---

The piecewise parabolic method (PPM) is a finite volume scheme for [hyperbolic conservation laws](/hyperbolic-conservation-law/) that gives each cell a parabola instead of the straight line of [MUSCL](/muscl-scheme/). The parabola has the cell average as its mean and matches face values from a fourth order interpolation. Three simple tests then change the face values so that the parabola is monotone in the cell and stays inside the range of the neighbors. For linear advection, moving the parabolas exactly gives a scheme that is [TVD](/total-variation-diminishing/) and sharper than MUSCL. For gas dynamics, Colella and Woodward add a steeper reconstruction at contacts and flattening near strong shocks, and the scheme is much used in astrophysics codes.

## In plain words

A straight line in each cell cannot follow a curved profile well, so make it a parabola. Pick the values at the cell edges first, by fitting a cubic through four neighbor averages and reading off its value at the edge. Then fit the parabola in each cell with those two edge values and the cell average. If the cell is a local peak or dip, the parabola would overshoot, so make it flat. If the parabola would turn around inside the cell, pull the edge value on the far side toward the average until it no longer turns. What remains moves along with the flow.

## The problem

Given cell averages $a_j$ of $u_t + f(u)_x = 0$ on a uniform grid with width $h$, find a reconstruction that is accurate for smooth data and creates no new extrema, and use it in a conservative update. The page treats linear advection $u_t + cu_x = 0$ with $c > 0$ in full, and uses the same reconstruction for the [Euler equations](/euler-equations-of-gas-dynamics/) with $U = (\rho, \rho u, E)$ and $\gamma = 1.4$. The values are cell averages, so errors are measured against exact cell averages.

## The algorithm

```pseudo id=main
PPM-ADVECTION-STEP(a, ν)                                   ▷ u_t + c u_x = 0, c > 0, ν = cΔt/h ≤ 1
L1  add three ghost cells on each side (wrap for periodic, copy for outflow)
L2  δa_j <- MC slope: minmod((a_{j+1} - a_{j-1})/2, 2(a_j - a_{j-1}), 2(a_{j+1} - a_j))
L3  a_{j+1/2} <- (a_j + a_{j+1})/2 - (δa_{j+1} - δa_j)/6         ▷ 7/12 and -1/12 when no slope is limited
L4  for each cell: a_L, a_R <- a_{j-1/2}, a_{j+1/2}, changed by the three monotonicity tests
L5  F_{j+1/2} <- a_R - (ν/2)(Δa - (1 - 2ν/3) a_6),  Δa = a_R - a_L,  a_6 = 6(a_j - (a_L + a_R)/2)
L6  a_j <- a_j - ν(F_{j+1/2} - F_{j-1/2})
```

The parabola in cell $j$ is $P(\xi) = a_L + \xi(\Delta a + a_6(1 - \xi))$ for $\xi \in [0, 1]$, and its mean is $a_j$. The three tests of line L4 are:

1. if $a_j$ is not strictly between $a_L$ and $a_R$, set $a_L = a_R = a_j$ (flat at extrema);
2. if the parabola would turn inside the cell near the left edge, set $a_L = 3a_j - 2a_R$;
3. if it would turn near the right edge, set $a_R = 3a_j - 2a_L$.

Line L5 is $c$ times the average of $P$ over the right part $[1 - \nu, 1]$ of the cell, which is the amount that crosses the face in one step divided by $c\Delta t$. For the Euler equations, the code computes $a_L$ and $a_R$ for each conserved component with lines L1 to L4, puts the values on the two sides of each face into the [HLL](/hll-riemann-solver/) flux with Davis speeds, and integrates with SSP RK3 at Courant number 0.5. This is a method of lines form. The original gas dynamics PPM instead traces characteristics through the parabolas to get time averaged face states for an exact Riemann solver, and adds contact steepening and flattening; the code leaves these out.

## Example

**One step by hand.** Take $a = (0, 0, 1, 3, 4, 4)$, outflow boundaries and $\nu = \frac12$. The MC slopes are $\frac32$ in cells 3 and 4 and zero elsewhere. Line L3 gives the face values $\frac12 - \frac14 = \frac14$ between cells 2 and 3, $2$ between cells 3 and 4, and $\frac72 + \frac14 = \frac{15}4$ between cells 4 and 5. In cell 3, $a_L = \frac14$, $a_R = 2$ and $a_3 = 1$; then $\Delta a = \frac74$ and $a_6 = 6(1 - \frac98) = -\frac34$, so the tests do not apply ($|a_6| \le |\Delta a|$). The flux out of cell 3 is $2 - \frac14(\frac74 + \frac23\cdot\frac34) = \frac{23}{16}$, and the new value is $1 - \frac12\cdot\frac{23}{16} = \frac9{32}$. The whole step gives $(0, 0, \frac9{32}, 2, \frac{119}{32}, 4)$. The test checks the face values and the step exactly in `Fraction` arithmetic. MUSCL with MC gives $\frac5{16} = \frac{10}{32}$ in cell 3 on the same data.

**Smooth advection.** For the cell averages of $\sin(2\pi x)$, $\nu = 0.5$ and one period, these $L^1$ errors are measurements made with the code on this page.

| $M$ | 20 | 40 | 80 | 160 |
|---|---|---|---|---|
| error | 0.0189537 | 0.0039237 | 0.0007292 | 0.0001404 |
| order | | 2.27 | 2.43 | 2.38 |

The orders lie between 2 and 3: the face values are fourth order, but test 1 flattens the parabolas at the crest and the trough. On the same runs, the MUSCL-Hancock code of the MUSCL page with the MC limiter has the errors 0.0228951, 0.0056305, 0.0012618 and 0.0002487, so PPM is better by a factor between 1.2 and 1.8. For a square wave on 100 cells after one period at $\nu = 0.5$, the $L^1$ error is 0.01941 for PPM and 0.02862 for MUSCL with MC.

**Euler equations.** For $\rho = 1 + 0.2\sin(2\pi(x - t))$, $u = 1$, $p = 1$ on a periodic grid to $t = 0.1$, the $L^1$ density errors at $M = 25, 50, 100$ are 0.00124528, 0.00030744 and 0.00007047 (orders 2.02 and 2.13). For Sod's tube to $t = 0.2$, the $L^1$ density error is 0.005261 at $M = 100$ (87 steps) and 0.002812 at $M = 200$ (175 steps). The MUSCL page reports 0.00462 and 0.00265 for MUSCL-Hancock with the HLLC flux and the van Leer limiter. So this method of lines form, with the HLL flux and without contact steepening, does not do better than MUSCL on Sod's tube; the gain of PPM shows on the advection runs above.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Theorem: with the MC slopes, every face value lies between its two neighbor averages. After the three tests each parabola has the cell average as its mean, is monotone, and stays between the smallest and the largest of the three averages around it. The piecewise parabolic function then has exactly the total variation of the averages. For linear advection with $0 \le \nu \le 1$, the step is the exact average of the moved parabolas, so it is conservative, TVD, and makes no new extrema; at $\nu = 1$ it is the exact shift.

The order of accuracy is measured, not proved. For the Euler equations no TVD or positivity property is proved here.

## Complexity

Theorem, in the [real-RAM](/real-ram/) model: lines L2 to L6 do a constant amount of work per cell and component, so one step costs $O(mM)$ and keeps $O(mM)$ numbers. A fixed end time at a fixed Courant number needs $K = O(M)$ steps. Per step PPM costs a small constant factor more than MUSCL, and for the Euler runs here the SSP RK3 time stepper adds three flux evaluations per face and step.

## Properties

- **Fourth order face values, flat at extrema.** Exact for cubics where no slope is limited; the order on smooth data with extrema is between 2 and 3.
- **TVD for linear advection** with $\nu \le 1$, and exact at $\nu = 1$. Proved.
- **Conservative.** The parabola has the cell average as its mean, and the fluxes telescope.
- **Low numerical diffusion.** On the advection runs of the example, PPM has a smaller error than MUSCL with the MC limiter, for both the sine and the square wave.
- **Not positivity preserving** for the Euler equations in general.

## Variants and improvements

- **Contact steepening and flattening.** Colella and Woodward steepen the face values at contacts, detected from the density and pressure, and flatten the parabolas behind strong shocks to reduce oscillations there.
- **Characteristic tracing.** For systems, the original scheme averages the parabolas over the domain of dependence of each characteristic family and solves a Riemann problem with the time averaged states.
- **Better treatment of smooth extrema.** Later work changes test 1 so that smooth peaks are not flattened, which restores higher order there.
- **Method of lines.** The face values of lines L1 to L4 can be used with any Riemann flux and Runge-Kutta method, as the code does for the Euler equations.

## When to use it

Use PPM for gas dynamics with strong shocks and contacts where low numerical diffusion matters, for example in astrophysical codes with [adaptive mesh refinement](/adaptive-mesh-refinement/). For a simpler code, MUSCL with a good limiter is often enough. For very high order on smooth flows, use [WENO](/weno-scheme/).

## Pitfalls

- **Unlimited face values.** The fourth order interpolation alone overshoots at jumps. Lines L2 and L4 are both needed.
- **Extrema are flattened.** Test 1 cuts smooth peaks to a constant, so the max norm error at extrema is first order. This is by design and not a bug.
- **Three ghost cells.** The face values need slopes, which need neighbors, so the stencil reaches three cells past each face.
- **Courant number above 1.** Line L5 assumes the part that crosses the face comes from one cell only.
- **Calling the method of lines form PPM without saying so.** The code's Euler runs use only the reconstruction. Results differ from the full gas dynamics scheme near contacts and strong shocks.

## Implementations

## History

Van Leer's MUSCL (1979) used limited straight lines in each cell. Colella and Woodward (1984) used parabolas, with face values from a fourth order interpolation of the primitive function and three monotonicity tests. For gas dynamics they gave both a Lagrangian scheme with a remap and a direct Eulerian scheme, each with contact steepening and flattening near strong shocks. PPM is used in several astrophysics codes.

## References
