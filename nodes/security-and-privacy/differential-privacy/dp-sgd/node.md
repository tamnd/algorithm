---
tag: X5S7AN
kind: algorithm
slug: dp-sgd
name: Differentially private stochastic gradient descent
aliases:
- DP-SGD
- noisy SGD with clipping
area: security-and-privacy/differential-privacy
level: advanced
summary: "Clips each example's gradient to a fixed norm, adds Gaussian noise to the sum of a random batch, and tracks the privacy cost of training."
model: real-ram
complexity:
  vars: {T: the number of steps, n: the number of examples, d: the number of parameters}
  time: {worst: O(T n d)}
  space: {extra: O(d)}
properties: {deterministic: false, randomized: true}
history:
  year: 2016
  people: [Martín Abadi, Andy Chu, Ian Goodfellow, H. Brendan McMahan, Ilya Mironov, Kunal Talwar, Li Zhang]
  note: "Abadi et al. trained deep networks with per-example clipping and Gaussian noise at ACM CCS 2016, and introduced the moments accountant. Noisy SGD for private learning goes back to Song, Chaudhuri and Sarwate (2013) and Bassily, Smith and Thakurta (2014)."
prereqs: [stochastic-gradient-descent, gaussian-mechanism, moments-accountant, privacy-amplification-by-subsampling]
see_also: [renyi-differential-privacy, gradient-clipping, logistic-regression, objective-perturbation, output-perturbation, pate, membership-inference-attack, numerical-privacy-accounting]
sources:
  - url: "https://arxiv.org/abs/1607.00133"
    title: "Martín Abadi, Andy Chu, Ian Goodfellow, H. Brendan McMahan, Ilya Mironov, Kunal Talwar and Li Zhang, Deep learning with differential privacy, ACM CCS 2016, pages 308 to 318"
    locator: "Algorithm 1 and Theorem 1 (Section 3.1), the moments accountant and its Theorem 2 (Section 3.2), and the example with q = 0.01, sigma = 4, delta = 1e-5 and 10000 steps"
  - url: "https://arxiv.org/abs/1908.10530"
    title: "Ilya Mironov, Kunal Talwar and Li Zhang, Renyi differential privacy of the sampled Gaussian mechanism, arXiv 1908.10530, 2019"
    locator: "Theorem 4 (Section 2, the reduction to one dimension), the quantities A_alpha and B_alpha and Theorem 5 (Section 3.1), and the computation at integer orders"
  - paper: doi:10.1109/GlobalSIP.2013.6736861
    title: "Shuang Song, Kamalika Chaudhuri and Anand D. Sarwate, Stochastic gradient descent with differentially private updates, IEEE GlobalSIP 2013, pages 245 to 248"
    locator: the noisy stochastic gradient update with a bounded gradient and its privacy
  - paper: "Raef Bassily, Adam Smith and Abhradeep Thakurta, Private empirical risk minimization: efficient algorithms and tight error bounds, IEEE FOCS 2014, pages 464 to 473"
    locator: the noisy stochastic gradient method for private convex empirical risk minimization and its excess risk bounds
  - paper: "Ilya Mironov, Renyi differential privacy, IEEE Computer Security Foundations Symposium 2017"
    locator: the composition of Renyi DP and its conversion to (epsilon, delta)-DP
---

Differentially private stochastic gradient descent (DP-SGD) trains a model so that the trained parameters are $(\varepsilon, \delta)$-differentially private with respect to each training example. At each step it samples a random batch, computes the gradient of each example on its own, clips each gradient to a fixed norm $C$, sums them, and adds Gaussian noise with standard deviation $\sigma C$. Clipping bounds the effect of one example, the noise hides it, and the random batch amplifies the privacy ([privacy amplification by subsampling](/privacy-amplification-by-subsampling/)). An accountant then adds up the privacy cost of all steps. Abadi et al. (2016) introduced this form and the [moments accountant](/moments-accountant/), and trained deep networks with it. It is the standard method for private deep learning.

## In plain words

Normal training looks at a batch of examples, finds the direction that improves the model on them, and takes a small step. One unusual example can pull the model far toward itself, and the model may then remember that example.

