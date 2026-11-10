---
tag: AW5Q0G
kind: algorithm
slug: independence-sampler
name: Independence sampler
aliases:
- independent Metropolis-Hastings
- Metropolized independence sampler
area: randomized/markov-chain-monte-carlo
level: core
summary: Metropolis-Hastings whose proposal q ignores the current state. It accepts with probability min(1, w(y)/w(x)), w = π/q, and it is uniformly ergodic exactly when w is bounded.
solves: [sampling-from-stationary-distribution]
model: real-ram
complexity:
  vars: {T: the number of steps, c: the cost of one draw from q plus one evaluation of the weight w}
  time: {worst: Θ(T c)}
  space: {extra: Θ(1)}
properties: {in_place: true, online: true, deterministic: false, recursive: false}
history:
  year: 1994
  people: [W. Keith Hastings, Luke Tierney, Jun S. Liu, Kerrie L. Mengersen, Richard L. Tweedie]
  note: Hastings (1970) allowed any proposal. Tierney (1994) named the independence chain, Mengersen and Tweedie (1996) found when it is uniformly ergodic, and Liu (1996) found its eigenvalues on finite spaces.
prereqs: [metropolis-hastings, proposal-distribution, rejection-sampling]
see_also: [importance-sampling, random-walk-metropolis, acceptance-probability, mixing-time, total-variation-distance, coupling-method]
sources:
  - paper: doi:10.1214/aos/1033066201
    title: Kerrie L. Mengersen and Richard L. Tweedie, Rates of convergence of the Hastings and Metropolis algorithms, Annals of Statistics 24(1), 1996
    locator: pages 101 to 121 (the independence sampler is uniformly ergodic when q/π is bounded below and not geometrically ergodic otherwise)
  - paper: doi:10.1007/BF00162521
    title: Jun S. Liu, Metropolized independent sampling with comparisons to rejection sampling and importance sampling, Statistics and Computing 6(2), 1996
    locator: pages 113 to 119 (the eigenvalues of the kernel on a finite space)
  - paper: doi:10.1214/aos/1176325750
    title: Luke Tierney, Markov chains for exploring posterior distributions, Annals of Statistics 22(4), 1994
    locator: pages 1701 to 1728 (independence chains, and their comparison with rejection sampling)
  - paper: doi:10.1093/biomet/57.1.97
    title: W. Keith Hastings, Monte Carlo sampling methods using Markov chains and their applications, Biometrika 57(1), 1970
    locator: pages 97 to 109 (the general proposal and the acceptance ratio)
  - book: isbn:9780387212395
    title: Christian P. Robert and George Casella, Monte Carlo Statistical Methods, second edition, Springer, 2004
    locator: Chapter 7 (the independent Metropolis-Hastings algorithm)
---

The independence sampler is the [Metropolis-Hastings](/metropolis-hastings/) algorithm with a [proposal](/proposal-distribution/) $q$ that does not depend on the current state. A proposal $y \sim q$ is accepted with probability $\min(1, w(y)/w(x))$, where $w = \pi/q$ is the importance weight, so the chain prefers states that $q$ under-samples. If $w \le M$ everywhere, the chain is uniformly ergodic and $\|P^t(x, \cdot) - \pi\|_{TV} \le (1 - 1/M)^t$ from every start; if $w$ is unbounded, it is not even geometrically ergodic (Mengersen and Tweedie 1996). It uses the same pair $(\pi, q)$ as [rejection sampling](/rejection-sampling/) and [importance sampling](/importance-sampling/), but it needs neither the bound $M$ nor the normalizing constant.

## In plain words

You have a simple distribution you can draw from, and you want draws from a harder one. Each step, draw a fresh candidate from the simple distribution, without looking at where you are now. Give each point a weight: how much more likely it is under the target than under the simple distribution. Move to the candidate if its weight is larger than your current weight; otherwise move only with a chance equal to the ratio of the weights.

If the simple distribution covers the target well everywhere, this works very well, because each candidate is a new independent guess. If the simple distribution almost never reaches some likely part of the target, the chain can get stuck there for a very long time once it gets in.

## The problem

