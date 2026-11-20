---
tag: EGQBSZ
kind: algorithm
slug: metadynamics
name: Metadynamics
area: scientific-computing/molecular-simulation
level: advanced
summary: "Adds Gaussian hills at visited values of collective variables so the system escapes free energy minima; in the well-tempered form the bias converges to a scaled free energy."
model: real-ram
complexity:
  vars: {T: the number of time steps, m: the number of hills, G: the number of grid points of the bias}
  time: {worst: O(T + m G)}
  space: {extra: O(G)}
properties: {deterministic: false, randomized: true, iterative: true, unbiased: false, consistent: false}
history:
  year: 2002
  people: [Alessandro Laio, Michele Parrinello]
  note: Laio and Parrinello introduced a history-dependent bias of Gaussians on a few collective variables that fills the free energy wells; Barducci, Bussi and Parrinello added the well-tempered form with decreasing hill heights in 2008.
prereqs: [collective-variable, langevin-dynamics, euler-maruyama-method]
see_also: [umbrella-sampling, wang-landau, weighted-histogram-analysis-method, parallel-tempering, hyperdynamics, temperature-accelerated-dynamics, kernel-density-estimation, energy-landscape]
sources:
  - paper: doi:10.1073/pnas.202427399
    title: Alessandro Laio and Michele Parrinello, Escaping free-energy minima, Proceedings of the National Academy of Sciences of the USA 99(20), 2002, 12562-12566
    locator: the history-dependent bias on collective variables and its use to explore and reconstruct the free energy
  - paper: doi:10.1103/PhysRevLett.100.020603
    title: Alessandro Barducci, Giovanni Bussi and Michele Parrinello, Well-tempered metadynamics, a smoothly converging and tunable free-energy method, Physical Review Letters 100, 020603, 2008
    locator: the hill height that decreases with the local bias, the convergence of the bias to a scaled free energy, and the effective temperature of the collective variables
  - paper: doi:10.1103/PhysRevLett.112.240602
    title: James F. Dama, Michele Parrinello and Gregory A. Voth, Well-tempered metadynamics converges asymptotically, Physical Review Letters 112, 240602, 2014
    locator: the proof that the well-tempered bias converges in the long-time limit
---

Metadynamics computes a free energy surface along a few [collective variables](/collective-variable/) $s(x)$ by building a bias during the run. Every $\tau$ steps it adds a small Gaussian hill of width $\sigma$ to a bias $V(s)$ at the current value of $s$. Hills pile up where the system stays, so a free energy well fills until the system spills over the barrier into the next well, which then fills too. The system thus escapes minima that ordinary [Langevin dynamics](/langevin-dynamics/) would not leave in the time available. In standard metadynamics (Laio and Parrinello 2002) the hills have a constant height $w$, and at long times $-V(s)$ follows the free energy $F(s)$ up to a constant, but it keeps fluctuating with an error that does not shrink, and the bias grows without bound. In well-tempered metadynamics (Barducci, Bussi and Parrinello 2008) the height is $w\,e^{-V(s)/(k_B \Delta T)}$, the hills shrink as the bias grows, and the bias converges to $V = -\frac{\Delta T}{T + \Delta T} F$ up to a constant (Dama, Parrinello and Voth 2014), so $F = -\frac{T + \Delta T}{\Delta T} V$.

## In plain words

Picture a ball rolling in a landscape of valleys, with the ball shaken by heat. It stays in one valley for a very long time because the hills around it are high.

Metadynamics drops a small pile of sand wherever the ball is, every few steps. The valley slowly fills with sand, the ball rises with it, and at last it rolls over into the next valley, which then fills in turn. In the end the landscape is nearly flat, and the sand that was added has the shape of the valleys, upside down.

In the well-tempered form the piles get smaller where much sand already lies, so the sand settles to a fixed shape instead of growing for ever.

## The problem

