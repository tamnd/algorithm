---
tag: 6M248J
kind: theorem
slug: balls-into-bins-max-load
name: Maximum load of balls into bins
aliases:
- max load theorem for balls into bins
- maximum bin load theorem
area: systems/load-balancing-and-hashing
level: core
summary: "With n balls thrown at random into n bins, the fullest bin holds (1 + o(1)) ln n / ln ln n balls with high probability; with m >= n ln n balls the excess over m/n is Theta(sqrt(m ln n / n))."
prereqs: [balls-into-bins, union-bound, chernoff-bound, poisson-distribution]
see_also: [random-load-balancing, power-of-two-choices, power-of-d-choices-theorem, consistent-hashing-max-load-bound, chaining-analysis, high-probability-bounds, coupon-collector-problem, load-balancing-problem]
sources:
  - paper: "Gaston H. Gonnet, Expected length of the longest probe sequence in hash code searching, Journal of the ACM 28(2), 1981"
    locator: pp. 289 to 304, the expected maximum load of n keys in n chains, asymptotic to the inverse of the Gamma function at n
  - paper: "Martin Raab and Angelika Steger, Balls into bins: a simple and tight analysis, Randomization and Approximation Techniques in Computer Science (RANDOM 1998), Lecture Notes in Computer Science 1518, Springer"
    locator: pp. 159 to 170, the main theorem (the maximum load for each range of m against n, by the first and second moment methods)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 5, Section 5.2 (the upper bound 3 ln n / ln ln n) and Section 5.4 (the Poisson approximation and the lower bound ln n / ln ln n)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 3, Section 3.1 (occupancy problems, the maximum load of n balls in n bins)
---

The maximum load theorem says that when $n$ balls are thrown independently and uniformly into $n$ bins, the fullest bin holds $(1 + o(1)) \ln n / \ln\ln n$ balls [with high probability](/high-probability-bounds/), and that when $m \ge n \ln n$ balls are thrown, the fullest bin holds $m/n + \Theta(\sqrt{m \ln n / n})$. It is the guarantee of [random load balancing](/random-load-balancing/) and the length of the longest chain in a hash table with [chaining](/chaining-analysis/). The general model, its expectations and the bounds with the constants 3 and 1 are on the page [balls into bins](/balls-into-bins/); this page proves the sharp constant 1 on both sides and the heavily loaded case.

## Statement

Throw $m$ balls into $n \ge 2$ bins. Each ball picks its bin uniformly from the $n$ bins, independently of the other balls. Let $X_j$ be the number of balls in bin $j$, and let $M = \max_j X_j$ be the maximum load. Write $L_n = \ln n / \ln\ln n$.

**Theorem (light case, $m = n$).** For each fixed $\varepsilon \in (0, 1)$ there is an $n_0(\varepsilon)$ such that for all $n \ge n_0(\varepsilon)$

$$ \Pr\bigl[M \ge (1 + \varepsilon) L_n\bigr] \le n^{-\varepsilon/2} \qquad\text{and}\qquad \Pr\bigl[M \le (1 - \varepsilon) L_n\bigr] \le e\sqrt n\,\exp\bigl(-n^{\varepsilon/2}/e\bigr). $$

So $M = (1 + o(1))\ln n / \ln\ln n$ with probability $1 - o(1)$.

**Theorem (heavy case).** If $m \ge 6 n \ln n$, then $\Pr\bigl[M \ge m/n + \sqrt{6 (m/n)\ln n}\bigr] \le 1/n$.

The bounds are proved here. Raab and Steger prove the matching lower bound of the heavy case and the second-order terms of both cases. They show that for $m$ large compared to $n \ln n$ the maximum load is $m/n + (1 + o(1))\sqrt{2 m \ln n / n}$ with high probability, and that for $m = c\, n \ln n$ with a constant $c$ it is $\Theta(\ln n)$.

## In plain words

You throw as many balls as there are bins, each one at random. On average each bin gets one ball. The fullest bin gets more than one, and the theorem says how much more: about the logarithm of the number of bins, divided by the logarithm of that logarithm. This grows, but very slowly. For a million bins the fullest bin usually holds eight to ten balls.

If you throw many more balls than bins, every bin gets close to the average. The fullest bin is above the average by about the square root of the average times the logarithm of the number of bins. The excess grows, but it becomes a smaller and smaller part of the average.

## Proof

The full proof is in the proof file. It has three parts.

**Upper bound.** For a fixed bin and an integer $k$, the bin has $k$ or more balls only if some set of $k$ balls all chose it. A [union bound](/union-bound/) over the $\binom nk$ sets gives $\Pr[X_1 \ge k] \le \binom nk n^{-k} \le 1/k!$, and a second union bound over the bins gives $\Pr[M \ge k] \le n/k!$. With $k = \lceil (1+\varepsilon)L_n\rceil$ and $k! \ge (k/e)^k$, a direct computation gives $\ln k! \ge (1 + \varepsilon/2)\ln n$ for large $n$.

**Lower bound.** The loads are dependent, because they add up to $m$. Replace them with independent [Poisson](/poisson-distribution/) variables $Y_j$ with mean $m/n$. For any event $A$ on the vector of loads, $\Pr[X \in A] \le e\sqrt m\,\Pr[Y \in A]$, because each vector with sum $m$ has probability $m!\,e^m/m^m \le e\sqrt m$ times larger under $X$ than under $Y$. In the Poisson model the bins are independent, and a bin reaches $k$ with probability at least $1/(e\,k!)$. So no bin reaches $k = \lfloor (1-\varepsilon)L_n\rfloor + 1$ with probability at most $\exp(-n/(e\,k!))$, and $n/k! \ge n^{\varepsilon/2}$ for large $n$.

