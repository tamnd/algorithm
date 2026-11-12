---
tag: 0EGAS8
kind: definition
slug: cross-entropy-loss
name: Cross-entropy loss
aliases:
- log loss
- softmax cross-entropy
- categorical cross-entropy
area: machine-learning/supervised-learning
level: intro
summary: "The negative log probability that a categorical model gives the true label. It is cross-entropy against the one-hot label, and its gradient in the logits is p - y."
prereqs: [loss-function, shannon-entropy]
see_also: [logistic-loss, softmax-regression, maximum-likelihood-estimation, label-smoothing, focal-loss, knowledge-distillation, mean-squared-error]
sources:
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 4.1 (overflow and underflow, the stable softmax), Section 5.5 (maximum likelihood and cross-entropy) and Section 6.2.2.3 (softmax units for multinoulli outputs)
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 4.3.4 (multiclass logistic regression, the cross-entropy error and its gradient)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 2 (entropy, relative entropy, and the information inequality D(p||q) >= 0)
---

The cross-entropy loss of a classifier that outputs a probability vector $p$ over $k$ classes is $-\log p_y$, the negative log probability of the true label $y$. It is the negative log likelihood of a categorical model, and it equals the cross-entropy $H(q, p)$ between the one-hot label $q$ and $p$. When $p$ is the softmax of a score vector $z$, the loss is $\operatorname{LSE}(z) - z_y$ and its gradient in $z$ is $p - q$. It is the standard loss of [softmax regression](/softmax-regression/) and of neural network classifiers; its two-class case is the [logistic loss](/logistic-loss/).

## Definition

**Setting.** Labels lie in $[k] = \{1, \ldots, k\}$. A model maps an input $x$ to a score vector (logits) $z = f_\theta(x) \in \mathbb{R}^k$ and to the probabilities

$$p_j = \operatorname{softmax}(z)_j = \frac{e^{z_j}}{\sum_{i=1}^{k} e^{z_i}}, \qquad j \in [k].$$

**The loss.** For a target distribution $q$ on $[k]$ (a one-hot vector $q = e_y$ in ordinary classification),

$$\ell(z, q) = -\sum_{j=1}^{k} q_j \log p_j, \qquad \ell(z, y) = -\log p_y = \operatorname{LSE}(z) - z_y, \qquad \operatorname{LSE}(z) = \log \sum_{i=1}^{k} e^{z_i}.$$

On $n$ examples the empirical risk is $L(\theta) = \frac1n \sum_{i=1}^{n} \ell(f_\theta(x_i), y_i)$. With the natural logarithm the unit is the nat; divide by $\ln 2$ for bits.

**It is the negative log likelihood.** The categorical model says $P(y = j \mid x) = p_j(x; \theta)$. The likelihood of independent labels is $\prod_i p_{y_i}(x_i; \theta)$, so $-\frac1n \log$ of it is exactly $L(\theta)$. Minimizing the cross-entropy loss is [maximum likelihood estimation](/maximum-likelihood-estimation/) of $\theta$.

**It is a cross-entropy.** For distributions $q$ and $p$ on $[k]$, the cross-entropy is $H(q, p) = -\sum_j q_j \log p_j$. With the [Shannon entropy](/shannon-entropy/) $H(q) = -\sum_j q_j \log q_j$ and the Kullback-Leibler divergence $\mathrm{KL}(q \,\|\, p) = \sum_j q_j \log (q_j / p_j)$,

$$H(q, p) = H(q) + \mathrm{KL}(q \,\|\, p).$$

The proof is one line: add and subtract $\sum_j q_j \log q_j$. Since $\mathrm{KL}(q \,\|\, p) \ge 0$ with equality only at $p = q$ (Gibbs' inequality, from Jensen's inequality for $-\log$), the expected loss under the true conditional law $q$ is smallest at $p = q$. So the log loss is a strictly proper scoring rule (see [loss function](/loss-function/)). For a one-hot $q$, $H(q) = 0$ and the loss equals the KL divergence. In coding terms, $H(q, p)$ is the mean length per symbol of a code built for $p$ and used on data from $q$.

**The gradient is $p - q$.** For $q$ with $\sum_j q_j = 1$,

$$\ell(z, q) = \operatorname{LSE}(z) - \sum_j q_j z_j, \qquad \frac{\partial \operatorname{LSE}}{\partial z_j} = \frac{e^{z_j}}{\sum_i e^{z_i}} = p_j, \qquad \text{so} \qquad \nabla_z \ell = p - q.$$

