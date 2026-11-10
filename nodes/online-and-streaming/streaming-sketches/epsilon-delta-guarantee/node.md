---
tag: WX276H
kind: definition
slug: epsilon-delta-guarantee
name: Epsilon-delta approximation guarantee
aliases:
- (epsilon, delta)-approximation
- (ε, δ) guarantee
- (ε, δ)-approximation
- epsilon-delta approximation
- PAC-style guarantee
area: online-and-streaming/streaming-sketches
level: core
summary: An estimate within relative error epsilon with probability at least 1 - delta.
prereqs: [streaming-model, monte-carlo-algorithm, chebyshev-inequality]
see_also: [median-trick, two-sided-error, error-amplification, fpras, relative-error, morris-counter, count-min-sketch, hyperloglog]
sources:
  - paper: doi:10.1016/0196-6774(89)90038-2
    title: Richard M. Karp, Michael Luby and Neal Madras, Monte-Carlo approximation algorithms for enumeration problems, Journal of Algorithms 10(3), 1989
    locator: pp. 429 to 448 (the ε, δ approximation of a count by a randomized algorithm)
  - paper: doi:10.1006/jcss.1997.1545
    title: Noga Alon, Yossi Matias and Mario Szegedy, The space complexity of approximating the frequency moments, Journal of Computer and System Sciences 58(1), 1999
    locator: pp. 137 to 147 (estimates within a factor 1 ± λ with probability 1 − ε, from the mean and the median of copies)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: the chapter The Monte Carlo Method (the definition of an (ε, δ)-approximation and the estimator theorem)
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 1, Introduction
---

An $(\varepsilon, \delta)$ guarantee says how close a randomized estimate is to the truth, and how often. In the relative form, the estimate $\hat Q$ of a quantity $Q > 0$ satisfies $|\hat Q - Q| \le \varepsilon Q$ with probability at least $1 - \delta$. In the additive form, the error bound is $\varepsilon B$ for a known scale $B$, such as the stream length $m$ or a norm of the [frequency vector](/frequency-vector/). The probability is over the random bits of the algorithm, for each fixed input. Nearly every streaming sketch states its accuracy in this form, and its space as a function of $1/\varepsilon$ and $\log(1/\delta)$.

## Definition

Let $Q(\sigma)$ be a quantity of the input $\sigma$, and let $A$ be a randomized algorithm whose output on $\sigma$ is the random variable $\hat Q(\sigma)$. Let $\varepsilon > 0$ and $\delta \in (0, 1)$.

**Relative form.** $A$ gives an $(\varepsilon, \delta)$-approximation of $Q$ if, for every input $\sigma$ with $Q(\sigma) > 0$,
$$\Pr\big[(1 - \varepsilon)\,Q(\sigma) \le \hat Q(\sigma) \le (1 + \varepsilon)\,Q(\sigma)\big] \ge 1 - \delta.$$

**Additive form.** Given a scale $B(\sigma)$, $A$ gives an $(\varepsilon, \delta)$ additive approximation if, for every $\sigma$,
$$\Pr\big[\,|\hat Q(\sigma) - Q(\sigma)| \le \varepsilon\, B(\sigma)\big] \ge 1 - \delta.$$
The usual scales are $B = m$, $B = \|f\|_1$ and $B = \|f\|_2$. A page must say which.

Four points are part of the definition.

1. **The probability is over the algorithm.** The input is fixed first, and then the random bits are drawn. It is a worst case statement over inputs, not an average over inputs.
2. **The input does not depend on the random bits.** The stream is chosen by an oblivious adversary. If later items can depend on earlier outputs, the guarantee can fail; this is the adaptive, or adversarially robust, setting.
3. **One query at a time.** For a stream, the guarantee holds for each fixed query time separately. A bound for all $T$ query times at once follows from the [union bound](/union-bound/) with $\delta/T$ in place of $\delta$.
4. **One-sided forms.** Some sketches never underestimate. The [count-min sketch](/count-min-sketch/) satisfies $f_i \le \hat f_i$ always, and $\hat f_i \le f_i + \varepsilon\|f\|_1$ with probability $1 - \delta$.

