---
tag: C4EVM2
kind: algorithm
slug: random-walk-metropolis
name: Random-walk Metropolis
aliases:
- random-walk Metropolis-Hastings
- RWM
area: randomized/markov-chain-monte-carlo
level: core
summary: Metropolis-Hastings with the symmetric proposal y = x + σZ, accepted with probability min(1, π(y)/π(x)). For product targets as d → ∞, the best σ is near 2.38/√d, with acceptance rate 0.234.
solves: [sampling-from-stationary-distribution]
model: real-ram
complexity:
  vars: {T: the number of steps, d: the dimension, c: the cost of one evaluation of the unnormalized target}
  time: {worst: Θ(T (d + c))}
  space: {extra: Θ(d)}
properties: {in_place: true, online: true, deterministic: false, recursive: false}
history:
  year: 1953
  people: [Nicholas Metropolis, Gareth O. Roberts, Andrew Gelman, Walter R. Gilks]
  note: The 1953 Metropolis method used symmetric random moves. Roberts, Gelman and Gilks proved the optimal scaling result with the rate 0.234 in 1997.
prereqs: [metropolis-hastings, proposal-distribution]
see_also: [acceptance-probability, metropolis-adjusted-langevin-algorithm, hamiltonian-monte-carlo, independence-sampler, effective-sample-size, burn-in]
sources:
  - paper: doi:10.1214/aoap/1034625254
    title: Gareth O. Roberts, Andrew Gelman and Walter R. Gilks, Weak convergence and optimal scaling of random walk Metropolis algorithms, Annals of Applied Probability 7(1), 1997
    locator: pages 110 to 120 (the diffusion limit for product targets, the speed h(ℓ) and the rate 0.234)
  - paper: doi:10.1214/ss/1015346320
    title: Gareth O. Roberts and Jeffrey S. Rosenthal, Optimal scaling for various Metropolis-Hastings algorithms, Statistical Science 16(4), 2001
    locator: pages 351 to 367 (a survey of the scaling results, their hypotheses, and the rule 2.38/√d for Gaussian targets)
  - paper: doi:10.1214/aos/1033066201
    title: Kerrie L. Mengersen and Richard L. Tweedie, Rates of convergence of the Hastings and Metropolis algorithms, Annals of Statistics 24(1), 1996
    locator: pages 101 to 121 (geometric ergodicity of the random-walk algorithm on the real line)
  - paper: doi:10.1063/1.1699114
    title: Nicholas Metropolis, Arianna W. Rosenbluth, Marshall N. Rosenbluth, Augusta H. Teller and Edward Teller, Equation of state calculations by fast computing machines, Journal of Chemical Physics 21(6), 1953
    locator: pages 1087 to 1092 (symmetric uniform moves of one particle)
  - book: isbn:9780387212395
    title: Christian P. Robert and George Casella, Monte Carlo Statistical Methods, second edition, Springer, 2004
    locator: Chapter 7 (random walk Metropolis-Hastings and the calibration of the scale)
---

Random-walk Metropolis is the [Metropolis-Hastings](/metropolis-hastings/) algorithm with a symmetric random-walk [proposal](/proposal-distribution/): from $x \in \mathbb{R}^d$ it proposes $y = x + \sigma Z$, where $Z$ has a symmetric distribution, usually $\mathcal{N}(0, I_d)$. Because the proposal is symmetric, the [acceptance probability](/acceptance-probability/) is $\min(1, \pi(y)/\pi(x))$, with no Hastings factor. It needs only the values of the unnormalized density, no gradient. The one tuning parameter is the scale $\sigma$: for product targets in high dimension, the best $\sigma$ is about $2.38/\sqrt{d}$ in units of the target's spread, and then about $23.4\%$ of the proposals are accepted (Roberts, Gelman and Gilks 1997).

## In plain words

You stand at a point and take a random step of about a fixed size in a random direction. If the new point is more likely under the target, you move there. If it is less likely, you move there only with a chance equal to the ratio of the two likelihoods; otherwise you stay and count your current point again.

The step size is the only setting. With tiny steps, almost every step is accepted, but you crawl. With huge steps, you almost always land in an unlikely place and stay where you are. In many dimensions, the best step size gives about one accepted step in four, and the steps must get smaller as the number of dimensions grows, so the method gets slower in high dimension.

## The problem