The Hessian is $\nabla_z^2 \ell = \operatorname{diag}(p) - p p^\top$, the covariance matrix of the one-hot vector under $p$. It is positive semidefinite, so $\ell$ is [convex](/convex-function/) in $z$, and for a linear model $z = Wx$ it is convex in $W$, with $\nabla_W \ell = (p - q)\, x^\top$. It is not strictly convex in $z$: adding the same constant to every $z_j$ leaves $p$ and $\ell$ unchanged. In a neural network the vector $p - q$ is the error signal that [backpropagation](/backpropagation/) sends into the last layer.

**Stable computation.** $e^{z_j}$ overflows a double for $z_j > 709.78$, and a tiny $p_y$ rounds to 0, so $\log p_y = -\infty$. The fix uses the shift identity $\operatorname{LSE}(z) = m + \log \sum_i e^{z_i - m}$ for any $m$. With $m = \max_i z_i$ every exponent is at most 0, at least one term equals 1, and the sum lies in $[1, k]$, so it neither overflows nor underflows to 0. Compute the loss as $\operatorname{LSE}(z) - z_y$ from the logits, never as $-\log$ of a rounded softmax output. Libraries take logits for this reason.

## Examples and non-examples

**A worked example.** Take $k = 3$, $z = (2, 1, 0.1)$. Then $\operatorname{LSE}(z) = 2.4170$ and $p = (0.6590, 0.2424, 0.0986)$.

- For $y = 1$ (the first class) the loss is $2.4170 - 2 = 0.4170$ nats, or $0.6016$ bits. The gradient is $p - e_1 = (-0.3410, 0.2424, 0.0986)$: a gradient step raises $z_1$ and lowers the other scores, in proportion to their probabilities.
- For $y = 3$ the loss is $2.4170 - 0.1 = 2.3170$ nats.
- A model that outputs $z = (0, 0, 0)$ has $p$ uniform and loss $\ln 3 = 1.0986$ for every label. This is the loss to beat.

**Soft targets.** With $q = (0.7, 0.2, 0.1)$ and the same $z$, $H(q, p) = 0.8070$, $H(q) = 0.8018$ and $\mathrm{KL}(q \,\|\, p) = 0.0052$. Soft targets appear in [label smoothing](/label-smoothing/) and in [knowledge distillation](/knowledge-distillation/).

**Overflow.** For $z = (1000, 0)$ the naive formula computes $e^{1000}$, which is infinite in double precision, and returns NaN. The shifted form gives $\operatorname{LSE}(z) = 1000 + \log(1 + e^{-1000}) = 1000$, so the loss is $0$ for $y = 1$ and $1000$ for $y = 2$.

**Non-example: a zero probability.** If a model outputs $p_y = 0$ for the true label, the loss is $+\infty$. A softmax output is never exactly 0 in exact arithmetic, but a model that outputs probabilities directly (for example a histogram) must clip or smooth them.

**Non-example: the reversed arguments.** $H(p, q) = -\sum_j p_j \log q_j$ is a different quantity, and with a one-hot $q$ it is infinite whenever $p$ puts mass off the label. The loss is always $H(\text{target}, \text{model})$.

**Non-example: multilabel targets.** When an input can have several labels at once, the softmax is the wrong model, because it forces the probabilities to sum to 1. Use one [logistic loss](/logistic-loss/) per label instead (often called binary cross-entropy).

**Non-example: squared error on probabilities.** $\sum_j (p_j - q_j)^2$ is the Brier score, also proper, but bounded by 2. Its gradient in $z$ vanishes when $p$ is confidently wrong, which slows the training of a softmax model; the cross-entropy gradient $p - q$ does not vanish there.

## Related definitions

- [Logistic loss](/logistic-loss/): the case $k = 2$, with the score $f = z_2 - z_1$.
- [Softmax regression](/softmax-regression/): the linear model $z = Wx + b$ fitted by minimizing this loss.
- [Shannon entropy](/shannon-entropy/): $H(q)$, the smallest value of $H(q, p)$ over $p$.
- [Maximum likelihood estimation](/maximum-likelihood-estimation/): the general principle that this loss implements.
- [Label smoothing](/label-smoothing/): replaces $e_y$ by a mix of $e_y$ and the uniform distribution.
- [Focal loss](/focal-loss/): multiplies $-\log p_y$ by $(1 - p_y)^\gamma$ to down-weight easy examples.
- [Mean squared error](/mean-squared-error/): the loss of the Gaussian model, as this is the loss of the categorical model.

## References
