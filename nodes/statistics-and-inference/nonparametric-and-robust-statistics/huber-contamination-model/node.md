---
tag: PNPD11
kind: model
slug: huber-contamination-model
name: Huber contamination model
aliases:
- epsilon-contamination model
- gross error model
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: The data come from (1 - epsilon) F + epsilon G, where F is the model and G is an arbitrary distribution of outliers. Robust estimators are judged on it.
history:
  year: 1964
  people: [Peter J. Huber]
  note: Huber introduced the gross error neighbourhood of the normal law in 1964 and found the M-estimator that minimizes the maximum asymptotic variance over it.
prereqs: [estimator, total-variation-distance, empirical-distribution-function]
see_also: [breakdown-point, influence-function, huber-m-estimator, median, m-estimator, robust-mean-estimation-filter, minimum-covariance-determinant, robust-model-fitting]
sources:
  - paper: doi:10.1214/aoms/1177703732
    title: Peter J. Huber, Robust estimation of a location parameter, The Annals of Mathematical Statistics 35(1), 1964
    locator: pp. 73 to 101 (the gross error model, the least favourable distribution and the minimax M-estimator)
  - book: isbn:9780470129906
    title: Peter J. Huber and Elvezio M. Ronchetti, Robust Statistics, second edition, Wiley, 2009
    locator: Chapter 4 (the minimax approach for location, the minimax bias of the median, the least favourable density and the minimax variance)
  - book: isbn:9780471829218
    title: Frank R. Hampel, Elvezio M. Ronchetti, Peter J. Rousseeuw and Werner A. Stahel, Robust Statistics, The Approach Based on Influence Functions, Wiley, 1986
    locator: Chapter 1 (neighbourhoods of a model) and Chapter 2 (the one-dimensional location problem)
  - paper: doi:10.1137/17M1126680
    title: Ilias Diakonikolas, Gautam Kamath, Daniel M. Kane, Jerry Li, Ankur Moitra and Alistair Stewart, Robust estimators in high dimensions without the computational intractability, SIAM Journal on Computing 48(2), 2019
    locator: pp. 742 to 864 (the strong contamination model and the filter for the mean of a Gaussian)
  - paper: doi:10.1109/FOCS.2016.76
    title: Kevin A. Lai, Anup B. Rao and Santosh Vempala, Agnostic estimation of mean and covariance, FOCS 2016
    locator: pp. 665 to 674 (polynomial-time estimators with an error that grows only as the square root of log d)
  - book: isbn:9781108837811
    title: Ilias Diakonikolas and Daniel M. Kane, Algorithmic High-Dimensional Robust Statistics, Cambridge University Press, 2023
    locator: Chapter 1 (contamination models and the information-theoretic limits) and Chapter 2 (efficient robust mean estimation)
---

The Huber contamination model says that a fraction $1 - \varepsilon$ of the data follows a model $F$ and a fraction $\varepsilon$ follows an unknown law $G$ of outliers. Robust statistics uses it as the yardstick for an [estimator](/estimator/): how much can the outliers move the estimate, and how much variance does the estimate lose? The model is due to Huber (1964). It is the base of the [breakdown point](/breakdown-point/), of the [influence function](/influence-function/) and of the [Huber M-estimator](/huber-m-estimator/).

## The machine

Fix a parametric model $\{F_\theta : \theta \in \Theta\}$ on $\mathbb{R}$ or $\mathbb{R}^d$ and a contamination fraction $0 \le \varepsilon < 1/2$. The data $X_1, \ldots, X_n$ are independent with the law

$$P = (1 - \varepsilon) F_\theta + \varepsilon G,$$

where $G$ is any probability law. The statistician knows the family $F_\theta$ and the value of $\varepsilon$ (or an upper bound on it). The statistician does not know $\theta$ or $G$. The set of all such $P$ is the gross error neighbourhood

$$\mathcal{P}_\varepsilon(F_\theta) = \{(1 - \varepsilon) F_\theta + \varepsilon G : G \text{ a probability law}\}.$$

A sampling view is useful. For each $i$, toss a coin with heads probability $\varepsilon$. On tails, draw $X_i$ from $F_\theta$. On heads, draw $X_i$ from $G$. The number of outliers is then Binomial$(n, \varepsilon)$, and the outliers do not depend on the clean points.

Two stronger models are in common use.

