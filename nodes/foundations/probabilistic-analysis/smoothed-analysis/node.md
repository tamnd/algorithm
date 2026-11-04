---
tag: V6KZDE
kind: concept
slug: smoothed-analysis
name: Smoothed analysis
aliases:
- smoothed complexity
area: foundations/probabilistic-analysis
level: advanced
summary: Bounds the worst-case expected cost when inputs are randomly perturbed, explaining why the simplex method works in practice.
prereqs: [worst-case-analysis, average-case-analysis, expected-value, simplex-method]
see_also: [klee-minty-cube, linear-programming-problem, hirsch-conjecture, condition-number, knapsack-problem, two-opt, k-means, hiring-problem]
sources:
  - paper: doi:10.1145/990308.990310
    title: Daniel A. Spielman and Shang-Hua Teng, Smoothed analysis of algorithms, Why the simplex algorithm usually takes polynomial time, Journal of the ACM 51(3), 2004
    locator: pp. 385 to 463, the definition of smoothed complexity and the polynomial smoothed complexity of the shadow-vertex simplex method
  - paper: doi:10.1145/1562764.1562785
    title: Daniel A. Spielman and Shang-Hua Teng, Smoothed analysis, an attempt to explain the behavior of algorithms in practice, Communications of the ACM 52(10), 2009
    locator: pp. 76 to 84, a survey of the model and its results
  - paper: doi:10.1016/j.jcss.2004.04.004
    title: René Beier and Berthold Vöcking, Random knapsack in expected polynomial time, Journal of Computer and System Sciences 69(3), 2004
    locator: pp. 306 to 329, the expected number of Pareto optimal knapsack solutions under random perturbation
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 5 (probabilistic analysis, the hiring problem used in the example) and Chapter 29 (linear programming and the simplex method)
---

Smoothed analysis measures an algorithm by its worst-case expected cost when an adversary picks the input and then the input is randomly perturbed by a small amount. It lies between [worst-case analysis](/worst-case-analysis/), which a few fragile inputs can dominate, and [average-case analysis](/average-case-analysis/), whose random inputs may look nothing like real ones. Spielman and Teng introduced it in 2004 to explain why the [simplex method](/simplex-method/) is fast in practice, although some of its variants take exponential time on inputs such as the [Klee-Minty cube](/klee-minty-cube/). An algorithm with polynomial smoothed complexity is slow only on inputs that lie in small, isolated regions of the input space.

## In plain words

Some programs are fast on almost every input but very slow on a few special ones. A test that only looks at the worst input calls such a program slow. A test that looks at random inputs may call it fast, but real inputs are not random.

Smoothed analysis takes a middle path. Let an enemy choose the worst input. Then shake the input a little, the way real data always has small errors in it. Ask how long the program takes on the shaken input, on average over the shaking. If the answer is small even for a small shake, then the slow inputs are rare and fragile. A small error in the data makes them go away. This explains why some methods with a bad worst case work well in practice.

## The idea

**Definition.** Let $T(x)$ be the cost of an algorithm on input $x$. Inputs of size $n$ are vectors in $\mathbb{R}^m$, scaled so that the entries have size at most 1. Let $g$ be a random perturbation, usually a vector of independent Gaussian variables with mean 0 and standard deviation 1. The *smoothed complexity* with perturbation size $\sigma > 0$ is
$$ C(n, \sigma) = \max_{x} \; \mathbb{E}_{g}\big[T(x + \sigma g)\big]. $$
An algorithm has *polynomial smoothed complexity* if $C(n, \sigma)$ is bounded by a polynomial in $n$ and $1/\sigma$.

**The two limits.** When $\sigma \to 0$, the perturbation vanishes and $C(n, \sigma)$ tends to the worst-case cost. When $\sigma$ is large, the perturbation hides the input $x$ and $C(n, \sigma)$ becomes an average-case cost over a wide distribution. Smoothed analysis asks how fast the cost falls as $\sigma$ grows from 0.

**What a good bound means.** If $C(n, \sigma) \le \mathrm{poly}(n, 1/\sigma)$, then each input has a neighborhood of radius about $\sigma$ in which most points are easy. The hard inputs, if any, are isolated and need exact data. Real data comes from measurement or rounding, so it is perturbed anyway.

**The other models.** Average-case analysis fixes one distribution. [Expected running time](/expected-running-time/) of a [randomized algorithm](/randomized-algorithm/) puts the randomness into the algorithm. Smoothed analysis puts the randomness into the input, but only a small part of it, and keeps a worst-case choice for the rest. The perturbation can be Gaussian, uniform on an interval, or any density bounded by $\phi$; some results use the bound $\phi$ in place of $1/\sigma$.

**The simplex method.** Linear programs are solved in polynomial time in the worst case by the [ellipsoid method](/ellipsoid-method/) and [interior point methods](/interior-point-method/). The simplex method with common pivot rules takes exponentially many steps on the Klee-Minty cube and related inputs, yet it is fast in practice. Spielman and Teng proved that the shadow-vertex simplex method has smoothed complexity polynomial in the number of constraints, the dimension and $1/\sigma$, for a linear program whose constraint matrix and right side are perturbed by Gaussian noise of standard deviation $\sigma$, after the data is scaled to norm at most 1. The key quantity is the number of vertices of the *shadow*, the projection of the feasible polytope onto a fixed plane, which is small in expectation after perturbation. The proof is long, and later work improved the exponents.

