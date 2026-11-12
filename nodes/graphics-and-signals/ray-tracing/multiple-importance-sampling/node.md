---
tag: T595A6
kind: technique
slug: multiple-importance-sampling
name: Multiple importance sampling
area: graphics-and-signals/ray-tracing
level: advanced
summary: Draw samples from several densities and weight each sample, by the balance or power heuristic, so that the weights sum to 1. The result is unbiased and robust when each density fails somewhere.
prereqs: [importance-sampling, next-event-estimation]
see_also: [bidirectional-path-tracing, path-guiding, vertex-connection-and-merging, restir, monte-carlo-integration, variance, stratified-sampling]
sources:
  - paper: doi:10.1145/218380.218498
    title: Eric Veach and Leonidas J. Guibas, Optimally combining sampling techniques for Monte Carlo rendering, Proceedings of SIGGRAPH 95, 1995, 419 to 428
    locator: the multi-sample estimator, the balance heuristic and its variance bound, the power and maximum heuristics, and the glossy highlights test
  - url: https://graphics.stanford.edu/papers/veach_thesis/
    title: Eric Veach, Robust Monte Carlo Methods for Light Transport Simulation, PhD thesis, Stanford University, 1997
    locator: Chapter 9, Multiple Importance Sampling, and its Appendix 9.A with the proofs
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 13.10 Importance Sampling (multiple importance sampling), Section 14.3 Direct Lighting
---

Multiple importance sampling estimates an integral $\int f$ with samples from several densities $p_1, \dots, p_k$ at once, and multiplies the contribution $f(X) / p_i(X)$ of each sample by a weight $w_i(X)$. If the weights sum to 1 wherever $f \ne 0$, the estimate is unbiased; the balance heuristic $w_i = n_i p_i / \sum_k n_k p_k$ makes its [variance](/variance/) nearly as low as that of any such weighting, by a bound of Veach and Guibas. It extends [importance sampling](/importance-sampling/) to the case where no single density fits the integrand everywhere. In rendering it combines light sampling and BSDF sampling in [next event estimation](/next-event-estimation/), and the strategies of [bidirectional path tracing](/bidirectional-path-tracing/).

## In plain words

Importance sampling works well when the samples go where the function is large. Often no single way of sampling does that everywhere. To light a shiny surface, aiming at the lamp works for a large lamp on a rough surface, and following the reflection works for a small lamp on a smooth surface. Each way fails badly in the other case.

Multiple importance sampling uses both ways. Each sample then counts as a share of a whole, and the shares of all the ways must add up to one at every point. The share of a way is large where that way is likely to sample the point, and small where it is unlikely. So each part of the integral is counted mostly by the way that samples it well, and a way that would give a rare huge value gives it a small share.

## When it applies

- **Several sampling methods, each good on part of the domain.** For direct light: sampling the light is good for small lights and rough surfaces, sampling the BSDF is good for large lights and glossy surfaces.
- **The density of each method can be evaluated at any point.** A weight needs $p_k(x)$ for every method $k$, also for the methods that did not produce $x$. In rendering this means the light sampler must give the density of a direction found by BSDF sampling, and the other way around, in the same measure.
- **Each part of the integrand is reachable.** At each $x$ with $f(x) \ne 0$, at least one method has $p_i(x) > 0$. A single method may miss parts of the domain; the union must not.

## The template

The multi-sample estimator takes $n_i$ samples $X_{i,1}, \dots, X_{i,n_i}$ from each density $p_i$.

```pseudo id=main
MIS-ESTIMATE(f, p1 .. pk, n1 .. nk)
L1  F ← 0
L2  for i ← 1 to k, for j ← 1 to ni:  draw X from pi          ▷ hole: the techniques
L3      w ← wi(X)                                             ▷ hole: the weights
L4      F ← F + w · f(X) / (ni · pi(X))
L5  return F
```

The estimate is $F = \sum_i \frac{1}{n_i} \sum_j w_i(X_{i,j})\, f(X_{i,j}) / p_i(X_{i,j})$. The weights must satisfy two conditions:

- **(W1)** $\sum_i w_i(x) = 1$ wherever $f(x) \ne 0$;
- **(W2)** $w_i(x) = 0$ wherever $p_i(x) = 0$.

**Why the mean is exact.** By (W2), $E\big[w_i(X_{i,j}) f(X_{i,j}) / p_i(X_{i,j})\big] = \int_{p_i > 0} w_i f = \int w_i f$. Each of the $n_i$ samples of technique $i$ has this mean, so technique $i$ contributes $\mu_i = \int w_i f$, and by (W1) $\sum_i \mu_i = \int f$.

