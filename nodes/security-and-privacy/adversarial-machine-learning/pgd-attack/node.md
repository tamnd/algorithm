---
tag: YAKX8W
kind: algorithm
slug: pgd-attack
name: Projected gradient descent attack
aliases:
- PGD attack
- iterative FGSM
- basic iterative method
area: security-and-privacy/adversarial-machine-learning
level: core
summary: "Repeats small signed gradient steps on the loss and projects back onto the epsilon ball and the valid box, from a random start. The standard first-order attack for robust accuracy."
model: real-ram
complexity:
  vars: {d: the input dimension, T: the number of steps, g: the cost of one input gradient of the loss}
  time: {worst: O(T (g + d))}
  space: {extra: Θ(d)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2017
  people: [Aleksander Madry, Aleksandar Makelov, Ludwig Schmidt, Dimitris Tsipras, Adrian Vladu]
  note: Kurakin, Goodfellow and Bengio (2016) repeated the FGSM step with clipping as the basic iterative method. Madry et al. (2017, ICLR 2018) added the random start, called it projected gradient descent and used it as the inner step of robust training.
prereqs: [fast-gradient-sign-method, projected-gradient-descent]
see_also: [adversarial-training, carlini-wagner-attack, deepfool, evasion-attack, randomized-smoothing, interval-bound-propagation, backward-pass-differentiable-approximation, expectation-over-transformation]
sources:
  - url: https://arxiv.org/abs/1706.06083
    title: Aleksander Madry, Aleksandar Makelov, Ludwig Schmidt, Dimitris Tsipras and Adrian Vladu, Towards deep learning models resistant to adversarial attacks, ICLR 2018
    locator: Section 2 (the saddle point problem, equation 2.1, and the PGD step), Section 3.1 (the landscape of local maxima over random restarts), Section 3.2 (first-order adversaries), Section 5 (the attack settings on MNIST and CIFAR10 and Tables 1 and 2)
  - url: https://arxiv.org/abs/1607.02533
    title: Alexey Kurakin, Ian Goodfellow and Samy Bengio, Adversarial examples in the physical world, ICLR 2017 workshop
    locator: the basic iterative method, which repeats the FGSM step and clips to the epsilon box after each step
  - url: https://arxiv.org/abs/1412.6572
    title: Ian J. Goodfellow, Jonathon Shlens and Christian Szegedy, Explaining and harnessing adversarial examples, ICLR 2015
    locator: Section 4 (the one-step method that PGD repeats)
  - url: https://arxiv.org/abs/1802.00420
    title: Anish Athalye, Nicholas Carlini and David Wagner, Obfuscated gradients give a false sense of security, circumventing defenses to adversarial examples, ICML 2018
    locator: the defenses that made PGD fail through obfuscated gradients, and the adapted attacks that broke them
  - url: https://arxiv.org/abs/1902.06705
    title: Nicholas Carlini, Anish Athalye, Nicolas Papernot, Wieland Brendel, Jonas Rauber, Dimitris Tsipras, Ian Goodfellow, Aleksander Madry and Alexey Kurakin, On evaluating adversarial robustness, arXiv 2019
    locator: the advice on step counts, restarts, the loss to use and the checks of an evaluation
  - url: https://arxiv.org/abs/2003.01690
    title: Francesco Croce and Matthias Hein, Reliable evaluation of adversarial robustness with an ensemble of diverse parameter-free attacks, ICML 2020
    locator: the PGD variant with an adaptive step size (APGD) and the AutoAttack suite
  - paper: "Battista Biggio and Fabio Roli, Wild patterns: Ten years after the rise of adversarial machine learning, Pattern Recognition 84, pages 317 to 331, 2018"
    locator: the threat model in three parts used on this page
---

The projected gradient descent attack (PGD attack) searches for an [adversarial example](/adversarial-example/) inside a fixed set $S = B_p(x, \epsilon) \cap [0,1]^d$ by gradient ascent on the loss. It starts at a random point of $S$, takes a step of size $\alpha$ in the steepest ascent direction for the norm, and projects the result back onto $S$. It repeats this $T$ times and keeps the point with the largest loss. One step from $x$ with $\alpha = \epsilon$ in $\ell_\infty$ is the [fast gradient sign method](/fast-gradient-sign-method/). Madry et al. (2018) showed that the local maxima that PGD finds from many random starts have similar loss values, and they made PGD the inner step of [adversarial training](/adversarial-training/). PGD is the standard attack for an upper bound on robust accuracy against an attacker with gradients.

**Threat model.** The goal is untargeted (a targeted variant is below). The knowledge is white box: the attacker computes the input gradient of the loss. The capability is a change at test time within $B_p(x, \epsilon) \cap [0,1]^d$, here for $p = \infty$ or $p = 2$.

## In plain words

FGSM looks at the slope of the loss one time and jumps to the edge of the allowed region. If the loss curves, that jump can land in the wrong place.

PGD walks instead. It takes many small steps uphill, and after each step it looks at the slope again. When a step leaves the allowed region, PGD pulls the point back to the nearest allowed point. When the walk is done, PGD returns the highest point that it saw.

Because the loss of a network has many hills, PGD often starts from a random point of the region, and an evaluation runs it several times from different starts. A model that keeps its label against all these walks is likely, but not proved, to be robust at that radius.

## The problem

Given a model with loss $L(\theta, x, y)$, an input $x \in [0,1]^d$ with label $y$, a norm $p \in \{2, \infty\}$ and a radius $\epsilon \ge 0$, find
$$x' \in \arg\max_{v \in S} L(\theta, v, y), \qquad S = B_p(x, \epsilon) \cap [0,1]^d.$$
If $f(x') \ne y$, then $x'$ is an adversarial example. This is the inner maximization of the saddle point problem $\min_\theta \mathbb{E}[\max_{\eta} L(\theta, x + \eta, y)]$ of Madry et al. (2018). For a network the objective is not concave, so PGD is a local method: it gives a feasible point with a large loss, not a certified maximum.

## The algorithm

Write $P_S$ for the map of line L5 into $S$. For $p = \infty$ it clips coordinate $i$ to $[\max(x_i - \epsilon, 0), \min(x_i + \epsilon, 1)]$; this is the Euclidean projection onto the box $S$. For $p = 2$ it rescales $v - x$ to length at most $\epsilon$ and then clips to $[0,1]^d$. The step direction $u(g)$ is $\operatorname{sign}(g)$ for $p = \infty$ and $g / \lVert g \rVert_2$ for $p = 2$, the direction of steepest ascent of a linear function for that norm.

```pseudo id=main
PGD(L, x, y, epsilon, alpha, T)            ▷ x in [0, 1]^d with label y
L1  x^0 ← P_S(x + random point of B_p(0, epsilon))   ▷ or x^0 ← x without a random start
L2  best ← x^0; bestloss ← L(θ, x^0, y)
L3  for t ← 0 to T - 1 do
L4      g ← ∇_x L(θ, x^t, y)                ▷ one forward and one backward pass
L5      x^{t+1} ← P_S(x^t + alpha · u(g))   ▷ step, then project
L6      if L(θ, x^{t+1}, y) > bestloss then best ← x^{t+1}; bestloss ← L(θ, x^{t+1}, y)
L7  return best
```

Line L1 draws the start uniformly from the $\ell_\infty$ box or from the $\ell_2$ ball and maps it into $S$. Lines L4 and L5 are one step of [projected gradient descent](/projected-gradient-descent/) on $-L$, with the normalized direction $u$ in place of the raw gradient. Line L6 keeps the best iterate, because a step of fixed size can overshoot a maximum and lower the loss.

For a targeted attack toward class $t$, use the loss $-L(\theta, v, t)$, so that the walk lowers the loss of the target label. Madry et al. also run PGD on the margin loss of the [Carlini-Wagner attack](/carlini-wagner-attack/), $\max_{k \ne y} z_k(v) - z_y(v)$, in place of the cross-entropy.

**Parameters.** The step size $\alpha$ and the step count $T$ must satisfy $\alpha T \ge 2\epsilon$ in $\ell_\infty$, so that a walk can cross the whole box. Madry et al. used $\epsilon = 0.3$, $T = 40$ and $\alpha = 0.01$ on MNIST, and $\epsilon = 8$ on the pixel scale 0 to 255, $T = 7$ and $\alpha = 2$ on CIFAR10, with $T = 20$ for their hardest test. For the sweeps of their Figure 6 they used $T = 100$ and $\alpha = 2.5\,\epsilon / 100$. These are choices of the paper, not rules.

## Example

**A linear model.** Take the logistic model of the FGSM page: $w = (1.5, -2, 0.5, 1, -0.5, 3)$, $b = 1$, $x = (0.2, 0.9, 0.5, 0, 1, 0.4)$, $y = 1$, the [logistic loss](/logistic-loss/), $\ell_\infty$ with $\epsilon = 0.1$ and $\alpha = 0.025$, and the start $x^0 = x$. The gradient is $(\sigma(z) - 1)\,w$ at every point, so its sign pattern $(-, +, -, -, +, -)$ never changes.

| $t$ | $x^t$ | logit $z$ | loss |
|---|---|---|---|
| 0 | (0.2, 0.9, 0.5, 0, 1, 0.4) | 0.45 | 0.493249 |
| 1 | (0.175, 0.925, 0.475, 0, 1, 0.375) | 0.275 | 0.565071 |
| 2 | (0.15, 0.95, 0.45, 0, 1, 0.35) | 0.1 | 0.644397 |
| 3 | (0.125, 0.975, 0.425, 0, 1, 0.325) | -0.075 | 0.731350 |
| 4 | (0.1, 1, 0.4, 0, 1, 0.3) | -0.25 | 0.825939 |
| 5 | (0.1, 1, 0.4, 0, 1, 0.3) | -0.25 | 0.825939 |

Coordinates 4 and 5 never move: the box holds them at $0$ and $1$. Each other coordinate moves by $0.025$ per step until the projection stops it at $x_i \pm 0.1$, after $4$ steps. From then on the iterate is fixed at the FGSM point, which is the exact maximum of the loss over $S$. The label changes at step 3.

In $\ell_2$ with $\epsilon = 0.1$ and the same $\alpha$, each step moves along $-w / \lVert w \rVert_2$ with $\lVert w \rVert_2 = 4.0927$, and the clip to the box removes the part of the step on coordinates 4 and 5. After 1, 2 and 4 steps the logit is $0.3553$, $0.2606$ and $0.0713$, and after 8 steps it is $0.0569$, so the label is still $1$. Without the box the best logit in the ball would be $0.45 - 0.1 \cdot 4.0927 = 0.0407$, still positive. So no $\ell_2$ adversarial example exists at radius $0.1$, while in $\ell_\infty$ one does: the $\ell_\infty$ ball of the same radius is much larger.

**A network where one step fails.** Take the network of `mlkit.tiny_relu_net` with seed 2744, $d = 2$ inputs, $h = 4$ hidden ReLU units and $K = 2$ classes. Its first layer has the rows $(1.188, -1.941)$, $(-0.523, -0.003)$, $(-0.188, 1.168)$ and $(1.157, 0.158)$ with biases $(0.106, 0.001, 0.078, 0.038)$, and its output layer has the rows $(-1.175, 0.061, 0.208, 0.244)$ and $(1.592, -0.171, 0.257, -0.354)$ with biases $(-0.142, -0.110)$ (rounded to three places). The input is $x = (0.63, 0.46)$ with label $0$, and $\epsilon = 0.1$ in $\ell_\infty$.

At $x$ the gradient is $(-0.274, -0.015)$, so FGSM moves to $(0.53, 0.36)$. There the logits are $(0.070, -0.199)$, and the label is still $0$. PGD with $\alpha = 0.025$ and $T = 10$ from $x$ gives:

| $t$ | $x^t$ | logits $(z_0, z_1)$ | gradient |
|---|---|---|---|
| 0 | (0.63, 0.46) | (0.166, -0.280) | (-0.274, -0.015) |
| 2 | (0.58, 0.41) | (0.140, -0.269) | (-0.280, -0.015) |
| 3 | (0.555, 0.385) | (0.105, -0.234) | (1.076, -2.249) |
| 4 | (0.58, 0.36) | (0.012, -0.127) | (1.203, -2.516) |
| 6 | (0.63, 0.36) | (-0.046, -0.056) | (1.286, -2.690) |
| 7 | (0.655, 0.36) | (-0.074, -0.020) | (1.328, -2.777) |
| 10 | (0.73, 0.36) | (-0.161, 0.088) | (1.452, -3.038) |

At step 3 the first hidden unit, with pre-activation $1.188 x_1 - 1.941 x_2 + 0.106$, turns on, and the sign of the first partial derivative flips. FGSM saw only the slope at $x$ and moved $x_1$ the wrong way. PGD saw the new slope, turned around, and reached class $1$ at step 7. The final point $(0.73, 0.36)$ is the opposite corner in the first coordinate from the FGSM point.

## Correctness

**Theorem 1 (feasibility).** Every iterate lies in $S$, and the output is an iterate with the largest loss among $x^0, \dots, x^T$.

**Theorem 2 (linear model, $\ell_\infty$).** For logistic regression and $\alpha T \ge 2\epsilon$, from any start in $S$ the last iterate agrees with the FGSM point on every coordinate with $w_i \ne 0$, and the output maximizes the loss over $S$.

**Theorem 3 (linear model, $\ell_2$).** For logistic regression with $w \ne 0$, start $x$ and $\alpha T \ge \epsilon$, if the point $x - s\,\epsilon\, w / \lVert w \rVert_2$ with $s = 2y - 1$ lies in $[0,1]^d$, then it is the last iterate and the maximizer of the loss over $S$.

Theorem 1 holds because both forms of $P_S$ land in $S$: the clip of the $\ell_2$ case moves each coordinate toward $[0,1]$, which contains $x_i$, so it cannot leave the ball. Theorems 2 and 3 hold because the sign, or the direction, of the gradient of a logistic model is the same at every point, so the walk is a straight line that the projection stops at the optimal face. The full proofs are in `proofs/correctness.md`.

For a network, nothing more is proved. PGD can stop at a local maximum, and a failure of PGD is no proof of robustness. Madry et al. give experimental evidence, not a theorem, that the local maxima have similar losses (their Section 3.1, with $10^5$ restarts on a few MNIST and CIFAR10 points).

## Complexity

- **Time.** Each step costs one gradient, $g$, by [backpropagation](/backpropagation/), one loss value (at most a forward pass, so $O(g)$), and $O(d)$ for the step and the projection. The total is $O(T (g + d))$. With $R$ restarts the cost is $R$ times larger.
- **Space.** $\Theta(d)$ for the iterate, the gradient and the best point, plus the memory of one backward pass.
- **Model.** These counts are in the real-ram model, with one gradient as a unit of work.

## Properties

- **Randomized.** With a random start, two runs give different outputs. With the start $x$ the method is deterministic.
- **Anytime.** The best loss never goes down from one step to the next, so the run can stop at any step with a valid point.
- **An upper bound only.** A misclassified output proves that $x$ is not robust at radius $\epsilon$. A correct output proves nothing.
- **Agrees with FGSM on linear models.** On a linear model with $\alpha T \ge 2\epsilon$, PGD ends at the FGSM point (Theorem 2). The two differ only when the gradient changes sign inside $S$, as in the network example.

## Variants and improvements

- **Basic iterative method.** Kurakin, Goodfellow and Bengio (2017) start at $x$, take steps of size $\alpha$ and clip after each step. It is PGD without the random start.
- **Targeted PGD and the margin loss.** Descend on the loss of a target label, or ascend on the margin $\max_{k \ne y} z_k - z_y$, which does not saturate like the cross-entropy.
- **Restarts.** Run $R$ walks from different random starts and keep the best. Madry et al. report robust accuracy that goes down a little as steps and restarts grow (their Table 1).
- **Step size schedules.** A step size that shrinks over time, or one that adapts to the progress of the loss, removes the need to tune $\alpha$. The AutoAttack suite of Croce and Hein (2020) uses such a variant.
- **Other norms.** For $\ell_1$, the steepest ascent direction moves only the largest coordinates of $g$, and the projection onto the $\ell_1$ ball needs a sort.
- **PGD for training.** [Adversarial training](/adversarial-training/) runs PGD on each training batch and trains on the result.

## When to use it

Use PGD with restarts as the first strong attack in a robustness evaluation, and as the inner step of adversarial training. Report the norm, $\epsilon$, $\alpha$, $T$, the number of restarts and the loss. Add a minimal-distance attack, such as the [Carlini-Wagner attack](/carlini-wagner-attack/) or [DeepFool](/deepfool/), to see how far the decision boundary is. For a defense that changes the gradients, adapt the attack ([BPDA](/backward-pass-differentiable-approximation/), [EOT](/expectation-over-transformation/)). To prove robustness, use a certificate such as [randomized smoothing](/randomized-smoothing/) or [interval bound propagation](/interval-bound-propagation/).

## Pitfalls

- **Too few steps.** If $\alpha T < 2\epsilon$, part of the box cannot be reached, and the robust accuracy is too high. Check that a larger $T$ does not lower it further.
- **Only the last iterate.** A fixed step size can overshoot. Keep the best iterate, as line L6 does, or the result can be worse than FGSM.
- **No clip to the box.** Without the clip of $P_S$ to $[0,1]^d$, the output is not a valid input.
- **Clip in the wrong order for $\ell_2$.** Clip after the rescaling, not before. The clip after the rescaling cannot leave the ball (Theorem 1); a rescaling after the clip can leave the box.
- **Gradient masking.** Defenses with saturated softmax outputs, random input transformations or non-differentiable steps can make PGD fail while the model is not robust. Athalye, Carlini and Wagner (2018) broke 7 of 9 ICLR 2018 defenses in this way. A check: an unbounded attack with a large $\epsilon$ must reach 100 percent success (Carlini et al. 2019).
- **The cross-entropy saturates.** When the softmax gives the true label a probability near $1$, the gradient of the cross-entropy is tiny. The margin loss avoids this.

## Implementations

The code of this page is an abstract model on synthetic data. The attack runs only on models that the tests build from a fixed seed: a logistic regression with given weights, or a two-layer ReLU network from `mlkit.tiny_relu_net`, on seeded random inputs. It never reads real data or touches a real system. The tests check the trace of the linear example, the network example where FGSM fails and PGD succeeds, that one step from $x$ with $\alpha = \epsilon$ equals FGSM, that PGD from a random start reaches the maximum over all corners of the box on random logistic models, that it reaches the closed-form $\ell_2$ optimum, that every iterate stays in $S$ on 500 random networks for both norms, and that the $\ell_2$ random start is uniform in the disc.

## History

Kurakin, Goodfellow and Bengio (2016) proposed the basic iterative method, which repeats the FGSM step with clipping, and used it on photos of printed adversarial images. Madry, Makelov, Schmidt, Tsipras and Vladu posted their paper in June 2017 (ICLR 2018). They stated robustness as a saddle point problem, added the random start, called the inner method projected gradient descent and argued that it is a "universal" first-order adversary. Their PGD-trained models reached more than 89 percent accuracy on MNIST against their strongest white-box attack at $\epsilon = 0.3$, and 45.8 percent on CIFAR10 against PGD with 20 steps at $\epsilon = 8/255$ (measurements in their Section 5). They also published the models as open challenges. Later evaluations with stronger variants, such as AutoAttack, lowered such numbers a little but did not break PGD training.

## References
