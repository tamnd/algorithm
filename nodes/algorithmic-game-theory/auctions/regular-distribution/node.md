---
tag: 4BCCM2
kind: definition
slug: regular-distribution
name: Regular distribution
aliases:
- regular valuation distribution
area: algorithmic-game-theory/auctions
level: core
summary: "A value distribution whose virtual valuation is nondecreasing, so that its revenue curve is concave. Distributions with monotone hazard rate are regular."
prereqs: [virtual-valuation]
see_also: [myerson-optimal-auction, ironing, reserve-price, bulow-klemperer-theorem, sample-complexity-of-revenue-maximization, independent-private-values, vickrey-auction]
sources:
  - paper: doi:10.1287/moor.6.1.58
    title: "Roger B. Myerson, Optimal auction design, Mathematics of Operations Research 6(1) (1981), 58-73"
    locator: the regularity condition under which the optimal auction needs no ironing, and the general case without it
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 5, Revenue-maximizing auctions, Section 5.2 (regular distributions and the optimal auction for them)
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 13, Jason D. Hartline and Anna R. Karlin, Profit maximization in mechanism design (regular distributions and the optimal mechanism)
  - paper: "Jason D. Hartline, Mechanism Design and Approximation, book draft, version with Chapters 1 to 7 revised in September 2021, https://jasonhartline.com/MDnA/"
    locator: Chapter 3, Optimal mechanisms, and Chapter 4, Bayesian approximation (regular and monotone hazard rate distributions)
---

A distribution of values is regular when its [virtual valuation](/virtual-valuation/) $\varphi(v) = v - (1 - F(v))/f(v)$ is nondecreasing in $v$. Equivalently, its revenue curve in quantile space is concave. Regularity is the condition under which [Myerson's optimal auction](/myerson-optimal-auction/) needs no [ironing](/ironing/), and under which many simple auctions, such as the [Vickrey auction](/vickrey-auction/) with a reserve, are optimal or close to optimal. It is a condition on one bidder's distribution, not on a mechanism, and it says nothing about truthfulness, which [Myerson's lemma](/myerson-lemma/) handles for every distribution.

## Definition

Let $F$ have a density $f > 0$ on an interval $[a, b]$ with $0 \le a < b \le \infty$. The distribution is **regular** if

$$\varphi(v) = v - \frac{1 - F(v)}{f(v)}$$

is nondecreasing on $[a, b]$.

**Revenue curve form.** Let $R(q) = q \cdot F^{-1}(1 - q)$ be the revenue of the posted price that sells with probability $q$. Then $R'(q) = \varphi(F^{-1}(1 - q))$. As $q$ grows, the value $F^{-1}(1 - q)$ falls. So $\varphi$ is nondecreasing in $v$ exactly when $R'$ is nonincreasing in $q$, that is, when $R$ is concave on $[0, 1]$. This form needs no density and is the definition used for general distributions.

**Discrete form.** A distribution on $s_1 < \cdots < s_K$ is regular when its discrete virtual values $\varphi(s_1) \le \cdots \le \varphi(s_K)$ are nondecreasing, that is, when the points $(0, 0)$ and $(\Pr[v \ge s_k], s_k \Pr[v \ge s_k])$ lie on a concave curve.

**Monotone hazard rate.** The hazard rate is $h(v) = f(v)/(1 - F(v))$, and $F$ has a monotone hazard rate (MHR) if $h$ is nondecreasing. Then $\varphi(v) = v - 1/h(v)$ is the sum of $v$ and the nondecreasing function $-1/h(v)$, so every MHR distribution is regular. The converse fails.

## Examples and non-examples

- **Uniform.** For $U[0, 1]$, $\varphi(v) = 2v - 1$, and $h(v) = 1/(1 - v)$ is increasing. Regular and MHR. The revenue curve is $R(q) = q(1 - q)$.
- **Exponential.** For $F(v) = 1 - e^{-\lambda v}$, $h = \lambda$ is constant and $\varphi(v) = v - 1/\lambda$. Regular and MHR.
- **Log-concave densities.** Every distribution with a log-concave density, such as the normal distribution truncated to $[0, \infty)$, has a monotone hazard rate and so is regular.
- **Pareto with $\alpha = 2$.** For $F(v) = 1 - v^{-2}$ on $[1, \infty)$, $h(v) = 2/v$ decreases, so it is not MHR. But $\varphi(v) = v - v/2 = v/2$ increases, so it is regular.
- **Equal-revenue distribution.** For $F(v) = 1 - 1/v$ on $[1, \infty)$, $\varphi(v) = 0$ for every $v$. It is regular, on the edge: every price $p \ge 1$ earns exactly 1.
- **Not regular: a bimodal density.** Let $f = 9/20$ on $[0, 1)$ and on $[2, 3]$, and $f = 1/10$ on $[1, 2)$. Just below $v = 1$, $1 - F = 11/20$ and $\varphi = 1 - (11/20)/(9/20) = -2/9$. Just above it, $\varphi = 1 - (11/20)/(1/10) = -9/2$. The virtual valuation drops, so the distribution is not regular. It is a mixture of three uniform distributions, each regular, so regularity is not kept under mixtures.
- **Not regular: a discrete example.** Values $2, 3, 5$ with probabilities $1/2, 1/6, 1/3$ have $\varphi = (1, -1, 5)$. The revenue curve has the points $(1/3, 5/3)$, $(1/2, 3/2)$ and $(1, 2)$, and the middle one lies below the chord of the other two.

## Related definitions

- **Virtual valuation.** The function whose monotonicity defines regularity ([virtual valuation](/virtual-valuation/)).
- **Ironing.** For a distribution that is not regular, replacing the revenue curve by its concave hull gives ironed virtual values that are nondecreasing ([ironing](/ironing/)). For a regular distribution, ironing changes nothing.
- **Monopoly reserve.** For a regular distribution, the zero of $\varphi$ is the price that maximizes $p(1 - F(p))$, and it is the optimal [reserve price](/reserve-price/) for i.i.d. bidders.
- **Results that need regularity.** With i.i.d. regular values, the optimal auction is the Vickrey auction with the monopoly reserve, the [Bulow-Klemperer theorem](/bulow-klemperer-theorem/) holds, and one sample of the value gives half of the optimal revenue (see [sample complexity of revenue maximization](/sample-complexity-of-revenue-maximization/)). Without regularity, each of these can fail.
- **Stronger conditions.** MHR gives better constants for simple mechanisms and smaller sample complexity than regularity alone.

## References