- **Total variation contamination.** $P$ is any law with $d_{TV}(P, F_\theta) \le \varepsilon$ (see [total variation distance](/total-variation-distance/)). The adversary can also remove mass from $F_\theta$, not only add it. Each Huber neighbourhood is inside the total variation ball of the same radius, because $d_{TV}((1-\varepsilon)F + \varepsilon G, F) = \varepsilon\, d_{TV}(G, F) \le \varepsilon$.
- **Strong (adaptive) contamination.** Draw $n$ clean points from $F_\theta$. An adversary sees them and replaces any $\lfloor \varepsilon n \rfloor$ of them with arbitrary points. This is the model of the finite-sample [breakdown point](/breakdown-point/) and of the [filter](/robust-mean-estimation-filter/).

## What it counts

The model measures an estimator $T$ by its worst case over the neighbourhood. Write $T(P)$ for the value of the functional at the law $P$ (the limit of $T(X_1, \ldots, X_n)$ as $n$ grows) and take $\theta$ fixed.

- **Maximum bias.** $b_T(\varepsilon) = \sup_G |T((1-\varepsilon)F_\theta + \varepsilon G) - \theta|$. The asymptotic breakdown point is the smallest $\varepsilon$ with $b_T(\varepsilon) = \infty$.
- **Maximum asymptotic variance.** $v_T(\varepsilon) = \sup_G V(T, (1-\varepsilon)F_\theta + \varepsilon G)$, where $V(T, P)$ is the variance of the limit law of $\sqrt n\,(T_n - T(P))$. Huber's minimax problem asks for the $T$ with the least $v_T(\varepsilon)$.
- **Error in high dimension.** For a mean in $\mathbb{R}^d$, the count is $\|\hat\mu - \mu\|_2$ as a function of $\varepsilon$, $d$ and $n$, and the running time of the estimator.

Bias is the effect that more data cannot remove. Variance shrinks like $1/n$, but the bias stays. So for large $n$ the bias term decides.

## Relation to other models

- **The classical model** is the case $\varepsilon = 0$. Every efficient estimator in it, such as the sample mean for $F_\theta = N(\theta, 1)$, has $b(\varepsilon) = \infty$ for every $\varepsilon > 0$: one point mass $G = \delta_x$ with $x \to \infty$ moves the mean by $\varepsilon x$.
- **The influence function** is the derivative of $T((1-t)F + t\delta_x)$ at $t = 0$. It is the first-order picture of this model for small $\varepsilon$ and a point mass $G$.
- **The breakdown point** is the largest $\varepsilon$ that the model can carry before the bias is unbounded.
- **Total variation and strong contamination** contain the Huber model, as shown above. Most results below hold in all three models with the same rates.
- **Mixture models.** The law $(1-\varepsilon)F + \varepsilon G$ is a two-part mixture, as in a [Gaussian mixture model](/gaussian-mixture-model/). The difference is that $G$ has no shape here, so a likelihood fit of $G$ is not possible.
- **Computer vision** uses the same idea with a large outlier fraction, often above one half, and solves it by sampling, as in [RANSAC](/ransac/) and [robust model fitting](/robust-model-fitting/).

## Known results in the model