DP-SGD limits the pull of each example. It measures how hard each example pulls, and cuts every pull down to a fixed limit. Then it adds random noise to the total pull, large enough to hide any one example. The batch itself is picked at random, so an observer does not even know which examples took part in each step.

A privacy ledger counts how much each step leaks. More steps or less noise give a larger total leak.

## The problem

The data is a multiset $D$ of $n$ examples, and $\ell(\theta, x)$ is the loss of the model with parameters $\theta \in \mathbb R^d$ on example $x$. The goal is a $\theta$ with a small average loss, such that the whole sequence of parameters is $(\varepsilon, \delta)$-[DP](/approximate-differential-privacy/). The neighbor relation is add/remove: $D'$ is $D$ with one example added or removed. The loss may be non-convex, and it may have no bound on its gradient; clipping makes the bound.

## The algorithm

The inputs are the rate $q \in (0, 1]$, the noise multiplier $\sigma > 0$, the clipping norm $C > 0$, the step size $\eta$ and the number of steps $T$.

```pseudo id=main
DP-SGD(D, q, sigma, C, eta, T)
L1  theta <- theta_0
L2  for t = 1 to T do
L3      B <- each example of D, independently with probability q      ▷ Poisson sampling
L4      for each x in B: g_x <- grad of loss(theta, x)
L5      clip: g_x <- g_x / max(1, |g_x| / C)                          ▷ now |g_x| <= C
L6      G <- (sum over x in B of g_x) + N(0, sigma^2 C^2 I)
L7      theta <- theta - eta G / (q n)                                ▷ q n is the expected batch size
L8  return theta
```

Line L3 draws the batch by Poisson sampling: each example joins with probability $q$, on its own. The size of the batch is random, with mean $qn$. Line L4 computes one gradient per example, not one gradient of the batch. Line L5 scales each gradient down to the norm $C$ if it is longer. Line L6 sums the clipped gradients and adds Gaussian noise in every coordinate. Adding or removing one example changes the sum by a vector of norm at most $C$, so this is the [Gaussian mechanism](/gaussian-mechanism/) with the sensitivity $C$ on a random sample. Line L7 takes a step with the noisy average. It divides by the fixed number $qn$, not by the size of the batch, which is private.

The accountant computes the privacy of the $T$ steps. For an integer order $\alpha \ge 2$, one step is $(\alpha, \rho_\alpha)$-[Renyi DP](/renyi-differential-privacy/) with

$$\rho_\alpha = \frac{1}{\alpha - 1} \ln \sum_{k=0}^{\alpha} \binom{\alpha}{k} (1 - q)^{\alpha - k} q^k \exp\!\left(\frac{k^2 - k}{2\sigma^2}\right),$$

the bound of Mironov, Talwar and Zhang for the sampled Gaussian. $T$ steps give $T\rho_\alpha$. The result is $(\varepsilon, \delta)$-DP with $\varepsilon = \min_\alpha \big(T\rho_\alpha + \ln(1/\delta)/(\alpha - 1)\big)$. The code computes the sum in log space and takes the minimum over the orders 2 to 256. Other accountants use the same steps with a sharper conversion; see [numerical privacy accounting](/numerical-privacy-accounting/).

The code trains logistic regression so that it needs no library, and it uses floats and a seeded generator. That shows the algorithm but is not a safe deployment: the analysis assumes real-valued Gaussian noise and exact Poisson sampling, and floating-point samplers can leak (Mironov 2012). A deployment needs a cryptographic source of randomness and a sampler built for DP, such as the [discrete Gaussian](/discrete-gaussian-mechanism/).

## Example

**One step.** Take logistic regression in the plane with $\theta = (0, 0)$, four examples, $q = 1/2$, $\sigma = 1$, $C = 1$ and $\eta = 0.5$. At $\theta = 0$ the gradient of the logistic loss of $(x, y)$ is $-yx/2$.

| example | $x$, $y$ | $g_x$ (line L4) | $\lvert g_x \rvert$ | clipped (line L5) | in $B$ (line L3) |
|---|---|---|---|---|---|
| 1 | (2, 1), +1 | (-1, -0.5) | 1.118 | (-0.8944, -0.4472) | yes |
| 2 | (0.5, -1), -1 | (0.25, -0.5) | 0.559 | (0.25, -0.5) | no |
| 3 | (-3, 0), -1 | (-1.5, 0) | 1.5 | (-1, 0) | yes |
| 4 | (1, 1), +1 | (-0.5, -0.5) | 0.7071 | (-0.5, -0.5) | yes |

