---
tag: XQYJDD
kind: definition
slug: logistic-loss
name: Logistic loss
aliases:
- logit loss
- binary cross-entropy
- binomial deviance
area: machine-learning/supervised-learning
level: intro
summary: "The margin loss log(1 + exp(-y f)) for labels in {-1, +1}. It equals binary cross-entropy with labels in {0, 1}, is convex and smooth, and its minimizer is the log-odds."
prereqs: [loss-function, cross-entropy-loss]
see_also: [logistic-regression, hinge-loss, softmax-regression, convex-function, smoothness, gradient-descent, stochastic-gradient-descent, boosting]
sources:
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Section 9.3 (logistic regression and the loss log(1 + exp(-y w.x))) and Chapter 12 (convex, Lipschitz and smooth losses)
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 4.3.2 (logistic regression, the cross-entropy error with targets in {0, 1}) and Section 7.1.2 (the same error written for targets in {-1, +1})
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 10.6 (binomial deviance as a margin loss) and Section 12.3.2 (Table 12.1, its minimizing function is the log-odds)
  - paper: doi:10.1198/016214505000000907
    title: Peter L. Bartlett, Michael I. Jordan and Jon D. McAuliffe, Convexity, classification, and risk bounds, Journal of the American Statistical Association 101(473), 138-156, 2006
    locator: the logistic loss as a classification calibrated convex loss
---

The logistic loss of a real score $f$ for a label $y \in \{-1, +1\}$ is $\ell(y, f) = \log(1 + e^{-y f})$. With labels $t = (y + 1)/2 \in \{0, 1\}$ and the probability $\sigma(f) = 1/(1 + e^{-f})$ it is exactly the binary [cross-entropy](/cross-entropy-loss/) $-t \log \sigma(f) - (1 - t) \log(1 - \sigma(f))$. It is convex and smooth in $f$, its gradient in a linear model is Lipschitz with constant $\lVert x \rVert^2 / 4$, and its conditional risk is minimized by the log-odds, so it is both classification calibrated and a proper loss for probabilities. This page is about the loss; the model that minimizes it is [logistic regression](/logistic-regression/).

## Definition

**Margin form.** For $y \in \{-1, +1\}$ and a score $f = f(x) \in \mathbb{R}$,

$$\ell(y, f) = \log\big(1 + e^{-y f}\big) = \varphi(y f), \qquad \varphi(m) = \log(1 + e^{-m}).$$

The logarithm is natural. On $n$ examples the empirical risk is $L(\theta) = \frac1n \sum_i \ell(y_i, f_\theta(x_i))$.

**Probability form, and the change of variables.** Put $t = (y + 1)/2$, so $y = +1 \leftrightarrow t = 1$ and $y = -1 \leftrightarrow t = 0$, and use $1 - \sigma(f) = \sigma(-f)$. Then

- if $y = +1$ ($t = 1$): $-\log \sigma(f) = \log(1 + e^{-f}) = \ell(+1, f)$;
- if $y = -1$ ($t = 0$): $-\log(1 - \sigma(f)) = -\log \sigma(-f) = \log(1 + e^{f}) = \ell(-1, f)$.

So $\ell(y, f) = -t \log \sigma(f) - (1 - t) \log(1 - \sigma(f))$ in both cases. It is also $-\log \sigma(y f)$: the negative log likelihood of the Bernoulli model $P(y \mid x) = \sigma(y f(x))$. As a two-class cross-entropy with logits $(z_1, z_2)$, the score is $f = z_2 - z_1$.

**Derivative.** $\frac{d}{dm}\varphi(m) = -\frac{e^{-m}}{1 + e^{-m}} = -\sigma(-m)$, so

$$\frac{\partial \ell}{\partial f} = -y\, \sigma(-y f) = \sigma(f) - t, \qquad \frac{\partial^2 \ell}{\partial f^2} = \sigma(f)\big(1 - \sigma(f)\big).$$

The second form of the first derivative follows from the two cases above. For a linear score $f = w \cdot x$ the chain rule gives $\nabla_w \ell = (\sigma(w \cdot x) - t)\, x$ and $\nabla_w^2 \ell = \sigma(1 - \sigma)\, x x^\top$.

**Convexity and smoothness.** Let $s = \sigma(f) \in (0, 1)$. Then $0 < s(1 - s) \le \frac14$, because $\frac14 - s(1 - s) = (s - \frac12)^2 \ge 0$, with equality only at $f = 0$. Hence:

