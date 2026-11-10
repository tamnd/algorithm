---
tag: 97GJYT
kind: algorithm
slug: slice-sampling
name: Slice sampling
aliases:
- slice sampler
- Neal slice sampler
area: randomized/markov-chain-monte-carlo
level: core
summary: Samples uniformly under the graph of f ∝ π. Draw a height y under f(x), then a new x from the slice {f > y} by stepping out and shrinking an interval. There is no rejection and little tuning.
solves: [sampling-from-stationary-distribution]
model: real-ram
complexity:
  vars: {T: the number of steps, d: the number of coordinates, m: the limit on the number of stepping-out moves, k: the number of shrinkage draws in one update, c: the cost of one evaluation of f}
  time: {worst: Θ(T d (m + k) c)}
  space: {extra: Θ(d)}
properties: {in_place: true, online: true, deterministic: false, recursive: false}
history:
  year: 2003
  people: [Radford M. Neal, Paul Damien, Jon Wakefield, Stephen Walker]
  note: Auxiliary-variable methods of this kind go back to Swendsen and Wang. Neal (2003) gave the stepping-out, doubling and shrinkage procedures that make slice sampling practical.
prereqs: [gibbs-sampling]
see_also: [metropolis-hastings, random-walk-metropolis, swendsen-wang, uniform-distribution, rejection-sampling, detailed-balance]
sources:
  - paper: doi:10.1214/aos/1056562461
    title: Radford M. Neal, Slice sampling, Annals of Statistics 31(3), 2003
    locator: pages 705 to 767 (stepping out, doubling, shrinkage, and the proof that the updates leave the uniform distribution on the slice invariant)
  - paper: doi:10.1111/1467-9868.00179
    title: Paul Damien, Jon Wakefield and Stephen Walker, Gibbs sampling for Bayesian non-conjugate and hierarchical models by using auxiliary variables, Journal of the Royal Statistical Society Series B 61(2), 1999
    locator: pages 331 to 344 (auxiliary uniform variables that make every conditional easy to sample)
  - paper: doi:10.1111/1467-9868.00198
    title: Gareth O. Roberts and Jeffrey S. Rosenthal, Convergence of slice sampler Markov chains, Journal of the Royal Statistical Society Series B 61(3), 1999
    locator: pages 643 to 660 (geometric ergodicity and quantitative bounds for the simple slice sampler)
  - paper: doi:10.1111/1467-9469.00267
    title: Antonietta Mira and Luke Tierney, Efficiency and convergence properties of slice samplers, Scandinavian Journal of Statistics 29(1), 2002
    locator: pages 1 to 12 (uniform ergodicity of the simple slice sampler, and a comparison with independence samplers)
---

Slice sampling draws from a density $\pi \propto f$ by sampling uniformly from the region under the graph of $f$, $U = \{(x, y) : 0 < y < f(x)\}$, and keeping $x$. It alternates two moves that each leave the uniform distribution on $U$ invariant: a vertical move that draws a height $y$ uniformly from $(0, f(x))$, and a horizontal move that draws a new $x$ from the slice $S_y = \{x : f(x) > y\}$. The horizontal move does not need to find $S_y$: Neal (2003) builds an interval around $x$ by stepping out, then samples from it and shrinks it toward $x$ on each miss. Every update moves, no proposal is rejected, and the one width parameter $w$ is much less sensitive than the scale of [random-walk Metropolis](/random-walk-metropolis/).

## In plain words

Draw the graph of the target density. The points under the curve form a region, and if you pick a point uniformly from that region, its horizontal position has exactly the target distribution.

So walk inside that region. From where you are, pick a random height under the curve at your position. At that height, draw a horizontal line; the part of the line under the curve is the slice. Pick a new position somewhere on the slice. To find the slice, lay down a short interval around you and widen it in fixed steps until both ends are outside the curve. Then pick random points in the interval; each time a point falls outside the curve, cut the interval at that point, keeping your side. Soon a point lands inside, and you move there.

## The problem

