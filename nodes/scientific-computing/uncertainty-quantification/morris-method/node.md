---
tag: 2Q63VY
kind: algorithm
slug: morris-method
name: Morris method
aliases:
- elementary effects method
area: scientific-computing/uncertainty-quantification
level: core
summary: Screens many inputs cheaply by averaging one-at-a-time differences along random trajectories, ranking inputs by their mean and spread.
model: real-ram
complexity:
  vars: {r: the number of trajectories, d: the number of inputs, F: the cost of one model run}
  time: {worst: O(r d F + r d^2)}
  space: {extra: O(r d)}
properties: {deterministic: false, randomized: true, exact: false, iterative: false}
history:
  year: 1991
  people: [Max D. Morris, Francesca Campolongo, Jessica Cariboni, Andrea Saltelli]
  note: Morris proposed the elementary effects on random one-at-a-time trajectories with the measures mu and sigma in 1991. Campolongo, Cariboni and Saltelli added mu*, the mean of the absolute effects, in 2007.
prereqs: [forward-uncertainty-propagation]
see_also: [sobol-indices, saltelli-sampling-scheme, fourier-amplitude-sensitivity-test, hoeffding-sobol-decomposition, finite-difference-method, latin-hypercube-sampling, active-subspaces, curse-of-dimensionality]
sources:
  - paper: doi:10.1080/00401706.1991.10484804
    title: Max D. Morris, Factorial sampling plans for preliminary computational experiments, Technometrics 33(2), 1991, 161-174
    locator: the elementary effects, the grid of p levels with the step p/(2(p - 1)), the random trajectories and the measures mu and sigma
  - paper: doi:10.1016/j.envsoft.2006.10.004
    title: Francesca Campolongo, Jessica Cariboni and Andrea Saltelli, An effective screening design for sensitivity analysis of large models, Environmental Modelling and Software 22(10), 2007, 1509-1518
    locator: the measure mu*, its use as a proxy of the total index, and the choice of trajectories with a large spread
  - book: isbn:9780470059975
    title: Andrea Saltelli, Marco Ratto, Terry Andres, Francesca Campolongo, Jessica Cariboni, Debora Gatelli, Michaela Saisana and Stefano Tarantola, Global Sensitivity Analysis, The Primer, Wiley, 2008
    locator: Chapter 3 (the elementary effects method)
---

The Morris method screens a model with many inputs for the few that matter, at a cost that grows only linearly with the number $d$ of inputs. It moves through the input space along random trajectories, changing one input at a time by a fixed step, and records the change of the output divided by the step: an elementary effect, a coarse finite difference. Each trajectory gives one elementary effect of each input with $d + 1$ runs. Over $r$ trajectories, the mean of the absolute effects $\mu^*$ ranks the inputs by overall influence, and their standard deviation $\sigma$ shows nonlinearity or interactions. The method gives a ranking, not a share of the variance like the [Sobol indices](/sobol-indices/), and it is usually run first, to decide which inputs deserve a costly variance-based study.

## In plain words

Your model has fifty knobs, and each run takes an hour. You want to know which knobs are worth a closer look.

Start at a random setting. Turn one knob by a fixed amount and see how much the output moves. Then turn a second knob from there, then a third, until each knob has moved once. That walk costs one run per knob, plus one. Repeat the walk from a few random starting points. A knob whose turns always move the output a lot is important. A knob whose effect changes much from walk to walk has a curved effect or works together with other knobs. A knob that never moves the output can be left fixed.

## The problem

The input is a model $y = f(x)$ with $d$ inputs, each scaled to $[0, 1]$, and a budget of model runs. The output is, for each input $i$, three screening measures of its elementary effects

$$EE_i(x) = \frac{f(x + \Delta e_i) - f(x)}{\Delta},$$

where $e_i$ is the unit vector of input $i$. The inputs take values on a grid of $p$ levels $\{0, \frac{1}{p-1}, \ldots, 1\}$ with $p$ even, and the step is $\Delta = \frac{p}{2(p - 1)}$, half the grid plus half a cell. The measures are the mean $\mu_i$, the mean of the absolute values $\mu^*_i$ and the standard deviation $\sigma_i$ of $EE_i(x)$ over the grid points $x$ where both $x$ and $x + \Delta e_i$ are on the grid. An input with large $\mu^*_i$ is important; a large $\sigma_i$ means that its effect depends on where it is measured.

## The algorithm

