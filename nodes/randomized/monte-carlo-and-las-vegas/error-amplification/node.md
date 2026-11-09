---
tag: 6AMN1G
kind: technique
slug: error-amplification
name: Error amplification by repetition
aliases:
- probability amplification
- amplification by repetition
- error reduction
area: randomized/monte-carlo-and-las-vegas
level: core
summary: Repeat a randomized test and take a majority or an OR of the outcomes to make the error probability exponentially small.
prereqs: [one-sided-error, two-sided-error, chernoff-bound, independent-random-variables]
see_also: [monte-carlo-algorithm, hoeffding-inequality, median-trick, randomness-amplification, miller-rabin-primality-test, freivalds-algorithm, karger-min-cut, bpp]
sources:
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 7, Randomized computation (error reduction for RP and for BPP, with the Chernoff bound); Chapter 21 (expander walks for randomness-efficient error reduction)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 1, Section 1.1 (repeating the min-cut algorithm) and Section 1.5 (reducing the error of RP and BPP algorithms); Chapter 4 (tail inequalities)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 1 (repetition for polynomial identities, matrix multiplication and min cut) and Chapter 4 (Chernoff and Hoeffding bounds)
  - paper: doi:10.1080/01621459.1963.10500830
    title: Wassily Hoeffding, Probability inequalities for sums of bounded random variables, Journal of the American Statistical Association 58(301), 1963
    locator: pages 13 to 30 (the bound exp(-2 t^2 n) for the mean of n bounded independent variables)
---

Error amplification makes the error of a [Monte Carlo algorithm](/monte-carlo-algorithm/) as small as needed by running it several times with independent random bits and combining the answers. For [one-sided error](/one-sided-error/), an OR of $k$ runs has error at most $\delta_0^k$. For [two-sided error](/two-sided-error/), a majority vote of $k$ runs has error at most $e^{-2\gamma^2 k}$, where $\gamma$ is the gap of each run's error below $1/2$; the proof is a [Chernoff](/chernoff-bound/)-type bound. Both turn a constant error into error $\delta$ with $O(\log(1/\delta))$ runs, which is why the constants $1/2$ and $1/3$ in the definitions of [RP](/rp/) and [BPP](/bpp/) do not matter.

## In plain words

A test that is right most of the time can be made almost always right by running it again with new coin flips. How to combine the runs depends on the kind of mistake.

If one answer is always trustworthy, for example "this number is composite", then a single trustworthy answer settles the question. The test is wrong only if every run gives the other answer, and the chance of that drops by the same factor with each run.

If both answers can be wrong, take a vote. Each run is right more often than wrong, so the majority of many runs is wrong only when an unusually large share of runs go wrong at once, and that chance also drops exponentially in the number of runs.

## When it applies

- A randomized decision procedure whose error is bounded on **every input**, with fresh, independent random bits available for each run.
- One-sided error with any error $\delta_0 < 1$, even $1 - 1/q(n)$ for a polynomial $q$.
- Two-sided error with a gap: each run is correct with probability at least $1/2 + \gamma$, with $\gamma$ a constant or at least an inverse polynomial.
- Search and optimization problems whose outputs can be compared or checked, such as cuts by their size.

Notation on this page: $\delta_0$ is the error of one run, $\delta$ is the target error, $\gamma = 1/2 - \delta_0$ is the gap for two-sided error, and $k$ is the number of runs. Probabilities are over the random bits for one fixed input.

## The template

```pseudo id=main
AMPLIFY(x, A, k, mode)                ▷ A is the base test; k runs
L1  yes ← 0
L2  for i ← 1 to k do
L3      if A(x) with fresh random bits says yes then yes ← yes + 1
L4  if mode = OR then return yes ≥ 1            ▷ one-sided, "yes" is certain
L5  if mode = AND then return yes = k           ▷ one-sided, "no" is certain
L6  return yes > k/2                              ▷ two-sided, k odd
```

In OR mode the loop can stop at the first "yes", and in AND mode at the first "no". For a search problem, the loop keeps the best output so far, or the first output that a verifier accepts.

### One-sided error: OR of the runs

**Claim.** If $A$ has RP-type error $\delta_0$ (a "yes" is always correct), then OR mode has RP-type error at most $\delta_0^k$.

*Proof.* On a "no" input, every run says "no", so line L4 returns "no". On a "yes" input, line L4 returns "no" only if all $k$ runs say "no". The runs use independent bits, so this has probability $\prod_{i=1}^{k} \Pr[\text{run } i \text{ says no}] \le \delta_0^k$. $\square$