**Heavy case.** Each load is a sum of $m$ independent indicators with mean $\mu = m/n$. The [Chernoff bound](/chernoff-bound/) $\Pr[X_j \ge (1+\delta)\mu] \le e^{-\mu\delta^2/3}$ with $\delta = \sqrt{6\ln n/\mu} \le 1$ gives $n^{-2}$ for each bin, and a union bound gives $1/n$.

## Consequences

- **Random load balancing.** A dispatcher that sends $n$ equal jobs to $n$ servers at random, as in [random load balancing](/random-load-balancing/), leaves the busiest server with $(1 + o(1))\ln n/\ln\ln n$ jobs, not 1. With $m$ jobs and $m \ge 6n\ln n$, the busiest server is at most $\sqrt{6(m/n)\ln n}$ above the mean with probability at least $1 - 1/n$.
- **Hashing with chaining.** With $n$ keys in $n$ slots under the uniform hashing assumption, the longest chain has length $(1 + o(1))\ln n/\ln\ln n$ with high probability, so the worst lookup is that slow even when the average is $O(1)$; see [chaining analysis](/chaining-analysis/).
- **Two choices.** The gap between this bound and the bound $\ln\ln n/\ln d + O(1)$ of the [power of d choices theorem](/power-of-d-choices-theorem/) is the reason for [the power of two choices](/power-of-two-choices/). In the heavy case the gap to the mean is $\Theta(\sqrt{m\ln n/n})$ with one choice, but stays $\ln\ln n/\ln d + O(1)$ with $d \ge 2$ choices, independent of $m$.
- **Consistent hashing.** Keys on a hash ring are balls thrown into bins of random sizes. The bin sizes add a factor of up to $\Theta(\log n)$, see the [consistent hashing load bound](/consistent-hashing-max-load-bound/).

## Tightness

**Exact values for small $n$.** The exact law of $M$ for $m = n$ follows from the generating function: the number of maps from $m$ balls to $n$ bins with all loads below $k$ is $m!\,[x^m]\bigl(\sum_{j<k} x^j/j!\bigr)^n$.

| $n$ | $\Pr[M \ge 2]$ | $\Pr[M \ge 3]$ | $\Pr[M \ge 4]$ | $\Pr[M \ge 5]$ | $\mathbb{E}[M]$ |
| --- | --- | --- | --- | --- | --- |
| 3 | 7/9 | 1/9 | | | 17/9 = 1.889 |
| 4 | 29/32 | 13/64 | 1/64 | | 17/8 = 2.125 |
| 5 | 601/625 | 181/625 | 21/625 | 1/625 | 1429/625 = 2.286 |

For $n = 4$, the union bound of the proof gives $\Pr[M \ge 3] \le 4\binom43/4^3 = 1/4$, against the exact $13/64 = 0.203$. The exact expected maximum is 2.749 for $n = 10$, 4.233 for $n = 100$ and 5.514 for $n = 1000$.

**Simulation.** Seeded runs of the process (Python `random.Random(1)` for $m = n$, `random.Random(2)` for the heavy case):

| $n$ | runs | $L_n$ | mean of $M$ | range of $M$ |
| --- | --- | --- | --- | --- |
| $10^3$ | 1000 | 3.57 | 5.53 | 4 to 9 |
| $10^4$ | 200 | 4.15 | 6.67 | 6 to 9 |
| $10^5$ | 40 | 4.71 | 7.75 | 7 to 9 |
| $10^6$ | 10 | 5.26 | 8.90 | 8 to 10 |

The ratio $M/L_n$ is about 1.6 to 1.7 at these sizes. The theorem says the ratio tends to 1, but the $o(1)$ term falls like $\ln\ln\ln n/\ln\ln n$, so the limit is not visible at any size a computer can simulate. The explicit $n_0(\varepsilon)$ of the proof is astronomically large for this reason.

| $n$ | $m/n$ | runs | mean of $M - m/n$ | range | $\sqrt{2(m/n)\ln n}$ | $\sqrt{6(m/n)\ln n}$ |
| --- | --- | --- | --- | --- | --- | --- |
| 1000 | 100 | 20 | 34.35 | 28 to 42 | 37.17 | 64.38 |
| 1000 | 1000 | 20 | 108.70 | 89 to 129 | 117.54 | 203.58 |

The excess is close to $\sqrt{2(m/n)\ln n}$, the Gaussian value that Raab and Steger prove in the limit. The constant 6 of the Chernoff proof is not tight.

**The constant 1 is the right one.** The lower bound shows that no upper bound of the form $c\,L_n$ with $c < 1$ holds with high probability, and the upper bound shows that no lower bound $c\,L_n$ with $c > 1$ holds. So the leading constant of the light case cannot change.

## History

Gonnet computed the expected length of the longest chain in a hash table with $n$ keys in $n$ chains in 1981, and showed that it is asymptotic to $\Gamma^{-1}(n)$, the inverse of the Gamma function, which is $(1 + o(1))\ln n/\ln\ln n$. Raab and Steger gave a short first and second moment proof for all ratios of $m$ to $n$ at RANDOM 1998. The union bound and Poisson approximation proofs follow the textbook of Mitzenmacher and Upfal, Chapter 5.

## References
