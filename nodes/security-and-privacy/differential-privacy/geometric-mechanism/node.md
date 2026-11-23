---
tag: 12JV5Q
kind: algorithm
slug: geometric-mechanism
name: Geometric mechanism
aliases:
- discrete Laplace mechanism
- two-sided geometric mechanism
area: security-and-privacy/differential-privacy
level: core
summary: Adds two-sided geometric noise to an integer count, and is universally utility-maximizing for count queries under differential privacy.
model: word-ram
complexity:
  vars: {a: "the noise parameter alpha = e^(-epsilon), so that 1/(1 - a) <= 1 + 1/epsilon"}
  time: {expected: O(1/(1 - a))}
  space: {extra: O(1)}
properties: {deterministic: false, randomized: true, exact: true}
history:
  year: 2009
  people: [Arpita Ghosh, Tim Roughgarden, Mukund Sundararajan]
  note: Ghosh, Roughgarden and Sundararajan defined the geometric mechanism at STOC 2009 and proved that it is universally utility maximizing for one count query.
prereqs: [laplace-mechanism, global-sensitivity, geometric-distribution]
see_also: [laplace-mechanism, discrete-gaussian-mechanism, randomized-response, post-processing-theorem, geometric-distribution, expected-value, bayes-theorem, private-query-release]
sources:
  - paper: doi:10.1137/09076828X
    title: "Arpita Ghosh, Tim Roughgarden and Mukund Sundararajan, Universally utility-maximizing privacy mechanisms, SIAM Journal on Computing 41(6), 2012, pages 1673 to 1693"
    locator: "Example 2.1 (the geometric mechanism), Example 2.2 (the truncated geometric mechanism), Theorem 3.2 (the main characterization) and Corollary 3.3 (universal utility maximization)"
  - paper: "Arpita Ghosh, Tim Roughgarden and Mukund Sundararajan, Universally utility-maximizing privacy mechanisms, STOC 2009, pages 351 to 360"
    locator: the conference version of the same results
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), 2014, pages 211 to 407"
    locator: "Section 3.3, the Laplace mechanism, of which this is the discrete analog"
  - paper: "Clement L. Canonne, Gautam Kamath and Thomas Steinke, The discrete Gaussian for differential privacy, NeurIPS 2020"
    locator: the exact samplers for discrete Laplace noise with an irrational parameter
  - paper: "Ilya Mironov, On significance of the least significant bits for differential privacy, ACM CCS 2012, pages 650 to 661"
    locator: why a deployment needs exact samplers
---

The geometric mechanism answers an integer query, such as a count, with integer noise from the two-sided geometric distribution. The noise $Z$ has $\Pr[Z = d] \propto \alpha^{|d|}$ with $\alpha = e^{-\varepsilon}$, and the output is $\varepsilon$-[differentially private](/differential-privacy-definition/) for a query of [sensitivity](/global-sensitivity/) 1. It is the discrete analog of the [Laplace mechanism](/laplace-mechanism/), and it needs no real numbers, so an exact sampler is simple. Ghosh, Roughgarden and Sundararajan (2009) proved that, for one count, it is optimal for every user at the same time, after a post-processing step that depends on the user.

## In plain words

You want to publish a count. One person can change the count by at most one. So you add a random whole number to it. Zero is the most likely value of the noise, and each step away from zero is less likely by the same factor. The published value is a whole number, which is natural for a count.

You can make the noise with a coin that has a known bias. Count how many times in a row the coin comes up heads, then do it again, and subtract the two counts. The result has the right shape. If you know the count is between two limits, you can move any output that is outside them to the nearest limit, and this costs no privacy.

## The problem

