---
tag: NNCV7X
kind: algorithm
slug: nudged-elastic-band
name: Nudged elastic band method
aliases:
- NEB method
- climbing image nudged elastic band
- NEB
area: scientific-computing/multiscale-methods
level: core
summary: "Finds a minimum energy path between two minima: a chain of images moves under the true force across the path and spring forces along it. A climbing image converges to the saddle."
model: real-ram
complexity:
  vars: {N: the number of segments of the band, d: the number of coordinates, G: the cost of one gradient, I: the number of iterations}
  time: {worst: O(I N (G + d))}
  space: {extra: O(N d)}
properties: {deterministic: true, randomized: false, exact: false, iterative: true}
history:
  year: 1994
  people: [Greg Mills, Hannes Jonsson, Karsten W. Jacobsen, Graeme Henkelman, Blas P. Uberuaga]
  note: Mills and Jonsson gave the method in 1994, and Jonsson, Mills and Jacobsen described it in full in 1998. Henkelman, Uberuaga and Jonsson added the climbing image in 2000, and Henkelman and Jonsson gave the improved tangent in the same year.
prereqs: [gradient-descent, energy-landscape]
see_also: [string-method, dimer-method, harmonic-transition-state-theory, kinetic-monte-carlo, transition-path-sampling, bfgs, molecular-dynamics, collective-variable]
sources:
  - paper: doi:10.1103/PhysRevLett.72.1124
    title: "Greg Mills and Hannes Jonsson, Quantum and thermal effects in H2 dissociative adsorption: evaluation of free energy barriers in multidimensional quantum systems, Physical Review Letters 72(7), 1994, 1124-1127"
    locator: the first use of the nudged elastic band, there for paths of quantum (path integral) systems
  - paper: doi:10.1142/9789812839664_0016
    title: Hannes Jonsson, Greg Mills and Karsten W. Jacobsen, Nudged elastic band method for finding minimum energy paths of transitions, in Classical and Quantum Dynamics in Condensed Phase Simulations, World Scientific, 1998, 385-404
    locator: the full description, the projections of the true force and the spring force, and the comparison with the plain elastic band
  - paper: doi:10.1063/1.1329672
    title: Graeme Henkelman, Blas P. Uberuaga and Hannes Jonsson, A climbing image nudged elastic band method for finding saddle points and minimum energy paths, Journal of Chemical Physics 113(22), 2000, 9901-9904
    locator: the climbing image, with the parallel force inverted and no spring force
  - paper: doi:10.1063/1.1323224
    title: Graeme Henkelman and Hannes Jonsson, Improved tangent estimate in the nudged elastic band method for finding minimum energy paths and saddle points, Journal of Chemical Physics 113(22), 2000, 9978-9985
    locator: the tangent to the neighbour of higher energy, the weighted tangent at extremes, and the spring force from the difference of the distances
  - paper: doi:10.1063/1.2841941
    title: Daniel Sheppard, Rye Terrell and Graeme Henkelman, Optimization methods for finding minimum energy paths, Journal of Chemical Physics 128(13), 2008, 134106
    locator: the comparison of optimizers for the NEB force, which is not the gradient of an objective
  - paper: doi:10.1007/BF00547608
    title: Klaus Muller and Leo D. Brown, Location of saddle points and minimum energy paths by a constrained simplex optimization procedure, Theoretica Chimica Acta 53(1), 1979, 75-93
    locator: the two-dimensional test potential of the example
---

The nudged elastic band (NEB) method finds a minimum energy path between two minima of a potential energy, and the saddle point on it. It places a chain of copies of the system, called images, between the two minima, joins them by springs, and moves each image under a force with two parts: the true force across the path and the spring force along it. When the forces are zero, the images lie on a minimum energy path, evenly spaced. With a climbing image, the highest image moves up along the path to the saddle. The barrier height and the curvatures at the saddle then give the rate by [harmonic transition state theory](/harmonic-transition-state-theory/).

## In plain words

Two valleys of an energy landscape are joined by many paths. The most likely path for a slow transition goes over the lowest pass, and on it each step goes straight downhill, away from the pass. This is the minimum energy path.

The band is a string of beads from one valley to the other. Each bead feels the pull of the landscape, but only across the string, so it does not slide back into a valley. Springs pull the beads only along the string, so they stay evenly spaced and do not cut corners. The string falls into the bottom of the channel that joins the valleys. One bead, the highest, gets a different rule: it climbs up along the string and stays down across it. It stops exactly at the pass.

## The problem

The input is a potential $V: \mathbb{R}^d \to \mathbb{R}$ with its gradient $\nabla V$, two minima $R_0$ and $R_N$, and the number $N$ of segments. For atoms, $V$ is the potential energy of the [energy landscape](/energy-landscape/) and the coordinates are mass weighted if the masses differ. The output is a band $R_0, \ldots, R_N$ that approximates a minimum energy path (MEP): a curve on which the gradient is parallel to the tangent at every point. The highest point of an MEP is a first-order saddle: a stationary point whose Hessian has exactly one negative eigenvalue.

