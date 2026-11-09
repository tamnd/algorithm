---
tag: GYVPW2
kind: problem
slug: stochastic-optimization
name: Stochastic optimization
aliases:
- stochastic programming with gradient oracles
- expected risk minimization
- stochastic convex optimization
area: optimization/gradient-methods
level: core
summary: Minimize an expectation of a function using noisy gradient estimates.
prereqs: [expected-value, gradient, convex-function]
see_also: [stochastic-gradient-descent, robbins-monro-algorithm, finite-sum-minimization, empirical-risk-minimization, online-convex-optimization, stochastic-approximation, first-order-lower-bound, svrg]
sources:
  - paper: doi:10.1137/070704277
    title: Arkadi Nemirovski, Anatoli Juditsky, Guanghui Lan and Alexander Shapiro, Robust stochastic approximation approach to stochastic programming, SIAM Journal on Optimization 19(4), 2009
    locator: pages 1574 to 1609, the comparison of stochastic approximation and sample average approximation, and the O(1/√k) and O(1/k) rates
  - book: isbn:9781611973426
    title: Alexander Shapiro, Darinka Dentcheva and Andrzej Ruszczyński, Lectures on Stochastic Programming, Modeling and Theory, second edition, SIAM, 2014
    locator: Chapter 5, statistical inference and the sample average approximation method
  - paper: doi:10.1109/TIT.2011.2182178
    title: Alekh Agarwal, Peter L. Bartlett, Pradeep Ravikumar and Martin J. Wainwright, Information-theoretic lower bounds on the oracle complexity of stochastic convex optimization, IEEE Transactions on Information Theory 58(5), 2012
    locator: pages 3235 to 3249, lower bounds of order 1/√k for convex and 1/k for strongly convex objectives
  - paper: doi:10.1007/s10107-022-01822-7
    title: Yossi Arjevani, Yair Carmon, John C. Duchi, Dylan J. Foster, Nathan Srebro and Blake Woodworth, Lower bounds for non-convex stochastic optimization, Mathematical Programming 199, 2023
    locator: pages 165 to 214, the Ω(ε^-4) lower bound for finding an ε-stationary point with a bounded variance oracle
  - paper: doi:10.1137/120880811
    title: Saeed Ghadimi and Guanghui Lan, Stochastic first- and zeroth-order methods for nonconvex stochastic programming, SIAM Journal on Optimization 23(4), 2013
    locator: pages 2341 to 2368, the O(ε^-4) rate of SGD for smooth nonconvex functions
  - paper: doi:10.1007/s10107-010-0434-y
    title: Guanghui Lan, An optimal method for stochastic composite optimization, Mathematical Programming 133, 2012
    locator: pages 365 to 397, the accelerated stochastic approximation method with the rate L R^2/k^2 + σ R/√k
  - paper: doi:10.1109/TIT.2004.833339
    title: Nicolò Cesa-Bianchi, Alex Conconi and Claudio Gentile, On the generalization ability of on-line learning algorithms, IEEE Transactions on Information Theory 50(9), 2004
    locator: pages 2050 to 2057, the conversion of a regret bound into a bound on the expected risk
  - paper: doi:10.1214/aoms/1177729586
    title: Herbert Robbins and Sutton Monro, A stochastic approximation method, Annals of Mathematical Statistics 22(3), 1951
    locator: pages 400 to 407, root finding from noisy observations
  - url: https://arxiv.org/abs/1109.5647
    title: Alexander Rakhlin, Ohad Shamir and Karthik Sridharan, Making gradient descent optimal for strongly convex stochastic optimization, ICML 2012
    locator: Section 3 for the log k loss of the plain average, Section 4 for suffix averaging
---

Stochastic optimization is the problem of minimizing a function $F(x) = \mathbb{E}_\xi[f(x, \xi)]$ that is an [expected value](/expected-value/) over a random variable $\xi$, when the distribution of $\xi$ is known only through samples. An algorithm gets one sample at a time, or equivalently a noisy but unbiased estimate of the [gradient](/gradient/) $\nabla F(x)$. The cost is the number of samples, and the noise sets the limit: for [convex](/convex-function/) $F$ the best possible accuracy after $k$ samples is of order $1/\sqrt{k}$, and $1/k$ under strong convexity. Training a model on fresh data from a population is the main example.

## In plain words

You want to set a dial so that the average outcome of a random process is as good as possible, but you can only watch single outcomes, and each one is noisy. Each observation hints at which way to turn the dial, but the hint can be wrong.

The question is how many observations you need to get close to the best setting. With noise, the error cannot shrink faster than roughly one over the square root of the number of observations, because that is how fast an average of noisy numbers settles down.

## Definition

Notation: $n$ is the number of variables, $k$ the number of oracle calls, and $\varepsilon$ the target accuracy.