The input is an unnormalized target $\tilde\pi = Z_\pi\pi$, a proposal density $q$ that we can sample from and evaluate up to a constant ($\tilde q = Z_q q$), a start $x_0$ with $\tilde\pi(x_0) > 0$, and a number of steps $T$. The weight is $\tilde w = \tilde\pi/\tilde q$, a constant times $w = \pi/q$. The output is a Markov chain $X_1, \ldots, X_T$ with $\pi$ as a stationary distribution: [sampling from a stationary distribution](/sampling-from-stationary-distribution/). We need $q(y) > 0$ wherever $\pi(y) > 0$, otherwise the chain can never reach part of the support. The model of randomness is a draw from $q$ and one uniform real in $[0, 1)$ for each step. $\|\mu - \nu\|_{TV}$ is the [total variation distance](/total-variation-distance/).

## The algorithm

```pseudo id=main
INDEPENDENCE-SAMPLER(π̃, q̃, x0, T)       ▷ π̃(x0) > 0, and q > 0 where π > 0
L1  x ← x0
L2  for t ← 1 to T do
L3      draw y ~ q                          ▷ does not depend on x
L4      r ← w̃(y) / w̃(x)                     ▷ w̃ = π̃ / q̃, so Z_π and Z_q cancel
L5      draw u uniformly from [0, 1)
L6      if u < r then x ← y
L7      X_t ← x
L8  return X_1, …, X_T
```

Line L4 is the Metropolis-Hastings ratio $\pi(y)q(x)/(\pi(x)q(y))$ with $Q(x, y) = q(y)$. In code, keep $\log\tilde w(x)$ and compare logarithms.

## Example

Let the states be $\{0, 1, 2\}$ with $\pi = (1/6, 1/3, 1/2)$ and $q = (1/2, 1/4, 1/4)$. The weights are $w = (1/3, 4/3, 2)$, so $M = \max w = 2$. From state 1, the proposal 0 is accepted with probability $w(0)/w(1) = 1/4$, and the proposal 2 is always accepted. The exact kernel is

$$P = \begin{pmatrix} 1/2 & 1/4 & 1/4 \\ 1/8 & 5/8 & 1/4 \\ 1/12 & 1/6 & 3/4 \end{pmatrix}.$$

Each row of $P$ dominates $\pi/M = (1/12, 1/6, 1/4)$, as the proof below needs. The eigenvalues are $1$, $1/2$ and $3/8$. The total variation distance after $t$ steps from state 0 is

| $t$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $\|P^t(0, \cdot) - \pi\|_{TV}$ | 1/3 | 13/96 | 1/16 | 1/32 | 1/64 |
| bound $(1 - 1/M)^t$ | 1/2 | 1/4 | 1/8 | 1/16 | 1/32 |

The second eigenvalue is exactly $1 - 1/M = 1/2$. Liu (1996) showed this in general on a finite space: if the states are sorted so that $w_1 \ge w_2 \ge \cdots \ge w_n$, the eigenvalues other than 1 are $\lambda_k = \sum_{i \ge k}(q_i - \pi_i/w_k)$ for $k = 1, \ldots, n - 1$, and the largest is $\lambda_1 = 1 - 1/w_1$. Here the sorted order is $(2, 1, 0)$, which gives $\lambda_1 = 1/2$ and $\lambda_2 = (1/4 + 1/2) - (1/3 + 1/6)\cdot\frac34 = 3/8$.

## Correctness

The proposal is $Q(x, y) = q(y)$, so the general [detailed balance](/detailed-balance/) proof on the [Metropolis-Hastings](/metropolis-hastings/) page applies with the ratio $\pi(y)q(x)/(\pi(x)q(y)) = w(y)/w(x)$. So $\pi$ is stationary.

**Theorem (Mengersen and Tweedie 1996).** If $w(y) \le M$ for $\pi$-almost every $y$, then for every start $x$ and every $t \ge 0$, $\|P^t(x, \cdot) - \pi\|_{TV} \le (1 - 1/M)^t$. If $w$ is not $\pi$-essentially bounded, the chain is not geometrically ergodic.