## Examples

**Records of a perturbed sequence.** This small example shows the full method. Take the [hiring problem](/hiring-problem/) with candidate scores $x_1, \ldots, x_n$ in $[0, 1]$ chosen by an adversary. The worst input is increasing, with $n$ hires. Perturb each score: $y_i = x_i + \sigma u_i$, where $u_1, \ldots, u_n$ are independent and uniform on $[0, 1]$. Let $m$ be the number of records of $y$, that is, of hires.

*Claim.* For each input $x \in [0,1]^n$ and each $\varepsilon \in (0, 1]$,
$$ \mathbb{E}[m] \le \left\lceil \frac{1}{\sigma\varepsilon}\right\rceil H_n + \varepsilon n. $$
With $\varepsilon = \sqrt{H_n/(\sigma n)}$ (when this is at most 1), this gives $\mathbb{E}[m] \le 2\sqrt{nH_n/\sigma} + H_n$. So the smoothed number of hires is $O(\sqrt{n\log n/\sigma})$, polynomially less than $n$ for each fixed $\sigma$.

*Proof.* Cut $[0, 1]$ into $K = \lceil 1/(\sigma\varepsilon)\rceil$ intervals of length at most $\sigma\varepsilon$, and put each index $i$ in the group of the interval that holds $x_i$. Fix an index $i$, and let $A$ be the set of earlier indices $j < i$ in the same group. If $i$ is a record, then $y_i > y_j$ for each $j \in A$. Since $|x_i - x_j| \le \sigma\varepsilon$, this needs $u_i > u_j - \varepsilon$ for each $j \in A$, that is, $u_i > M - \varepsilon$ with $M = \max_{j \in A} u_j$. Now $u_i$ is independent of $M$ and has density 1, so
$$ \Pr[u_i > M - \varepsilon] \le \Pr[u_i > M] + \Pr[M - \varepsilon < u_i \le M] \le \frac{1}{|A| + 1} + \varepsilon, $$
where $\Pr[u_i > M] = 1/(|A| + 1)$ because each of the $|A| + 1$ independent uniform variables is equally likely to be the largest. In a group of size $s$, the $a$-th index has $|A| = a - 1$, so the group contributes at most $\sum_{a=1}^{s}(1/a + \varepsilon) = H_s + \varepsilon s \le H_n + \varepsilon s$. Adding over the $K$ groups gives the claim, by [linearity of expectation](/linearity-of-expectation/). $\square$

*Simulation.* The table uses the worst input $x_i = (i-1)/(n-1)$, which is increasing, with $n = 10^4$ and $H_n = 9.79$. The mean is over 100 runs (numpy, seed 7). The bound is $2\sqrt{nH_n/\sigma} + H_n$, which is above $n$, and so trivial, for $\sigma \le 0.001$.

| $\sigma$ | mean number of hires | bound | $\sqrt{n/\sigma}$ |
| --- | --- | --- | --- |
| 0 | 10000 | | |
| $10^{-4}$ | 10000 | trivial | 10000 |
| $10^{-3}$ | 4133 | trivial | 3162 |
| 0.01 | 1271 | 6267 | 1000 |
| 0.1 | 401 | 1988 | 316 |
| 1 | 129 | 635 | 100 |
| 10 | 44.9 | 208 | 31.6 |
| 100 | 19.1 | 72 | 10.0 |

At $\sigma = 10^{-4}$ the noise is smaller than the gaps $1/(n-1)$ between the scores, so the order does not change and every candidate is hired. As $\sigma$ grows, the count falls about like $\sqrt{n/\sigma}$, and for very large $\sigma$ it tends to the average-case value $H_n$.

**The knapsack problem.** The [knapsack problem](/knapsack-problem/) is NP-hard, but the number of Pareto optimal solutions, those not beaten in both weight and profit, is polynomial in expectation when the profits or the weights are perturbed. Beier and Vöcking proved such a bound for random knapsack instances in a model that is a precursor of the smoothed one. An algorithm that lists the Pareto optimal solutions then runs in expected polynomial time.

## Where it is used

- **Linear programming.** The main motivating result: the shadow-vertex simplex method on perturbed [linear programs](/linear-programming-problem/). It also bears on the [Hirsch conjecture](/hirsch-conjecture/), since the shadow bound limits the length of the path that the method follows.
- **Combinatorial optimization.** Local search heuristics such as [2-opt](/two-opt/) for the [traveling salesman problem](/traveling-salesman-problem/) and the [k-means](/k-means/) method are exponential in the worst case and have been studied in the smoothed model. Integer programs with perturbed coefficients, as in knapsack, form another line of work.
- **Numerical analysis.** The [condition number](/condition-number/) of a perturbed matrix is small with high probability, which explains the stability of [Gaussian elimination](/gaussian-elimination/) on most inputs.
- **Machine learning.** The [perceptron](/perceptron/) algorithm and other methods with bad worst cases have been analyzed for perturbed data.
- **Pitfalls.** A smoothed bound depends on the perturbation model. A result for Gaussian noise of every entry does not hold if the input has structure that the noise does not touch, such as zeros in a sparse matrix or integer data. The bounds are often large polynomials, so they explain why an algorithm is not exponential more than they predict its running time. And for $\sigma \to 0$ the smoothed bound tends to the worst case, which can be exponential.

## References
