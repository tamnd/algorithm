---
tag: TF4M5C
kind: technique
slug: rejection-sampling
name: Rejection sampling
aliases:
- acceptance-rejection method
- von Neumann rejection
- accept-reject method
area: randomized/sampling
level: core
summary: Propose from an envelope distribution and accept with probability proportional to target over envelope.
prereqs: [probability-density-function, uniform-distribution, geometric-distribution]
see_also: [inverse-transform-sampling, adaptive-rejection-sampling, ratio-of-uniforms, ziggurat-method, importance-sampling, random-variate-generation, las-vegas-algorithm, independence-sampler]
sources:
  - paper: "John von Neumann, Various techniques used in connection with random digits, in Monte Carlo Method, National Bureau of Standards Applied Mathematics Series 12, 1951"
    locator: pages 36 to 38
  - book: isbn:9780387963051
    title: Luc Devroye, Non-Uniform Random Variate Generation, Springer, 1986
    locator: Chapter II, Section 3 (the rejection method, with the squeeze principle), and Chapter III, Section 5.1 (discrete rejection)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 3.4.1 (the rejection method)
  - url: https://artowen.su.domains/mc/
    title: Art B. Owen, Monte Carlo theory, methods and examples, 2013
    locator: Chapter 4 (non-uniform random variables), the section on acceptance-rejection
---

Rejection sampling draws from a target density $f$ using a proposal density $g$ that is easy to sample and a constant $M$ with $f \le M g$ everywhere. Draw $Y$ from $g$ and a uniform $U$; accept $Y$ if $U \cdot M g(Y) \le f(Y)$, and otherwise try again. The accepted $Y$ has density exactly $f$, and the number of tries is geometric with mean $M$. The target only needs to be known up to a constant factor: with $f = \tilde f / Z$ and $\tilde f \le M g$, the mean number of tries is $M/Z$. Von Neumann described the method in 1951. It is a [Las Vegas algorithm](/las-vegas-algorithm/): the output is always exact, and only the running time is random.

## In plain words

Draw the graph of the density you want. Over it, draw a second curve that is everywhere higher and whose shape you know how to sample. Throw random points evenly under the higher curve. Keep the first point that also lies under the lower curve, and return its position on the x axis.

Points that land under the lower curve are spread evenly under it, so their x positions follow the density you want. The ones between the two curves are thrown away. The tighter the upper curve fits, the fewer points are wasted.

## When it applies

- The target density $f$, or a constant multiple $\tilde f$, can be evaluated at any point.
- There is a proposal $g$ that is easy to sample, and a known $M$ with $f(y) \le M g(y)$ for all $y$. In particular $g$ must be positive wherever $f$ is, and the tails of $g$ must be at least as heavy as those of $f$.
- $M$ is not too large. The cost is proportional to $M$, and in high dimension $M$ usually grows exponentially, so rejection sampling is a tool for low dimension.

When no envelope with a small $M$ exists, weight the samples instead with [importance sampling](/importance-sampling/), or build a Markov chain with [Metropolis-Hastings](/metropolis-hastings/).

## The template

Notation: $f$ is the target density, $g$ the proposal density, $M \ge \sup_y f(y)/g(y)$ the envelope constant. The holes to fill are $g$, a sampler for $g$, and $M$.

```pseudo id=main
REJECT(f, g, M)
L1  repeat
L2      Y ← a sample from g
L3      U ← a uniform real in [0, 1)
L4  until U · M · g(Y) ≤ f(Y)              ▷ accept with probability f(Y) / (M g(Y))
L5  return Y
```

The same template works on any space, discrete or continuous, with $f$ and $g$ densities with respect to the same measure. For a discrete target with integer weights $w_1, \ldots, w_n$ and a uniform proposal, take $M g = w_{\max}$ and replace lines L3 and L4 by "$t \leftarrow$ a uniform integer in $\{0, \ldots, w_{\max} - 1\}$; accept if $t < w_Y$". Then every probability is rational and the method is exact with integer arithmetic.

### Example

**Discrete.** Weights $(1, 3, 2)$, a uniform proposal on $\{1, 2, 3\}$ and $w_{\max} = 3$. Each try accepts index $i$ with probability $\frac{1}{3} \cdot \frac{w_i}{3}$, so a try is accepted with probability $\frac{6}{9} = \frac{2}{3}$, and the mean number of tries is $\frac{3}{2}$. Two tries:

| try | $Y$ | $t$ | test $t < w_Y$ | result |
|---|---|---|---|---|
| 1 | 1 | 2 | $2 < 1$ fails | reject |
| 2 | 3 | 1 | $1 < 2$ holds | return 3 |

**Normal from exponential.** For the half-normal $f(y) = \sqrt{2/\pi}\, e^{-y^2/2}$ on $y \ge 0$ and $g(y) = e^{-y}$, the ratio $f/g = \sqrt{2/\pi}\, e^{y - y^2/2}$ is largest at $y = 1$, so $M = \sqrt{2e/\pi} \approx 1.3155$. The test in line L4 becomes $U \le e^{-(Y - 1)^2/2}$. A random sign then gives a standard normal variate.

**Beta(2, 2).** $f(x) = 6x(1-x)$ on $[0, 1]$, $g = 1$ and $M = \frac{3}{2}$: accept $Y$ when $U \cdot \frac{3}{2} \le 6Y(1 - Y)$.

### Why it is correct