The sum over the batch is $(-2.3944, -0.9472)$. Suppose line L6 draws the noise $(0.31, -1.20)$. Then $G = (-2.0844, -2.1472)$, and line L7 gives $\theta = -0.5 \cdot G / 2 = (0.5211, 0.5368)$. The noise is as large as the signal here; with thousands of examples per batch it is small against the sum.

**The privacy of training.** The accountant of the code gives these values for $\delta = 10^{-5}$.

| $q$ | $\sigma$ | $T$ | $\varepsilon$ | best order $\alpha$ |
|---|---|---|---|---|
| 1 | 2 | 1 | 2.5263 | 11 |
| 0.01 | 1.0 | 1000 | 2.5383 | 8 |
| 0.01 | 1.0 | 10000 | 7.4692 | 4 |
| 0.01 | 1.1 | 10000 | 6.2798 | 5 |
| 0.01 | 2 | 10000 | 2.7354 | 10 |
| 0.01 | 4 | 10000 | 1.2586 | 20 |

The last row is the example of Abadi et al.: they report $\varepsilon \approx 1.26$ with the moments accountant, against about 9.34 with the strong composition theorem. The first row is the Gaussian mechanism with no sampling, where $\rho_\alpha = \alpha/8$. The best real order gives 2.5243, so the integer orders lose very little.

## Correctness

**Theorem (privacy).** For every integer $\alpha \ge 2$, each step is $(\alpha, \rho_\alpha)$-RDP under add/remove, $T$ steps are $(\alpha, T\rho_\alpha)$-RDP, and the output is $(\varepsilon, \delta)$-DP for the $\varepsilon$ above.

The proof has three parts. First, clipping bounds the change of the sum by $C$. Second, the joint convexity of $\int p^\alpha q^{1 - \alpha}$ reduces the sampled Gaussian in $d$ dimensions to the mixture $(1 - q)\mathcal N(0, \sigma^2) + q\mathcal N(1, \sigma^2)$ on the line, whose divergence the binomial sum computes exactly. Third, Renyi DP composes by adding, and Markov's inequality converts it. The direction from $D$ to $D \cup \{x\}$ needs a further fact, that the other mixture divergence is smaller, which is Theorem 5 of Mironov, Talwar and Zhang. The correctness proof of this page proves every step except that one, which it quotes.

**Theorem (Abadi et al., Theorem 1).** There are constants $c_1, c_2$ such that for $\varepsilon < c_1 q^2 T$, the noise $\sigma \ge c_2\, q\sqrt{T \ln(1/\delta)}/\varepsilon$ gives $(\varepsilon, \delta)$-DP. So $\varepsilon$ grows like $q\sqrt T$, not like $qT$.

**What is not proved.** Nothing above says that the model is accurate. For convex losses, Bassily, Smith and Thakurta (2014) bound the excess risk of noisy SGD. For deep networks, the accuracy is measured. The clipping norm $C$ and the other settings are tuned, and their choice is a heuristic.

## Complexity

The model is the [real RAM](/real-ram/), with one Gaussian sample counted as $O(1)$.

- **One step.** Line L3 makes $n$ coin flips. Lines L4 and L5 cost $O(d)$ for each example of the batch, and the batch has $qn$ examples on average and $n$ at most. Line L6 costs $O(d)$ for the noise and line L7 costs $O(d)$. So a step costs $O(n d)$ in the worst case and $O(n + qnd)$ on average.
- **Training.** $T$ steps cost $O(T n d)$ in the worst case. The extra space is $O(d)$ for the sum and the noise.
- **Accountant.** One order costs $O(\alpha)$, so all orders up to $\alpha_{\max}$ cost $O(\alpha_{\max}^2)$, which does not depend on $n$ or $d$.
- **In practice.** The cost of per-example gradients is the main overhead in deep learning frameworks, since a normal step computes only the batch gradient.

## Properties

