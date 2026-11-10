---
tag: 6K52JJ
kind: technique
slug: median-trick
name: Median trick
aliases:
- median amplification
- median of estimates
- median of means
- median boosting
area: online-and-streaming/streaming-sketches
level: core
summary: Repeat an estimator independently and take the median to boost success probability to 1 - delta.
prereqs: [epsilon-delta-guarantee, chernoff-bound, independent-random-variables]
see_also: [error-amplification, hoeffding-inequality, binomial-tail-bounds, ams-sketch, count-sketch, morris-counter, flajolet-martin-algorithm, mergeable-summaries]
sources:
  - paper: doi:10.1006/jcss.1997.1545
    title: Noga Alon, Yossi Matias and Mario Szegedy, The space complexity of approximating the frequency moments, Journal of Computer and System Sciences 58(1), 1999
    locator: pp. 137 to 147, Section 2 (the median of means of the F_k estimators, with a Chernoff bound)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 4, Chernoff and Hoeffding bounds
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 1, Introduction (from a constant probability to 1 − δ by the median of copies)
---

The median trick turns an estimator that is good with a constant probability into one that is good with probability $1 - \delta$. Run $t = O(\log(1/\delta))$ independent copies and return their median. If each copy is outside the target interval with probability at most $p < 1/2$, the median is outside it only when at least half the copies are, and a [Chernoff bound](/chernoff-bound/) makes that event exponentially rare in $t$: its probability is at most $(4p(1-p))^{t/2}$. So the cost of a small $\delta$ is a factor $\log(1/\delta)$ in space, not $1/\delta$. Alon, Matias and Szegedy used it with the mean of copies inside, as the median of means, for the frequency moments. This page proves the bound in full.

## In plain words

You have a measuring tool that gives a good reading two times out of three, and a wild reading the other time. One reading is not reliable. The average of many readings is not reliable either, because one wild reading can pull the average far away. Instead, take many independent readings and sort them. Report the one in the middle. For the middle reading to be wild, at least half of the readings must be wild, and that is very unlikely when each one is wild only a third of the time. Each new pair of readings makes a bad result less likely by a fixed factor, so a few dozen readings already give a very reliable answer.

## When it applies

