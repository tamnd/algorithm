---
tag: H90CB5
kind: algorithm
slug: umbrella-sampling
name: Umbrella sampling
area: scientific-computing/molecular-simulation
level: core
summary: "Adds biasing potentials that restrain a collective variable in overlapping windows so rare regions are sampled, and removes the bias afterwards."
model: real-ram
complexity:
  vars: {K: the number of windows, n: the number of samples per window, B: the number of histogram bins}
  time: {worst: O(K n + K B)}
  space: {extra: O(K B)}
properties: {deterministic: false, randomized: true, iterative: false, unbiased: false, consistent: true, parallel: true}
history:
  year: 1977
  people: [Glenn M. Torrie, John P. Valleau]
  note: Torrie and Valleau introduced non-physical sampling distributions that cover the important regions of two states at once, and named them umbrella sampling for the way one distribution spans both.
prereqs: [collective-variable, metropolis-hastings, importance-sampling]
see_also: [weighted-histogram-analysis-method, metadynamics, free-energy-perturbation, thermodynamic-integration, bennett-acceptance-ratio, parallel-tempering, wang-landau, energy-landscape]
sources:
  - paper: doi:10.1016/0021-9991(77)90121-8
    title: Glenn M. Torrie and John P. Valleau, Nonphysical sampling distributions in Monte Carlo free-energy estimation, umbrella sampling, Journal of Computational Physics 23(2), 1977, 187-199
    locator: the biased sampling distribution and the reweighting of its samples to the unbiased ensemble
  - paper: doi:10.1002/wcms.66
    title: Johannes Kästner, Umbrella sampling, Wiley Interdisciplinary Reviews, Computational Molecular Science 1(6), 2011, 932-942
    locator: the review of harmonic window biases, the choice of force constant and window spacing, and the ways to combine windows
  - paper: doi:10.1002/jcc.540130812
    title: Shankar Kumar, John M. Rosenberg, Djamal Bouzida, Robert H. Swendsen and Peter A. Kollman, The weighted histogram analysis method for free-energy calculations on biomolecules. I. The method, Journal of Computational Chemistry 13(8), 1992, 1011-1021
    locator: the combination of the biased histograms of many umbrella windows into one free energy profile
  - book: doi:10.1016/B978-0-12-267351-1.X5000-7
    title: Daan Frenkel and Berend Smit, Understanding Molecular Simulation, From Algorithms to Applications, second edition, Academic Press, 2002
    locator: the chapter on free energy calculations, the section on umbrella sampling
---

Umbrella sampling computes the free energy profile $F(s) = -k_B T \ln p(s)$ along a [collective variable](/collective-variable/) $s(x)$ when ordinary sampling never crosses the barriers between the low regions of $F$. It runs $K$ separate simulations, called windows. Window $k$ adds a bias $w_k(s)$, usually a harmonic spring $\frac{\kappa}{2}(s - s_k)^2$, that holds $s$ near the centre $s_k$, so each window samples a narrow range of $s$, including the high-energy ones. In each window the bias is known exactly, so it can be removed from the window histogram, which leaves $F$ on that range up to an unknown constant. The constants come from the overlap of neighbouring windows. This page uses a simple join of neighbours; the [weighted histogram analysis method](/weighted-histogram-analysis-method/) (WHAM) is the standard way to combine all windows at once. It is a form of [importance sampling](/importance-sampling/) with a chosen, non-physical sampling distribution (Torrie and Valleau 1977).

## In plain words

Some molecular events, such as a bond breaking or a protein changing shape, need the system to climb over a high hill of energy. An ordinary simulation stays in a valley and almost never makes that climb.

Umbrella sampling puts a spring on the system that holds one chosen quantity near a chosen value. One simulation is held at the bottom of the valley, the next a little higher up the hill, and so on over the top. Each simulation sees only its own small piece of the hill.

