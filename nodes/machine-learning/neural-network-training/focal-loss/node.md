---
tag: 05AH1D
kind: definition
slug: focal-loss
name: Focal loss
area: machine-learning/neural-network-training
level: advanced
summary: "The loss -α_t (1 - p_t)^γ log(p_t): cross-entropy scaled down for examples the model already gets right, so training focuses on hard, rare ones. γ = 0 gives cross-entropy."
prereqs: [cross-entropy-loss, logistic-loss]
see_also: [label-smoothing, loss-function, precision-and-recall, roc-auc, classification, softmax-regression, data-augmentation]
sources:
  - paper: doi:10.1109/ICCV.2017.324
    title: Tsung-Yi Lin, Priya Goyal, Ross Girshick, Kaiming He and Piotr Dollár, Focal loss for dense object detection, ICCV 2017
    locator: Section 3.1 (balanced cross-entropy), Section 3.2 (the definition and the effect of the modulating factor), Section 3.3 (the prior initialization), Section 4.1 (α = 0.25 and γ = 2, the normalization by the number of positive anchors), Appendix B (the derivative in the logit)
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 6.2.2 (sigmoid and softmax output units with the log-likelihood loss)
---

The focal loss (Lin, Goyal, Girshick, He and Dollár, 2017) is a loss for classification that multiplies the [cross-entropy](/cross-entropy-loss/) $-\log p_t$ of each example by the modulating factor $(1 - p_t)^\gamma$, where $p_t$ is the probability that the model gives to the true class and $\gamma \ge 0$ is a focusing parameter. An example that the model already classifies well, with $p_t$ near 1, gets a factor near 0, so its loss and gradient almost vanish; a misclassified example, with $p_t$ small, keeps nearly its full cross-entropy. With $\gamma = 0$ the focal loss is the cross-entropy. It was made for one-stage object detectors, which score about $10^4$ to $10^5$ candidate boxes per image, almost all of them easy background; under the cross-entropy the many small losses of these easy negatives add up to more than the losses of the few real objects.

## Definition

**Binary form.** A model gives a logit $x \in \mathbb{R}$ and the probability $p = \sigma(x) = 1/(1 + e^{-x})$ of the positive class. For a label $y \in \{+1, -1\}$, let

$$p_t = \begin{cases} p & y = +1 \\ 1 - p & y = -1 \end{cases} \;=\; \sigma(y x), \qquad \alpha_t = \begin{cases} \alpha & y = +1 \\ 1 - \alpha & y = -1. \end{cases}$$

The focal loss with focusing parameter $\gamma \ge 0$ and weight $\alpha \in (0, 1)$ is

$$\mathrm{FL}(p_t) = -\alpha_t\, (1 - p_t)^\gamma \log(p_t).$$

The form without $\alpha_t$ (that is, $\alpha_t = 1$) is also called the focal loss. Lin et al. use $\gamma = 2$ and $\alpha = 0.25$ for their RetinaNet detector, and sum the loss over all candidate boxes of an image, divided by the number of boxes assigned to an object.

**The case $\gamma = 0$.** $\mathrm{FL} = -\alpha_t \log p_t$, the $\alpha$-balanced cross-entropy; with $\alpha_t = 1$ it is the [logistic loss](/logistic-loss/) $\log(1 + e^{-y x})$.

**The gradient.** Since $p_t = \sigma(y x)$, $\partial p_t/\partial x = y\, p_t (1 - p_t)$. The chain rule gives

$$\frac{\partial\, \mathrm{FL}}{\partial x} = \alpha_t\, y\, (1 - p_t)^\gamma \big(\gamma\, p_t \log p_t + p_t - 1\big),$$

which is the formula of Lin et al. (Appendix B) with the factor $\alpha_t$. *Derivation:* $\frac{d}{dp_t}\big[-(1 - p_t)^\gamma \log p_t\big] = \gamma (1 - p_t)^{\gamma - 1}\log p_t - (1 - p_t)^\gamma/p_t$, and multiplying by $y p_t (1 - p_t)$ gives $y (1 - p_t)^\gamma(\gamma p_t \log p_t - (1 - p_t))$. For $\gamma = 0$ this is $\alpha_t y (p_t - 1)$, the familiar gradient of the cross-entropy.

**Softmax form.** For logits $z \in \mathbb{R}^K$, $p = \operatorname{softmax}(z)$ and true class $c$, the focal loss is $-(1 - p_c)^\gamma \log p_c$, optionally times a weight $\alpha_c$ per class. With $\partial p_c/\partial z_j = p_c(\delta_{jc} - p_j)$,

$$\frac{\partial\, \mathrm{FL}}{\partial z_j} = \Big(\gamma (1 - p_c)^{\gamma - 1} p_c \log p_c - (1 - p_c)^\gamma\Big)(\delta_{jc} - p_j).$$

For $K = 2$ and $z = (x, 0)$ it is the binary form with $\alpha_t = 1$.

