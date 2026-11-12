---
tag: 12NTY4
kind: definition
slug: hinge-loss
name: Hinge loss
aliases:
- max-margin loss
- squared hinge loss
- multiclass hinge loss
area: machine-learning/supervised-learning
level: intro
summary: "The margin loss max(0, 1 - y f) of support vector machines. It is convex, has a subgradient, and its conditional risk is minimized by sign(2 eta - 1)."
prereqs: [loss-function, subgradient]
see_also: [support-vector-machine, svm-training, logistic-loss, perceptron, multiclass-classification, margin-generalization-bound, stochastic-gradient-descent, subdifferential]
sources:
  - paper: doi:10.1007/BF00994018
    title: Corinna Cortes and Vladimir Vapnik, Support-vector networks, Machine Learning 20(3), 273-297, 1995
    locator: the soft margin hyperplane, whose slack variables equal the hinge loss at the optimum
  - paper: "Yi Lin, Support vector machines and the Bayes rule in classification, Data Mining and Knowledge Discovery 6(3), 259-275, 2002"
    locator: the minimizer of the expected hinge loss is sign(2 eta - 1)
  - paper: "Koby Crammer and Yoram Singer, On the algorithmic implementation of multiclass kernel-based vector machines, Journal of Machine Learning Research 2, 265-292, 2001"
    locator: the multiclass margin loss max(0, 1 + max over j != y of f_j - f_y) and its dual
  - paper: "Jason Weston and Chris Watkins, Support vector machines for multi-class pattern recognition, Proceedings of ESANN 1999, 219-224"
    locator: the multiclass SVM with one slack variable for each wrong class
  - paper: "Ambuj Tewari and Peter L. Bartlett, On the consistency of multiclass classification methods, Journal of Machine Learning Research 8, 1007-1025, 2007"
    locator: which multiclass surrogate losses are classification calibrated
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Chapter 15 (soft-SVM as regularized hinge loss minimization) and Chapter 17 (the generalized hinge loss for multiclass prediction)
---

The hinge loss of a real score $f$ for a label $y \in \{-1, +1\}$ is $\ell(y, f) = \max(0, 1 - y f)$. It is zero when the margin $y f$ is at least 1 and grows linearly below that. It is the loss of the soft-margin [support vector machine](/support-vector-machine/): it is convex, has a simple [subgradient](/subgradient/), and its conditional risk is minimized by $\operatorname{sign}(2\eta - 1)$, the Bayes decision, so it is classification calibrated. Unlike the [logistic loss](/logistic-loss/), its minimizer carries no probability.

## Definition

**Binary hinge loss.** For $y \in \{-1, +1\}$ and a score $f = f(x) \in \mathbb{R}$, with the margin $m = y f$,

$$\ell(y, f) = \max(0, 1 - y f) = (1 - m)_+.$$

It is convex and piecewise linear in $m$, with slope $-1$ for $m < 1$ and slope 0 for $m > 1$, and it is an upper bound of the 0-1 loss $\mathbb{1}[m \le 0]$. The soft-margin SVM minimizes $\frac{\lambda}{2}\lVert w \rVert^2 + \frac1n \sum_{i=1}^{n} \ell(y_i, w \cdot x_i + b)$ over $w$ and $b$.

**Subgradient.** The hinge is convex but not differentiable at $m = 1$. For a linear score $f = w \cdot x$ the [subdifferential](/subdifferential/) in $w$ is

$$\partial_w \ell = \begin{cases} \{-y x\} & \text{if } y\, w \cdot x < 1, \\ \{0\} & \text{if } y\, w \cdot x > 1, \\ \{-c\, y x : c \in [0, 1]\} & \text{if } y\, w \cdot x = 1. \end{cases}$$

Each element $g$ satisfies $\ell(w') \ge \ell(w) + g \cdot (w' - w)$ for all $w'$. A subgradient step on one example moves $w$ toward $y x$ only when the example is inside the margin; this is the update of Pegasos-style [stochastic subgradient](/stochastic-gradient-descent/) SVM training. Compare the [perceptron](/perceptron/), which updates only when $y\, w \cdot x \le 0$.

**Squared hinge.** $\ell_2(y, f) = \max(0, 1 - y f)^2$ is differentiable everywhere, with $\partial \ell_2 / \partial f = -2 y \max(0, 1 - y f)$. Its derivative is continuous and Lipschitz, but its second derivative jumps at $m = 1$. It penalizes large violations more and outliers more.

**The minimizer of the conditional risk is $\operatorname{sign}(2\eta - 1)$.** Fix $x$, let $\eta = P(y = 1 \mid x)$, and let

$$C_\eta(\alpha) = \eta\,(1 - \alpha)_+ + (1 - \eta)\,(1 + \alpha)_+ .$$

*Claim.* For $\eta > \frac12$ the unique minimizer is $\alpha = 1$; for $\eta < \frac12$ it is $\alpha = -1$; for $\eta = \frac12$ the minimizers are $[-1, 1]$. In each case $\min_\alpha C_\eta = 2 \min(\eta, 1 - \eta)$. (At $\eta = 1$ every $\alpha \ge 1$ is optimal, and at $\eta = 0$ every $\alpha \le -1$.)