The input is an unnormalized density $\tilde\pi = Z\pi$ on $\mathbb{R}^d$ (or on a lattice), a start $x_0$ with $\tilde\pi(x_0) > 0$, a scale $\sigma > 0$ and a number of steps $T$. The output is a Markov chain $X_1, \ldots, X_T$ with $\pi$ as a stationary distribution; this is [sampling from a stationary distribution](/sampling-from-stationary-distribution/). Pr, E and Var are probability, expectation and variance, $\Phi$ is the standard normal distribution function, and $I_d$ is the $d \times d$ identity. The model of randomness is $d$ standard normal reals and one uniform real in $[0, 1)$ for each step; in floating point, both are approximations of real random variables.

## The algorithm

```pseudo id=main
RANDOM-WALK-METROPOLIS(π̃, x0, σ, T)          ▷ π̃(x0) > 0
L1  x ← x0
L2  for t ← 1 to T do
L3      draw Z ~ N(0, I_d)
L4      y ← x + σ Z                             ▷ symmetric: Q(x, y) = Q(y, x)
L5      draw u uniformly from [0, 1)
L6      if u < π̃(y) / π̃(x) then x ← y          ▷ accept with probability min(1, π̃(y)/π̃(x))
L7      X_t ← x
L8  return X_1, …, X_T
```

The proposal density $Q(x, y) = (2\pi\sigma^2)^{-d/2}e^{-|y - x|^2/(2\sigma^2)}$ depends only on $|y - x|$, so $Q(x, y) = Q(y, x)$ and the Hastings factor is 1. Any symmetric increment works: uniform on a cube or a ball, or $\sigma L Z$ with a fixed matrix $L$, which has covariance $\sigma^2 LL^\top$. In code, line L6 compares logarithms: accept when $\log u < \log\tilde\pi(y) - \log\tilde\pi(x)$.

## Example

**A trace.** Let $\pi = \mathcal{N}(0, 1)$, so $\log\tilde\pi(x) = -x^2/2$, with $\sigma = 2.4$ and $x_0 = 0$.

| step | $x$ | $Z$ | $y$ | $\pi(y)/\pi(x)$ | $u$ | $X_t$ |
|---|---|---|---|---|---|---|
| 1 | 0 | 0.5 | 1.2 | $e^{-0.72} = 0.487$ | 0.30 | 1.2 |
| 2 | 1.2 | 0.8 | 3.12 | $e^{-4.147} = 0.016$ | 0.10 | 1.2 |
| 3 | 1.2 | −1.0 | −1.2 | $e^{0} = 1$ | 0.99 | −1.2 |
| 4 | −1.2 | 0.25 | −0.6 | $e^{0.54} = 1.716$ | 0.70 | −0.6 |

Step 2 is rejected, so the state 1.2 is recorded twice. Step 3 lands at the same density and is accepted for every $u$.

**The acceptance rate in one dimension.** For $\pi = \mathcal{N}(0, 1)$ and Gaussian steps of scale $\sigma$, the stationary acceptance rate is exactly

$$\bar\alpha(\sigma) = \frac{2}{\pi}\arctan\frac{2}{\sigma}.$$

So $\bar\alpha(1) = 0.705$, $\bar\alpha(2.4) = 0.442$ and $\bar\alpha(5) = 0.242$. The proof is in the proof file. The expected squared jump $E(X_{t+1} - X_t)^2$ is largest near $\sigma = 2.4$; the table on the [proposal distribution](/proposal-distribution/) page lists it for six scales.

## Correctness

**Theorem.** If $Z$ has a density $g$ with $g(z) = g(-z)$, the chain satisfies [detailed balance](/detailed-balance/) with respect to $\pi$, so $\pi$ is stationary.

The proposal density is $Q(x, y) = \sigma^{-d}g((y - x)/\sigma)$, which equals $Q(y, x)$ by the symmetry of $g$. So the Metropolis-Hastings ratio is $\tilde\pi(y)/\tilde\pi(x)$, which is the test of line L6, and the general proof on the [Metropolis-Hastings](/metropolis-hastings/) page applies. The full proof, with the acceptance rate formula, is in the proof file. For convergence: if $\pi$ is positive and continuous on $\mathbb{R}^d$ and $g > 0$ near 0, the chain is $\pi$-irreducible and aperiodic, so it converges in total variation from almost every start. The rate is another matter. On the real line, Mengersen and Tweedie (1996) showed that the chain is geometrically ergodic when the target's tails are log-concave, and that it is not geometrically ergodic when the tails are heavier than exponential, for example for a Cauchy target.

## Complexity

One step draws $d$ normals, adds two vectors and evaluates $\tilde\pi$ once (the value at $x$ is kept), so it costs $\Theta(d + c)$ time and $\Theta(d)$ space, and $T$ steps cost $\Theta(T(d + c))$.

**Optimal scaling (Roberts, Gelman and Gilks 1997).** The hypotheses are exact:

- the target is a product, $\pi_d(x) = \prod_{i=1}^d f(x_i)$, of one fixed density $f$ on $\mathbb{R}$, with $f$ positive and twice differentiable, $f'/f$ Lipschitz, $E_f[(f'(X)/f(X))^8] < \infty$ and $E_f[(f''(X)/f(X))^4] < \infty$;
- the proposal is $\mathcal{N}(x, (\ell^2/d)\,I_d)$ for a fixed $\ell > 0$;
- the chain starts in stationarity, $X_0 \sim \pi_d$, and $d \to \infty$.

Let $U^d_s$ be the first coordinate of $X_{\lfloor sd\rfloor}$, so time is sped up by the factor $d$. Then $U^d$ converges weakly to the Langevin diffusion $dU_s = h(\ell)^{1/2}dB_s + \frac12 h(\ell)(\log f)'(U_s)\,ds$, with speed

$$h(\ell) = 2\ell^2\,\Phi\Big(-\frac{\ell\sqrt{I}}{2}\Big), \qquad I = E_f\big[((\log f)'(X))^2\big],$$

and the mean acceptance rate tends to $a(\ell) = 2\Phi(-\ell\sqrt{I}/2)$. The speed $h$ is largest at $\ell = 2.38/\sqrt{I}$, where $a(\ell) = 0.234$ (more precisely $0.2338$). So the chain needs $O(d)$ steps per unit of diffusion time: the cost to move a fixed distance in each coordinate grows linearly with $d$.

The result is asymptotic and assumes a product target, a start in stationarity, and a Gaussian proposal. Later work extended it to some non-product targets (Roberts and Rosenthal 2001 survey them). It does not say that $0.234$ is best in low dimension (in one dimension, about $0.44$ is better, as the example above shows), or that $0.234$ is best for targets with very different scales in different directions.

## Properties

- **No gradient.** Only values of $\tilde\pi$ are needed, so it works for non-smooth targets.
- **Symmetric.** The Hastings factor is 1.
- **Scale-sensitive.** Performance depends on $\sigma$ and on how well the proposal covariance matches the target's covariance. For a Gaussian target with covariance $\Sigma$, use the proposal covariance $(2.38^2/d)\,\Sigma$.
- **Diffusive.** Accepted moves go in random directions, so the distance covered grows like the square root of the number of steps.

## Variants and improvements

- **Adaptive Metropolis.** Estimate the target covariance from the chain and set the proposal covariance to $(2.38^2/d)$ times it. Adapt only during [burn-in](/burn-in/), or use a scheme with diminishing adaptation.
- **Component-wise random walk.** Move one coordinate at a time (Metropolis-within-Gibbs).
- **[MALA](/metropolis-adjusted-langevin-algorithm/).** Add a drift along the gradient of $\log\pi$; the step can then scale as $d^{-1/3}$ instead of $d^{-1/2}$.
- **[HMC](/hamiltonian-monte-carlo/) and [NUTS](/no-u-turn-sampler/).** Follow a simulated trajectory to make long moves with high acceptance.
- **Heavy-tailed increments.** A $t$ or Cauchy increment helps on heavy-tailed targets.

## When to use it

Use random-walk Metropolis for a target in a few dimensions, for a target without a usable gradient, or as a first try that needs only $\log\tilde\pi$. In tens or hundreds of dimensions with a smooth target, gradient methods are much faster. For targets with separated modes, add [parallel tempering](/parallel-tempering/).

## Pitfalls

- **Tuning to a high acceptance rate.** A rate near 1 means the steps are too small. In high dimension aim near $0.234$, in one dimension near $0.44$, and check the [effective sample size](/effective-sample-size/), not the rate alone.
- **An isotropic step on a stretched target.** If the target's scales differ by a factor of 100, a common $\sigma$ must fit the smallest scale, and the chain crawls along the largest one. Rescale the coordinates, or use a proposal covariance.
- **Proposals outside the support.** If $\tilde\pi(y) = 0$, line L6 rejects. This is correct; do not reflect or clip $y$ without the matching correction.
- **Reading the 0.234 rule as a theorem for every target.** It is a limit theorem under the hypotheses above.

## Implementations

## History

The method of Metropolis, the Rosenbluths and the Tellers (1953) moved one particle at a time by a uniform symmetric step, so it was a random-walk Metropolis algorithm. Gelman, Roberts and Gilks proposed the scale $2.38/\sqrt d$ for Gaussian targets in the mid-1990s, and Roberts, Gelman and Gilks (1997) proved the diffusion limit and the rate $0.234$.

## References