**Computing it.** Compute $\log p_t$ from the logit as $-\log(1 + e^{-y x})$ in a stable form, never as the logarithm of a rounded probability. For $y x = -800$ the loss is then 800, and the gradient is $-y$, as for the cross-entropy, since the factor $(1 - p_t)^\gamma$ is 1 there.

**Properties.**

- *Down-weighting of easy examples.* For $\gamma = 2$, an example with $p_t = 0.9$ has 100 times less loss than under the cross-entropy, since $(1 - 0.9)^2 = 0.01$, and an example with $p_t \approx 0.968$ about 1000 times less, since $0.032^2 = 0.001024$ (Lin et al., Section 3.2).
- *Monotone.* For fixed $\gamma \ge 0$ the loss decreases in $p_t$: both $(1 - p_t)^\gamma$ and $-\log p_t$ are non-negative and decreasing.
- *Not a proper scoring rule for $\gamma > 0$.* If the label is $+1$ with probability $q$, the expected loss $-q(1 - p)^\gamma \log p - (1 - q)p^\gamma \log(1 - p)$ is not minimized at $p = q$. For $q = 0.9$ the minimizer is $p \approx 0.774$ for $\gamma = 1$ and $p \approx 0.694$ for $\gamma = 2$, so the predicted probabilities of a model fitted with the focal loss are pulled toward $1/2$ and are not estimates of $q$. The cross-entropy ($\gamma = 0$) has its minimizer at $p = q$.
- *Prior initialization* (Lin et al., Section 3.3). With many easy negatives, training is unstable at the start if every box begins with $p = 1/2$. This holds for the cross-entropy loss ($\gamma = 0$) as well as for $\gamma > 0$. They set the bias of the last layer to $b = -\log((1 - \pi)/\pi)$ with $\pi = 0.01$, so that every box starts with $p = \pi$. This gives $b \approx -4.595$.

## Examples and non-examples

**Loss values.** For a positive example ($y = +1$, $\alpha_t = 1$):

| $p_t$ | $\gamma = 0$ (cross-entropy) | $\gamma = 1$ | $\gamma = 2$ | $\gamma = 5$ |
|---|---|---|---|---|
| 0.1 | 2.303 | 2.07 | 1.87 | 1.36 |
| 0.5 | 0.693 | 0.347 | 0.173 | 0.0217 |
| 0.9 | 0.105 | 0.0105 | 0.00105 | 0.00000105 |
| 0.968 | 0.0325 | 0.00104 | 0.0000333 | 0.00000000109 |
| 0.99 | 0.0101 | 0.000101 | 0.00000101 | about $10^{-12}$ |

**Gradients.** At $p_t = 0.9$ the derivative in the logit is $-0.1$ for the cross-entropy and $-0.0029$ for $\gamma = 2$. At $p_t = 0.1$ it is $-0.9$ for the cross-entropy and $-1.10$ for $\gamma = 2$: the focal loss gives a hard example a larger gradient than the cross-entropy does, because of the term $\gamma p_t \log p_t$.

**Many easy negatives.** Take one hard positive with $p_t = 0.1$ and 10000 easy negatives with $p_t = 0.99$. Under the cross-entropy the negatives contribute $10000 \cdot 0.01005 = 100.5$ and the positive $2.303$, so the negatives are 98% of the loss. Under the focal loss with $\gamma = 2$ the negatives contribute $10000 \cdot 1.005 \times 10^{-6} = 0.01005$ and the positive $0.81 \cdot 2.303 = 1.865$, more than 99% of the loss.

**Non-example: class weights alone.** The $\alpha$-balanced cross-entropy ($\gamma = 0$) gives every negative the same weight, easy or hard. It changes the balance between the classes, not between easy and hard examples, so the sum over 10000 easy negatives can still dominate.

**Non-example: hard example mining.** Online hard example mining and fixed sampling ratios of positives and negatives select a subset of the examples and drop the rest. The focal loss keeps every example and reweights it smoothly.

**Non-example: [label smoothing](/label-smoothing/).** Label smoothing also stops the model from pushing $p_t$ to 1, but it does so by changing the target, and it penalizes confident correct predictions; the focal loss keeps the one-hot target and only reduces the loss of confident correct predictions.

**Non-example: a calibrated probability.** Since the focal loss is not proper, a predicted $p = 0.7$ from a model trained with $\gamma = 2$ does not mean a 70% chance. If probabilities are needed, they must be recalibrated on held-out data.

## Related definitions

- [Cross-entropy loss](/cross-entropy-loss/): the case $\gamma = 0$, $\alpha_t = 1$; a strictly proper scoring rule.
- [Logistic loss](/logistic-loss/): the binary cross-entropy, in terms of the logit.
- [Loss function](/loss-function/): the general notion, and proper scoring rules.
- [Label smoothing](/label-smoothing/): another change of the cross-entropy that limits confidence.
- [Precision and recall](/precision-and-recall/) and [ROC AUC](/roc-auc/): the measures used for imbalanced detection and classification, where the focal loss is used.
- [Softmax regression](/softmax-regression/): the linear model with the softmax output, to which the softmax form applies.

## References