**Input.** A closed convex set $X \subseteq \mathbb{R}^n$ (possibly $\mathbb{R}^n$), a random variable $\xi$ with an unknown distribution, and a function $f(x, \xi)$ such that $F(x) = \mathbb{E}f(x, \xi)$ is finite on $X$. Access is through a **stochastic first-order oracle**: on a query $x$ it draws a fresh independent $\xi$ and returns $f(x, \xi)$ and a vector $G(x, \xi)$ with

$$\mathbb{E}\,G(x, \xi) = \nabla F(x) \quad (\text{or } \in \partial F(x)), \qquad \mathbb{E}\lVert G(x, \xi) - \nabla F(x)\rVert^2 \le \sigma^2 \quad \text{or} \quad \mathbb{E}\lVert G(x, \xi)\rVert^2 \le G^2.$$

**Output.** A random point $\hat{x} \in X$, computed from $k$ oracle calls, with

- $\mathbb{E}F(\hat{x}) - F^* \le \varepsilon$ when $F$ is convex, where $F^* = \inf_XF$, or
- $\mathbb{E}\lVert\nabla F(\hat{x})\rVert^2 \le \varepsilon^2$ when $F$ is smooth and nonconvex.

The **sample complexity** is the smallest $k$ that achieves this for every problem in a class (for example, convex with $\mathbb{E}\lVert G\rVert^2 \le G^2$ and $\lVert x_0 - x^*\rVert \le R$).

## Variants

- **Sample average approximation (SAA).** Draw $N$ samples once, minimize $\frac{1}{N}\sum_if(x, \xi_i)$ with a deterministic method, and study how close its minimizer is to that of $F$ (Shapiro, Dentcheva and Ruszczyński 2014). The inner problem is [finite-sum minimization](/finite-sum-minimization/).
- **Stochastic approximation (SA).** Use each sample once, in an iterative method such as [stochastic gradient descent](/stochastic-gradient-descent/). Nemirovski, Juditsky, Lan and Shapiro (2009) showed that SA with averaging matches SAA in sample complexity at a much lower cost.
- **Online optimization.** The functions $f(\cdot, \xi_t)$ may be chosen by an adversary, and the measure is the [regret](/regret/) ([online convex optimization](/online-convex-optimization/)).
- **High probability.** Ask for $F(\hat{x}) - F^* \le \varepsilon$ with probability $1 - \delta$; this costs a factor $\log(1/\delta)$ for light-tailed noise.
- **Zeroth order.** The oracle returns only $f(x, \xi)$; gradients are estimated from differences, at a cost that grows with $n$.
- **Root finding.** Find $x$ with $M(x) = \mathbb{E}\,Y(x) = 0$ from noisy observations $Y(x)$, which is the setting of the [Robbins-Monro algorithm](/robbins-monro-algorithm/). Stationary points of $F$ are roots of $\nabla F$.

## Examples

**Estimating a mean.** Let $f(x, \xi) = \frac{1}{2}(x - \xi)^2$ with $\mathbb{E}\xi = m$ and $\operatorname{Var}\xi = s^2$. Then $F(x) = \frac{1}{2}(x - m)^2 + \frac{1}{2}s^2$, $x^* = m$ and $F^* = s^2/2$. The oracle returns $G = x - \xi$, with variance $s^2$. Stochastic gradient descent with the step $1/(k+1)$ gives

$$x_{k+1} = x_k - \frac{1}{k+1}(x_k - \xi_{k+1}) = \frac{1}{k+1}\sum_{j=1}^{k+1}\xi_j,$$

the running mean, whatever $x_0$ is. So $\mathbb{E}F(x_k) - F^* = \frac{1}{2}\mathbb{E}(x_k - m)^2 = s^2/(2k)$. This is the rate $\sigma^2/(\mu k)$ of the strongly convex class with $\mu = 1$, and for Gaussian $\xi$ no estimator from $k$ samples can do better than $s^2/(2k)$ for all $m$.

**Newsvendor.** Order $x$ units at cost $c$ each; demand $D$ is random and each sold unit brings $p > c$. Minimize $F(x) = \mathbb{E}[cx - p\min(x, D)]$. A subgradient is $c - p\,\mathbb{1}[D > x]$, so $F'(x) = c - p\Pr(D > x)$, and $x^*$ is the $(1 - c/p)$-quantile of $D$. With $c = 1$ and $p = 4$, $x^*$ is the $0.75$-quantile. The objective is convex but not smooth or strongly convex in general.

**Population risk of a linear model.** For data $(a, b)$ from a population and the [logistic loss](/logistic-loss/) $f(x, (a, b)) = \log(1 + e^{-b\langle a, x\rangle})$, $F$ is the expected loss on new data. One example gives an unbiased gradient. This is the problem that [empirical risk minimization](/empirical-risk-minimization/) approximates with a fixed sample.