The input is a potential $U(x)$, a collective variable $s(x)$, the temperature $T$, a dynamics that samples $e^{-\beta(U + V)}$ with $\beta = 1/(k_B T)$, and the hill parameters $w$, $\sigma$, $\tau$, and $\Delta T$ for the well-tempered form. The target is the free energy profile
$$F(s) = -k_B T \ln p(s) + \text{const}$$
of the marginal $p(s)$ of $s(x)$ in the canonical ensemble. The output is the bias $V$ on a grid and the estimate of $F$ that follows from it. Unlike [umbrella sampling](/umbrella-sampling/) the bias is not known in advance and is not fixed; unlike plain sampling, the run crosses the barriers.

## The algorithm

```pseudo id=main
METADYNAMICS(U, s, x_0, kT, h, steps, w, sigma, tau, k dT)
L1  V ← 0 on a grid of s
L2  for n ← 1 to steps do
L3      x ← x - h (U'(x) + V'(s(x)) s'(x)) + sqrt(2 kT h) xi        ▷ xi ~ N(0, 1)
L4      if n mod tau = 0 then
L5          height ← w (standard) or w exp(-V(s(x)) / k dT) (well-tempered)
L6          V(s') ← V(s') + height exp(-(s' - s(x))^2 / (2 sigma^2)) on the grid
L7  return F ≈ -V (standard) or -((kT + k dT) / k dT) V (well-tempered), up to a constant
```

Line L3 is one Euler-Maruyama step of overdamped Langevin dynamics on $U + V$; molecular dynamics with a thermostat is the usual choice in practice. Line L6 keeps $V$ on a grid as values and slopes, and the code reads it back by cubic Hermite interpolation, so the force in line L3 is the exact derivative of the bias that is read and one step costs $O(1)$. Line L7 rescales the well-tempered bias by the bias factor. The ratio $\gamma = (T + \Delta T)/T$ is called the bias factor, and the collective variable is sampled as if at the higher temperature $T + \Delta T$ (Claim 2 of the proof).

## Example

Take $U(x) = 8(x^2 - 1)^2$, $s = x$, $k_B T = 1$, so $F = U$ with minima at $\pm 1$ and a barrier of $8\,k_B T$. Use $h = 0.005$, $\sigma = 0.2$, $w = 0.1$ and $\tau = 10$, start at $x = -1$, and count a transition each time $x$ passes from below $-0.5$ to above $0.5$ or back.

**Escape.** In 10000 steps (seed 1) plain dynamics made 0 transitions and standard metadynamics made 25.

**The profile after 80000 steps** (seed 1), on the region with $U < 5$ after the best constant shift:

| form | largest value of $V$ | largest error | barrier $F(0) - F(1)$ | asymmetry $F(-1) - F(1)$ |
|---|---|---|---|---|
| well-tempered, $k_B \Delta T = 7$ | 24.0 | 0.418 | 7.932 | 0.197 |
| standard | 111.7 | 0.785 | 8.684 | 0.963 |

The exact barrier is 8 and the exact asymmetry is 0. The standard bias kept growing: its integral is exactly the number of hills times $w \sigma \sqrt{2\pi}$, so it rises linearly with time (Claim 1). Over three seeds and times from 5000 to 80000 steps, the largest error of standard metadynamics stayed between 0.7 and 1.8 and did not decrease; with $k_B \Delta T = 7$ it was 0.42 to 0.74 at 80000 steps. The grid bias agreed with the direct sum of all hills to $4.8 \times 10^{-8}$, and its force with a finite difference to $10^{-9}$.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. **The standard bias grows without bound.** With constant heights, the integral of $V$ over the whole line equals the number of hills times $w \sigma \sqrt{2\pi}$, so $V$ cannot converge.
2. **The fixed shape of the bias.** In the limit of slow deposition and narrow hills, the deposition rate is uniform in $s$ exactly when $V = -\frac{\Delta T}{T + \Delta T} F + c$; then $s$ is distributed as $e^{-F/(k_B (T + \Delta T))}$. The limit $\Delta T \to \infty$ gives the standard form with $V = -F + c$ and a flat distribution of $s$, and $\Delta T \to 0$ gives no bias.
3. **The constant grows like a logarithm.** In the same limit the well-tempered constant $c(t)$ grows like $k_B \Delta T \ln t$, so the hill heights decay like $1/t$.
4. **The grid.** The cubic Hermite bias is continuously differentiable, its derivative is the force used, and its error against the sum of the hills is at most $\Delta s^4 \max |V^{(4)}| / 384$ for grid spacing $\Delta s$.

