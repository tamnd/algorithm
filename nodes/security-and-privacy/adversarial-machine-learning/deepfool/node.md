---
tag: A515G9
kind: algorithm
slug: deepfool
name: DeepFool
aliases:
- DeepFool attack
area: security-and-privacy/adversarial-machine-learning
level: core
summary: "Finds a near-minimal l2 perturbation by linearizing the classifier, stepping to the nearest boundary of the linear model, and repeating until the label changes. Exact in one step for affine models."
model: real-ram
complexity:
  vars: {d: the input dimension, K: the number of classes, T: the number of iterations, g: the cost of the logits and their Jacobian}
  time: {worst: O(T (g + K d))}
  space: {extra: Θ(K d)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2015
  people: [Seyed-Mohsen Moosavi-Dezfooli, Alhussein Fawzi, Pascal Frossard]
  note: Moosavi-Dezfooli, Fawzi and Frossard posted DeepFool in November 2015 (CVPR 2016) as a fast and accurate way to measure the robustness of deep classifiers.
prereqs: [adversarial-example, logistic-regression]
see_also: [carlini-wagner-attack, fast-gradient-sign-method, universal-adversarial-perturbation, pgd-attack, evasion-attack, randomized-smoothing, linear-bound-propagation, adversarial-training]
sources:
  - url: https://arxiv.org/abs/1511.04599
    title: Seyed-Mohsen Moosavi-Dezfooli, Alhussein Fawzi and Pascal Frossard, DeepFool, a simple and accurate method to fool deep neural networks, CVPR 2016, pages 2574 to 2582
    locator: Section 2 (the binary case, exact for an affine classifier, and the iterative algorithm), Section 3 (the multiclass case and the extension to l_p norms), Section 4 (the robustness measure and the comparison with FGSM and the L-BFGS method of Szegedy et al.)
  - url: https://arxiv.org/abs/1610.08401
    title: Seyed-Mohsen Moosavi-Dezfooli, Alhussein Fawzi, Omar Fawzi and Pascal Frossard, Universal adversarial perturbations, CVPR 2017
    locator: the use of DeepFool as the inner step of the universal perturbation
  - url: https://arxiv.org/abs/1608.04644
    title: Nicholas Carlini and David Wagner, Towards evaluating the robustness of neural networks, IEEE Symposium on Security and Privacy 2017, pages 39 to 57
    locator: the comparison of the distances found by DeepFool and by the C&W attack
  - paper: "Battista Biggio and Fabio Roli, Wild patterns: Ten years after the rise of adversarial machine learning, Pattern Recognition 84, pages 317 to 331, 2018"
    locator: the threat model in three parts used on this page
---

DeepFool finds a small change that moves an input across the nearest decision boundary of a classifier, in the $\ell_2$ norm. At the current point it replaces the classifier by its first-order model, a set of hyperplanes, one for each wrong class. It computes the distance to each hyperplane, takes the shortest step to the nearest one, and repeats from the new point until the label changes. For an affine classifier the first step is the exact minimal perturbation. Moosavi-Dezfooli, Fawzi and Frossard (2016) proposed it to measure robustness: the size of the change estimates the distance $\rho_2(x)$ from $x$ to the nearest point with another label. It needs only a few gradients, far fewer than the [Carlini-Wagner attack](/carlini-wagner-attack/), and it is the inner step of the [universal adversarial perturbation](/universal-adversarial-perturbation/).

**Threat model.** The goal is untargeted. The knowledge is white box: the attacker computes the logits and their Jacobian. The capability is a change at test time in $[0,1]^d$ of any size; the attack reports the $\ell_2$ size of the change it found, so the radius $\epsilon$ is an output.

## In plain words

Picture the regions of the classes as countries with straight borders. If you stand in one country and want to leave it in the fewest steps, you walk straight to the nearest border, at a right angle to it.

A real classifier has curved borders. DeepFool pretends that the borders near you are straight, walks to the nearest straight border, and looks again. If you are still inside, the borders were bent, and it repeats. Usually two or three walks are enough.

At the end it walks a little further, by a factor $1 + \gamma$ with a small overshoot $\gamma$, so that the point is really on the other side and not on the border.

## The problem

Given logits $z(v) \in \mathbb{R}^K$ on $v \in [0,1]^d$ and an input $x$ with label $k_0 = \arg\max_k z_k(x)$, estimate
$$\rho_2(x) = \min \{\lVert r \rVert_2 : \arg\max_k z_k(x + r) \ne k_0\}$$
and return a point $x + r$ with another label and $\lVert r \rVert_2$ close to $\rho_2(x)$.

For an affine model $z(v) = Wv + b$ the answer has a closed form. Write $f_k(v) = z_k(v) - z_{k_0}(v)$ and $w_k = \nabla f_k$ for $k \ne k_0$. The region of class $k_0$ is the polyhedron $\{v : f_k(v) \le 0 \text{ for all } k\}$, and the distance to the face of class $k$ is $|f_k(x)| / \lVert w_k \rVert_2$. So
$$\rho_2(x) = \min_{k \ne k_0} \frac{|f_k(x)|}{\lVert w_k \rVert_2}, \qquad r^\star = \frac{|f_l(x)|}{\lVert w_l \rVert_2^2}\, w_l,$$
with $l$ the class that attains the minimum (ignoring the box). For two classes this is the distance $|w^\top x + b| / \lVert w \rVert_2$ to a hyperplane.

## The algorithm

```pseudo id=main
DEEPFOOL(z, x, gamma, T)                    ▷ gamma ≥ 0 is the overshoot
L1  k0 ← argmax_k z_k(x); r ← 0
L2  for it ← 0 to T do
L3      p ← clip_[0,1](x + (1 + gamma) r)
L4      if argmax_k z_k(p) ≠ k0 or it = T then return (p, it)
L5      J ← the Jacobian of z at p
L6      for k ≠ k0: w_k ← J_k - J_k0; f_k ← z_k(p) - z_k0(p); l ← the k with the least |f_k| / ||w_k||_2; step ← (|f_l| / ||w_l||_2^2) w_l
L7      r ← r + step
L8  return (p, T)
```

Line L6 is the closed form above, applied to the linear model of $z$ at $p$. The code adds $10^{-12}$ to $|f_l|$ so that the step crosses the hyperplane, and skips classes with $w_k = 0$. Line L3 applies the overshoot to the whole sum of the steps, as in the paper (they use $\gamma = 0.02$), and clips to the box. Line L4 stops at the first point with another label, or after $T$ iterations, in which case the label may still be $k_0$.

## Example

**An affine model, one step.** Take the model of the page [adversarial example](/adversarial-example/): $K = 3$, $z(v) = Wv$ with rows $(1, 0)$, $(0, 1)$ and $(-1, -1)$, and $x = (0.6, 0.4)$ with $k_0 = 0$ and $\gamma = 0.02$. The logits are $(0.6, 0.4, -1)$.

| class $k$ | $w_k = W_k - W_0$ | $f_k(x)$ | $\lVert w_k \rVert_2$ | distance $\lvert f_k \rvert / \lVert w_k \rVert_2$ |
|---|---|---|---|---|
| 1 | $(-1, 1)$ | $-0.2$ | $1.41421$ | $0.141421$ |
| 2 | $(-2, -1)$ | $-1.6$ | $2.23607$ | $0.715542$ |

Class 1 is nearest. The step is $(0.2/2)(-1, 1) = (-0.1, 0.1)$, and line L3 gives $p = x + 1.02 \cdot (-0.1, 0.1) = (0.498, 0.502)$, with logits $(0.498, 0.502, -1)$ and label $1$. DeepFool stops after one iteration. The distance is $1.02 \cdot 0.141421 = 0.144250$, the true minimum times $1 + \gamma$. It used one Jacobian and two logit calls.

**A small network, two steps.** Take the network of `mlkit.tiny_relu_net` with seed 3, $d = 2$, $h = 4$ hidden ReLU units and $K = 3$, at $x = (0.5, 0.5)$:

| iteration | $p$ | logits | label | step |
|---|---|---|---|---|
| 0 | (0.5, 0.5) | (-0.0741, -0.4478, -0.4643) | 0 | (0.0826, -0.3447) |
| 1 | (0.5843, 0.1485) | (-0.1340, -0.1821, -0.4723) | 0 | (0.0047, -0.0570) |
| 2 | (0.5891, 0.0903) | (-0.1490, -0.1481, -0.4679) | 1 | none |

The first step aims at a straight line that the network bends, so the point falls short. The second step, from the new linear model, crosses the border. The distance found is $0.41925$. A search over a grid of step $1/400$ on $[0,1]^2$ finds no point of another label closer than $0.41468$ (an estimate from the grid, accurate to about $0.002$). So DeepFool is within about $1.1$ percent of the minimum here, and $\gamma$ accounts for most of it.

## Correctness

**Theorem 1 (affine models).** Let $z$ be affine, and let $q = x + (1 + \gamma) r^\star$ lie in $[0,1]^d$. Then DeepFool returns $q$ after one iteration, the label of $q$ is not $k_0$, and $\lVert q - x \rVert_2 = (1 + \gamma)\rho_2(x)$, up to the $10^{-12}$ margin.

**Theorem 2 (any model).** DeepFool returns a point of $[0,1]^d$ after at most $T$ iterations. If it stops before $T$, the label of the point is not $k_0$. It calls the logits $it + 2$ times and the Jacobian $it$ times.

Theorem 1 holds because the region of $k_0$ is the intersection of the half spaces $f_k \le 0$, the distance to a union of half spaces is the least distance to one of them, and the step of line L6 is the shortest vector to the nearest one. For two classes the step reduces to $-f(x)\, w / \lVert w \rVert_2^2$, the orthogonal projection onto the hyperplane. The full proofs are in `proofs/correctness.md`.

For a nonlinear model, DeepFool is a heuristic. Its distance is an upper bound on $\rho_2(x)$, and it can stop at $T$ without a label change.

## Complexity

- **Time.** Each iteration costs one logit evaluation and one Jacobian, $g$, which is $K$ backward passes in general, plus $O(K d)$ for line L6. The total is $O(T (g + K d))$. The paper reports that a few iterations are enough on its image models (a measurement). For many classes, the paper limits line L6 to the classes with the highest logits.
- **Space.** $\Theta(K d)$ for the Jacobian, plus $\Theta(d)$ for $r$ and $p$.
- **Model.** These counts are in the real-ram model, with one Jacobian as a unit of work.

## Properties

- **Deterministic.** No randomness.
- **Minimal on affine models.** Theorem 1. On a network it is close to minimal when the borders bend little near $x$.
- **An upper bound on the distance.** The point found has another label, so $\rho_2(x) \le \lVert p - x \rVert_2$. To get robust accuracy at radius $\epsilon$, count the points whose DeepFool distance is above $\epsilon$; this gives an upper bound on robust accuracy.
- **Not tied to a radius.** DeepFool does not take $\epsilon$. This makes it good for measuring robustness and poor for testing a given threat model.

## Variants and improvements

- **Other norms.** For $\ell_p$ with dual exponent $q$, $1/p + 1/q = 1$, the distance to the face of class $k$ is $|f_k| / \lVert w_k \rVert_q$, and the step is $\frac{|f_l|}{\lVert w_l \rVert_q^q} |w_l|^{q - 1} \odot \operatorname{sign}(w_l)$. For $\ell_\infty$ it is $\frac{|f_l|}{\lVert w_l \rVert_1}\operatorname{sign}(w_l)$, an FGSM-like step with the exact size.
- **Robustness measure.** The paper reports $\hat\rho_{\mathrm{adv}} = \frac{1}{n}\sum_x \lVert r(x) \rVert_2 / \lVert x \rVert_2$ over a test set of $n$ points.
- **Universal perturbations.** The [universal adversarial perturbation](/universal-adversarial-perturbation/) runs DeepFool on many inputs in turn and adds the steps into one vector.
- **Targeted step.** Fix $l = t$ in line L6 to move toward a chosen class.
- **Training.** The paper fine-tunes networks on DeepFool points and reports larger distances afterward. [Adversarial training](/adversarial-training/) with PGD is the more common method today.

## When to use it

Use DeepFool to estimate how far inputs are from the decision boundary, to compare models, or as a fast start for a slower minimal attack. For a precise minimal $\ell_2$ distance, follow it with the [Carlini-Wagner attack](/carlini-wagner-attack/). To test robustness at a fixed radius, use the [PGD attack](/pgd-attack/). To prove that no closer point exists, use a certificate such as [randomized smoothing](/randomized-smoothing/) or [linear bound propagation](/linear-bound-propagation/).

## Pitfalls

- **No overshoot.** With $\gamma = 0$ the point lands on the border, and rounding can keep the old label. Keep a small $\gamma$, such as $0.02$.
- **The box.** The linear step ignores $[0,1]^d$, and the clip of line L3 shortens it. Then the loop can creep toward the border by steps that shrink geometrically. On the network of seed 131 in the same family, at $x = (0.5, 0.5)$, the second coordinate hits $0$ at iteration 2, and DeepFool needs 20 iterations, with a distance of $0.551$ against $0.518$ on the grid.
- **Gradients of zero.** If $w_k(p) = 0$ for all $k$, as in a flat region of a ReLU network, the step is $0$ and the loop runs to $T$. A failure then proves nothing.
- **Gradient masking.** Like every gradient attack, DeepFool fails on models whose gradients are hidden or noisy. Large DeepFool distances on a defended model are not a proof of robustness.
- **Comparing norms.** The distance is in $\ell_2$. Do not compare it with an $\ell_\infty$ radius.

## Implementations

The code of this page is an abstract model on synthetic data. The attack runs only on models that the tests build from a fixed seed: affine models with given or seeded weights, or two-layer ReLU networks from `mlkit.tiny_relu_net`, on seeded random inputs. It never reads real data or touches a real system. The tests check the two examples of the page, edge cases, that the step on 500 random binary affine models equals the closed-form projection onto the hyperplane, that on random multiclass affine models DeepFool stops after one iteration at $(1 + \gamma)$ times the closed-form minimum, and that the outputs on random networks lie in the box and change the label when the loop stops early.

## History

Szegedy et al. (2014) measured robustness with a slow box-constrained L-BFGS search, and Goodfellow, Shlens and Szegedy (2015) with the fast but coarse FGSM. Moosavi-Dezfooli, Fawzi and Frossard posted DeepFool in November 2015 (CVPR 2016). It found smaller perturbations than FGSM at a cost close to it on MNIST, CIFAR10 and ImageNet models, and it showed that FGSM overestimates robustness (measurements in their Section 4). The same group later used DeepFool to build universal perturbations (2017) and to study the curvature of decision boundaries. Carlini and Wagner (2017) found that their attack gives somewhat smaller distances than DeepFool, at a much higher cost.

## References