The input is a function $f \ge 0$ on $\mathbb{R}$ (or on $\mathbb{R}^d$, one coordinate at a time) with $0 < \int f < \infty$, a start $x_0$ with $f(x_0) > 0$, a width $w > 0$, a limit $m \ge 1$ on the number of stepping-out moves, and a number of steps $T$. The target is $\pi = f/\int f$. The output is a Markov chain $X_1, \ldots, X_T$ with $\pi$ as a stationary distribution: [sampling from a stationary distribution](/sampling-from-stationary-distribution/). The model of randomness is a stream of independent uniform reals in $[0, 1)$.

## The algorithm

One update of a single real variable, with stepping out and shrinkage:

```pseudo id=main
SLICE-SAMPLER(f, x0, w, m, T)            ▷ f(x0) > 0, width w > 0, limit m ≥ 1
L1  x ← x0
L2  for t ← 1 to T do
L3      draw y uniformly from (0, f(x))                     ▷ vertical move
L4      draw U, V uniformly; L ← x − wU; R ← L + w; J ← ⌊mV⌋; K ← m − 1 − J
L5      while J > 0 and y < f(L) do L ← L − w; J ← J − 1   ▷ step out to the left
L6      while K > 0 and y < f(R) do R ← R + w; K ← K − 1   ▷ step out to the right
L7      repeat: draw x1 uniformly from (L, R)
L8          if y < f(x1) then x ← x1 and leave the loop      ▷ x1 is in the slice
L9          if x1 < x then L ← x1 else R ← x1               ▷ shrink toward x
L10     X_t ← x
L11 return X_1, …, X_T
```

For $x \in \mathbb{R}^d$, apply lines L3 to L9 to one coordinate at a time, with the other coordinates fixed; this is a [Gibbs](/gibbs-sampling/)-style sweep with a slice update in place of an exact conditional draw. In code, work with $\log f$: line L3 becomes $\log y = \log f(x) + \log(1 - u)$ for a uniform $u$, which avoids underflow.

## Example

Let $f(x) = e^{-x^2/2}$, $x_0 = 0.5$, $w = 1$ and $m = 4$, so $f(x_0) = 0.8825$.

1. Line L3 draws $y = 0.6 f(x_0) = 0.5295$. The true slice is $|x| < \sqrt{-2\ln 0.5295} = 1.128$, but the algorithm does not know this.
2. Line L4 with $U = 0.3$ and $V = 0.6$ gives $L = 0.2$, $R = 1.2$, $J = 2$ and $K = 1$.
3. Line L5: $f(0.2) = 0.980 > y$, so $L = -0.8$ and $J = 1$. Then $f(-0.8) = 0.726 > y$, so $L = -1.8$ and $J = 0$, and the budget stops the loop.
4. Line L6: $f(1.2) = 0.487 < y$, so $R$ stays at 1.2.
5. Line L7 draws $x_1 = -1.5$. Then $f(-1.5) = 0.325 < y$, a miss, and $-1.5 < x$, so line L9 sets $L = -1.5$.
6. Line L7 draws $x_1 = 0.39$ from $(-1.5, 1.2)$. Then $f(0.39) = 0.927 > y$, so $x = 0.39$.

The interval $(-1.8, 1.2)$ did not cover the whole slice on the right, and the left end overshot. Neither matters for correctness, as the proof shows.

## Correctness

**Theorem.** Each update leaves $\pi$ invariant.

The proof is in the proof file; here is the outline. Let $\mu$ be the uniform distribution on the region $U$ under the graph; its $x$-marginal is $\pi$. The vertical move draws $y$ from its exact conditional given $x$ under $\mu$, so it is a Gibbs step and leaves $\mu$ invariant. For the horizontal move, fix $y$. It is enough to show that the transition density $T_y(x_0, x_1)$ on the slice $S_y$ is symmetric, $T_y(x_0, x_1) = T_y(x_1, x_0)$ for $x_0, x_1 \in S_y$, because then the uniform distribution on $S_y$, which is the conditional of $x$ given $y$ under $\mu$, is invariant. Symmetry has two parts.

