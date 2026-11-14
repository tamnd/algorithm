---
tag: XMR9Q0
kind: algorithm
slug: statistical-static-timing-analysis
name: Statistical static timing analysis
aliases:
- SSTA
area: eda/timing-and-verification
level: advanced
summary: Propagates delays as random variables, often linear in shared Gaussian sources of variation, through the timing graph by sum and statistical max.
solves: [longest-path-problem]
model: real-ram
complexity:
  vars: {V: the number of vertices (pins) of the timing graph, E: the number of edges, m: the number of global sources of variation}
  time: {worst: Θ((V + E) m), average: Θ((V + E) m), best: Θ((V + E) m)}
  space: {extra: Θ(V m)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2004
  people: [Chandu Visweswariah, Kaushik Ravindran, Kerim Kalafala, Steven G. Walker, Sambasivan Narayan]
  note: Visweswariah and his colleagues at IBM gave the first-order canonical form and the block-based propagation with Clark's max in 2004. Clark had derived the moments of the max of two Gaussians in 1961 for PERT networks.
prereqs: [static-timing-analysis, probability-distribution, covariance-matrix]
see_also: [arrival-and-required-time, timing-graph, nonlinear-delay-model, principal-component-analysis, monte-carlo-integration, critical-path-method, jensens-inequality]
sources:
  - paper: "Chandu Visweswariah, Kaushik Ravindran, Kerim Kalafala, Steven G. Walker and Sambasivan Narayan, First-order incremental block-based statistical timing analysis, Proceedings of the 41st Design Automation Conference, 331 to 336, 2004"
    locator: the canonical first-order form, the sum and the max operations, tightness probabilities and the incremental analysis
  - paper: doi:10.1109/TCAD.2005.862751
    title: Chandu Visweswariah, Kaushik Ravindran, Kerim Kalafala, Steven G. Walker, Sambasivan Narayan and others, First-order incremental block-based statistical timing analysis, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 25(10), from page 2170, 2006
    locator: the journal version, with the criticality probabilities and the results on IBM designs
  - paper: "Charles E. Clark, The greatest of a finite set of random variables, Operations Research 9(2), 145 to 162, 1961"
    locator: the mean and the variance of the max of two jointly normal variables, and its correlation with a third normal variable
  - book: doi:10.1007/978-0-387-93820-2
    title: J. Bhasker and Rakesh Chadha, Static Timing Analysis for Nanometer Designs, A Practical Approach, Springer, 2009
    locator: Section 10.9, Statistical Static Timing Analysis
---

Statistical static timing analysis (SSTA) is [static timing analysis](/static-timing-analysis/) in which the delays are random variables instead of numbers. Variations of the manufacturing process, such as the gate length or the oxide thickness, change all delays on a chip together, and random effects change each gate on its own. In the block-based method of Visweswariah and his colleagues (2004), each delay and each arrival time is a linear function of a few shared standard normal sources and one private normal term, the *canonical form*. The forward pass adds forms along the edges and combines the in-edges at a vertex by a *statistical max*, which uses Clark's (1961) formulas for the max of two Gaussians. The pass is linear in the size of the timing graph. The sum is exact. The max keeps the mean, the variance and the correlations, but the true max is not Gaussian, so the result is an approximation.

## In plain words

Plain STA asks how late a signal can arrive. On a real chip, the delays change from chip to chip, and many of them change together. SSTA asks for the distribution of the arrival time: its mean, its spread and how it moves with each shared cause of variation.

Each delay is written as "mean plus some amount of each shared cause plus some private noise". Adding two delays adds these amounts. Taking the later of two arrivals is harder, because the later of two bell curves is not a bell curve. SSTA replaces it by the bell curve that has the same mean and the same spread, and that depends on each shared cause the same way. At the end, the distribution at an output gives the fraction of chips that meet the clock period.

## The problem

The input is a timing graph $G = (V, E)$ that is a [DAG](/directed-acyclic-graph/), a canonical form for each edge delay and for the arrival time at each start point, all over the same global sources $Z_1, \ldots, Z_m$. A canonical form is
$$ X = \mu + \sum_{i=1}^m a_i Z_i + r R, $$
where the $Z_i$ and $R$ are independent standard normal variables, and $R$ is private: it is independent of the private term of every other form. So $\mathrm{Var}(X) = \sum a_i^2 + r^2$ and $\mathrm{Cov}(X, Z_i) = a_i$. The sources often come from a [principal component analysis](/principal-component-analysis/) of correlated parameters, which makes them independent.

The true arrival time at $v$ is the random variable $\max_P (AT_0(s) + d(P))$ over all paths $P$ from a start point $s$ to $v$, as in the [longest path problem](/longest-path-problem/), but with random delays. The goal is its distribution, or at least its mean, its variance and its covariance with each $Z_i$, and from these the *timing yield* $P(AT(t) \le T)$ at each endpoint $t$ for a clock period $T$.

## The algorithm

```pseudo id=main
SSTA(G, d, AT0)
L1  order ← a topological order of G (stop with an error if G has a cycle)
L2  for each vertex v in order do
L3      if v has no in-edge then AT(v) ← AT0(v)
L4      else for each in-edge (u, v), in a fixed order, do S ← ADD(AT(u), d(u, v))
L5          AT(v) ← S for the first in-edge, else MAX(AT(v), S)
L6  return AT

ADD(A, B)
L7  c_i ← a_i + b_i for i = 1 .. m
L8  return (μ_A + μ_B, c, sqrt(r_A² + r_B²))

MAX(A, B)
L9  if θ² = σ_A² + σ_B² − 2 Σ a_i b_i is 0 then
L10     return A if μ_A ≥ μ_B else B                 ▷ A − B is a constant
L11 θ ← sqrt(θ²);  α ← (μ_A − μ_B) / θ
L12 T ← Φ(α)                                        ▷ tightness probability P(A > B)
L13 μ ← μ_A T + μ_B (1 − T) + θ φ(α)
L14 s ← (μ_A² + σ_A²) T + (μ_B² + σ_B²)(1 − T) + (μ_A + μ_B) θ φ(α)
L15 c_i ← T a_i + (1 − T) b_i for i = 1 .. m
L16 r ← sqrt(s − μ² − Σ c_i²)                       ▷ the variance is matched
L17 return (μ, c, r)
```

Here $\Phi$ and $\varphi$ are the standard normal distribution function and density. Line L13 is Clark's mean of $\max(A, B)$ and line L14 its second moment. Line L15 is the covariance of $\max(A, B)$ with $Z_i$, which Clark's formula gives as the tightness-weighted mix of the two inputs. Line L16 puts the rest of the variance into the private term. The timing yield of an endpoint is $\Phi((T - \mu)/\sigma)$ for its form.

## Example

**Two independent standard normals.** For $A = B$ in distribution, standard normal and independent ($a = b = 0$, $r_A = r_B = 1$): $\theta = \sqrt 2$, $\alpha = 0$, $T = 1/2$, and line L13 gives $\mu = \sqrt 2 \, \varphi(0) = 1/\sqrt\pi \approx 0.5642$. Line L14 gives $s = 1$, so the variance is $1 - 1/\pi \approx 0.6817$. These are the exact mean and variance of the max of two independent standard normals.

**A diamond with one global source.** Vertex 0 has arrival time 0 and two paths lead to vertex 3, through 1 and through 2. The edge delays are $d(0,1) = 3 + 0.4 Z + 0.3 R$, $d(1,3) = 2 + 0.2 Z + 0.2 R$, $d(0,2) = 2.6 + 0.1 Z + 0.5 R$ and $d(2,3) = 2.5 + 0.3 Z + 0.2 R$, where each $R$ is a different private variable.

| step | form | std. dev. |
| --- | --- | --- |
| L4 on $(1, 3)$ | $A = 5.0 + 0.6 Z + 0.3606 R$ | 0.7 |
| L4 on $(2, 3)$ | $B = 5.1 + 0.4 Z + 0.5385 R$ | 0.6708 |
| L11 | $\theta^2 = 0.49 + 0.45 - 2 \cdot 0.24 = 0.46$, $\theta = 0.6782$, $\alpha = -0.1474$ | |
| L12 | $T = \Phi(-0.1474) = 0.4414$ | |
| L13 to L17 | $AT(3) = 5.3235 + 0.4883 Z + 0.3961 R$ | 0.6288 |

STA with the mean delays gives 5.1. The mean of the max is larger, 5.3235, because a max of random variables has a mean at least the max of the means ([Jensen's inequality](/jensens-inequality/)). Path $A$ is the later one with probability 0.44, although its mean is smaller, because it has the larger spread. Here only one max is taken, of two path sums with separate private terms, so the mean, the variance and the coefficient of $Z$ are exact (see Correctness). A Monte Carlo run with 200000 samples (Python `random.Random(7)`) gives mean 5.3246 and standard deviation 0.6285, within its sampling error. The shape is not exact: the timing yield at $T = 5.5$ is 0.6105 from the form and 0.6129 from Monte Carlo; at $T = 6.0$ both are 0.859.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Clark's formulas.** For jointly Gaussian $A$ and $B$, lines L12 to L15 give exactly $P(A > B)$, the mean and the second moment of $\max(A, B)$, and its covariance with every $Z_i$.
- **The max form matches the first two moments.** The value under the root in line L16 is never negative, by Bessel's inequality, and the form has the mean, the variance and the covariances with the $Z_i$ of the true max of its two inputs. If $\theta = 0$, the max is exact.
- **The sum is exact.** ADD gives the exact joint distribution of $A + B$ and the $Z_i$.
- **Chains are exact.** If no vertex has two in-edges, every arrival time is exact.
- **No variation gives STA.** With all coefficients 0, the algorithm is static timing analysis.

What is not proved is how close the result is on a general DAG. Two approximations add up there: each max is replaced by a Gaussian, and the private terms of later forms are taken as independent although they share earlier ones. As a measurement only: on 60 random DAGs with 4 to 8 vertices, 1 to 3 global sources and edge delays with means from 1 to 4 and coefficients up to 0.5 (seed 1), the mean of the endpoint form was within 0.05 standard deviations of a Monte Carlo estimate with 4000 samples, and its standard deviation within 0.04 standard deviations. The tests use a tolerance of 0.12 standard deviations with 3000 samples.

## Complexity

- **Time.** Line L1 takes $\Theta(V + E)$. Each edge causes one ADD and at most one MAX, each with $\Theta(m)$ operations and a constant number of evaluations of $\Phi$, $\varphi$ and the square root. In total $\Theta((V + E) m)$, compared with $\Theta(V + E)$ for STA.
- **Space.** One form of $m + 2$ numbers per vertex, $\Theta(V m)$.
- **Comparison with Monte Carlo.** A Monte Carlo analysis runs STA once per sample, so $N$ samples cost $\Theta(N (V + E))$. Its error falls like $1/\sqrt N$, so thousands of samples are needed for the tails. SSTA does one pass.

## Properties

- **Approximate, not a bound.** The result is not an upper bound on the true distribution, and it is not exact on a DAG with reconvergent paths. In practice its error is small compared with the spread of the delays, as the measurement above shows.
- **Correlations are kept.** Since each form keeps its coefficients of the global sources, reconvergent paths that share variation are not treated as independent, and the arrival times at different endpoints stay correlated. This is what makes the yield of a whole chip computable.
- **Order of the in-edges.** MAX of three or more forms is done in pairs, and the result depends slightly on the order.
- **Block-based.** Like STA, the cost does not depend on the number of paths, and the analysis can be updated incrementally after a change.

## Variants and improvements

- **Required times and criticality.** A backward pass with a statistical min gives required times and slacks as forms. The tightness probabilities of line L12, multiplied along paths, give the probability that each edge is on the critical path (the criticality), which guides optimization.
- **Path-based SSTA.** Enumerate the worst paths of STA and compute the distribution of each path delay exactly as a sum, then the max over the few paths. This avoids the errors of repeated max steps but may miss paths.
- **Non-Gaussian and non-linear models.** Quadratic canonical forms, or forms with non-Gaussian sources, follow strongly non-linear delays better, at a higher cost per operation.
- **Monte Carlo.** Sampling the sources and running STA per sample is the reference method. It is exact in the limit and costly.
- **Statistical libraries.** The coefficients of the cell delays come from libraries with sensitivities or standard deviations next to each table of a [nonlinear delay model](/nonlinear-delay-model/).

## When to use it

- When the variation of the delays is large compared with the margins, so that corner-based STA, which assumes every delay at its worst value at once, is too pessimistic or misses correlations.
- To estimate the timing yield of a design and to find the edges that are most often critical.
- Not when a guaranteed bound is required. Sign-off with STA at corners gives bounds under its assumptions, and SSTA gives an estimate of a distribution.

## Pitfalls

- **Reading the result as exact.** The max of Gaussians is not Gaussian. Far in the tails, where yield is decided, the error of the shape can matter even when the mean and the variance are right.
- **Ignoring correlation.** Treating all delays as independent makes the variance of long paths far too small and the yield far too high. The global sources in the forms are there to prevent this.
- **Clamping.** In exact arithmetic the value in line L16 is not negative. With rounding it can be a tiny negative number, so implementations clamp it at 0; a large negative value means a bug.
- **Mixing modes.** The hold check needs a statistical min of early arrival times, with the same care about correlation, not the late forms.

## Implementations

## History

Clark (1961) derived the mean and the variance of the max of two jointly normal variables, and the correlation of the max with a third normal variable, to analyse PERT networks with random activity times. Visweswariah, Ravindran, Kalafala, Walker and Narayan presented the first-order canonical form at DAC 2004, with the incremental analysis and the tightness probabilities, as a tool used at IBM. The journal version appeared in 2006.

## References