**The heuristics.** All four satisfy (W1) and (W2).

| heuristic | $w_i(x)$ |
|---|---|
| balance | $\dfrac{n_i p_i(x)}{\sum_k n_k p_k(x)}$ |
| power, exponent $\beta$ | $\dfrac{(n_i p_i(x))^\beta}{\sum_k (n_k p_k(x))^\beta}$, usually $\beta = 2$ |
| maximum | $1$ for the technique with the largest $n_i p_i(x)$, $0$ for the others |
| cutoff, $\alpha \in [0, 1]$ | $n_i p_i(x)$ over the sum of those $n_k p_k(x)$ that are at least $\alpha \max_l n_l p_l(x)$, and $0$ when $n_i p_i(x)$ is below that |

With the balance heuristic, each term of $F$ is $f(X) / \sum_k n_k p_k(X)$: the sample is treated as if it came from the mixture of all the techniques.

**The variance bound.** For $f \ge 0$ and weights in $[0, 1]$ that satisfy (W1) and (W2), let $F$ be any such estimator and $\hat F$ the one with the balance heuristic. Then

$$\operatorname{Var}[\hat F] \le \operatorname{Var}[F] + \Big(\frac{1}{\min_i n_i} - \frac{1}{\sum_i n_i}\Big)\, \mu^2, \qquad \mu = \int f.$$

*Proof.* The samples are independent, so $\operatorname{Var}[F] = \int f^2 \sum_i \frac{w_i^2}{n_i p_i} - \sum_i \frac{\mu_i^2}{n_i}$, with the sum inside the integral over the techniques with $p_i > 0$. At each $x$, the Cauchy-Schwarz inequality gives $1 = (\sum_i w_i)^2 \le \big(\sum_i \frac{w_i^2}{n_i p_i}\big)\big(\sum_i n_i p_i\big)$, so $\sum_i \frac{w_i^2}{n_i p_i} \ge 1 / \sum_k n_k p_k$, with equality for the balance weights. So the first term is smallest for $\hat F$. For the second term, Cauchy-Schwarz again gives $\sum_i \hat\mu_i^2 / n_i \ge (\sum_i \hat\mu_i)^2 / \sum_i n_i = \mu^2 / \sum_i n_i$, and since $\mu_i \ge 0$, $\sum_i \mu_i^2 / n_i \le \frac{1}{\min_i n_i} \sum_i \mu_i^2 \le \mu^2 / \min_i n_i$. Subtracting gives the bound. $\square$

The bound says that no other weighting can do much better than the balance heuristic when the variance is large compared with $\mu^2$, which is the case where variance matters. The power heuristic with $\beta = 2$ often does a little better in practice, when one technique is much better than the others at a point; it has a similar bound.

**The one-sample model.** Choose technique $i$ with the probability $c_i$, draw one $X$ from $p_i$, and return $w_i(X) f(X) / (c_i p_i(X))$. It is unbiased under (W1) and (W2), and with the balance weights $c_i p_i / \sum_k c_k p_k$ it is exactly the estimator $f(X) / \sum_k c_k p_k(X)$ of the mixture density.

## Classic examples

**A finite domain, exact.** The domain is $\{0, \dots, 5\}$ with $f = (2, 3, 1, 4, 0, 6)$, so $\int f = 16$. Technique 1 has $p_1 = (0, \tfrac{1}{10}, \tfrac{1}{10}, \tfrac15, \tfrac15, \tfrac25)$ and cannot sample $x = 0$; technique 2 has $p_2 = (\tfrac12, \tfrac15, \tfrac{1}{10}, \tfrac{1}{10}, \tfrac{1}{10}, 0)$ and cannot sample $x = 5$. Alone, technique 1 has the mean $14$ and technique 2 the mean $10$: each misses a part. With one sample of each, the exact means and variances are:

| weights | mean | variance |
|---|---|---|
| balance | $16$ | $\tfrac{881}{18} \approx 48.94$ |
| power, $\beta = 2$ | $16$ | $\tfrac{2721}{50} = 54.42$ |
| the same share for each technique that can sample $x$ | $16$ | $\tfrac{243}{4} = 60.75$ |
| maximum | $16$ | $87$ |
| $\tfrac12$ each everywhere, which breaks (W2) | $12$ | biased |

The last row has weights that do not satisfy (W2): technique 1 gives $x = 0$ the weight $\tfrac12$ but never samples it, so half of $f(0)$ and half of $f(5)$ are lost, and the mean is $16 - 1 - 3 = 12$. The slack term of the bound is $(1 - \tfrac12)\, 16^2 = 128$ here.