**1. Identifiability (proved here).** Let $F$ and $F'$ have densities $f$ and $f'$ (with respect to any common measure), and let $0 < \varepsilon < 1$. Then there are laws $G$ and $G'$ with
$$(1 - \varepsilon) F + \varepsilon G = (1 - \varepsilon) F' + \varepsilon G'$$
if and only if $d_{TV}(F, F') \le \varepsilon/(1-\varepsilon)$.

*Proof.* Write $\delta = d_{TV}(F, F') = \int (f' - f)^+ = \int (f - f')^+$. Suppose that $\delta \le \varepsilon/(1-\varepsilon)$. Let $r$ be any density with total mass $1 - \frac{1-\varepsilon}{\varepsilon}\delta \ge 0$, and put
$$g = \tfrac{1-\varepsilon}{\varepsilon}(f' - f)^+ + r, \qquad g' = \tfrac{1-\varepsilon}{\varepsilon}(f - f')^+ + r.$$
Both are densities of mass 1. Then $(1-\varepsilon) f + \varepsilon g = (1-\varepsilon)(f + (f'-f)^+) + \varepsilon r = (1-\varepsilon)\max(f, f') + \varepsilon r$, and the same holds for the right side. For the converse, the equality gives $(1-\varepsilon)(f' - f) = \varepsilon (g - g') \le \varepsilon g$. On the set where $f' > f$ this gives $(1-\varepsilon)(f'-f)^+ \le \varepsilon g$. Integrate: $(1-\varepsilon)\delta \le \varepsilon$. $\square$

So no estimator can tell $\theta$ from $\theta'$ when $d_{TV}(F_\theta, F_{\theta'}) \le \varepsilon/(1-\varepsilon)$, even with infinite data. The worst-case error of any functional $T$ is at least half the largest such gap $|\theta - \theta'|$, because $T$ takes one value at the common law, and that value is at distance at least $|\theta - \theta'|/2$ from $\theta$ or from $\theta'$.

**2. The median is minimax for the bias at the normal (proved here).** Take $F_\theta = N(\theta, 1)$, so $d_{TV}(F_0, F_\Delta) = 2\Phi(\Delta/2) - 1$. Result 1 gives the lower bound $b(\varepsilon) \ge \Delta^*/2$ with $2\Phi(\Delta^*/2) - 1 = \varepsilon/(1-\varepsilon)$, that is
$$b(\varepsilon) \ge \Phi^{-1}\!\Big(\frac{1}{2(1-\varepsilon)}\Big) \quad \text{for every functional } T.$$
The [median](/median/) attains this bound. Put all of $G$ at $+\infty$. The median $m$ of $P$ then solves $(1-\varepsilon)\Phi(m) = 1/2$, so $m = \Phi^{-1}(1/(2(1-\varepsilon)))$. For any other $G$, $P(X \le m) \ge (1-\varepsilon)\Phi(m) = 1/2$, so the median of $P$ is at most $m$. By symmetry it is at least $-m$. So the maximum bias of the median is exactly the lower bound. Huber (1964) gave this result. The values are:

| $\varepsilon$ | 0.05 | 0.10 | 0.20 | 0.25 | 0.30 | 0.40 | 0.45 |
|---|---|---|---|---|---|---|---|
| $b(\varepsilon)$ | 0.0660 | 0.1397 | 0.3186 | 0.4307 | 0.5659 | 0.9674 | 1.3352 |

The bias is about $1.25\,\varepsilon$ for small $\varepsilon$ (the slope is $\sqrt{2\pi}/2$, the gross-error sensitivity of the median) and tends to infinity as $\varepsilon \to 1/2$.

**3. Huber's minimax variance (cited, not proved here).** Take $F = \Phi$ and symmetric contamination $G$. Among M-estimators of location, the one with the least maximum asymptotic variance over $\mathcal{P}_\varepsilon(\Phi)$ has $\psi_k(x) = \max(-k, \min(k, x))$, where $k$ solves
$$\frac{2\varphi(k)}{k} - 2\Phi(-k) = \frac{\varepsilon}{1-\varepsilon}.$$
The least favourable law has the density $(1-\varepsilon)\varphi(x)$ for $|x| \le k$ and $(1-\varepsilon)\varphi(k)e^{-k(|x|-k)}$ for $|x| > k$: normal in the middle, exponential in the tails. The estimator is the maximum likelihood estimator for this law. A script that solves the equation by bisection gives:

| $\varepsilon$ | 0.01 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|
| $k$ | 1.945 | 1.398 | 1.140 | 0.862 |

The common choice $k = 1.345$ comes from a different rule (95 percent efficiency at the normal) and fits $\varepsilon \approx 0.06$. See the [Huber M-estimator](/huber-m-estimator/) for the computation.

**4. High dimension (cited).** For $F = N(\mu, I_d)$, the best error that any estimator can get is $\Theta(\varepsilon)$, independent of $d$, with $n$ of order $(d + \log(1/\tau))/\varepsilon^2$ samples for failure probability $\tau$. The [Tukey median](/tukey-median/) gets $O(\varepsilon)$, but it is hard to compute. Simple estimators lose a factor that grows with $d$: the coordinatewise median and the [geometric median](/geometric-median/) have error of order $\varepsilon\sqrt d$. In 2016 two papers gave the first polynomial-time estimators with an error that does not grow polynomially in $d$. Diakonikolas, Kamath, Kane, Li, Moitra and Stewart get $O(\varepsilon\sqrt{\log(1/\varepsilon)})$ with the [filter](/robust-mean-estimation-filter/). Lai, Rao and Vempala get an error with a $\sqrt{\log d}$ factor.

**5. The fraction one half.** For $\varepsilon \ge 1/2$ the model cannot identify a location: $G = F_{\theta'}$ makes $(1-\varepsilon)F_\theta + \varepsilon F_{\theta'}$ with $\varepsilon = 1/2$ symmetric in $\theta$ and $\theta'$. So every translation equivariant estimator has breakdown point at most one half. The [breakdown point](/breakdown-point/) page proves the finite-sample form of this bound.

## References