- **Stepping out.** The offset $U$ puts a grid of spacing $w$ on the line, and the grid has the same uniform offset from any start. For a fixed grid, the final interval from $x_0$ is $[L, R)$ only if every grid point strictly inside is in the slice, and the number of values of $J$ that give $[L, R)$ is the same from every start cell inside $[L, R)$. This is why the budget $m$ is split at random between the two sides.
- **Shrinkage.** From $x_0$, a run of rejected points $r_1, \ldots, r_k$ followed by $x_1$ can happen only if no $r_i$ lies between $x_0$ and $x_1$, since otherwise $x_1$ would have been cut off. Then each $r_i$ is on the same side of $x_1$ as of $x_0$, so the run $r_1, \ldots, r_k$ followed by $x_0$ from $x_1$ shrinks the same intervals, and it has the same density.

The combined update is not a Metropolis-Hastings step: it always moves to a point of the slice, but how far it moves adapts to the slice.

## Complexity

One update costs at most $m + 1$ evaluations of $f$ in stepping out, plus one for each shrinkage draw. If the slice is an interval of length $\ell$, stepping out uses about $\ell/w$ evaluations when $m$ is large, and shrinkage cuts the interval by a constant factor on average for each miss, so it needs about $O(\log(mw/\ell))$ draws. A width $w$ that is too small costs about $\ell/w$ evaluations, and a $w$ that is too large costs about $\log(w/\ell)$ evaluations. This logarithmic penalty is why slice sampling is robust to $w$, while a random-walk proposal that is too large loses acceptance in proportion. Per sweep over $d$ coordinates, the time is $\Theta(d(m + k)c)$, where $k$ is the number of shrinkage draws in one update. The extra space is $\Theta(d)$.

## Properties

- **No rejections.** Each update returns a point of the slice. The chain can still stay near $x$ if the slice is short.
- **Adaptive step.** The size of the move adapts to the local scale of $f$.
- **Only values of $f$.** No gradient, and $f$ need not be normalized.
- **Convergence of the simple slice sampler.** The idealized sampler that draws exactly from the uniform distribution on each slice has strong convergence properties: Roberts and Rosenthal (1999) proved geometric ergodicity and quantitative bounds for broad classes of targets, and Mira and Tierney (2002) gave conditions for uniform ergodicity, for example a bounded $f$ with bounded support.

## Variants and improvements

- **Doubling.** Double the interval instead of stepping out by $w$. This finds wide slices faster, but needs an extra acceptance check that the same interval could have been built from $x_1$ (Neal 2003).
- **Multivariate slice sampling.** Use a hyperrectangle around $x$ and shrink it on each miss, instead of one coordinate at a time.
- **Elliptical slice sampling.** For a Gaussian prior times a likelihood, propose on an ellipse through $x$ and shrink the angle. Murray, Adams and MacKay introduced it in 2010.
- **Auxiliary variables in general.** [Swendsen-Wang](/swendsen-wang/) adds one auxiliary variable per edge, which can be written as a uniform variable under that edge's factor, on the [Ising model](/ising-model/), and Damien, Wakefield and Walker (1999) used one uniform variable per likelihood factor.

## When to use it

Use slice sampling for low-dimensional or coordinate-wise updates when the scale of the target is unknown or varies, for example for hyperparameters in hierarchical models. In high dimension with strong correlations, coordinate-wise slice updates are slow, just like [Gibbs sampling](/gibbs-sampling/), and [HMC](/hamiltonian-monte-carlo/) is usually better.

## Pitfalls

- **Rounding in the vertical move.** Compute $\log y$, not $y$: for a peaked or high-dimensional target, $f(x)$ underflows.
- **Changing the rules between steps.** The symmetry proof needs that the stepping-out rule is the same from every point of the interval. Do not stop the expansion based on information other than the endpoint values, and do not shrink away from $x$.
- **Multimodal slices.** If the slice has several pieces separated by more than $w$, stepping out may not reach them. The update is still correct, but it mixes slowly between modes.
- **Unbounded loops.** With $m = \infty$ and a density with heavy tails, stepping out can take many steps. Keep $m$ finite.

## Implementations

## History

Auxiliary-variable samplers began with the [Swendsen-Wang](/swendsen-wang/) algorithm (1987) and its interpretation by Edwards and Sokal (1988). Statisticians used one uniform auxiliary variable per factor in the late 1990s, among them Damien, Wakefield and Walker (1999). Neal (2003) gave general and practical procedures, stepping out, doubling and shrinkage, with the proof that they leave the target invariant.

## References
