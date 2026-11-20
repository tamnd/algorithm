---
tag: BK5R80
kind: algorithm
slug: finite-difference-migration
name: Finite-difference migration
aliases:
- 15-degree migration
- Claerbout migration
area: imaging-and-inverse-problems/seismic-imaging
level: advanced
summary: "Downward continue the wavefield with a finite difference solver of a one-way paraxial wave equation, which handles lateral velocity changes."
solves: [seismic-migration]
model: real-ram
complexity:
  vars: {t: "the number of time samples", x: "the number of traces", z: "the number of depth steps"}
  time: {per_step: "O(x)", total: "O(z t x + x t log t)"}
  space: {extra: "O(t x + z x)"}
properties: {deterministic: true, lateral_velocity: true, unconditionally_stable: true, exact_for: "vertical waves", angle_limit: "about 15 degrees for small error"}
history:
  year: 1972
  people: [Jon F. Claerbout, Stephen M. Doherty]
  note: Claerbout introduced migration by finite differences of a one-way wave equation in 1971, and Claerbout and Doherty (1972) gave the downward continuation scheme for zero-offset sections with the 15-degree equation.
prereqs: [phase-shift-migration, thomas-algorithm, crank-nicolson-method]
see_also: [phase-shift-migration, split-step-fourier-migration, reverse-time-migration, crank-nicolson-method, thomas-algorithm, diagonally-dominant-matrix, finite-difference-method, seismic-migration]
sources:
  - paper: doi:10.1190/1.1440298
    title: Jon F. Claerbout and Stephen M. Doherty, Downward continuation of moveout-corrected seismograms, Geophysics 37(5), 1972, 741 to 768
    locator: the finite-difference downward continuation of the 15-degree equation
  - paper: doi:10.1190/1.1440185
    title: Jon F. Claerbout, Toward a unified theory of reflector mapping, Geophysics 36(3), 1971, 467 to 481
    locator: the one-way wave equation and the imaging principle
  - book: isbn:9780865423046
    title: Jon F. Claerbout, Imaging the Earth's Interior, Blackwell Scientific, 1985
    locator: the chapters on the 15-degree equation, its Crank-Nicolson solution and its dispersion
  - book: isbn:9781560800941
    title: Oz Yilmaz, Seismic Data Analysis, Society of Exploration Geophysicists, 2001
    locator: Chapter 4 (migration), finite-difference migration and its angle limits
---