```pseudo id=main
MORRIS(f, d, r, p)
L1  for t = 1..r do                                    ▷ one trajectory per pass
L2      x*_k ← uniform on {0, 1/(p-1), ..., 1 - Δ} for k = 1..d,   Δ = p / (2(p - 1))
L3      u_k ← up or down with probability 1/2 for k = 1..d; start x_k ← x*_k if up, x*_k + Δ if down
L4      π ← a uniformly random order of 1..d
L5      for each input k in the order π: x_k ← x_k + Δ if up, x_k - Δ if down; record the point
L6      y_0..y_d ← f at the d + 1 points of the trajectory
L7      for the j-th move, of input k = π_j: EE_k ← (y_j - y_(j-1)) / (signed step of input k)
L8  μ_i, μ*_i, σ_i ← mean, mean of absolute values and standard deviation of the r effects of input i
L9  return μ, μ*, σ and the run count r(d + 1)
```

Lines L2 to L5 build one trajectory: a start point and $d$ moves, each of one input, by $\pm\Delta$, so that consecutive points differ in exactly one input. The base values of line L2 keep every point on the grid. Line L6 is the only step that runs the model. In line L7, the move of input $k$ changes only $x_k$, so the difference of the two outputs, divided by the signed step, is an elementary effect of input $k$ at a grid point. Line L8 uses the divisor $r - 1$ for $\sigma$.

## Example

**By hand.** Let $f(x) = x_1 + x_1 x_2$ with $p = 4$, so the grid is $\{0, 1/3, 2/3, 1\}$ and $\Delta = 2/3$. The exact effects are $EE_1 = 1 + x_2$ and $EE_2 = x_1$, so over the grid $\mu_1 = 1 + 1/2 = 1.5$ and $\mu_2 = 1/2$. One trajectory with $x^* = (0, 1/3)$, both directions up and the order $\pi = (1, 2)$:

| point | $x_1$ | $x_2$ | $f$ | move | effect |
|---|---|---|---|---|---|
| 0 | 0 | 1/3 | 0 | start | |
| 1 | 2/3 | 1/3 | 8/9 | $x_1$ by $+2/3$ | $EE_1 = (8/9 - 0)/(2/3) = 4/3$ |
| 2 | 2/3 | 1 | 4/3 | $x_2$ by $+2/3$ | $EE_2 = (4/3 - 8/9)/(2/3) = 2/3$ |

Three runs give one effect of each input. $EE_1 = 4/3 = 1 + x_2$ at $x_2 = 1/3$, and $EE_2 = 2/3 = x_1$ at $x_1 = 2/3$. Different trajectories meet different values of $x_2$ and $x_1$, so $\sigma_1$ and $\sigma_2$ are positive: each effect depends on the other input, which is the interaction $x_1 x_2$.

**The Ishigami function.** With $f(x) = \sin x_1 + 7\sin^2 x_2 + 0.1\, x_3^4 \sin x_1$ on $[-\pi, \pi]^3$, scaled to the unit cube, and $p = 4$, the grid measures over all 32 grid pairs of each input are:

| input | $\mu_i$ | $\mu^*_i$ | spread of $EE_i$ | $S_i$ | $S_{Ti}$ |
|---|---|---|---|---|---|
| $x_1$ | 7.7041 | 7.7041 | 6.2488 | 0.3139 | 0.5576 |
| $x_2$ | 0 | 7.875 | 7.875 | 0.4424 | 0.4424 |
| $x_3$ | 0 | 6.2488 | 8.8371 | 0 | 0.2437 |

A run with $r = 10$ trajectories (40 runs) and `random.Random(1991)` gives $\widehat{\mu}^* = (5.205, 7.875, 6.249)$, a measurement. The method finds that all three inputs matter, and $x_3$ with $\mu_3 = 0$ and a large spread acts through an interaction or a sign change, which is right. But $\mu^*$ ranks $x_2$ above $x_1$, while the total indices rank $x_1$ first: $\mu^*$ is a screening measure, not a variance share.

## Correctness

The claim is that each elementary effect of input $i$ in line L7 is a uniform random draw from the list of all grid differences of input $i$, so that $\widehat{\mu}_i$ and $\widehat{\mu}^*_i$ are unbiased for the grid means $\mu_i$ and $\mu^*_i$, $\widehat{\sigma}^2_i$ is unbiased for the grid variance, and all three converge as $r \to \infty$. The key step is the point before the move of input $i$: its other inputs have either moved or not, depending on the random order, but in both cases a fair coin decides whether they sit at $x^*_k$ or $x^*_k + \Delta$, which makes each of them uniform on the whole grid. This uses that $p$ is even, so that $\Delta$ is a whole number of grid cells. The full proof is in the proof file. There is no theorem that $\mu^*$ orders the inputs like the total Sobol indices; that is an empirical finding of Campolongo, Cariboni and Saltelli.