**Theorem.** Suppose $f$ and $g$ are densities with $f \le M g$, the proposals are independent, and each $U$ is uniform and independent of the rest. Then REJECT returns $Y$ with density $f$. The number of tries $N$ is geometric with success probability $1/M$, so $\mathbb{E}[N] = M$ and $\Pr[N > k] = (1 - 1/M)^k$.

*Proof.* Fix a measurable set $A$. In one try, given $Y = y$, the test in line L4 holds with probability $\Pr[U \le f(y)/(M g(y))] = f(y)/(M g(y))$, which is at most 1 by the hypothesis. So

$$\Pr[Y \in A \text{ and the try accepts}] = \int_A g(y) \frac{f(y)}{M g(y)}\,dy = \frac{1}{M}\int_A f(y)\,dy.$$

(Where $g(y) = 0$, the hypothesis gives $f(y) = 0$, and both sides get nothing from $y$.) With $A$ the whole space, a try accepts with probability $1/M$. The tries are independent and alike, so $N$ is geometric with success probability $1/M$, and the returned value is in $A$ with probability

$$\sum_{k \ge 1} \Bigl(1 - \frac{1}{M}\Bigr)^{k-1} \frac{1}{M}\int_A f = \int_A f. \qquad \blacksquare$$

If only $\tilde f = Z f$ is known and $\tilde f \le M g$, the same proof with $\tilde f$ in place of $f$ gives acceptance probability $Z/M$ per try and the same output law.

The theorem is about exact reals. With floating-point $U$ and rounded $f$ and $g$, the acceptance probability of each $y$ is off by about one unit in the last place, and the output law is off by the same relative amount. With integer weights and integer draws, as in the discrete form, the method is exact.

### Cost

- **Tries.** $M$ in expectation, or $M/Z$ for an unnormalized target. The tail is geometric: more than $k$ tries happen with probability $(1 - 1/M)^k$, so there is no worst-case bound, but long runs are rare.
- **Per try.** One proposal, one uniform, one evaluation of $f$ and one of $g$.
- **The best $M$** is $\sup f/g$. A larger $M$ is still correct, only slower.

## Classic examples

- **The [Marsaglia polar method](/marsaglia-polar-method/).** A uniform point in the disk by rejection from the square, $M = 4/\pi$.
- **The [ratio-of-uniforms](/ratio-of-uniforms/) method.** A uniform point in a region $C_h$ by rejection from a box.
- **The [ziggurat method](/ziggurat-method/).** Rejection from a stack of equal-area rectangles, with $M \approx 1.012$ for the normal.
- **[Adaptive rejection sampling](/adaptive-rejection-sampling/).** For log-concave densities, the envelope is rebuilt from the rejected points and $M$ falls toward 1.
- **Uniform integers from random bits.** To draw from $\{0, \ldots, n-1\}$, draw $\lceil \log_2 n \rceil$ bits and retry when the value is at least $n$. Here $M = 2^{\lceil \log_2 n \rceil}/n < 2$.
- **Discrete rejection.** Weighted sampling from a uniform proposal with $M = n w_{\max}/W$, useful when weights change often and are of similar size.

## Variations

- **The squeeze.** Find a simple function $s \le f$. If $U \cdot M g(Y) \le s(Y)$, accept without computing $f$. If a simple upper bound fails the test, reject without computing $f$. Correctness is unchanged, because the decision is the same; only the cost falls (Devroye, Section II.3).
- **Rejection in the log domain.** Test $\ln U \le \ln f(Y) - \ln M - \ln g(Y)$ when $f$ is tiny or huge.
- **Envelopes from mixtures.** Split the support into pieces with different simple envelopes and pick a piece with probability proportional to its envelope mass.
- **Rejection with an unknown $M$.** If $M$ is not known, the [independence sampler](/independence-sampler/), a Metropolis-Hastings chain with proposal $g$, needs only the ratio $f/g$ and has no envelope, at the cost of correlated samples.
- **Rejection versus [importance sampling](/importance-sampling/).** The same $f$ and $g$ can be used to weight every proposal by $f/g$ instead of rejecting. That keeps all samples but gives weighted ones.

## Pitfalls

- **An envelope that is not an envelope.** If $f(y) > M g(y)$ somewhere, the accepted law has density proportional to $\min(f, Mg)$, not $f$. Nothing in the output shows the error. Check $\sup f/g$ by calculus, not by a few test points.
- **Light-tailed proposals.** If $g$ has lighter tails than $f$, for example a normal proposal for a Cauchy target, no finite $M$ exists.
- **Reusing $U$.** $U$ must be independent of $Y$. Reusing the uniform that made $Y$ makes the test wrong.
- **High dimension.** For a $d$-dimensional product target and product proposal, $M$ is a product of $d$ factors and grows like $c^d$. A method with $M = 1.1$ per coordinate needs about $1.1^{100} \approx 13{,}800$ tries in 100 dimensions.
- **Rejection loops with a bad generator.** A short-period or correlated uniform generator can make the loop fail more or less often than $1/M$, and change the output law.

## Exercises

1. Show that the output law is $\min(f, Mg)/\int \min(f, Mg)$ when the envelope condition fails.
2. For the Cauchy target and the proposal $g(y) = \frac{1}{2}e^{-|y|}$, show that no finite $M$ exists. Then find the best $M$ for a normal target and the Cauchy proposal.
3. For a uniform integer in $\{0, \ldots, n-1\}$ from random bits, compute the expected number of bits used, and show that it is less than $2\lceil \log_2 n \rceil$.
4. Give the acceptance probability of the discrete form for weights $(1, 1, \ldots, 1, n)$, and compare it with the [alias method](/alias-method/).

## References