## The algorithm

```pseudo id=main
NUDGED-ELASTIC-BAND(V, R_0, R_N, N, k, h, tol)
L1  R_i ← R_0 + (i/N)(R_N - R_0) for i = 0, ..., N
L2  repeat
L3      E_i ← V(R_i), g_i ← ∇V(R_i) for i = 1, ..., N-1
L4      τ_i ← the unit tangent at R_i from E_{i-1}, E_i, E_{i+1}
L5      F_i^s ← k (|R_{i+1} - R_i| - |R_i - R_{i-1}|) τ_i     ▷ spring force, along the path
L6      F_i ← -g_i + (g_i · τ_i) τ_i + F_i^s                ▷ true force, across the path
L7      if climbing then c ← the i with the largest E_i, F_c ← -g_c + 2 (g_c · τ_c) τ_c
L8      if max_i |F_i| < tol then return R_0, ..., R_N
L9      R_i ← R_i + h F_i for i = 1, ..., N-1               ▷ the ends stay fixed
```

Line L1 starts from the straight line between the two minima. Line L4 uses the tangent of Henkelman and Jonsson: if the energy rises from $i-1$ through $i$ to $i+1$, $\tau_i$ points along $R_{i+1} - R_i$; if it falls, along $R_i - R_{i-1}$. At a maximum or a minimum of the energy along the band, $\tau_i$ is a mean of the two vectors with the weights $\max(|E_{i+1} - E_i|, |E_{i-1} - E_i|)$ and $\min(\ldots)$, the larger weight on the vector to the neighbour with the higher energy. Line L5 is the spring force of the same paper: it depends on the difference of the two distances, not on the vectors. Line L6 removes the part of the true force $-g_i$ along $\tau_i$. These two projections are the "nudging". Line L7 is the climbing image: no spring, and the component of the true force along the band is inverted, so the image goes uphill along the band and downhill across it. Line L9 is a step of steepest descent along the NEB force with a fixed step $h$. The implementation switches the climbing image on when the largest force first falls below a threshold, so that the band is near the path when the climbing starts.

## Example

**One force by hand.** Take $V(x, y) = (x^2 - 1)^2 + 2y^2$, with minima at $(\pm 1, 0)$ and the saddle $(0, 0)$, and three images $(-1, 0)$, $(0, 0.5)$, $(1, 0)$. The energies are $0, 1.5, 0$, so the middle image is a maximum along the band. The two weights are both $1.5$ and $\tau = (2, 0) / 2 = (1, 0)$. The gradient at $(0, 0.5)$ is $g = (0, 2)$, so $g \cdot \tau = 0$ and the true force across the band is $(0, -2)$. The two distances are both $\sqrt{1.25}$, so the spring force is zero. The force is $F = (0, -2)$, with or without climbing. A step with $h = 0.05$ moves the image to $(0, 0.4)$. A band of 9 images started on $y = 0.5 \sin(\pi i / 8)$ converges in 101 iterations to $y = 0$ with the images at $x = -1, -0.75, \ldots, 1$, and the climbing image at the saddle $(0, 0)$.

**The Muller-Brown surface.** The Muller-Brown potential has minima $A = (-0.55822, 1.44173)$ with $V = -146.6995$, $C = (-0.05001, 0.46669)$ with $V = -80.7678$ and $B = (0.62350, 0.02804)$ with $V = -108.1667$. The saddle between A and C is $S1 = (-0.82200, 0.62431)$ with $V = -40.6648$, and between C and B it is $S2 = (0.21249, 0.29299)$ with $V = -72.2489$. On the straight line from A to C the energy reaches $3.39$, far above the saddle: the MEP bends far to the side. With $k = 50$, $h = 2 \times 10^{-4}$ and $\mathrm{tol} = 10^{-3}$, and the climbing image on below a force of 5, the band from A to C gives:

| segments $N$ | highest image, plain NEB | iterations | climbing image | iterations |
|---|---|---|---|---|
| 4 | $-42.7083$ at $(-0.8500, 0.6970)$ | 1303 | $-40.6648$ at $(-0.82200, 0.62431)$ | 440 |
| 8 | $-43.7972$ at $(-0.8581, 0.7094)$ | 4180 | $-40.6648$ at $(-0.82200, 0.62431)$ | 1350 |
| 16 | $-40.7129$ at $(-0.8132, 0.6171)$ | 14128 | $-40.6648$ at $(-0.82200, 0.62431)$ | 4310 |

The plain band puts no image at the saddle, so its highest image underestimates the barrier, by 3.1 for $N = 8$. The climbing image finds the saddle to the tolerance with any $N$. From C to B, the climbing image converges to S2. From A to B with $N = 8$, the band passes through C (one image has $V = -80.73$), and the climbing image goes to S1, the higher of the two saddles. A band joins two minima through every intermediate minimum on the way, and the climbing image finds only the highest saddle.

## Correctness