The upper bound has a short proof, given in full in the proof file. For every $x$ and $y$, $q(y)\min(1, w(y)/w(x)) = \min(q(y), \pi(y)/w(x)) \ge \pi(y)/M$, because $q(y) = \pi(y)/w(y) \ge \pi(y)/M$ and $w(x) \le M$. So $P(x, \cdot) \ge \pi/M$: each step is, with probability at least $1/M$, a fresh exact draw from $\pi$. This is a Doeblin minorization, and it gives the geometric bound by a [coupling](/coupling-method/) or a contraction argument. The converse is harder: if $w$ is unbounded, then from states with large $w(x)$ the probability of leaving is at most about $1/w(x)$, so the chain holds there for a long time, and Mengersen and Tweedie showed that this rules out a geometric rate.

## Complexity

One step costs one draw from $q$ and one evaluation of $\tilde w$, so $\Theta(c)$, and $T$ steps cost $\Theta(Tc)$. The extra space is $\Theta(1)$ beyond one state. With $w \le M$, the [mixing time](/mixing-time/) is at most $\lceil M\ln(1/\varepsilon)\rceil$ steps for distance $\varepsilon$, since $(1 - 1/M)^t \le e^{-t/M}$. In $d$ dimensions with a product target and a product proposal, $M$ is usually exponential in $d$, so the method is practical only when $q$ is a very good fit.

## Properties

- **Global moves.** Each proposal is independent of the state, so one accepted move can jump between modes.
- **The same weights as importance sampling.** The chain is a resampling scheme driven by $w$. Liu (1996) showed that its efficiency is close to that of rejection sampling with the same $M$, and that rejection sampling is a little better when $M$ is known.
- **No knowledge of $M$.** Unlike [rejection sampling](/rejection-sampling/), the algorithm runs without a bound; the bound only controls the speed.
- **Positive correlation.** Rejections repeat states, so the samples are correlated, and the [effective sample size](/effective-sample-size/) is below $T$.

## Variants and improvements

- **Adaptive independence samplers.** Fit $q$ to the chain, for example a mixture of Gaussians or a $t$ distribution at the posterior mode, and refit during [burn-in](/burn-in/).
- **Mixtures with local moves.** Alternate independence steps with [random-walk Metropolis](/random-walk-metropolis/) steps: the independence steps jump between modes, and the local steps explore inside a mode.
- **Multiple-try and particle independence samplers.** Draw several candidates per step and choose among them by weight.
- **Rejection with a Metropolis correction.** Tierney (1994) combined a rejection step with an independence step, so that an inexact bound $M$ still gives a correct chain.

## When to use it

Use it when a good global approximation of $\pi$ is available, for example a Laplace or variational approximation with heavier tails than $\pi$. Choose $q$ with heavier tails than $\pi$, so that $w$ stays bounded. Do not use it with a proposal that is narrower than the target, or in high dimension without a very good fit.

## Pitfalls

- **Light-tailed proposals.** If $q$ has lighter tails than $\pi$, $w$ is unbounded, and the chain gets stuck in the tails. Short runs may never visit the tails, so the output can look fine and still be wrong. For example, $\pi = \mathcal{N}(0, 4)$ with $q = \mathcal{N}(0, 1)$ has $w(6) = e^{13.5}/2 \approx 3.6 \times 10^5$. The probability of leaving $x$ is at most $E_q[w(Y)]/w(x) = 1/w(x)$, so from $x = 6$ the chain stays for at least $3.6 \times 10^5$ steps on average.
- **A high acceptance rate is good here.** Unlike for random-walk proposals, an acceptance rate near 1 means that $q$ is close to $\pi$.
- **Forgetting the Hastings factor.** The ratio is $w(y)/w(x)$, not $\pi(y)/\pi(x)$. With the ratio $\pi(y)/\pi(x)$, the chain satisfies detailed balance with respect to the density proportional to $\pi q$, not $\pi$, because $\pi(x)q(x)\,q(y)\min(1, \pi(y)/\pi(x)) = q(x)q(y)\min(\pi(x), \pi(y))$ is symmetric.

## Implementations

## History

Hastings (1970) allowed proposals that ignore the current state. Tierney (1994) named the independence chain and gave its basic theory. In 1996, Mengersen and Tweedie proved that it is uniformly ergodic exactly when $\pi/q$ is bounded, and Liu found the full spectrum on finite spaces and compared the sampler with rejection sampling and importance sampling.

## References