**Direct light in [next event estimation](/next-event-estimation/).** At each vertex, take one light sample and one BSDF sample. Weight the light sample with $w_L = p_L^2 / (p_L^2 + p_B^2)$ and the emission that the BSDF ray hits with $w_B = p_B^2 / (p_L^2 + p_B^2)$, both densities per unit solid angle at the vertex. The light density of a direction is the area density times $|y - x|^2 / \cos\theta_y$. In a sphere of radius 2 with albedo $\tfrac45$ around an emitting sphere of radius $\tfrac35$ with radiance $1$ and albedo $\tfrac12$, the exact radiance of the outer wall is $\tfrac{18}{59} \approx 0.3051$. With 2000 paths (seed 1) the estimates are:

| technique | mean | standard error |
|---|---|---|
| light sampling only | $0.2922$ | $0.0086$ |
| BSDF sampling only | $0.2860$ | $0.0118$ |
| MIS, balance | $0.2912$ | $0.0075$ |
| MIS, power | $0.2916$ | $0.0077$ |

All four are within 2 standard errors of the exact value, and MIS has the lowest error. MIS is not always the best of its parts: inside a single sphere, light sampling has zero variance per sample, and MIS with BSDF sampling is noisier than light sampling alone. MIS is robust, not optimal.

**[Bidirectional path tracing](/bidirectional-path-tracing/).** A path of $k$ edges can be built in $k + 1$ or more ways, by the number $s$ of vertices from the light and $t$ from the camera. MIS weights the $(s, t)$ strategies of each path with the densities of all the strategies that could have made it.

**[Path guiding](/path-guiding/).** A one-sample mixture of the BSDF and a learned guiding density, with the balance weights of the one-sample model.

**[Vertex connection and merging](/vertex-connection-and-merging/).** MIS between the connections of bidirectional path tracing and the merges of photon density estimation.

**[ReSTIR](/restir/).** Combining reservoirs from several pixels uses MIS weights over the pixels whose target functions could have produced the sample.

## Variations

- **Choosing the counts $n_i$.** The bound depends on $\min_i n_i$. Equal counts are common. Adaptive methods change the counts or the mixture probabilities $c_i$ to lower the variance.
- **Optimal MIS.** The balance heuristic is optimal among weights that do not depend on $f$. Weights that use estimates of $f$ itself, or that allow negative values, can give lower variance; the bound above does not cover them.
- **Defensive mixtures.** In statistics, sampling from $\alpha p + (1 - \alpha) q$ guards against a poor proposal $q$; this is the one-sample balance heuristic with the fixed mixture probabilities $\alpha$ and $1 - \alpha$.
- **MIS with [stratified sampling](/stratified-sampling/) and quasi-Monte Carlo.** The weights stay the same; only the samples are placed better.
- **MIS compensation.** Change one of the densities to sample less where the other techniques are already good, so that the combined density fits $f$ better.

## Pitfalls

- **Densities in different measures.** A light sampler gives a density per unit area and a BSDF sampler a density per unit solid angle. Convert one to the other, with $p_\omega = p_A\, |y - x|^2 / \cos\theta_y$, before computing a weight.
- **Missing factors in the other density.** The density of the light sampler for a direction found by BSDF sampling must include the probability of choosing that light among all lights.
- **Weights that do not sum to 1.** A renderer that weights the light sample but adds the emission that the BSDF ray hits with weight 1 counts the direct light more than once.
- **Delta densities.** An ideal mirror has a BSDF density with a point mass, which no light sample can produce. Give the BSDF sample the weight 1 there and do not take a light sample.
- **Overflow in the power heuristic.** $(n_i p_i)^\beta$ can overflow for large densities; divide by the largest term first.
- **No good technique.** MIS keeps the variance near that of the best technique at each point. If all of them are poor somewhere, as for a caustic seen in a mirror, MIS does not help there.

## Exercises

1. Prove that the multi-sample estimator is unbiased under (W1) and (W2), and give an example where (W1) holds but (W2) does not and the mean is wrong.
2. Show that the balance weights minimize $\sum_i w_i^2 / (n_i p_i)$ at each point subject to $\sum_i w_i = 1$.
3. In the finite example, compute the variance with the balance heuristic and the counts $n_1 = 2$, $n_2 = 3$. (The answer is $\tfrac{585511}{23520} \approx 24.89$.)
4. Show that the power heuristic tends to the maximum heuristic as $\beta \to \infty$, at points where the largest $n_i p_i$ is unique.
5. Show that the one-sample model with the balance heuristic is the importance sampling estimator of the mixture $\sum_k c_k p_k$.

## References
