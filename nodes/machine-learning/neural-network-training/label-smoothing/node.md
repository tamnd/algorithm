---
tag: 6Q5BPV
kind: technique
slug: label-smoothing
name: Label smoothing
area: machine-learning/neural-network-training
level: advanced
summary: "Train a classifier on the target (1 - ε) y + ε/K instead of the one-hot label y. This adds ε times a cross-entropy to the uniform distribution and keeps the logits bounded."
prereqs: [cross-entropy-loss, softmax-regression, regularization]
see_also: [knowledge-distillation, focal-loss, data-augmentation, dropout, multiclass-classification, shannon-entropy, overfitting, weight-decay]
sources:
  - paper: doi:10.1109/CVPR.2016.308
    title: Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe, Jonathon Shlens and Zbigniew Wojna, Rethinking the Inception architecture for computer vision, CVPR 2016
    locator: Section 7 (model regularization via label smoothing, H(q', p) = (1 - ε) H(q, p) + ε H(u, p), ε = 0.1 with K = 1000 on ImageNet)
  - url: https://arxiv.org/abs/1906.02629
    title: Rafael Müller, Simon Kornblith and Geoffrey Hinton, When does label smoothing help?, NeurIPS 2019
    locator: Section 2 (the penultimate layer representations form tight clusters), Section 3 (calibration), Section 4 (teachers trained with label smoothing give worse students in knowledge distillation)
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 7.5.1 (injecting noise at the output targets, the targets ε/(k - 1) and 1 - ε)
---

Label smoothing (Szegedy, Vanhoucke, Ioffe, Shlens and Wojna, 2016) is a [regularization](/regularization/) method for classifiers trained with the [cross-entropy loss](/cross-entropy-loss/). Instead of the one-hot label $y$ of an example among $K$ classes, the target is $q' = (1 - \varepsilon)\, y + \varepsilon\, u$, where $u$ is the uniform distribution, $u_j = 1/K$. The true class gets $1 - \varepsilon + \varepsilon/K$ and every other class gets $\varepsilon/K$. Because the cross-entropy is linear in the target, the new loss is $(1 - \varepsilon) H(y, p) + \varepsilon H(u, p)$: the usual loss plus a penalty that pulls the predicted distribution $p$ toward the uniform one. With a one-hot target, the loss keeps falling as the logit of the true class grows without bound; with label smoothing the minimum is at a finite logit gap of $\log\big((1 - \varepsilon + \varepsilon/K)/(\varepsilon/K)\big)$. Szegedy et al. used $\varepsilon = 0.1$ on ImageNet with $K = 1000$.

## In plain words

A classifier is usually told that the right class has probability one and every other class has probability zero. To get close to this, it must make its scores more and more extreme, and it becomes too sure of itself. Label smoothing tells it a softer truth: the right class has most of the probability, say 90%, and the rest is spread evenly over all classes. The classifier can now reach its goal with scores of a moderate size, so it stops pushing them to extremes. Its stated confidence is closer to how often it is right. The cost is that it learns less about which wrong classes are close to the right one.

## When it applies

- **Problem.** [Multiclass classification](/multiclass-classification/) with a softmax output and the cross-entropy loss, where the model can fit the training labels almost perfectly and becomes overconfident.
- **Part of the training loop.** The targets of the loss. The model and the optimizer are unchanged.
- **Typical values.** $\varepsilon$ between 0.05 and 0.2; 0.1 is common for image classification and machine translation.
- **Not for** a teacher whose soft outputs will be used for [knowledge distillation](/knowledge-distillation/) (see Pitfalls).

## The template

Notation: $z \in \mathbb{R}^K$ are the logits of one example, $p = \operatorname{softmax}(z)$, and $c$ is the index of the true class.

```pseudo id=template
LABEL-SMOOTHED-LOSS(z, c, ε)
L1  for j ← 1 to K: q'_j ← ε / K
L2  q'_c ← q'_c + (1 − ε)
L3  s ← log Σ_j exp(z_j)                     ▷ computed with the max subtracted
L4  loss ← Σ_j q'_j (s − z_j)                ▷ = H(q', softmax(z))
L5  ∂loss/∂z ← softmax(z) − q'
```

**Cost.** $\Theta(K)$ per example, the same as the plain cross-entropy. The smoothed target never has to be stored for all classes: $\sum_j q'_j(s - z_j) = (1 - \varepsilon)(s - z_c) + \frac{\varepsilon}{K}\sum_j (s - z_j)$.

### The decomposition of the loss

**Claim 1.** For any distribution $p$ with positive entries,

$$H(q', p) = (1 - \varepsilon)\, H(y, p) + \varepsilon\, H(u, p), \qquad H(u, p) = D_{\mathrm{KL}}(u \,\|\, p) + \log K .$$

*Proof.* $H(q, p) = -\sum_j q_j \log p_j$ is linear in $q$, and $q' = (1 - \varepsilon) y + \varepsilon u$. For the second identity, $D_{\mathrm{KL}}(u\|p) = \sum_j u_j \log(u_j/p_j) = -\log K + H(u, p)$, and $\log K$ is the [entropy](/shannon-entropy/) of $u$. $\blacksquare$

So label smoothing is the cross-entropy with weight $1 - \varepsilon$ plus a penalty $\varepsilon\, D_{\mathrm{KL}}(u\|p)$ on the distance of the prediction from the uniform distribution, up to a constant. Szegedy et al. (Section 7) state the first identity.

### The gradient and the minimizer

**Claim 2.** The gradient of $H(q', \operatorname{softmax}(z))$ with respect to $z$ is $p - q'$. Its minimizers over $z$ are exactly the $z$ with $p = q'$, which are $z_j = \log q'_j + b$ for any constant $b$; there the gap between the logit of the true class and any other logit is

$$z_c - z_j = \log\frac{1 - \varepsilon + \varepsilon/K}{\varepsilon/K} = \log\Big(1 + \frac{K(1 - \varepsilon)}{\varepsilon}\Big).$$

*Proof.* $H(q', \operatorname{softmax}(z)) = \log\sum_j e^{z_j} - \sum_j q'_j z_j$, since $\sum_j q'_j = 1$. The derivative of the first term in $z_k$ is $p_k$ and of the second is $q'_k$. The function is convex in $z$, so its minimizers are its stationary points, $p = q'$. The softmax is unchanged by adding a constant to all logits, which gives the form $\log q'_j + b$ and the gap. $\blacksquare$

With $\varepsilon = 0$ the gradient on the true class is $p_c - 1 < 0$ for every finite $z$, so gradient descent on a training set that it can separate pushes the logit gaps to infinity. With $\varepsilon > 0$ the gap has a finite target; for $K = 1000$ and $\varepsilon = 0.1$ it is $\log 9001 \approx 9.105$, and for $K = 3$ the ratio is $(0.9 + 1/30)/(1/30) = 28$, so the gap is $\log 28 \approx 3.332$.

## Classic examples

**Exact losses in bits.** Take $K = 4$, $\varepsilon = 0.1$ and the prediction $p = (1/2, 1/4, 1/8, 1/8)$. Then $H(u, p) = (1 + 2 + 3 + 3)/4 = 9/4$ bits and $D_{\mathrm{KL}}(u\|p) = 9/4 - 2 = 1/4$ bit.

| true class | $H(y, p)$ in bits | $H(q', p)$ in bits |
|---|---|---|
| 1 | 1 | $0.9 \cdot 1 + 0.1 \cdot 9/4 = 9/8$ |
| 2 | 2 | $81/40$ |
| 3 or 4 | 3 | $117/40$ |

The penalty raises the loss of a confident correct prediction and lowers that of a confident wrong one.

**Bounded logits in a linear model.** Six points in the plane in three classes, separable by a linear softmax model, trained by full-batch gradient descent with step size 0.5. Without smoothing, the smallest logit gap on the training points grows from 3.11 after 100 steps to 5.32 after 1000 and 6.86 after 5000, and keeps growing. With $\varepsilon = 0.1$ the gaps settle between 2.89 and 3.40 after about 1000 steps, close to the target $\log 28 \approx 3.33$ of Claim 2.

**Image classification.** Szegedy et al. report a gain of about 0.2 percentage points in top-1 and top-5 error on ImageNet with $\varepsilon = 0.1$.

## Variations

- **Confidence penalty.** Subtract $\beta$ times the entropy of $p$ from the loss. Since $H(p) = \log K - D_{\mathrm{KL}}(p\|u)$, this penalizes $D_{\mathrm{KL}}(p\|u)$, the reverse direction of Claim 1.
- **Non-uniform smoothing.** Replace $u$ by a prior over the classes, such as the class frequencies, or by the predictions of another model, which leads to [knowledge distillation](/knowledge-distillation/).
- **Online or adaptive smoothing,** which changes $\varepsilon$ during training or per example.
- **Mixup** ([data augmentation](/data-augmentation/)) also trains on soft targets, made by mixing the labels of two examples.

## Pitfalls

- **Two conventions for $\varepsilon$.** Some texts, such as Goodfellow et al. (Section 7.5.1), give $1 - \varepsilon$ to the true class and $\varepsilon/(K - 1)$ to each other class. This is the template with $\varepsilon K/(K - 1)$ in place of $\varepsilon$. For $K = 2$ the difference is a factor of 2.
- **It can hurt distillation.** Müller, Kornblith and Hinton (2019) show that label smoothing makes the representations of the examples of one class cluster tightly and roughly equally far from all other classes. The logits then carry less information about which wrong classes are similar, and a teacher trained with label smoothing gives a worse student, even when the teacher itself is more accurate.
- **Probabilities are not the training targets.** A model trained with smoothing never predicts more than $1 - \varepsilon + \varepsilon/K$ at the minimum. Smoothing often improves calibration (Müller et al., Section 3), but the outputs should still be checked on validation data before they are used as probabilities.
- **Applying it twice.** Soft targets from mixup or from a teacher are already smooth; smoothing them again changes their meaning.
- **The loss value is not comparable.** With $\varepsilon > 0$ the smallest possible loss is the entropy of $q'$, not zero, so training curves with and without smoothing cannot be compared directly.

## Exercises

1. Show that $\min_p H(q', p) = H(q')$, and compute it for $K = 10$ and $\varepsilon = 0.1$.
2. Show that the Hessian of $H(q', \operatorname{softmax}(z))$ in $z$ is $\operatorname{diag}(p) - p p^\top$, independent of $\varepsilon$, and conclude that the loss is convex in $z$ but not strictly convex.
3. For the convention with $\varepsilon/(K - 1)$ on each wrong class, compute the optimal logit gap and compare it with Claim 2.
4. For binary classification with a sigmoid output, write the smoothed target and show that the optimal logit is $\log\big((1 - \varepsilon/2)/(\varepsilon/2)\big)$.
5. A model predicts $p$ with $p_c = 0.99$ on a training example. Compute the gradient of the smoothed loss with $K = 10$ and $\varepsilon = 0.1$, and show that it pushes $p_c$ down.

## References