- **Any loss.** The privacy proof does not need convexity or a bound on the gradient: clipping makes the bound. This is why DP-SGD works for deep networks.
- **All steps are released.** The theorem covers the whole sequence of parameters, so the intermediate models may be published. Releasing only the last model can leak less, but the theorem above does not show that.
- **Bias from clipping.** Clipping changes the gradient when many examples have norms above $C$, so DP-SGD does not minimize the true loss in general. A small $C$ means less noise relative to the signal, but more bias.
- **The neighbor relation.** The accountant above is for add/remove with Poisson sampling. Under replace, one example changes the sum by up to $2C$, and the bounds change.
- **Utility costs.** For a fixed $\varepsilon$, a larger batch rate $q$ needs fewer steps per epoch but more noise per step. The trade-off is tuned, not proved.

## Variants and improvements

- **Other accountants.** The moments accountant of Abadi et al. computes the same log moments at integer orders. Numerical accountants based on the privacy loss distribution, and the bound of Gaussian DP, give tighter values of $\varepsilon$ for the same training.
- **Per-layer clipping and adaptive clipping.** Clip each layer to its own norm, or set $C$ from a private quantile of the gradient norms during training.
- **Private convex optimization.** For convex losses with a bounded gradient, noisy SGD reaches the optimal excess risk (Bassily, Smith and Thakurta 2014). [Objective perturbation](/objective-perturbation/) and [output perturbation](/output-perturbation/) are other private methods for convex ERM.
- **Public data.** Pretraining on public data and private fine-tuning with DP-SGD often gives much better accuracy. [PATE](/pate/) is a different route, which uses public unlabeled data.
- **Federated learning.** The same clip and noise steps can run per user, not per example, so that the guarantee protects all the data of one user.

## When to use it

Use DP-SGD to train a model on sensitive data held by a trusted curator, when the model is a neural network or another model with a non-convex loss. For a convex model with a bounded loss gradient, objective perturbation can give better accuracy for the same $\varepsilon$. When public unlabeled data from the same distribution exists, PATE may be a better choice. Report the neighbor relation, the sampling method, $\varepsilon$, $\delta$ and the accountant with the model.

## Pitfalls

- **Clipping the batch gradient.** Line L5 applied to the sum, after line L6 or in place of the per-example clip, does not bound the effect of one example by $C$, and the noise of line L6 is then too small for the claimed $\varepsilon$. Line L5 must clip each gradient of line L4 before the sum.
- **Noise without the norm.** Line L6 with noise $\mathcal N(0, \sigma^2 I)$ in place of $\mathcal N(0, \sigma^2 C^2 I)$ gives the claimed privacy only when $C = 1$. The standard deviation must be $\sigma C$.
- **Shuffled batches with a Poisson accountant.** Line L3 replaced by fixed-size batches from a shuffle of the data is common in code, but the accountant above assumes Poisson sampling. Chua et al. (2024) showed that the gap can be large. Line L3 must match the sampling that the accountant assumes.
- **Dividing by the batch size.** Line L7 with the true size $|B|$ in place of $qn$ uses a private number that the noise of line L6 does not cover. Divide by the fixed $qn$.
- **Tuning on the private data.** Running many trainings with different $C$, $\eta$ or $\sigma$ and keeping the best one leaks more than one training. The tuning must be counted in the budget or done on public data.
- **Float samplers.** Lines L3 and L6 with `random()` and a float Gaussian, as in this code, do not give the exact distributions of the analysis. A deployment must use samplers built for DP.

## Implementations

## History

Song, Chaudhuri and Sarwate (2013) studied SGD with differentially private updates for convex learning. Bassily, Smith and Thakurta (FOCS 2014) analyzed noisy SGD for private empirical risk minimization and proved optimal excess risk bounds, using amplification by subsampling and advanced composition. Abadi, Chu, Goodfellow, McMahan, Mironov, Talwar and Zhang (CCS 2016) added per-example clipping for deep networks and the moments accountant, which gave much smaller values of $\varepsilon$ than the composition theorems. Mironov (2017) defined Renyi differential privacy, and Mironov, Talwar and Zhang (2019) gave the exact Renyi bound of the sampled Gaussian at integer orders, which libraries now use.

## References