A weaker form is the **constant factor guarantee**: $Q/c \le \hat Q \le cQ$ with probability $1 - \delta$, for a fixed $c > 1$. The [AMS distinct elements estimate](/flajolet-martin-algorithm/) has this form with $c = 3$.

## Examples and non-examples

**Examples.**

- **Approximate counting.** A [Morris counter](/morris-counter/) with base $1 + a$ and $a = 2\varepsilon^2\delta$ gives a relative $(\varepsilon, \delta)$-approximation of the number of events.
- **Point queries.** The count-min sketch with width $\lceil e/\varepsilon \rceil$ and depth $\lceil \ln(1/\delta) \rceil$ gives an additive guarantee with scale $\|f\|_1$, as in point 4.
- **From the variance (proved here).** Let $\hat Q$ be unbiased, $\mathbb{E}[\hat Q] = Q$, with $\mathrm{Var}(\hat Q) \le \sigma^2 Q^2$. The mean $\bar Q$ of $k$ independent copies has variance at most $\sigma^2 Q^2/k$. By [Chebyshev's inequality](/chebyshev-inequality/), $\Pr[|\bar Q - Q| > \varepsilon Q] \le \sigma^2/(k\varepsilon^2)$. So $k = \lceil \sigma^2/(\varepsilon^2\delta) \rceil$ copies give an $(\varepsilon, \delta)$-approximation. With $\delta = 1/3$ and the [median trick](/median-trick/) on top, $O(\sigma^2\varepsilon^{-2}\log(1/\delta))$ copies suffice for each $\delta$.
- **From a standard error.** [HyperLogLog](/hyperloglog/) with $m = 4096$ registers has a relative standard error of about $1.04/\sqrt{4096} = 0.01625$. Chebyshev with $\delta = 0.05$ gives $\varepsilon = 0.01625/\sqrt{0.05} \approx 0.073$. The normal approximation, which is not a proof, gives $\varepsilon \approx 1.96 \times 0.01625 \approx 0.032$.

**Non-examples.**

- **A bound on the standard error alone.** "The standard error is $1.04/\sqrt m$" is not an $(\varepsilon, \delta)$ guarantee until a tail bound turns it into one, as above. For HyperLogLog the standard error itself is an asymptotic statement for a fully random hash.
- **A bound in expectation.** $\mathbb{E}[|\hat Q - Q|] \le \varepsilon Q$ is weaker. [Markov's inequality](/markov-inequality/) gives only an $(\varepsilon/\delta, \delta)$ guarantee from it.
- **An average over inputs.** "For a random stream, the error is small with probability $1 - \delta$" allows the error to be large on some fixed stream for most seeds. That is average case analysis, not this guarantee.
- **A seed chosen after the input.** If the hash seed may depend on the stream, for example a fixed public seed against a chosen stream, an adversary can pick a stream on which the estimate is bad.
- **Exact algorithms with failure.** An algorithm that is exact with probability $1 - \delta$ satisfies the definition with $\varepsilon = 0$, but it is usually called a Monte Carlo algorithm with two-sided error.

## Related definitions

- **[Monte Carlo algorithm](/monte-carlo-algorithm/) and [two-sided error](/two-sided-error/).** An $(\varepsilon, \delta)$ estimator is a Monte Carlo algorithm whose answer is a number, and "correct" means "within the error bound".
- **[Error amplification](/error-amplification/).** For decision problems, repeating and taking the majority lowers $\delta$. For estimates, the analogue is the [median trick](/median-trick/).
- **[FPRAS](/fpras/).** A fully polynomial randomized approximation scheme is an algorithm with a relative $(\varepsilon, \delta)$ guarantee, here with $\delta = 1/4$, whose time is polynomial in the input size and $1/\varepsilon$. In streaming the cost is space, not time.
- **[Relative error](/relative-error/).** The relative form bounds the relative error $|\hat Q - Q|/Q$ by $\varepsilon$.
- **[High probability bounds](/high-probability-bounds/).** "With high probability" usually means $\delta = n^{-c}$ for a constant $c$.

## References