- There is a base estimator $E$ whose output is a real number, and a target interval $I$ (for example $[(1-\varepsilon)Q, (1+\varepsilon)Q]$) with $\Pr[E \notin I] \le p$ for a constant $p < 1/2$.
- Independent copies of $E$ can be run on the same input. In a stream this means independent seeds, kept side by side, and each update goes to each copy.
- The interval $I$ is a single interval of the real line. The median is about order, so it needs an order, and "good" must mean "between two bounds".
- The base estimator is often itself a mean: by [Chebyshev's inequality](/chebyshev-inequality/), the mean of $k = O(\sigma^2/\varepsilon^2)$ copies of an unbiased estimator with relative variance $\sigma^2$ is in $I$ with probability $3/4$.

## The template

```pseudo id=main
MEDIAN-BOOST(input, I, δ)
L1  pick a base estimator E with Pr[E ∉ I] ≤ p < 1/2           ▷ hole: the estimator and its bound p
L2  t ← the smallest odd integer ≥ 2 ln(1/δ) / ln(1 / (4p(1 − p)))
L3  draw t independent seeds; run copies E_1, ..., E_t on input   ▷ hole: the source of independence
L4  sort the t outputs
L5  return the output in position (t + 1)/2
```

The two holes are the base estimator of line L1, with its proved bound $p$, and the independence of line L3. The constant of line L2 comes from the theorem below. For $p = 1/3$ it is $2/\ln(9/8) \approx 16.98$, so $t \approx 17\ln(1/\delta)$. For $p = 1/4$ it is $2/\ln(4/3) \approx 6.95$.

**Theorem.** Let $Y_1, \ldots, Y_t$ be independent, with $t$ odd, and let $\Pr[Y_i \notin I] \le p < 1/2$ for each $i$, where $I = [lo, hi]$. Let $Z$ be the median. Then
$$\Pr[Z \notin I] \le (4p(1-p))^{t/2}.$$

*Proof.* Let $X_i$ be the [indicator](/indicator-random-variable/) of $Y_i \notin I$, and $B = \sum_i X_i$, the number of bad copies.

Step 1: a bad median needs many bad copies. If $Z > hi$, then $Z$ and the $(t-1)/2$ outputs above it are all above $hi$, so at least $(t+1)/2$ copies are bad. The case $Z < lo$ is the same. So $\Pr[Z \notin I] \le \Pr[B \ge (t+1)/2] \le \Pr[B \ge t/2]$.

Step 2: the moment generating function. Let $p_i = \Pr[X_i = 1] \le p$ and $\lambda > 0$. By independence,
$$\mathbb{E}[e^{\lambda B}] = \prod_{i=1}^{t} (1 - p_i + p_i e^{\lambda}) \le (1 - p + p e^{\lambda})^t,$$
because $1 - p_i + p_i e^\lambda = 1 + p_i(e^\lambda - 1)$ grows with $p_i$ when $\lambda > 0$.

Step 3: Markov's inequality on $e^{\lambda B}$. Since $x \mapsto e^{\lambda x}$ is increasing,
$$\Pr[B \ge t/2] = \Pr[e^{\lambda B} \ge e^{\lambda t/2}] \le \mathbb{E}[e^{\lambda B}]\,e^{-\lambda t/2} \le \big((1 - p + p e^\lambda)\,e^{-\lambda/2}\big)^t.$$

Step 4: the choice of $\lambda$. Take $e^\lambda = (1-p)/p$, which is more than 1 because $p < 1/2$, so $\lambda > 0$. Then $1 - p + p e^\lambda = 2(1-p)$ and $e^{-\lambda/2} = \sqrt{p/(1-p)}$. Their product is $2\sqrt{p(1-p)}$, so
$$\Pr[Z \notin I] \le \big(2\sqrt{p(1-p)}\big)^t = (4p(1-p))^{t/2}.$$
This choice minimizes the bound of Step 3 over $\lambda$. Since $4p(1-p) < 1$ for $p \ne 1/2$, the bound is at most $\delta$ when $t \ge 2\ln(1/\delta)/\ln(1/(4p(1-p)))$, which is line L2. $\square$

The [Hoeffding](/hoeffding-inequality/) bound gives $\Pr[B \ge t/2] \le e^{-2t(1/2 - p)^2}$, which is $e^{-t/18}$ for $p = 1/3$. It is a little weaker here: it needs $t \ge 18\ln(1/\delta)$.

The table compares the number of copies that each bound asks for with the smallest odd $t$ for which the exact binomial tail $\Pr[B \ge (t+1)/2]$ is at most $\delta$.

| $p$ | $\delta$ | theorem | Hoeffding | exact tail |
|---|---|---|---|---|
| 1/3 | 0.01 | 79 | 83 | 47 |
| 1/3 | 0.001 | 119 | 125 | 81 |
| 1/4 | 0.01 | 33 | 37 | 19 |

## Classic examples

- **[AMS sketch](/ams-sketch/) for $F_2$.** Each basic estimator is unbiased with variance at most $2F_2^2$. The mean of $O(\varepsilon^{-2})$ of them is within $\varepsilon F_2$ with probability $3/4$ or more, and the median of $O(\log(1/\delta))$ such means gives $1 - \delta$. This is the median of means of Alon, Matias and Szegedy.
- **[Count sketch](/count-sketch/).** Each row gives an estimate of $f_i$ within $\varepsilon\|f\|_2$ with constant probability, and the sketch reports the median over $O(\log(1/\delta))$ rows.
- **[Morris counter](/morris-counter/).** Morris++ is the median of $t$ copies of Morris+, the mean of $s$ counters. With $p = 1/3$ the page uses $t = \lceil 2\ln(1/\delta)/\ln(9/8) \rceil$, rounded up to odd.
- **[AMS distinct elements](/flajolet-martin-algorithm/).** Each copy is within a factor 3 with constant probability, and the median of copies keeps the factor 3 with probability $1 - \delta$. Here only each side has probability below $1/2$, so the one-sided variation below is the one to use.
- **[Count-min sketch](/count-min-sketch/) in the general turnstile model.** With negative entries the minimum over rows is no longer safe, and the median over rows is used instead.
- **[Mergeable summaries](/mergeable-summaries/).** A randomized mergeable summary that is valid with constant probability becomes valid with probability $1 - \delta$ by keeping $O(\log(1/\delta))$ copies and querying the median.

## Variations

- **One side at a time.** If $\Pr[Y_i > hi] \le q$ and $\Pr[Y_i < lo] \le q$ with $q < 1/2$, but $2q$ may be $1/2$ or more, apply the theorem to each side: the median is above $hi$ only if at least $(t+1)/2$ copies are above $hi$. Then $\Pr[Z \notin I] \le 2(4q(1-q))^{t/2}$. For the AMS distinct elements estimate, $q = \sqrt 2/3 \approx 0.471$ and $4q(1-q) \approx 0.99673$, so $t \approx 611\ln(2/\delta)$ copies suffice.
- **Median of means.** Use the mean of $k$ copies as the base estimator, as in the template's first hole. The total is $O(k \log(1/\delta))$ copies; the mean controls $\varepsilon$ and the median controls $\delta$.
- **The minimum for one-sided errors.** If each copy never underestimates and overestimates by more than the bound with probability at most $p$, the minimum is bad only if all copies are bad: $\Pr \le p^t$. This is how the count-min sketch combines its rows in the cash register model.
- **Majority vote.** For a yes or no answer, the median of the copies is their majority, and the theorem is the usual [error amplification](/error-amplification/) of a [two-sided error](/two-sided-error/) algorithm.
- **Many queries.** For $T$ queries at once, use $\delta/T$ in line L2. The cost grows only by $O(\log T)$.

## Pitfalls

- **The mean in place of the median in line L5.** One wild copy can move the mean anywhere. The mean of $t$ copies only lowers the variance by $t$, which gives $\delta \sim 1/t$, not $e^{-ct}$.
- **Copies that share randomness in line L3.** The Chernoff bound needs independent copies. Copies that use the same hash function, or seeds from a weak generator, can all fail together.
- **A base bound of $1/2$ or more in line L1.** If $p \ge 1/2$, the median gets worse, not better. A base estimator with $p = 1/2$ must first be improved, for example by a mean of more copies.
- **Using the median as an unbiased estimate.** The median of unbiased estimates is not unbiased. Use it for the tail bound only.
- **Too few copies from the asymptotic form.** "$t = O(\log(1/\delta))$" hides a constant near 17 for $p = 1/3$. With $\delta = 0.01$ the theorem asks for $t = 79$; the exact binomial tail allows $t = 47$.

## Exercises

1. For $p = 1/3$ and $t = 25$, compute the exact probability that at least 13 of 25 independent copies are bad, and compare it with $(8/9)^{12.5}$. (The exact value is about 0.0415, the bound about 0.229.)
2. Show that the bound of the theorem also holds when the copies have different failure probabilities $p_i \le p$, by checking Step 2 term by term.
3. Let each copy of the base estimator be the mean of $k$ independent unbiased estimates with variance $\sigma^2 Q^2$. Choose $k$ so that $p = 1/4$, and find the total number of estimates for $(\varepsilon, \delta) = (0.05, 10^{-3})$ when $\sigma^2 = 2$.
4. Let the good set be $[0, 1] \cup [2, 3]$, which is not an interval. Find three values, only one of them bad, whose median is bad. Explain which step of the proof fails.
5. Prove the Hoeffding form $\Pr[B \ge t/2] \le e^{-2t(1/2 - p)^2}$ from Hoeffding's inequality, and find the $t$ it needs for $p = 1/4$ and $\delta = 0.01$.

## References