- $\ell$ is strictly convex in $f$, and convex in $w$, since $\nabla_w^2 \ell = s(1 - s)\, x x^\top \succeq 0$.
- $\nabla_w^2 \ell \preceq \frac14 x x^\top$, and $v^\top x x^\top v \le \lVert x \rVert^2 \lVert v \rVert^2$. By the mean value theorem on $\nabla_w \ell$ along a segment, the gradient is Lipschitz: $\lVert \nabla_w \ell(w_1) - \nabla_w \ell(w_2) \rVert \le \frac{\lVert x \rVert^2}{4} \lVert w_1 - w_2 \rVert$. The constant $\frac14$ is attained at $f = 0$, so it cannot be improved.
- For the empirical risk, $\nabla^2 L(w) \preceq \frac{1}{4n} X^\top X$, so $L$ is [smooth](/smoothness/) with constant $\lambda_{\max}(X^\top X)/(4n) \le \frac{1}{4n}\sum_i \lVert x_i \rVert^2$. [Gradient descent](/gradient-descent/) with step $\eta = 1/\text{that constant}$ decreases $L$ at each step.
- $\lvert \partial \ell / \partial f \rvert < 1$, so $\ell$ is 1-Lipschitz in $f$: one outlier can change the gradient by at most $\lVert x \rVert$. The squared loss has no such bound.
- $\ell$ is *not* strongly convex: $s(1 - s) \to 0$ as $\lvert f \rvert \to \infty$. On linearly separable data $L(w) > 0$ for every $w$ but $\inf_w L = 0$, so no minimizer exists and the norm of the iterates grows without bound. A penalty $\frac{\lambda}{2}\lVert w \rVert^2$ fixes this.

**Conditional risk.** With $\eta = P(y = 1 \mid x)$, the conditional risk $\eta\,\varphi(\alpha) + (1 - \eta)\,\varphi(-\alpha)$ has derivative $\sigma(\alpha) - \eta$, which is zero at $\alpha^* = \log\frac{\eta}{1 - \eta}$, the log-odds. Its sign is the sign of $2\eta - 1$, so the loss is classification calibrated, and $\sigma(\alpha^*) = \eta$, so the fitted score gives a probability. Convexity, differentiability at 0 and $\varphi'(0) = -\frac12 < 0$ give calibration by the convex criterion of Bartlett, Jordan and McAuliffe (see [loss function](/loss-function/)).

**Stable computation.** Write $\operatorname{softplus}(u) = \log(1 + e^{u})$, so $\ell(y, f) = \operatorname{softplus}(-y f)$. For any real $u$,

$$\operatorname{softplus}(u) = \max(u, 0) + \operatorname{log1p}\big(e^{-\lvert u \rvert}\big),$$

because for $u > 0$, $\log(1 + e^{u}) = u + \log(e^{-u} + 1)$. The exponent is never positive, so nothing overflows, and $\operatorname{log1p}$ keeps the digits of a tiny argument. In the $\{0, 1\}$ form compute $\operatorname{softplus}(f) - t f$, never $\log$ of a rounded $\sigma(f)$. Compute $\sigma(f)$ as $1/(1 + e^{-f})$ for $f \ge 0$ and as $e^{f}/(1 + e^{f})$ for $f < 0$.

## Examples and non-examples

**Values.** At $f = 0$ the loss is $\log 2 = 0.6931$ for either label. At $f = 2$ it is $\log(1 + e^{-2}) = 0.1269$ for $y = +1$ and $\log(1 + e^{2}) = 2.1269$ for $y = -1$. The derivatives there are $-\sigma(-2) = -0.1192$ and $+\sigma(2) = 0.8808$: the wrong label pushes much harder.

**Large scores.** For $f = 800$ and $y = -1$, the naive formula computes $e^{800}$, which overflows a double (Python raises `OverflowError`, C returns infinity). The stable form gives $800 + \operatorname{log1p}(e^{-800}) = 800$. For $f = 40$ and $y = +1$, the naive formula returns $\log(1 + 4.25 \times 10^{-18}) = \log 1 = 0$, because $1 + 4.25 \times 10^{-18}$ rounds to 1. The stable form returns $\operatorname{log1p}(e^{-40}) = 4.25 \times 10^{-18}$, the right value.

**A data set.** Let $x_1 = (1, 2)$, $x_2 = (1, -1)$, $x_3 = (1, 0.5)$ with labels $+1, -1, -1$ (the first feature is a constant). The bound gives the smoothness constant $\frac{1}{12}(5 + 2 + 1.25) = 0.6875$, so gradient descent with $\eta = 1/0.6875 \approx 1.45$ is safe. The points are separable by the second feature at any threshold in $(0.5, 2)$, so the infimum $0$ is not attained.

**Non-example: $\{0, 1\}$ labels in the margin form.** If $y = 0$ is passed to $\log(1 + e^{-y f})$, the loss is $\log 2$ for every $f$ and its gradient is 0, so those examples teach the model nothing. This is a common bug when a library expects $\pm 1$ and the data has $0/1$.

**Non-example: other scalings.** Allwein, Schapire and Singer (2000) write the logistic loss as $\log(1 + e^{-2z})$, and the binomial deviance in ESL Section 10.6 is $\log(1 + e^{-2yf})$ for a score $f$ that is half the log-odds. These are the same loss after $f \mapsto 2f$; the minimizer is then $\frac12 \log\frac{\eta}{1 - \eta}$. Check the convention before you compare numbers.

## Related definitions

- [Cross-entropy loss](/cross-entropy-loss/): the $k$-class version with a softmax; logistic loss is its $k = 2$ case.
- [Hinge loss](/hinge-loss/): another convex calibrated margin loss; it is zero for margins at least 1 and gives no probabilities.
- [Logistic regression](/logistic-regression/): the linear model fitted by minimizing this loss, with or without a penalty.
- [Loss function](/loss-function/): surrogate losses, classification calibration and proper scoring rules.
- [Boosting](/boosting/): LogitBoost and gradient boosting with this loss fit an additive model of the log-odds.

## References