*Proof.* On $[-1, 1]$ both terms are active, so $C_\eta(\alpha) = 1 + (1 - 2\eta)\alpha$, a linear function. For $\alpha > 1$, $C_\eta(\alpha) = (1 - \eta)(1 + \alpha) \ge 2(1 - \eta) = C_\eta(1)$, strictly if $\eta < 1$. For $\alpha < -1$, $C_\eta(\alpha) = \eta(1 - \alpha) \ge 2\eta = C_\eta(-1)$, strictly if $\eta > 0$. So a minimizer lies in $[-1, 1]$, where the linear function is smallest at $\alpha = 1$ if $1 - 2\eta < 0$, at $\alpha = -1$ if $1 - 2\eta > 0$, and constant if $\eta = \frac12$. The minimum is $1 - \lvert 1 - 2\eta \rvert = 2\min(\eta, 1 - \eta)$. $\blacksquare$

So the hinge loss is classification calibrated (Lin 2002; Bartlett, Jordan and McAuliffe 2006), and its $\psi$-transform is $\psi(\theta) = \lvert \theta \rvert$: the excess 0-1 risk is at most the excess hinge risk. But $\alpha^*$ takes only the values $\pm 1$, so $\eta$ cannot be read back from it. For the squared hinge the same computation on $[-1, 1]$ gives $\alpha^* = 2\eta - 1$, which does determine $\eta$.

**Multiclass forms.** Labels are in $[k]$ and the model gives one score $f_j(x)$ for each class; predict $\arg\max_j f_j$.

- **Weston and Watkins (1999):** $\ell_{\mathrm{WW}}(f, y) = \sum_{j \ne y} \max\big(0, 1 - (f_y - f_j)\big)$. Each wrong class that comes within 1 of the true score adds a term. Weston and Watkins state the margin constraints with the constant 2; dividing all scores by 2 gives this form.
- **Crammer and Singer (2001):** $\ell_{\mathrm{CS}}(f, y) = \max\big(0, 1 + \max_{j \ne y} f_j - f_y\big) = \max_j \big(f_j + \mathbb{1}[j \ne y]\big) - f_y$. Only the strongest wrong class counts.

Both are convex in $f$ and both bound the multiclass 0-1 loss: if the prediction is wrong, some $f_j \ge f_y$ with $j \ne y$, and that term is at least 1. Since each WW term is at most the CS loss, $\ell_{\mathrm{CS}} \le \ell_{\mathrm{WW}} \le (k - 1)\,\ell_{\mathrm{CS}}$. For $k = 2$ both equal the binary hinge of the score difference $f_y - f_{j}$. A subgradient of $\ell_{\mathrm{CS}}$ in $f$ is $e_r - e_y$ with $r$ a maximizer of $f_j + \mathbb{1}[j \ne y]$; for $\ell_{\mathrm{WW}}$ it is $\sum_{j \in A}(e_j - e_y)$ over the set $A$ of active terms. Unlike the binary hinge, neither form is classification calibrated for all distributions when $k \ge 3$ (Tewari and Bartlett 2007).

## Examples and non-examples

**Binary values.** For $y = +1$ and $f = -2, -1, 0, 0.5, 1, 2$ the hinge loss is $3, 2, 1, 0.5, 0, 0$. At $f = 0.5$ the squared hinge is $0.25$ for $y = +1$ and $2.25$ for $y = -1$.

**A subgradient at the kink.** Take $w = (1, 0)$, $x = (1, 2)$, $y = +1$. Then $y\, w \cdot x = 1$, the loss is 0, and every $-c\,(1, 2)$ with $c \in [0, 1]$ is a subgradient, including $0$ (so $w$ may already be optimal for this one example).

**One input with $\eta = 0.7$.** $C_{0.7}(\alpha)$ is $0.6$ at $\alpha = 1$, $1$ at $\alpha = 0$ and $1.4$ at $\alpha = -1$; it is $0.3(1 + \alpha) > 0.6$ for $\alpha > 1$. So $\alpha^* = 1$ and $H(0.7) = 0.6 = 2 \min(0.7, 0.3)$.

**Multiclass.** With scores $f = (1.0, 0.5, 0.8)$ and the true class 1 (the first), the WW loss is $(1 - 0.5)_+ + (1 - 0.2)_+ = 0.5 + 0.8 = 1.3$, and the CS loss is $(1 + 0.8 - 1.0)_+ = 0.8$. The prediction is right, but both losses are positive because the margins are below 1. With $f = (3.2, 5.1, -1.7)$ and the true class 1, the prediction is wrong and both losses equal $2.9$, since only one wrong class is within the margin. With $f = (3, 1, 0.5)$ both are 0.

**Non-example: the perceptron loss.** $\max(0, -y f)$ has no margin term. It is convex but not differentiable at 0, so it is not calibrated, and $f \equiv 0$ minimizes it (see [loss function](/loss-function/)).

**Non-example: the hinge loss with labels $\{0, 1\}$.** With $y = 0$ the loss is the constant 1, so negative examples have no effect. Map labels to $\pm 1$ first.

**Non-example: a probability from an SVM score.** The hinge minimizer is $\pm 1$, so the score $f(x)$ of an SVM is not $\eta(x)$ or a function of it. A probability needs a separate fit on held-out data, for example a sigmoid of the score.

## Related definitions

- [Support vector machine](/support-vector-machine/) and [SVM training](/svm-training/): minimize the hinge loss plus $\frac{\lambda}{2}\lVert w \rVert^2$, in the primal or through the dual.
- [Logistic loss](/logistic-loss/): a smooth calibrated margin loss whose minimizer is the log-odds.
- [Loss function](/loss-function/): surrogate losses, classification calibration and the $\psi$-transform.
- [Margin generalization bound](/margin-generalization-bound/): bounds the 0-1 risk by the empirical rate of margins below $\gamma$, a scaled hinge-like count.
- [Multiclass classification](/multiclass-classification/), [one-vs-rest](/one-vs-rest/) and [one-vs-one](/one-vs-one/): the alternatives to a single multiclass hinge.

## References
