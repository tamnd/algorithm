---
tag: DE6SYB
kind: algorithm
slug: output-perturbation
name: Output perturbation
aliases:
- sensitivity-based model perturbation
area: security-and-privacy/differential-privacy
level: core
summary: Trains a model by regularized empirical risk minimization and adds noise scaled to the sensitivity of the minimizer.
model: real-ram
complexity:
  vars: {n: the number of examples, d: the dimension, K: the number of solver iterations}
  time: {worst: O(K n d)}
  space: {extra: O(d)}
properties: {deterministic: false, randomized: true}
history:
  year: 2008
  people: [Kamalika Chaudhuri, Claire Monteleoni, Anand D. Sarwate]
  note: "Chaudhuri and Monteleoni (NIPS 2008) applied the sensitivity method of Dwork, McSherry, Nissim and Smith to regularized logistic regression. Chaudhuri, Monteleoni and Sarwate (JMLR 2011) stated it for general strongly convex ERM as their Algorithm 1."
prereqs: [empirical-risk-minimization, global-sensitivity]
see_also: [objective-perturbation, laplace-mechanism, gaussian-mechanism, logistic-regression, dp-sgd, subsample-and-aggregate, convex-function, post-processing-theorem]
sources:
  - url: "https://www.jmlr.org/papers/v12/chaudhuri11a.html"
    title: "Kamalika Chaudhuri, Claire Monteleoni and Anand D. Sarwate, Differentially private empirical risk minimization, Journal of Machine Learning Research 12, 2011, pages 1069 to 1109"
    locator: "Algorithm 1 (Section 3.1), Theorem 6 (its privacy), Lemma 7 (the sensitivity of a strongly convex minimizer) and Corollary 8 (the bound 2/(n Lambda))"
  - paper: "Kamalika Chaudhuri and Claire Monteleoni, Privacy-preserving logistic regression, Advances in Neural Information Processing Systems 21 (NIPS 2008)"
    locator: the sensitivity method for regularized logistic regression and its comparison with objective perturbation
  - paper: doi:10.1007/11681878_14
    title: "Cynthia Dwork, Frank McSherry, Kobbi Nissim and Adam Smith, Calibrating noise to sensitivity in private data analysis, TCC 2006"
    locator: adding noise scaled to the sensitivity of a function
---

Output perturbation trains a model in the normal way and then adds random noise to the trained parameters. The training is regularized [empirical risk minimization](/empirical-risk-minimization/): minimize the average loss plus $(\Lambda/2)\|f\|^2$. The regularizer makes the minimizer stable, so that it moves by at most $2/(n\Lambda)$ when one of the $n$ examples changes. Noise scaled to that [sensitivity](/global-sensitivity/) then makes the released model $\varepsilon$-differentially private. Chaudhuri and Monteleoni (2008) used it for logistic regression, and Chaudhuri, Monteleoni and Sarwate (2011) stated it for strongly convex losses as their Algorithm 1. It is the simplest private learner for convex models, and the baseline that [objective perturbation](/objective-perturbation/) improves on.

## In plain words

Train the model on the private data as usual, but with a penalty on large weights. That penalty has a side effect: changing one example can move the trained weights only a little, and we can compute how much at most.

So add random noise to the weights, large enough to cover that small move. An observer who sees the noisy weights cannot tell whether any one example was in the data.

More data or a larger penalty makes the possible move smaller, and so the noise smaller. With few examples the noise can be larger than the weights.

## The problem

The data is $D = ((x_1, y_1), \ldots, (x_n, y_n))$ with $x_i \in \mathbb R^d$, $\|x_i\| \le 1$ and $y_i \in \{-1, +1\}$. The neighbor relation is replace: $D'$ is $D$ with one example changed to another, and $n$ is public. The loss is $\ell(y f^{\mathsf T} x)$ for a convex differentiable $\ell$ with $|\ell'| \le 1$; the code uses the logistic loss $\ell(z) = \ln(1 + e^{-z})$. The goal is an $\varepsilon$-[DP](/differential-privacy-definition/) vector $f$ with a small regularized risk

$$J_D(f) = \frac1n \sum_{i=1}^n \ell(y_i f^{\mathsf T} x_i) + \frac{\Lambda}{2}\|f\|^2.$$

## The algorithm

```pseudo id=main
OUTPUT-PERTURBATION(D, Lambda, epsilon)
L1  f* <- argmin over f of J_D(f)                  ▷ exact minimizer, unique since J_D is strongly convex
L2  beta <- n Lambda epsilon / 2                     ▷ 2/(n Lambda) is the L2 sensitivity of f*
L3  b <- a vector with density proportional to exp(-beta |b|)
L4  return f* + b
```