The input is a dataset $x$, an integer query $f$ with $|f(x) - f(x')| \le 1$ for all neighbors $x \sim x'$, and a number $\alpha \in (0, 1)$. The output is an integer $y$ such that the map from $x$ to $y$ is $\ln(1/\alpha)$-DP and $y$ is close to $f(x)$. With $\alpha = e^{-\varepsilon}$, the output is $\varepsilon$-DP. A count has sensitivity 1 under both neighbor relations: add/remove (one record added or removed) and replace (one record changed). Ghosh, Roughgarden and Sundararajan use replace neighbors, with $n$ fixed and $f(x) \in \{0, \ldots, n\}$.

The **two-sided geometric distribution** with parameter $\alpha$ has

$$\Pr[Z = d] = \frac{1 - \alpha}{1 + \alpha}\, \alpha^{|d|} \quad (d \in \mathbb Z), \qquad \Pr[|Z| \ge t] = \frac{2\alpha^t}{1 + \alpha} \quad (t \ge 1).$$

It is the distribution of $G_1 - G_2$ for two independent [geometric](/geometric-distribution/) variables with $\Pr[G = j] = (1 - \alpha)\alpha^j$ for $j \ge 0$. Its mean is 0 and its variance is $2\alpha/(1-\alpha)^2$.

## The algorithm

$\alpha$ is an exact fraction $a/q$, so that each coin of lines L3 and L5 is exact. The bounds $lo$ and $hi$ are optional, and are used when the true value is known to be in $[lo, hi]$.

```pseudo id=main
GEOMETRIC-MECHANISM(x, f, alpha, lo, hi)     ▷ f has sensitivity 1, alpha = e^(-epsilon)
L1  v <- f(x)
L2  g1 <- 0
L3  while a coin with Pr[heads] = alpha is heads do g1 <- g1 + 1
L4  g2 <- 0
L5  while a coin with Pr[heads] = alpha is heads do g2 <- g2 + 1
L6  z <- v + g1 - g2
L7  if lo is given and z < lo then z <- lo
L8  if hi is given and z > hi then z <- hi
L9  return z
```

Line L1 is the only line that reads the data. Lines L2 and L3 draw $G_1$: the number of heads before the first tail. Lines L4 and L5 draw $G_2$ in the same way. Line L6 adds the two-sided geometric noise $G_1 - G_2$. Lines L7 and L8 clamp the output to the known range, which gives the truncated geometric mechanism. A coin with $\Pr[\text{heads}] = a/q$ is one uniform integer in $\{0, \ldots, q-1\}$ compared with $a$.

The code uses a seeded generator so that the tests can repeat each run. A deployment needs a cryptographic source of randomness and an exact sampler (Mironov 2012; Canonne, Kamath and Steinke 2020). Canonne, Kamath and Steinke also give an exact sampler for $\alpha = e^{-\varepsilon}$ when this number is not rational.

## Example

Take $\varepsilon = \ln 2$, so $\alpha = 1/2$, and a count $v = f(x) = 4$ that is known to be in $[0, 6]$. Assume that the coins of line L3 are heads, tail, and the coins of line L5 are heads, heads, heads, tail.

| step | coin | $g_1$ | $g_2$ | $z$ |
|---|---|---|---|---|
| L1, L2 | | 0 | | |
| L3 | heads | 1 | | |
| L3 | tail (stop) | 1 | | |
| L4 | | 1 | 0 | |
| L5 | heads, heads, heads | 1 | 3 | |
| L5 | tail (stop) | 1 | 3 | |
| L6 | | | | $4 + 1 - 3 = 2$ |
| L7, L8 | $2 \in [0, 6]$ | | | 2 |

The output is 2. The noise $-2$ has probability $\frac{1/2}{3/2} \cdot \frac14 = \frac{1}{12}$. Noise 0 has probability $1/3$, and $\Pr[|Z| \ge 1] = 2/3$. With the clamp to $[0, 6]$ and $v = 4$, the exact output distribution is

| $y$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $\Pr$ | 1/24 | 1/24 | 1/12 | 1/6 | 1/3 | 1/6 | 1/6 |

The value 6 collects the whole upper tail: $\Pr[Z \ge 2] = \alpha^2/(1+\alpha) = 1/6$.

## Correctness

**Theorem (Ghosh, Roughgarden and Sundararajan 2009, Example 2.1).** If $f$ is integer valued with sensitivity 1 under a neighbor relation, then GEOMETRIC-MECHANISM is $\ln(1/\alpha)$-DP under that relation, with or without the clamp.

The key fact is that $G_1 - G_2$ has the pmf $\frac{1-\alpha}{1+\alpha}\alpha^{|d|}$. So for neighbors with $|f(x) - f(x')| \le 1$, the ratio of the output probabilities at each integer $y$ is $\alpha^{|y - f(x)| - |y - f(x')|} \le \alpha^{-1}$. The clamp of lines L7 and L8 is a function of $z$ alone, so it keeps the bound by the [post-processing theorem](/post-processing-theorem/). The full proof is in the correctness proof of this page.

**Accuracy.** For an integer $t \ge 1$, $\Pr[|z - f(x)| \ge t] \le 2\alpha^t / (1 + \alpha)$ without the clamp. The clamp never moves $z$ away from $f(x)$ when $f(x) \in [lo, hi]$, so the bound holds with it too.

## Complexity

The model is the [word RAM](/word-ram/): a uniform integer in $\{0, \ldots, q-1\}$ and each arithmetic step on words cost one unit.