## Complexity

Each trajectory makes $d + 1$ runs, so the method makes $r(d + 1)$ runs, $O(r d F)$ time for a run cost $F$. Recording the $d + 1$ points of length $d$ costs $O(d^2)$ per trajectory in the [real RAM](/real-ram/) model, or $O(d)$ if each point is stored as one change from the last. The effects take $O(r d)$ space; line L8 is $O(r d)$. A variance-based study with the [Saltelli sampling scheme](/saltelli-sampling-scheme/) needs $N(d + 2)$ runs with $N$ usually in the hundreds or more, while $r$ is usually between 10 and 50, so screening is cheaper by a factor of about $N / r$.

## Properties

- **Linear cost in d.** One trajectory gives one effect of every input with $d + 1$ runs.
- **Global, not local.** The step $\Delta$ is about half the range, and the start points cover the grid, so the effects sample the whole input space, unlike a derivative at one nominal point.
- **Exact for linear models.** If $f$ is linear, every effect of input $i$ is its coefficient, $\sigma_i = 0$ and $\mu^*_i = |c_i|$.
- **Qualitative.** The measures rank the inputs and flag nonlinearity or interaction; they do not split the variance and have no standard error in the original method.
- **Robust to sign changes with mu*.** Effects of opposite signs cancel in $\mu$ but not in $\mu^*$.

## Variants and improvements

- **Mu star.** Campolongo, Cariboni and Saltelli (2007) use $\mu^*$ instead of $\mu$, because $\mu$ can be near zero for an important input whose effect changes sign, as $x_2$ and $x_3$ of the Ishigami example show.
- **Spread-out trajectories.** Generate many candidate trajectories and keep the $r$ with the largest distances between them, for a better coverage of the input space at the same cost.
- **Radial designs.** Move each input from one common base point to a second random point, one input at a time; this shares the base run and is the screening analogue of the column swap in the Saltelli scheme.
- **Groups of inputs.** For very many inputs, move groups together, and screen the inputs of an important group in a second round.
- **Small steps.** As $\Delta \to 0$, the effects become derivatives, and the mean of their squares is a derivative-based global sensitivity measure, which bounds the total Sobol index for some input laws.

## When to use it

Use the Morris method when the model has many inputs, from tens to hundreds, runs are expensive, and the first question is which inputs can be fixed. Follow it with the [Saltelli sampling scheme](/saltelli-sampling-scheme/) or the [Fourier amplitude sensitivity test](/fourier-amplitude-sensitivity-test/) on the inputs that pass, if quantitative indices are needed. Use [active subspaces](/active-subspaces/) when gradients are available and important directions may be combinations of inputs rather than single inputs. A local [finite difference](/finite-difference-method/) at one nominal point costs the same $d + 1$ runs but says nothing about the rest of the input space.

## Pitfalls

- **An odd number of levels.** With $p$ odd, $\Delta = p/(2(p - 1))$ is not a whole number of cells, and line L5 leaves the grid; with the base values of line L2 the effects are no longer uniform on the grid. Use $p$ even, often $p = 4$.
- **Ranking by mu.** Using only $\mu$ in line L8 hides inputs whose effects change sign: $\mu_2 = 0$ for the Ishigami function although $x_2$ carries 44 percent of the variance. Rank by $\mu^*$ and look at $\sigma$.
- **Reading mu star as a variance share.** $\mu^*$ ranks $x_2$ above $x_1$ for the Ishigami function, although $S_{T1} > S_{T2}$. Use the ranking to discard inputs, not to compare close ones.
- **A fixed number of trajectories as a guarantee.** $r$ between 10 and 50 is a rule of thumb. Check that the ranking is stable when $r$ grows; with $r = 10$ in the example, $\widehat{\mu}^*_1 = 5.2$ against the grid value 7.7.
- **Unscaled inputs.** The effects in line L7 are per unit of the scaled input. If the inputs are not mapped to $[0, 1]$ through their ranges or quantiles, inputs with large units get small effects.

## Implementations

## History

Morris proposed the method in 1991 in Technometrics, as factorial sampling plans for preliminary computational experiments, with random one-at-a-time trajectories on a grid and the measures $\mu$ and $\sigma$. Campolongo, Cariboni and Saltelli introduced $\mu^*$ and the choice of trajectories with a large spread in 2007, and found that $\mu^*$ is a good proxy of the total Sobol index in their tests. The method is the standard screening tool in the sensitivity analysis primer of Saltelli and coauthors (2008).

## References