The proof below shows what a converged band is. Split each force into its parts along and across $\tau_i$. For an image that does not climb, the force is $-g_i^{\perp} + k(d_{i+1} - d_i)\tau_i$, where $d_i = |R_i - R_{i-1}|$, and the two parts are orthogonal. So the force is zero only if $g_i$ is parallel to the tangent (the discrete MEP condition) and the two distances are equal. For the climbing image, the force is $-(I - 2\tau\tau^{\mathsf T}) g_c$, a reflection of $-g_c$, so it has the length of the gradient, and a zero force means a stationary point of $V$. These are facts about the fixed points. The NEB force is not the gradient of any function, so there is no proof that the iteration converges; it does in practice when $h$ is small enough.

## Complexity

One iteration costs $N - 1$ evaluations of $V$ and $\nabla V$, of cost $G$ each, and $O(N d)$ arithmetic for the tangents, projections and steps, in the [real RAM](/real-ram/) model. The memory is $O(N d)$ for the band. The number $I$ of iterations depends on the conditioning of the landscape: steepest descent with step $h$ is stable only for $h < 2 / \lambda_{\max}$, where $\lambda_{\max}$ is the largest curvature, and it converges in a number of steps proportional to $\lambda_{\max} / \lambda_{\min}$. For Muller-Brown, $\lambda_{\max} \approx 4068$, so $h < 4.9 \times 10^{-4}$. For atoms, $G$ is the cost of a force call of the [interatomic potential](/interatomic-potential/) or of an electronic structure code, and it dominates everything else. The $N - 1$ force calls of one iteration are independent and run in parallel.

## Properties

- **Deterministic.** The same start gives the same band.
- **Gradients only.** No Hessian is needed. The curvatures at the saddle, needed for the rate, are computed once at the end.
- **Local.** The band finds an MEP near its start, not the MEP with the lowest barrier. Two different starts can give two different paths.
- **Not a minimization.** The NEB force is not the gradient of an objective, so optimizers that need a line search on an energy must be adapted (Sheppard, Terrell and Henkelman 2008).
- **Spacing control.** The spring constant $k$ sets only the spacing and the speed of convergence along the band, not the position of the converged path.

## Variants and improvements

- **The original tangent.** The first form of NEB estimated the tangent from the two neighbours without regard to their energies, and projected the vector sum of the two spring forces on it. Where the force along the path is large compared with the force across it, this gives kinks in the band; the improved tangent of line L4 removes them (Henkelman and Jonsson 2000).
- **The climbing image.** Line L7 is a modification of NEB that converges one image to the saddle. Without it, the barrier is found by interpolation between the images.
- **Optimizers.** Steepest descent is the simplest. Quick-min and FIRE are damped dynamics on the NEB force; [conjugate gradient](/conjugate-gradient-method/) and limited memory [BFGS](/bfgs/) over the whole band are often faster. Sheppard, Terrell and Henkelman compared them in 2008.
- **Variable springs.** A larger $k$ near the highest image puts more images near the saddle.
- **The string method.** The [string method](/string-method/) has no springs: it moves the images by the perpendicular force and then redistributes them by arc length.
- **Saddle refinement.** A short band, then the [dimer method](/dimer-method/) started from the highest image, often costs less than a fully converged band.

## When to use it

Use NEB when you know both end states of a transition, for example a vacancy hop or a surface reaction, and you need the barrier and the path. It needs only forces, and the images run in parallel. Use the [dimer method](/dimer-method/) when only the initial state is known, for example to build an event catalog for [kinetic Monte Carlo](/kinetic-monte-carlo/). At a finite temperature, when many paths contribute and the entropy matters, sample paths with [transition path sampling](/transition-path-sampling/) instead of finding one MEP.

## Pitfalls

- **End states that are not minima.** Relax both ends first. If an end is not at a minimum, the barrier is measured from a wrong reference.
- **A step that is too large.** With $h > 2 / \lambda_{\max}$ the stiff directions oscillate and the band blows up. Use a smaller $h$ or a damped optimizer.
- **Climbing too early.** If the climbing image is switched on far from the path, it can climb to a wrong region. Relax the plain band first.
- **Intermediate minima.** If an image sits in a minimum between the ends, the band has two barriers, and the climbing image finds only the higher one. Split the band into two at the intermediate minimum.
- **Too few images.** A band of few images can miss a bend of the MEP, and without a climbing image it underestimates the barrier, as in the table above.
- **The straight line start.** If the straight line passes through a region of very high energy, or atoms come too close on it, the first forces are huge. Start from a better interpolation.

## Implementations

## History

Mills and Jonsson introduced the nudged elastic band in 1994, in a study of the dissociative adsorption of H2 that used paths of quantum systems. Jonsson, Mills and Jacobsen gave the full method in 1998, with the projections that separate the true force from the spring force. In 2000 Henkelman, Uberuaga and Jonsson added the climbing image, and Henkelman and Jonsson gave the improved tangent that removes kinks. Muller and Brown had introduced their two-dimensional test potential in 1979 for an earlier method of finding saddles.

## References