## Known algorithms

| method | assumptions | guarantee after $k$ samples |
|---|---|---|
| [SGD](/stochastic-gradient-descent/) with averaging, step $R/(G\sqrt{k})$ | convex, $\mathbb{E}\lVert G\rVert^2 \le G^2$ | $GR/\sqrt{k}$ |
| SGD with step $2/(\mu(j + j_0))$ | $\mu$-strongly convex, $L$-smooth, variance $\sigma^2$ | $\mathbb{E}\lVert x_k - x^*\rVert^2 = O(\sigma^2/(\mu^2k))$ |
| stochastic [mirror descent](/mirror-descent/) | convex, non-Euclidean geometry | $G\sqrt{2D/(\sigma k)}$ in the matching norm |
| accelerated stochastic approximation (Lan 2012) | convex, $L$-smooth, variance $\sigma^2$ | $O(LR^2/k^2 + \sigma R/\sqrt{k})$ |
| SGD for nonconvex $F$ (Ghadimi and Lan 2013) | $L$-smooth, variance $\sigma^2$ | $\min_j\mathbb{E}\lVert\nabla F(x_j)\rVert^2 = O(\sqrt{L\Delta}\sigma/\sqrt{k} + L\Delta/k)$ |
| [Robbins-Monro](/robbins-monro-algorithm/) | strongly monotone root problem | mean-square convergence with steps $\sum a_k = \infty$, $\sum a_k^2 < \infty$ |
| [AdaGrad](/adagrad/), [Adam](/adam/) | as SGD; adaptive per-coordinate steps | AdaGrad: regret $O(\sqrt{k})$; Adam: see its page |
| SAA plus a deterministic solver | as SGD | the same statistical rate, at a higher cost |

In the nonconvex row, $\Delta = F(x_0) - \inf F$.

## Bounds

- **Convex.** Over problems with $\mathbb{E}\lVert G\rVert^2 \le G^2$ and $\lVert x_0 - x^*\rVert \le R$, the best guarantee after $k$ oracle calls is $\Theta(GR/\sqrt{k})$. SGD with averaging attains it, and Agarwal, Bartlett, Ravikumar and Wainwright (2012) prove the matching information-theoretic lower bound. Smoothness does not help the noise term: the lower bound $\Omega(\sigma R/\sqrt{k})$ remains, and the accelerated method of Lan (2012) is optimal in both terms.
- **Strongly convex.** The best guarantee is $\Theta(G^2/(\mu k))$ (Agarwal et al. 2012). SGD with steps of order $1/(\mu j)$ and a suitable average attains it; the plain average of all iterates loses a factor $\log k$ (Rakhlin, Shamir and Sridharan 2012).
- **Nonconvex.** For smooth $F$ and an oracle with variance $\sigma^2$, finding a point with $\mathbb{E}\lVert\nabla F\rVert \le \varepsilon$ needs $\Theta(\varepsilon^{-4})$ oracle calls in the worst case: SGD attains it (Ghadimi and Lan 2013), and Arjevani et al. (2023) prove the lower bound. If each sample $f(\cdot, \xi)$ is smooth in mean square, the bound improves to $\Theta(\varepsilon^{-3})$, attained by variance-reduced methods.
- **Against the deterministic case.** Without noise, convex smooth problems need only $O(1/\sqrt{\varepsilon})$ gradient calls ([first-order lower bound](/first-order-lower-bound/)). The noise term dominates as soon as $\varepsilon$ is small.

## Reductions

- **Online to batch.** Any online algorithm with regret $\mathcal{R}_k$ on the losses $f(\cdot, \xi_1), \dots, f(\cdot, \xi_k)$ gives $\mathbb{E}F(\bar{x}_k) - F^* \le \mathcal{R}_k/k$ for the average $\bar{x}_k$ of its iterates (Cesa-Bianchi, Conconi and Gentile 2004). So online gradient descent and [AdaGrad](/adagrad/) solve stochastic optimization.
- **To finite sums.** Sample average approximation replaces $F$ by an empirical average, and the statistical error is added to the optimization error.
- **From root finding.** Stochastic optimization of a smooth $F$ is root finding for $\nabla F$ from noisy observations, which is the problem of [stochastic approximation](/stochastic-approximation/).

## Applications

- Training machine learning models on streams of data or on a large population.
- Adaptive filters, such as the least mean squares filter, which runs SGD on a squared error.
- Inventory and revenue problems such as the newsvendor, and simulation-based optimization.
- Policy optimization in reinforcement learning, where returns are noisy samples.
- Portfolio selection with a random return model.

## References