Line L1 is the non-private training. The code runs [gradient descent](/gradient-descent/) with the step $1/(1/4 + \Lambda)$, since the logistic risk is $(1/4 + \Lambda)$-smooth, and stops when the gradient norm is at most $10^{-11}$. Line L2 sets the rate of the noise from the sensitivity bound $2/(n\Lambda)$ of Lemma 7 and Corollary 8 of Chaudhuri, Monteleoni and Sarwate. Line L3 draws the noise in two parts: the norm $\|b\|$ is a sum of $d$ independent exponential draws of rate $\beta$, which is the Gamma law of shape $d$, and the direction is a Gaussian vector divided by its norm. In one dimension this is the [Laplace mechanism](/laplace-mechanism/) with scale $1/\beta$. In $d$ dimensions it is not the same as Laplace noise in each coordinate: the noise is a function of the L2 norm, to match the L2 sensitivity. Line L4 releases the noisy model. Any use of it afterwards is private by [post-processing](/post-processing-theorem/).

The code uses floats and a seeded generator, which shows the algorithm but is not a safe deployment. The analysis assumes exact real noise, and floating-point samplers can leak (Mironov 2012). A deployment needs a cryptographic source of randomness and a sampler built for DP, such as the [discrete Gaussian](/discrete-gaussian-mechanism/) for the Gaussian variant.

## Example

Take $n = 4$ examples in the plane, $\Lambda = 0.5$ and $\varepsilon = 1$.

| $i$ | $x_i$ | $y_i$ |
|---|---|---|
| 1 | (0.6, 0.8) | +1 |
| 2 | (1, 0) | +1 |
| 3 | (-0.6, 0) | -1 |
| 4 | (0, -1) | -1 |

Line L1 gives $f^* = (0.4368, 0.3532)$, with $J_D(f^*) = 0.5935$. Replace example 4 by $((0, 1), -1)$: the minimizer becomes $(0.4568, -0.0642)$, at distance $0.4178$ from $f^*$, below the bound $2/(n\Lambda) = 1$. Line L2 gives $\beta = 4 \cdot 0.5 \cdot 1/2 = 1$. With the seed 9 the code draws $b = (0.7019, 0.8327)$, of norm $1.0891$, and returns $(1.1387, 1.1859)$.

The noise here is larger than the model, whose norm is $0.5618$. The table shows how the noise shrinks with $n$ for $\Lambda = 0.5$, $\varepsilon = 1$ and $d = 2$; the mean norm of $b$ is $d/\beta$.

| $n$ | sensitivity $2/(n\Lambda)$ | $\beta$ | mean $\lVert b \rVert$ |
|---|---|---|---|
| 4 | 1 | 1 | 2 |
| 100 | 0.04 | 25 | 0.08 |
| 1000 | 0.004 | 250 | 0.008 |
| 10000 | 0.0004 | 2500 | 0.0008 |

## Correctness