- **Time.** Lines L3 and L5 each run one coin more than the value they count. So the number of coins is $G_1 + G_2 + 2$, with expected value $2\alpha/(1-\alpha) + 2 = 2/(1-\alpha)$. With $\alpha = e^{-\varepsilon}$, $1 - \alpha \ge \varepsilon/(1+\varepsilon)$, so the expected time is $O(1 + 1/\varepsilon)$. There is no worst-case bound: each loop can run for any number of steps, with a probability that falls geometrically.
- **Space.** Two counters and the output: $O(1)$ words.

## Properties

- **Pure privacy, exact.** The output is exactly $\ln(1/\alpha)$-DP, and the bound is tight. The tests check this with exact fractions over all datasets of up to 5 records, under both neighbor relations, and check that $\ln(1/\alpha) - 0.01$ fails.
- **Integer output.** No rounding of a real number is needed, and all probabilities are rational when $\alpha$ is rational.
- **Unbiased without the clamp.** $\mathbb E[z] = f(x)$, $\mathrm{Var}[z] = 2\alpha/(1-\alpha)^2$ and $\mathbb E|z - f(x)| = 2\alpha/(1 - \alpha^2)$. With the clamp, the output is biased near the ends of the range, but its error is never larger.
- **Universally utility maximizing.** For one count query with $f(x) \in \{0, \ldots, n\}$ under replace neighbors, consider any user with a prior on the true count and a loss that is nondecreasing in $|y - f(x)|$. Among all $\varepsilon$-DP mechanisms, the best one for this user is the truncated geometric mechanism followed by a remap of its output that depends only on the user (GRS Theorem 3.2 and Corollary 3.3). This is a theorem about one count. It does not hold for general query classes.

## Variants and improvements

- **Sensitivity $s > 1$.** Use $\alpha = e^{-\varepsilon/s}$. Then the output is $\varepsilon$-DP. The tests check that a sensitivity-2 query with $\alpha = 1/4$ is $\ln 16$-DP and not $\ln 4$-DP, so the parameter must change with $s$.
- **Several counts.** Add independent geometric noise to each coordinate, with $\alpha = e^{-\varepsilon/\Delta_1}$, where $\Delta_1$ is the $\ell_1$ sensitivity of the vector. A histogram under add/remove has $\Delta_1 = 1$.
- **Discrete Gaussian.** The [discrete Gaussian mechanism](/discrete-gaussian-mechanism/) is the integer analog of the Gaussian mechanism, for $(\varepsilon, \delta)$-DP and better composition.
- **Exact samplers for any $\varepsilon$.** When $e^{-\varepsilon}$ is not rational, Canonne, Kamath and Steinke (2020) sample Bernoulli$(e^{-\gamma})$ exactly with rational coins, and from it the discrete Laplace distribution.
- **Bit flip on one bit.** For a count of 0 or 1, the truncated mechanism on $[0, 1]$ is [randomized response](/randomized-response/) with $p = 1/(1 + \alpha)$.

## When to use it

Use the geometric mechanism for counts and other integer queries of low sensitivity, when you want integer output with exact sampling and pure $\varepsilon$-DP. It has the same accuracy as the Laplace mechanism up to rounding, and it avoids the float problems of continuous noise. If you answer many counts and can accept a small $\delta$, the discrete Gaussian mechanism adds less noise per count. If you know the range of the count, clamp the output, because the clamp is free.

## Pitfalls

- **The wrong parameter for a larger sensitivity.** Line L3 with $\alpha = e^{-\varepsilon}$ on a query of sensitivity 2 is only $2\varepsilon$-DP. The coins of lines L3 and L5 must use $\alpha = e^{-\varepsilon/s}$ for sensitivity $s$.
- **One-sided noise.** Line L6 written as $z \leftarrow v + g_1$, with only one geometric variable, is not private at all: the output is never below $v$, so for neighbors with $f(x') = f(x) + 1$ the output $f(x)$ has probability 0 under $x'$. Line L6 must subtract the second variable, $z \leftarrow v + g_1 - g_2$.
- **A clamp to a range that depends on the data.** Lines L7 and L8 with $lo$ or $hi$ computed from $x$, such as the true minimum of a column, are not post-processing, and they leak. The bounds must be fixed before the data is seen, for example $[0, n]$ for a count with public $n$.
- **A float coin.** Lines L3 and L5 with "random float < alpha" make each coin slightly wrong. Use a uniform integer and the exact fraction $a/q$, or the exact samplers of Canonne, Kamath and Steinke.

## Implementations

## History

Ghosh, Roughgarden and Sundararajan introduced the geometric mechanism and its truncated form at STOC 2009, with the journal version in SIAM Journal on Computing in 2012. Their main result is that one mechanism is optimal for all users of a count, each with its own prior and loss, after a remap by the user. The discrete Laplace distribution itself is older, and the discrete Gaussian of Canonne, Kamath and Steinke (2020) is its Gaussian counterpart.

## References