Claims 2 and 3 are statements about the quasi-static limit, not a proof that the stochastic algorithm converges. That proof for the well-tempered form is due to Dama, Parrinello and Voth (2014) and is not repeated here.

## Complexity

Each step costs one force evaluation of $U$ and $O(1)$ for the grid bias. Each of the $m = T / \tau$ hills costs $O(G)$ to add on a grid of $G$ points, or less if only the points within a few $\sigma$ are updated. So the time is $O(T + m G)$ and the extra space is $O(G)$. Without a grid, each step must sum all hills so far, which costs $O(T^2 / \tau)$ in total. The grid grows exponentially with the number of collective variables, which limits metadynamics to about one to three of them.

## Properties

- **History-dependent bias.** The dynamics is not at equilibrium during the run; the bias changes the sampled distribution all the time.
- **Standard form does not converge.** $-V$ follows $F$ up to fluctuations of order of the hill size, and the bias grows without bound.
- **Well-tempered form converges** to $-\frac{\Delta T}{T + \Delta T} F$ up to a constant, and the hills shrink like $1/t$.
- **Tunable.** $\Delta T$ sets how far the bias flattens the surface: the barrier seen by $s$ is divided by the bias factor $\gamma$.
- **Exploration without a path.** It needs no windows or path in advance, only the collective variables.
- **Depends on the collective variables.** A slow motion that is not described by $s$ is not accelerated, and the bias can then be wrong.

## Variants and improvements

- **Well-tempered metadynamics** (Barducci, Bussi and Parrinello 2008), as above.
- **Reweighting.** Samples of the biased run can be reweighted to the unbiased ensemble to get averages of other quantities, using the bias and its time-dependent constant.
- **Multiple walkers.** Several runs add hills to one shared bias.
- **Parallel tempering metadynamics** and bias-exchange metadynamics combine the bias with [parallel tempering](/parallel-tempering/) or with exchanges between runs that bias different variables.
- **Related adaptive biases.** [Wang-Landau sampling](/wang-landau/) fills the density of states with a decreasing step, the adaptive biasing force method builds the mean force instead of the bias, and [hyperdynamics](/hyperdynamics/) uses a bias to accelerate rare events while keeping their rates.

## When to use it

Use metadynamics to explore an unknown free energy surface along one to three good collective variables, to find the states and the paths between them, and, in the well-tempered form, to compute the surface. Prefer umbrella sampling with WHAM when the path is known and the most accurate profile along it is wanted. Use the well-tempered form for any quantitative work; standard metadynamics is mainly a tool to explore.

## Pitfalls

- **Bad collective variables.** If a slow degree of freedom is missing from $s$, the system can be pushed over the wrong barrier and the bias shows hysteresis; check by running forward and backward and from different starts.
- **Hills too large or too frequent.** The system then is not near equilibrium under the current bias, and the error grows.
- **Standard bias used as a converged answer.** It keeps fluctuating; average over time or use the well-tempered form.
- **Missing scale factor.** The well-tempered bias must be multiplied by $(T + \Delta T)/\Delta T$.
- **Grid boundaries.** Outside the grid the bias is zero in the code here; in practice add walls, or the system can leave the grid and not feel the bias.
- **Overfilling at edges.** Near a hard wall in $s$ the Gaussians spill over and the estimate near the wall is wrong.

## Implementations

## History

Laio and Parrinello (2002) introduced metadynamics as a way to escape free energy minima, with a bias built from the history of the run in the space of a few collective variables. Barducci, Bussi and Parrinello (2008) made the hill height decrease with the bias and showed that the bias then settles to a scaled free energy. Dama, Parrinello and Voth (2014) proved that the well-tempered bias converges in the long-time limit. Laio and Gervasio (2008) review the method.

## References