The spring changes what each simulation sees, but its effect is known exactly, so it can be taken away afterwards. The pieces overlap, which tells us how to fit them together into the full shape of the hill.

## The problem

The input is a potential $U(x)$, a collective variable $s(x)$, the inverse temperature $\beta = 1/(k_B T)$, window centres $s_1 < \dots < s_K$, a spring constant $\kappa$, and bins on an interval of $s$. The target is the free energy profile
$$F(s) = -\beta^{-1} \ln p(s) + \text{const}, \qquad p(s) = \frac{1}{Z} \int \delta(s(x) - s)\, e^{-\beta U(x)}\,dx,$$
on the bins. In window $k$ the sampled density is proportional to $e^{-\beta (U(x) + w_k(s(x)))}$, and its marginal in $s$ is $p(s)\, e^{-\beta w_k(s)}$ up to a constant factor, so
$$F(s) = -\beta^{-1} \ln p_k^{\text{biased}}(s) - w_k(s) + c_k$$
with one unknown constant $c_k$ per window (Claim 1 of the proof).

## The algorithm

```pseudo id=main
UMBRELLA(U, s_1..s_K, kappa, beta, bins)
L1  for k ← 1 to K do                                  ▷ the windows are independent
L2      sample x from exp(-beta (U(x) + kappa/2 (s(x) - s_k)^2)), by Monte Carlo or MD
L3      n_k(b) ← number of samples with s(x) in bin b
L4      F_k(b) ← -ln(n_k(b)) / beta - w_k(centre of b) on bins with enough counts
L5  F ← F_1
L6  for k ← 2 to K do c ← mean of F(b) - F_k(b) over the bins defined in both
L7      merge F_k + c into F, as a count-weighted mean on shared bins
L8  return F - min F
```

Lines L1 to L4 are the sampling; the $K$ windows can run in parallel. Line L4 uses only bins with enough samples (50 in the code here), because $-\ln n$ of a small count is noisy and biased. Lines L5 to L7 fix the constants: each new window is shifted to agree on average with the profile so far on the bins they share. Line L8 sets the lowest point to 0, since $F$ is defined only up to a constant.

The spacing of the windows must let each pair of neighbours share several well-sampled bins. With a harmonic bias the width of window $k$ is about $1/\sqrt{\beta(\kappa + F''(s_k))}$ when $\kappa + F'' > 0$, so a spacing of one or two such widths is usual.

## Example

Take the double well $U(x) = 8(x^2 - 1)^2$ with $s = x$ and $k_B T = 1$, so the exact profile is $F = U$, with minima at $\pm 1$ and a barrier of $8\,k_B T$ at 0. A plain Metropolis chain started at $x = -1$ with step 0.3 did not reach $x > 0$ once in 50000 steps.

With 17 windows centred at $-1.6, -1.4, \dots, 1.6$, $\kappa = 50$, 20000 Metropolis samples per window with step 0.3 and 32 bins on $[-1.6, 1.6]$ (seed 1):

| quantity | umbrella sampling | exact at the bin centres |
|---|---|---|
| barrier, $F(0.05) - F(0.95)$ | 7.787 | 7.884 |
| asymmetry, $F(-0.95) - F(0.95)$ | $-0.195$ | 0 |
| largest error on bins with $U < 9$ | 0.263 | |

The barrier is within $0.1\,k_B T$. The asymmetry error comes from the 16 joins: each shift has a small error, and these errors add up from the left end to the right end. Other seeds gave barrier errors below $0.1$ and asymmetry errors from 0.1 to 0.25. With only 3000 samples per window and a count threshold of 10, the largest error was 0.247, so the join and the bin width, not the number of samples, limit the result here.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. **Unbiasing a window.** The marginal of $s$ in window $k$ is $p(s) e^{-\beta w_k(s)}$ up to a constant, so $-\beta^{-1} \ln p_k^{\text{biased}} - w_k$ equals $F$ up to a constant, for every bias $w_k$ that depends on $x$ only through $s$.
2. **Consistency of one window.** As the number of samples grows, line L4 converges to $F$ averaged over the bin, up to a constant, with a bin error at most the variation of $w_k$ across the bin.
3. **The join.** If each window profile is exact up to its constant on the shared bins, lines L5 to L8 return $F$ exactly up to a global constant; with errors in the windows, the error of the joined profile is bounded by a sum of window errors along the chain of joins.