**Rounds.** The error is at most $\delta$ when $\delta_0^k \le \delta$, so

$$k = \left\lceil \frac{\ln(1/\delta)}{\ln(1/\delta_0)} \right\rceil.$$

This is the least $k$ that works for every test whose error is exactly $\delta_0$. For a test with small success probability $p$, $\ln(1/(1-p)) \ge p$, so $k = \lceil \ln(1/\delta)/p \rceil$ is enough.

| target $\delta$ | $\delta_0 = 1/2$ (Freivalds) | $\delta_0 = 1/4$ (Miller-Rabin) | $p = 1/45$ (Karger, 10 vertices), $\lceil 45 \ln(1/\delta) \rceil$ |
| --- | --- | --- | --- |
| $10^{-2}$ | 7 | 4 | 208 |
| $10^{-6}$ | 20 | 10 | 622 |
| $10^{-9}$ | 30 | 15 | 933 |
| $2^{-64}$ | 64 | 32 | |

For Karger's case with $\delta = 10^{-3}$, the simple formula gives 311 runs and the exact formula $\lceil \ln 1000 / \ln(45/44) \rceil$ gives 308.

### Two-sided error: majority vote

**Claim.** If each run is correct with probability at least $1/2 + \gamma$, where $0 < \gamma \le 1/2$, and $k$ is odd, then line L6 is wrong with probability at most

$$(1 - 4\gamma^2)^{k/2} \le e^{-2\gamma^2 k}.$$

*Proof.* Let $q \le 1/2 - \gamma$ be the probability that one run is wrong. The majority is wrong only if the set $W$ of wrong runs has $|W| \ge k/2$. For a fixed set $W$ of size $w \ge k/2$, the runs are independent, so

$$\Pr[\text{exactly the runs of } W \text{ are wrong}] = q^{w}(1-q)^{k-w} = \big(q(1-q)\big)^{k/2} \left(\frac{q}{1-q}\right)^{w - k/2} \le \big(q(1-q)\big)^{k/2},$$

because $q < 1/2$ gives $q/(1-q) < 1$ and $w - k/2 \ge 0$. The function $x(1-x)$ increases on $[0, 1/2]$, so $q(1-q) \le (1/2-\gamma)(1/2+\gamma) = 1/4 - \gamma^2$. There are at most $2^k$ sets $W$, so the error is at most $2^k (1/4 - \gamma^2)^{k/2} = (1 - 4\gamma^2)^{k/2}$. Finally $1 - y \le e^{-y}$ gives $(1 - 4\gamma^2)^{k/2} \le e^{-2\gamma^2 k}$. $\square$