**Lemma (sensitivity).** For replace neighbors, $\|f^*_D - f^*_{D'}\| \le 2/(n\Lambda)$. The proof uses only the $\Lambda$-strong convexity of $J_D$ and the bound $\|\nabla_f \ell(y f^{\mathsf T} x)\| \le 1$.

**Theorem (privacy).** The output of line L4 is $\varepsilon$-DP under replace. The output density on $D$ is $\nu(z - f^*_D)$ with $\nu(b) \propto e^{-\beta\|b\|}$, and the triangle inequality bounds the log ratio of the two densities by $\beta\|f^*_D - f^*_{D'}\| \le \varepsilon$.

**An inexact solver.** If line L1 returns a point within $\tau$ of the minimizer for every input, the same proof gives $\varepsilon(1 + n\Lambda\tau)$. The stopping rule of the code gives $\tau = 10^{-11}/\Lambda$. A solver that stops after a fixed number of steps with no such bound gives no proved guarantee.

The correctness proof of this page proves all three claims. The tests check the minimizer against bisection in one dimension, the sensitivity bound on 500 random replace pairs, the log density ratio on a grid, and the law of the noise norm.

## Complexity

The model is the [real RAM](/real-ram/), with one exponential or Gaussian draw counted as $O(1)$.

- **Training.** One gradient costs $O(nd)$. Gradient descent on a $\Lambda$-strongly convex and $(1/4 + \Lambda)$-smooth risk needs $K = O((1 + 1/(4\Lambda)) \ln(1/t))$ steps to reach the gradient norm $t$, so line L1 costs $O(Knd)$.
- **Noise.** Line L3 costs $O(d)$ draws, and line L4 costs $O(d)$.
- **Space.** The extra space is $O(d)$ beyond the data.

The private part adds almost nothing to the cost of training.

## Properties

- **A black box.** Any solver can be used for line L1, as long as it returns the exact minimizer or a point with a known distance bound. The private step only touches the output.
- **Pure DP.** The guarantee is $\varepsilon$-DP with $\delta = 0$, under replace neighbors.
- **Needs strong convexity.** Without the regularizer, the minimizer can jump far when one example changes, and the sensitivity has no bound. The noise grows like $1/\Lambda$, so a small $\Lambda$ costs accuracy through the noise and a large $\Lambda$ costs accuracy through the bias.
- **Noise of order $d/(n\Lambda\varepsilon)$.** The expected norm of $b$ is $2d/(n\Lambda\varepsilon)$. Chaudhuri, Monteleoni and Sarwate prove learning bounds for it and show that objective perturbation needs fewer examples for the same accuracy in their bounds and experiments.
- **The hypotheses matter.** The bound $2/(n\Lambda)$ needs $\|x_i\| \le 1$ and $|\ell'| \le 1$. The squared loss has no such bound on $\ell'$, so linear regression needs bounded labels and a bounded domain for $f$ before the method applies.

## Variants and improvements

- **Gaussian noise.** With $b \sim \mathcal N(0, \sigma^2 I)$ and $\sigma = (2/(n\Lambda))\sqrt{2\ln(1.25/\delta)}/\varepsilon$ for $\varepsilon < 1$, the [Gaussian mechanism](/gaussian-mechanism/) gives $(\varepsilon, \delta)$-DP. Its noise norm grows like $\sqrt d$, not $d$.
- **[Objective perturbation](/objective-perturbation/).** Put the noise into the objective before minimizing it, not into the minimizer. It needs a twice differentiable loss and usually gives better accuracy.
- **Output perturbation of SGD.** For a fixed number of passes of SGD on a strongly convex loss, the sensitivity of the final iterate can be bounded directly, and the same noise applies. Wu et al. (SIGMOD 2017) built a system on this idea.
- **Other models.** The same step applies to any statistic with a known sensitivity, for example a private mean. When the sensitivity is not known in advance, [subsample and aggregate](/subsample-and-aggregate/) gives a bound by design.
- **Noisy training.** [DP-SGD](/dp-sgd/) adds noise during training, so it does not need convexity or an exact minimizer.

## When to use it

Use output perturbation for a convex model with a strongly convex regularizer, such as $L_2$-regularized [logistic regression](/logistic-regression/) or a support vector machine with a smooth loss, when the training code must stay as it is. It is simple to audit: the only private step is one line of noise. When accuracy matters more, try objective perturbation first. For non-convex models it does not apply, and DP-SGD is the usual choice.

## Pitfalls

- **Noise per coordinate.** Line L3 with independent Laplace noise of scale $2/(n\Lambda\varepsilon)$ in each coordinate is calibrated to the L1 sensitivity, which can be $\sqrt d$ times the L2 bound, so it does not give $\varepsilon$-DP for $d > 1$. Line L3 must draw the norm from the Gamma law and a uniform direction, or use the L1 sensitivity $2\sqrt d/(n\Lambda)$.
- **A stopped solver.** Line L1 run for a fixed number of steps with no bound on the distance to the minimizer breaks the sensitivity bound. Line L1 must stop at a known gradient norm $t$, and line L2 must then use $\varepsilon/(1 + nt)$ in place of $\varepsilon$ to keep the total at $\varepsilon$.
- **Features out of the ball.** Line L1 run on data with $\|x_i\| > 1$ breaks the bound $2/(n\Lambda)$ of line L2. Scale or clip each $x_i$ to the unit ball with a rule that does not depend on the data, before line L1.
- **A data-dependent $\Lambda$.** Line L2 with $\Lambda$ picked by cross-validation on the private data leaks through the choice. Line L2 must use a $\Lambda$ fixed in advance, or the tuning must be private and counted in the budget.
- **Add/remove neighbors.** Line L2 assumes replace neighbors with a public $n$. Under add/remove the size changes, and the bound must be recomputed for that relation.

## Implementations

## History

Dwork, McSherry, Nissim and Smith (TCC 2006) defined the sensitivity method: add noise scaled to how much one record can change the output. Chaudhuri and Monteleoni (NIPS 2008) applied it to regularized logistic regression, bounded the sensitivity of the minimizer, and proposed objective perturbation as a better method. Chaudhuri, Monteleoni and Sarwate (JMLR 2011) extended both methods to general strongly convex ERM and to kernels, proved generalization bounds, and compared the methods on real data.

## References