Finite-difference migration continues the recorded wavefield down into the ground with a finite-difference solver of a one-way paraxial wave equation. For each frequency it replaces the square root $\sqrt{1 - (v' k_x/\omega)^2}$ of the exact one-way equation by its Taylor polynomial $1 - (v' k_x/\omega)^2/2$, which gives the 15-degree equation $\partial_z P = i(\omega/v')P + i(v'/(2\omega))\partial_x^2 P$. Each depth step applies a thin lens $e^{i\omega\Delta z/v'}$ and one [Crank-Nicolson](/crank-nicolson-method/) step of the second term, a tridiagonal system solved by the [Thomas algorithm](/thomas-algorithm/) in $O(n_x)$. Because the velocity enters point by point, the method handles lateral velocity changes. The step is unitary for every $\Delta z$ (a theorem), and the error grows with the propagation angle: 0.06 percent at 15 degrees and 6 percent at 45 degrees (a theorem for plane waves in constant velocity).

## In plain words

The method moves the recorded wave down into the ground one depth step at a time, one frequency at a time. Each step has two parts. First every point is delayed by the time the wave needs to cross the step at the local speed, as if it went straight down. Then a small correction lets the wave spread sideways, which is how a slanted wave moves. The correction links each point only to its two neighbors, so it is a short chain of equations that a simple elimination solves quickly. The method is cheap and allows the speed to change from point to point, but the sideways correction is an approximation that is good only for waves close to vertical.

## The problem

Given a zero-offset section $d(t, x)$ and a velocity $v(x, z)$ on the image grid ($v_i[j]$ for the layer $i\Delta z \le z < (i + 1)\Delta z$ at $x_j$), find the image $m(x, z)$. This is [seismic migration](/seismic-migration/) in the [exploding reflector model](/exploding-reflector-model/), with the half velocity $v' = v/2$.

## The algorithm

The time transform is $U(\omega) = \sum_t u(t)e^{-i\omega t}$, and $T = \operatorname{tridiag}(1, -2, 1)$ is the second difference along $x$ with $P = 0$ outside the grid. The Crank-Nicolson step of $\partial_z P = i(v'/(2\omega))\partial_x^2 P$ is $(I - \frac{i}{2}BT)P_{\text{new}} = (I + \frac{i}{2}BT)P$ with $B = \operatorname{diag}(b_j)$.

```pseudo id=main
FINITE-DIFFERENCE-MIGRATION(d, Δt, Δx, Δz, v)     ▷ v[i][j]: velocity of layer i at x_j
L1  P_k ← DFT in time of every trace, for every frequency index k
L2  for every frequency ω = ω_k with 0 < ω_k < the Nyquist frequency do      ▷ p ← P_k
L3      for i ← 0 to n_z - 1 do
L4          image[i] ← image[i] + (2 / n_t) Re p
L5          p[j] ← p[j] · exp(i ω Δz / v'[j]) for every j      ▷ v' = v[i] / 2, the thin lens
L6          b[j] ← v'[j] Δz / (2 ω Δx²) for every j
L7          p ← solution of (I - (i/2) B T) p_new = (I + (i/2) B T) p, by the Thomas algorithm
L8  return image
```

Line L1 transforms every trace in time once. For one frequency, $p$ holds the field along $x$ at the current depth. Line L4 adds this frequency to the image row; the positive frequencies are enough, because the negative ones are their complex conjugates. Line L5 is the thin lens, the exact step for a vertical wave in the local velocity. Lines L6 and L7 are the diffraction term: one Crank-Nicolson step, which is a tridiagonal system with the diagonal $1 + i b_j$ and the off-diagonal entries $-\frac{i}{2}b_j$.

## Example

**The angle error by hand.** For a plane wave at the angle $\theta$, the exact one-way equation gives $k_z = (\omega/v')\cos\theta$ and the 15-degree equation gives $(\omega/v')(1 - \sin^2\theta/2)$. At 15 degrees: $\cos 15° = 0.965926$ against $1 - 0.066987/2 = 0.966506$, a relative error of $6.0 \times 10^{-4}$. At 45 degrees: $0.707107$ against $0.75$, a relative error of $0.061$. The 15-degree equation always gives a $k_z$ that is too large. A dipping event with the wavenumbers $(k_x, k_z)$ appears in the image with the dip $\arctan(k_x/k_z)$, so steep dips come out too small: they are undermigrated.

**One coefficient by hand.** With $f = 25$ Hz ($\omega = 157.08$ rad/s), $v' = 1500$ m/s, $\Delta z = 6$ m and $\Delta x = 10$ m, $b = 1500 \cdot 6/(2 \cdot 157.08 \cdot 100) = 0.286$. The tridiagonal matrix has the diagonal $1 + 0.286i$ (modulus 1.040) and off-diagonal entries of modulus 0.143, so every row is strictly diagonally dominant.

**Tests.** In constant velocity 3000 m/s with 32 traces at 10 m, 64 samples at 4 ms and $\Delta z = 6$ m, a point diffractor at row 32 and column 16 focuses within one row of its place, at column 16. A flat event at 0.2 s goes to row 50 (300 m) in the middle columns, because for $k_x = 0$ the scheme is the exact phase shift (measurements on these cases).

## Correctness

The full proof is in proofs/correctness.md.

- **The 15-degree relation (theorem).** $k_z^{15}$ is the Taylor polynomial of degree 2 of $k_z$ in $\sin\theta$, and $k_z \le k_z^{15}$ for all angles.
- **The Thomas algorithm succeeds (theorem).** Every row of $I - \frac{i}{2}BT$ is strictly [diagonally dominant](/diagonally-dominant-matrix/), since $\sqrt{1 + b_j^2} > b_j$, so no pivot is zero and no pivoting is needed.
- **Unitary step (theorem).** The map of line L7 keeps the norm $\sum_j |p_j|^2/b_j$. For constant $b$ it multiplies the sine mode with the eigenvalue $\lambda$ of $T$ by $e^{2i\arctan(b\lambda/2)}$ and keeps the plain norm.
- **What the code computes (theorem).** Line L8 returns $(2/n_t)\operatorname{Re}\sum_{0 < k < n_t/2} p_k^{(i)}$, where $p_k^{(i)}$ is the trace spectrum at index $k$ after $i$ lens and diffraction steps.
- **Consistency (theorem).** In constant velocity one step multiplies a sine mode by $e^{i k_z^{\text{CN}}\Delta z}$ with $k_z^{\text{CN}} - k_z^{15} = O(\Delta x^2 + \Delta z^2)$ for fixed $\omega$ and $k_x$.

## Complexity

- **Real-ram.** Line L1 costs $O(n_x n_t \log n_t)$ with an FFT. Each depth step for one frequency costs $O(n_x)$: the lens, the right-hand side and one Thomas solve. With about $n_t/2$ frequencies and $n_z$ steps the total is $O(n_z n_t n_x + n_x n_t \log n_t)$.
- **Against split step.** [Split-step Fourier migration](/split-step-fourier-migration/) needs two FFTs per step, $O(n_x \log n_x)$, so the finite-difference step is cheaper by a factor $\log n_x$, at the price of a smaller angle range.
- **Space.** One complex vector per frequency, the work arrays of the solver, and the image.

## Properties

- **Lateral velocity.** Both the lens and the coefficients $b_j$ use the local velocity, so lateral changes need no extra work.
- **Unconditionally stable.** The Crank-Nicolson step is unitary for every $\Delta z$, so there is no CFL condition, unlike the explicit time stepping of [reverse-time migration](/reverse-time-migration/).
- **Angle limit.** Accurate for waves within about 15 degrees of vertical; at 45 degrees the vertical wavenumber is 6 percent too large.
- **Numerical dispersion.** The second difference replaces $-k_x^2$ by $-4\sin^2(k_x\Delta x/2)/\Delta x^2$, which reduces the effective angle further at coarse $\Delta x$.
- **Edge reflections.** The Dirichlet ends ($P = 0$ outside the grid) reflect waves that reach the sides; production codes add absorbing boundary terms or tapers.

## Variants and improvements

- **45-degree and higher-order equations.** Replace the Taylor polynomial by a continued-fraction (Pade) approximation of the square root. The 45-degree equation has a rational symbol and still leads to tridiagonal systems per step.
- **Splitting in 3D.** Apply the diffraction term along $x$ and then along $y$, each with tridiagonal solves ([operator splitting](/operator-splitting/)). This adds an error that depends on the azimuth, which correction terms reduce.
- **Fourier finite difference.** Combine a phase shift with a reference velocity and a finite-difference correction for the difference, which widens the angle range in lateral velocity.
- **Time-domain form.** Claerbout's original schemes worked in the time and space domain with a retarded time; the frequency-domain form here is simpler for variable velocity.
- **Implicit weights above one half.** Using a weight a little above the Crank-Nicolson value $1/2$ on the new field damps high-wavenumber noise, at the cost of a step that is no longer unitary (a heuristic trade).

## When to use it

Use finite-difference migration when the velocity changes laterally and the dips are moderate, or when a cheap per-step cost matters. It is the classical method of the 1970s. For steep dips use the 45-degree or higher-order equations, [split-step Fourier migration](/split-step-fourier-migration/) with corrections, or [reverse-time migration](/reverse-time-migration/), which has no angle limit. For velocity that changes only with depth, [phase-shift migration](/phase-shift-migration/) is exact.

## Pitfalls

- **An explicit step.** Solving the diffraction term with forward Euler instead of line L7 is unstable for every $\Delta z$, because the operator is purely imaginary. Use the implicit Crank-Nicolson step of line L7.
- **The full velocity.** Using $v$ instead of $v' = v/2$ in lines L5 and L6 doubles every depth. Zero-offset data need the half velocity.
- **Pivoting in the solver.** The Thomas algorithm needs no pivoting here, because the matrix is strictly diagonally dominant; a general solver with $O(n_x^3)$ cost throws away the tridiagonal structure.
- **Steep events.** Trusting the image of steep dips: at 45 degrees the vertical wavenumber is 6 percent too large, so the imaged dip is too small. This is a systematic error, not noise.

## Implementations

## History

Claerbout (1971) proposed migration by finite differences of a one-way wave equation, and Claerbout and Doherty (1972) gave the downward continuation of zero-offset data with the 15-degree equation. The method was the first wave-equation migration in industry use, and Claerbout's book (1985) explained it with the Crank-Nicolson scheme and its dispersion. The angle limit motivated the 45-degree and higher-order equations, and later the phase-shift, Stolt and split-step methods in the frequency-wavenumber domain.

## References