The same proof gives $(4q(1-q))^{k/2}$, which is better when $q$ is small. [Hoeffding's inequality](/hoeffding-inequality/) on the fraction of correct runs gives the bound $e^{-2\gamma^2 k}$ directly.

**Rounds.** The error is at most $\delta$ when

$$k \ge \frac{\ln(1/\delta)}{2\gamma^2}, \qquad \text{for example } k \ge 18 \ln(1/\delta) \text{ when } \delta_0 = 1/3.$$

Take the least odd integer above this value. The bound is safe but not exact. The exact error of the majority of $k$ runs with error $q$ is the binomial tail $\sum_{i > k/2} \binom{k}{i} q^i (1-q)^{k-i}$, which increases with $q$, so its value at $q = \delta_0$ gives the least $k$ that works for every test with error at most $\delta_0$:

| $\delta_0$ | target $\delta$ | least odd $k$, exact tail | $k$ from $e^{-2\gamma^2 k} \le \delta$ |
| --- | --- | --- | --- |
| $1/3$ | $10^{-2}$ | 47 | 83 |
| $1/3$ | $10^{-6}$ | 193 | 249 |
| $1/3$ | $10^{-9}$ | 305 | 375 |
| $1/4$ | $10^{-2}$ | 19 | 37 |
| $1/4$ | $10^{-6}$ | 79 | 111 |
| $1/4$ | $10^{-9}$ | 125 | 167 |

The error of the majority for $\delta_0 = 1/3$, with the two bounds:

| $k$ | 1 | 5 | 15 | 51 | 101 |
| --- | --- | --- | --- | --- | --- |
| exact | 0.333 | 0.210 | 0.0882 | 0.00689 | 0.000272 |
| $(8/9)^{k/2}$ | 0.943 | 0.745 | 0.413 | 0.0496 | 0.00261 |
| $e^{-k/18}$ | 0.946 | 0.757 | 0.435 | 0.0588 | 0.00366 |

The bounds are about ten times too large here, but they have the right exponential rate up to a constant in the exponent, and they need no computation.

## Classic examples

- **[Freivalds' algorithm](/freivalds-algorithm/).** One-sided error $1/2$ per random vector in $\{0,1\}^n$. Twenty vectors give error below $10^{-6}$ in $O(20 n^2)$ time.
- **[Miller-Rabin](/miller-rabin-primality-test/).** One-sided error $1/4$ per base. Thirty-two bases give error at most $2^{-64}$, by the worst-case bound; for random inputs the real error is much smaller.
- **[Karger's minimum cut](/karger-min-cut/).** Success probability $p \ge 2/(n(n-1))$ per run. Keep the smallest cut of $\lceil \binom{n}{2} \ln(1/\delta) \rceil$ runs. The comparison of cut sizes plays the role of the OR: the smallest cut is a minimum cut as soon as one run finds one.
- **[BPP](/bpp/) to exponentially small error.** Majority of $O(n)$ runs makes the error below $2^{-n}$ for inputs of size $n$. [Adleman's theorem](/adleman-theorem/) then fixes one random string that works for all $2^n$ inputs of size $n$, by the [union bound](/union-bound/).
- **[Median trick](/median-trick/).** For an estimator that is within $\varepsilon$ of the truth with probability at least $3/4$, the median of $k$ independent estimates is within $\varepsilon$ with probability at least $1 - e^{-k/8}$, by the same majority argument with $\gamma = 1/4$.

## Variations

- **A larger sample space instead of repetition.** For [polynomial identity testing](/polynomial-identity-testing/), one evaluation at a point of $S^m$ has error at most $d/|S|$ by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/). Making $S$ larger lowers the error with one run; for Freivalds' algorithm a vector from $S^n$ has error at most $1/|S|$.
- **Pairwise independent runs.** Draw the $k$ random strings pairwise independently instead of fully independently, which costs far fewer random bits. For one-sided error $1/2$, let $X$ count the runs that say "yes" on a "yes" input. Then $\mathbb{E}[X] \ge k/2$, $\mathrm{Var}[X] \le k/4$, and [Chebyshev's inequality](/chebyshev-inequality/) gives $\Pr[X = 0] \le \mathrm{Var}[X]/\mathbb{E}[X]^2 \le 1/k$. The error falls only as $1/k$, not exponentially.
- **Walks on an expander.** Taking the $k$ random strings along a random walk on an expander graph gives error $2^{-\Omega(k)}$ with only $O(k)$ extra random bits, for both one-sided and two-sided error. See [randomness amplification](/randomness-amplification/) and the [expander walk sampler](/expander-walk-sampler/).
- **A small subroutine error inside a large algorithm.** If an algorithm calls a Monte Carlo subroutine $m$ times, the [union bound](/union-bound/) gives total error at most $m\delta$. Amplify each call to $\delta/m$; the cost is a factor $O(\log m)$ more runs.

## Pitfalls

- **An OR on two-sided error.** Line L4 on a test with two-sided error raises the error on "no" inputs to $1 - (1 - \delta_0)^k$. Use line L6.
- **Dependent runs.** Runs that share a seed or a random string give the same answer, and the error does not fall. Each run of line L3 needs fresh random bits.
- **An even number of votes.** With $k$ even, a tie at line L6 must be broken; counting a tie as "no" makes the error on "yes" inputs larger. Use odd $k$.
- **An error that is not bounded on every input.** Repetition cannot fix a test whose error is close to 1 on some inputs. The Fermat test on a [Carmichael number](/carmichael-number/) passes for every base coprime to it, so more bases help only by luck in hitting a common factor.
- **Confusing the bound with the error.** The table above shows that $e^{-2\gamma^2 k}$ can overestimate the real error by a factor of ten or more. When the cost of each run is high, compute the exact binomial tail.
- **Forgetting the gap.** If $\gamma$ is not bounded below by an inverse polynomial, as for the [PP](/pp/) algorithm for SAT, the number of runs $\ln(1/\delta)/(2\gamma^2)$ is exponential.

## Exercises

1. A test has RP-type error $0.9$. How many runs reach error $10^{-6}$? (Answer: $\lceil \ln 10^6 / \ln(10/9) \rceil = 132$.)
2. Show that the error of the majority of $k$ runs with error $q < 1/2$ increases with $q$, for each fixed odd $k$.
3. A test is correct with probability $0.6$. Use the claim above to find $k$ with error at most $10^{-3}$, then find the least odd $k$ from the exact binomial tail.

## References