## Complexity

Sampling costs $O(n)$ energy evaluations per window, so $O(K n)$ in total, and this term dominates in practice. The histograms cost $O(K n)$ and the join $O(K B)$. The windows are independent and run in parallel. The extra space is $O(K B)$ for the histograms. The number of windows needed grows with the length of the path in $s$ divided by the window width, and the statistical error of $F$ at a point grows roughly with the square root of the number of joins between it and the reference point.

## Properties

- **Exact unbiasing.** The bias is removed exactly in each window; the only errors are statistical, the bin width, and the join.
- **Any bias that depends only on $s$** can be used; the harmonic spring is the common choice.
- **Parallel.** The windows need no communication.
- **Depends on the collective variable.** It gives $F$ along $s$; if a slow motion is not described by $s$, each window can stay stuck in one valley of the hidden motion and the profile is wrong.
- **Consistent, not unbiased.** The log of a histogram count is biased for finite counts.

## Variants and improvements

- **WHAM and MBAR.** The [weighted histogram analysis method](/weighted-histogram-analysis-method/) combines all windows with weights of least variance and needs no order of joins; MBAR does the same without bins.
- **Umbrella integration.** Estimate the mean force $dF/ds$ in each window from the mean and variance of $s$, and integrate it; this needs no overlap between histograms (Kästner 2011).
- **Replica exchange umbrella sampling.** Run the windows in parallel and swap configurations between neighbouring windows, as in [parallel tempering](/parallel-tempering/), to relax hidden slow motions.
- **Adaptive biases.** [Metadynamics](/metadynamics/) and [Wang-Landau](/wang-landau/) sampling build a bias that flattens the profile during the run instead of using fixed windows.
- **Multidimensional windows.** Biases on two or three collective variables give a free energy surface, at a cost that grows with the number of windows on the grid.

## When to use it

Use umbrella sampling when a good collective variable is known, the path between the states along it is clear, and the barrier is too high for plain sampling. It is robust and simple, and with WHAM or MBAR it is a standard tool for potentials of mean force, for example along a distance in ligand unbinding or along a reaction coordinate in a QM/MM study. For many collective variables, or when the path is not known, adaptive methods such as metadynamics are often easier.

## Pitfalls

- **Too little overlap.** Neighbouring windows must share well-sampled bins; check the histograms of all windows on one plot.
- **Springs that are too stiff or too soft.** A stiff spring gives narrow windows and needs many of them; a soft one does not hold the system on a steep part of $F$.
- **Hidden slow motions.** If each window samples only one of two valleys orthogonal to $s$, the profile depends on the starting configuration; compare runs from different starts.
- **Equilibration.** Each window starts from a configuration that may be far from its biased equilibrium; discard the first part of each run.
- **Bin width.** Evaluating the bias at the bin centre adds an error up to the change of $w_k$ across the bin, which is largest far from the window centre.
- **Jacobian terms.** For a distance or an angle, $F(s)$ contains the entropy of the volume element, such as $-2 k_B T \ln r$ for a distance in three dimensions; this is part of $F$, not an error.

## Implementations

## History

Torrie and Valleau (1977) used sampling distributions that are not physical but cover the important regions of two states at once, and reweighted the samples to compute free energy differences; the distribution that spans both states gave the name. The use of many harmonic windows along a coordinate, combined with WHAM (Kumar and co-workers 1992), became the standard method for potentials of mean force in biomolecular simulation. Kästner (2011) reviews the method and its analysis.

## References
