---
tag: 96QQ15
kind: algorithm
slug: fast-gradient-sign-method
name: Fast gradient sign method
aliases:
- FGSM
area: security-and-privacy/adversarial-machine-learning
level: intro
summary: "Builds an adversarial example in one step by moving each input coordinate by epsilon in the sign of the loss gradient, then clipping to the valid range."
model: real-ram
complexity:
  vars: {d: the input dimension, g: the cost of one input gradient of the loss}
  time: {worst: O(g + d)}
  space: {extra: Θ(d)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2014
  people: [Ian J. Goodfellow, Jonathon Shlens, Christian Szegedy]
  note: Goodfellow, Shlens and Szegedy posted FGSM in December 2014 (ICLR 2015), together with the linear explanation of adversarial examples and adversarial training with FGSM.
prereqs: [adversarial-example, logistic-regression, gradient-descent]
see_also: [pgd-attack, adversarial-training, evasion-attack, logistic-loss, backpropagation, deepfool, adversarial-transferability, randomized-smoothing]
sources:
  - url: https://arxiv.org/abs/1412.6572
    title: Ian J. Goodfellow, Jonathon Shlens and Christian Szegedy, Explaining and harnessing adversarial examples, ICLR 2015
    locator: Section 3 (the linear explanation), Section 4 (the fast gradient sign method and its error rates on MNIST at epsilon 0.25), Sections 5 and 6 (adversarial training of linear and deep models)
  - url: https://arxiv.org/abs/1607.02533
    title: Alexey Kurakin, Ian Goodfellow and Samy Bengio, Adversarial examples in the physical world, ICLR 2017 workshop
    locator: the basic iterative method and the iterative least-likely class method, which repeat the FGSM step with clipping
  - url: https://arxiv.org/abs/1706.06083
    title: Aleksander Madry, Aleksandar Makelov, Ludwig Schmidt, Dimitris Tsipras and Adrian Vladu, Towards deep learning models resistant to adversarial attacks, ICLR 2018
    locator: the discussion of FGSM as one step of projected gradient ascent on the l_infinity ball
  - url: https://arxiv.org/abs/2001.03994
    title: Eric Wong, Leslie Rice and J. Zico Kolter, Fast is better than free, revisiting adversarial training, ICLR 2020
    locator: FGSM training with a random start, and catastrophic overfitting
  - paper: "Battista Biggio and Fabio Roli, Wild patterns: Ten years after the rise of adversarial machine learning, Pattern Recognition 84, pages 317 to 331, 2018"
    locator: the threat model in three parts used on this page
---

The fast gradient sign method (FGSM) builds an [adversarial example](/adversarial-example/) with one gradient. It computes the gradient $g = \nabla_x L(\theta, x, y)$ of the loss in the input, and moves every coordinate of $x$ by $\epsilon$ in the direction of the sign of $g$: $x' = \operatorname{clip}_{[0,1]}(x + \epsilon \operatorname{sign}(g))$. The step maximizes the first-order model of the loss over the $\ell_\infty$ ball of radius $\epsilon$, so on a linear model it is the exact worst case. Goodfellow, Shlens and Szegedy (2015) proposed it to support their claim that adversarial examples come from the near-linear behavior of networks. FGSM is the one-step special case of the [PGD attack](/pgd-attack/) and the classic inner step of [adversarial training](/adversarial-training/).

**Threat model.** The goal is untargeted (a targeted variant is below). The knowledge is white box: the attacker computes the input gradient of the loss. The capability is a change at test time within $B_\infty(x, \epsilon) \cap [0,1]^d$.

## In plain words

A model gives each input a score of how wrong it is, the loss. The gradient tells, for each part of the input, whether making that part a bit larger raises the loss or lowers it.

FGSM asks this question one time. Then it moves every part of the input by the same small amount, up where that raises the loss and down where it lowers the loss. It does not care how strong the effect of each part is, only its direction. Each part stays in its valid range, for example a pixel stays between black and white.

Many small changes in the same harmful direction add up. In an image with thousands of pixels, a change too small to see can change the answer of the model. FGSM is fast because it needs only one gradient, and it is weak for the same reason.

## The problem

Given a model with loss $L(\theta, x, y)$, an input $x \in [0,1]^d$ with label $y$ and a radius $\epsilon \ge 0$, find $x' \in S = B_\infty(x, \epsilon) \cap [0,1]^d$ with a large loss, ideally $\arg\max_{x' \in S} L(\theta, x', y)$. If the result has a label other than $y$, it is an adversarial example. FGSM solves the linearized problem $\max_{x' \in S} g^\top (x' - x)$ exactly.

## The algorithm

```pseudo id=main
FGSM(L, x, y, epsilon)                      ▷ x in [0, 1]^d with label y
L1  g ← ∇_x L(θ, x, y)                      ▷ one forward and one backward pass
L2  for i ← 1 to d do
L3      v ← x_i + epsilon · sign(g_i)       ▷ sign(0) = 0
L4      x'_i ← min(max(v, 0), 1)            ▷ stay in the valid range
L5  return x'
```

Line L1 is the only call of the model. Lines L2 to L4 work on each coordinate alone: a coordinate with a positive partial derivative goes up by $\epsilon$, one with a negative partial derivative goes down by $\epsilon$, and the clip of line L4 stops it at $0$ or $1$. Because $x_i \in [0,1]$, the clip never moves a coordinate by more than $\epsilon$ from $x_i$, so $x'$ stays in $S$.

For a targeted attack toward class $t$, line L1 takes the gradient of $L(\theta, x, t)$ and line L3 uses $-\epsilon$, so that the loss of the target label goes down.

## Example

Take [logistic regression](/logistic-regression/) with $w = (1.5, -2, 0.5, 1, -0.5, 3)$ and $b = 1$, the [logistic loss](/logistic-loss/) $L = \ln(1 + e^{-z})$ for the label $y = 1$, and $x = (0.2, 0.9, 0.5, 0, 1, 0.4)$ with $\epsilon = 0.1$. The logit is $z = w^\top x + b = 0.45$, so $\sigma(z) = 0.610639$ and $L = 0.493249$. The gradient of line L1 is $g = (\sigma(z) - 1)\, w = -0.389361\, w$.

| $i$ | $x_i$ | $w_i$ | $g_i$ | $\operatorname{sign}(g_i)$ | line L3 | line L4 |
|---|---|---|---|---|---|---|
| 1 | 0.2 | 1.5 | -0.5840 | -1 | 0.1 | 0.1 |
| 2 | 0.9 | -2 | 0.7787 | +1 | 1.0 | 1.0 |
| 3 | 0.5 | 0.5 | -0.1947 | -1 | 0.4 | 0.4 |
| 4 | 0 | 1 | -0.3894 | -1 | -0.1 | 0 |
| 5 | 1 | -0.5 | 0.1947 | +1 | 1.1 | 1 |
| 6 | 0.4 | 3 | -1.1681 | -1 | 0.3 | 0.3 |

The result is $x' = (0.1, 1, 0.4, 0, 1, 0.3)$. Its logit is $z' = 0.45 - 0.1(1.5 + 2 + 0.5 + 3) = -0.25$, so $\sigma(z') = 0.437823$, the label is $0$ and the loss is $0.825939$. The clip of line L4 removed the moves of coordinates 4 and 5, which would have lowered the logit by another $0.15$. Without the box the result would not be a valid input.

On this model FGSM is exact: no point of $S$ has a larger loss. At $\epsilon = 0.05$ the same step gives $z' = 0.1 > 0$, and so no adversarial example exists at that radius.

## Correctness

**Theorem.** The output $x'$ lies in $S = B_\infty(x, \epsilon) \cap [0,1]^d$. It maximizes the linearized loss $L(\theta, x, y) + g^\top (x' - x)$ over $S$, with gain $\epsilon \lVert g \rVert_1$ when no coordinate is clipped. For logistic regression it maximizes the true loss over $S$.

The key facts are that $S$ is a box $\prod_i [\max(x_i - \epsilon, 0), \min(x_i + \epsilon, 1)]$ and that the linear objective is a sum of terms in one coordinate each, so each term is maximized at the end of its interval that the sign of $g_i$ picks; lines L3 and L4 compute exactly that end. For logistic regression the sign of $g_i$ is $-s \operatorname{sign}(w_i)$ with $s = 2y - 1$ at every point, and the loss is increasing in $-s\, z$, so the linear argument applies to the true loss. The full proof is in `proofs/correctness.md`.

For a nonlinear model, FGSM is a heuristic: the linearization is valid only near $x$, and a larger loss inside $S$ may exist.

## Complexity

- **Time.** Line L1 costs one gradient, $g$, which by [backpropagation](/backpropagation/) is a small constant times the cost of a forward pass. Lines L2 to L4 cost $O(d)$. The total is $O(g + d)$.
- **Space.** $\Theta(d)$ for $g$ and $x'$, plus the memory of one backward pass.
- **Queries.** One gradient, against hundreds or thousands of steps for the [PGD attack](/pgd-attack/), the [Carlini-Wagner attack](/carlini-wagner-attack/) or a black-box attack.

## Properties

- **Deterministic.** The same model and input give the same output.
- **The perturbation is on a corner.** Every unclipped coordinate of $\eta = x' - x$ is $\pm\epsilon$, so $\lVert \eta \rVert_\infty = \epsilon$ and $\lVert \eta \rVert_2$ is close to $\epsilon \sqrt d$.
- **Only the sign matters.** Scaling the gradient, or the loss, by a positive number does not change the output. A gradient of exactly $0$ leaves the input unchanged.
- **Exact on linear models.** For a linear model the sign pattern of the gradient is the same at every point, so one step reaches the worst corner (theorem above).
- **An upper bound only.** If $x'$ is misclassified, $x$ is not robust at radius $\epsilon$. If it is not, $x$ may still have adversarial examples in $S$.

## Variants and improvements

- **Targeted FGSM.** Step against the gradient of the loss of a target label $t$ (see the end of "The algorithm").
- **Fast gradient method in $\ell_2$.** Replace $\operatorname{sign}(g)$ by $g / \lVert g \rVert_2$; this maximizes the linearized loss over the $\ell_2$ ball before the clip.
- **Iterative FGSM.** Repeat the step with a smaller size $\alpha$ and clip back to $S$ after each step. Kurakin, Goodfellow and Bengio (2017) call it the basic iterative method; with a random start it is the [PGD attack](/pgd-attack/) of Madry et al. (2018).
- **FGSM with a random start.** Start from a random point of $S$ and take one step of size somewhat above $\epsilon$. Wong, Rice and Kolter (2020) use it for fast [adversarial training](/adversarial-training/).
- **FGSM training.** Goodfellow, Shlens and Szegedy (2015) trained on a mix of the clean loss and the loss at the FGSM point. Training on FGSM points alone can make the model hide its gradients (see Pitfalls).

## When to use it

Use FGSM as a quick first check of a model, as the inner step of cheap adversarial training, or as a baseline in a paper. Do not use it alone to claim robustness: a model can resist FGSM and fail under the PGD attack. To measure robust accuracy, use the [PGD attack](/pgd-attack/) with restarts and a minimal-distance attack, and to prove robustness, use a certificate such as [randomized smoothing](/randomized-smoothing/) or [interval bound propagation](/interval-bound-propagation/).

## Pitfalls

- **No clip.** If line L4 is left out, $x'_i = x_i \pm \epsilon$ can leave $[0,1]$, as coordinates 4 and 5 do in the example. The output is then not a valid input, and the success rate is too high. Keep the clip of line L4.
- **The wrong sign for a targeted attack.** Using $+\epsilon$ in line L3 with the gradient of the target loss moves away from the target. The targeted step is $x_i - \epsilon \operatorname{sign}(g_i)$ with $g = \nabla_x L(\theta, x, t)$.
- **A sign function with $\operatorname{sign}(0) = 1$.** Some library functions, such as a copysign, return $\pm 1$ for $0$. Line L3 must leave a coordinate with $g_i = 0$ in place, or the output depends on rounding.
- **The predicted label in line L1.** Using $f(x)$ instead of the true $y$ is fine only when $x$ is correctly classified. For a misclassified $x$ the step makes the model more sure of its wrong label.
- **Gradient masking.** A model trained only on FGSM points, or a model with a saturated softmax, can have gradients that point the wrong way near $x$, so FGSM fails while the PGD attack or an attack from a random start succeeds. A low FGSM success rate is no proof of robustness (Athalye, Carlini and Wagner 2018; see [evasion attack](/evasion-attack/)). [Defensive distillation](/defensive-distillation/) is a known case.

## Implementations

The code of this page is an abstract model on synthetic data. The attack runs only on models that the tests build from a fixed seed: a logistic regression with given weights, or a two-layer ReLU network from `mlkit.tiny_relu_net`, on seeded random inputs. It never reads real data or touches a real system. The tests check the example table, that every output lies in $B_\infty(x, \epsilon) \cap [0,1]^d$, that FGSM attains the maximum of the loss of a logistic model over all corners of the box on 500 random cases, that it attains the linearized optimum $\epsilon \lVert g \rVert_1$ on 500 random ReLU networks, and the helper `mlkit.py` itself.

## History

Szegedy et al. (2014) found adversarial examples of deep networks with a slow box-constrained L-BFGS search, and Biggio et al. (2013) had found test-time evasion of classifiers with gradient steps. Goodfellow, Shlens and Szegedy posted FGSM in December 2014, and it appeared at ICLR 2015. They argued that adversarial examples come from linearity in high dimension, not from overfitting or nonlinearity, and they showed that the one-step attack is enough: at $\epsilon = 0.25$ on MNIST, FGSM gave an error rate of 99.9 percent on a shallow softmax classifier and 89.4 percent on a maxout network (a measurement on those models). They also proposed adversarial training with FGSM. Kurakin, Goodfellow and Bengio (2017) made the step iterative, and Madry et al. (2018) added random starts and showed that the iterative attack is the right inner step for robust training.

## References
