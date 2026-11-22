---
tag: NXJN7D
kind: algorithm
slug: jacobian-saliency-map-attack
name: Jacobian-based saliency map attack
aliases:
- JSMA
area: security-and-privacy/adversarial-machine-learning
level: advanced
summary: "A targeted l0 attack that uses a saliency map of the Jacobian to pick pairs of features, and sets them high until the model gives the target class or a budget of changed features runs out."
model: real-ram
complexity:
  vars: {d: the input dimension, K: the number of classes, G: the budget of changed features, g: the cost of the Jacobian of the logits}
  time: {worst: O(G (g + K d + d^2))}
  space: {extra: Θ(K d)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2015
  people: [Nicolas Papernot, Patrick McDaniel, Somesh Jha, Matt Fredrikson, Z. Berkay Celik, Ananthram Swami]
  note: Papernot and coauthors posted the attack in November 2015 (IEEE EuroS&P 2016) to craft adversarial inputs that change few features.
prereqs: [adversarial-example, backpropagation]
see_also: [deepfool, carlini-wagner-attack, fast-gradient-sign-method, evasion-attack, defensive-distillation, adversarial-transferability, pgd-attack]
sources:
  - url: https://arxiv.org/abs/1511.07528
    title: Nicolas Papernot, Patrick McDaniel, Somesh Jha, Matt Fredrikson, Z. Berkay Celik and Ananthram Swami, The limitations of deep learning in adversarial settings, IEEE European Symposium on Security and Privacy 2016, pages 372 to 387
    locator: the forward derivative, the saliency map with pairs of features, and the MNIST evaluation
  - url: https://arxiv.org/abs/1608.04644
    title: Nicolas Carlini and David Wagner, Towards evaluating the robustness of neural networks, IEEE Symposium on Security and Privacy 2017, pages 39 to 57
    locator: the description of JSMA on logits and on softmax outputs, and the l0 attack that they compare with it
  - url: https://arxiv.org/abs/1511.04508
    title: Nicolas Papernot, Patrick McDaniel, Xi Wu, Somesh Jha and Ananthram Swami, Distillation as a defense to adversarial perturbations against deep neural networks, IEEE Symposium on Security and Privacy 2016, pages 582 to 597
    locator: the use of JSMA to evaluate defensive distillation
  - paper: "Battista Biggio and Fabio Roli, Wild patterns: Ten years after the rise of adversarial machine learning, Pattern Recognition 84, pages 317 to 331, 2018"
    locator: the threat model in three parts used on this page
---

The Jacobian-based saliency map attack (JSMA) is a targeted attack that changes few input features, so it is small in the $\ell_0$ norm and not in $\ell_\infty$. At each step it computes the Jacobian of the logits, scores every pair of features by how much raising them helps the target class and hurts all the others, and sets the best pair to the top of the range. It stops when the model gives the target class, or when a budget of changed features runs out. Papernot, McDaniel, Jha, Fredrikson, Celik and Swami (2016) introduced it; on their MNIST network it reached the target in 97 percent of the cases with about 4 percent of the pixels changed, as their abstract reports.

**Threat model.** The goal is targeted: the class $t$ is given. The knowledge is white box: the attacker computes the Jacobian of the logits. The capability is a change at test time that raises at most $G = \lfloor \gamma d \rfloor$ features of $x \in [0,1]^d$ by $\theta$ each, clipped at $1$; $\gamma$ is the fraction of features that may change.

## In plain words

Each feature of the input can push the model toward some classes and away from others. The Jacobian tells you, for each feature, how much each logit grows when the feature grows.

JSMA looks for features that help the target class and at the same time hurt the other classes. One feature alone often does only one of the two, so JSMA scores pairs: a pair is allowed only if together the two features raise the target logit and lower the sum of the other logits. It takes the pair with the best score and sets both features to the maximum.

Then it computes the Jacobian again at the new point and repeats. Each feature changes at most once. The result changes few features, but each by a large amount.

## The problem

Given logits $z : [0,1]^d \to \mathbb{R}^K$, an input $x$, a target class $t$, a step $\theta > 0$ and a fraction $\gamma \in [0, 1]$, find $x'$ with
$$\arg\max_k z_k(x') = t, \qquad x' \in [0,1]^d, \qquad \lVert x' - x \rVert_0 \le \lfloor \gamma d \rfloor.$$
The smallest such change is a combinatorial search over sets of features. JSMA is a greedy method for it.

For a pair of features $(p, q)$ at the current point, write
$$\alpha_{pq} = \frac{\partial z_t}{\partial x_p} + \frac{\partial z_t}{\partial x_q}, \qquad \beta_{pq} = \sum_{j \ne t}\left(\frac{\partial z_j}{\partial x_p} + \frac{\partial z_j}{\partial x_q}\right).$$
The saliency of the pair is $-\alpha_{pq}\beta_{pq}$ when $\alpha_{pq} > 0$ and $\beta_{pq} < 0$, and $0$ otherwise.

## The algorithm

```pseudo id=main
JSMA(z, x, t, theta, gamma)
L1  x' ← x; D ← {i : x_i < 1}; C ← empty list       ▷ D is the search domain
L2  G ← floor(gamma · d)
L3  while argmax_k z_k(x') ≠ t and |C| + 2 ≤ G and |D| ≥ 2 do
L4      J ← the Jacobian of z at x'
L5      (p, q) ← the pair of D with alpha > 0, beta < 0 and the largest -alpha · beta
L6      if there is no such pair then stop the loop
L7      for i in (p, q): x'_i ← min(x'_i + theta, 1); remove i from D; append i to C
L8  return (x', argmax_k z_k(x') = t, C)
```

Line L5 checks all pairs of $D$, in order; the first pair with the best score wins a tie. Line L7 removes a chosen feature from $D$, so each feature changes at most once and $|C|$ counts the changed features. This is the version that raises features and uses the logits. The paper also describes a version that lowers features, and computes the map on the softmax outputs.

## Example

Take $K = 3$ classes, $d = 6$ features, the affine model $z(v) = Wv + b$ with
$$W = \begin{pmatrix} -0.5 & 0.5 & 1 & 0 & 0 & 0 \\ 1 & -1 & -0.5 & 0 & 0.5 & 0 \\ 1 & 0 & 0.5 & -1 & -1 & -1 \end{pmatrix}, \qquad b = (1, 0, 0),$$
the input $x = (0.2, 0, 0, 0.5, 0.2, 0.4)$, the target $t = 1$, $\theta = 1$ and $\gamma = 1$. The logits are $(0.9, 0.3, -0.9)$, so the label is $0$. The Jacobian is $W$ at every point. Per feature, $\partial z_1 / \partial x_i = (1, -1, -0.5, 0, 0.5, 0)$, and the sum of the other two rows is $(0.5, 0.5, 1.5, -1, -1, -1)$.

In the first iteration all six features are in $D$. Five pairs are allowed:

| pair | $\alpha$ | $\beta$ | saliency $-\alpha\beta$ |
|---|---|---|---|
| (0, 3) | 1.0 | -0.5 | 0.5 |
| (0, 4) | 1.5 | -0.5 | 0.75 |
| (0, 5) | 1.0 | -0.5 | 0.5 |
| (3, 4) | 0.5 | -2.0 | 1.0 |
| (4, 5) | 0.5 | -2.0 | 1.0 |

Pairs $(3, 4)$ and $(4, 5)$ tie, and $(3, 4)$ comes first. Line L7 sets $x_3 = x_4 = 1$, and the logits become $(0.9, 0.7, -2.2)$: the label is still $0$. In the second iteration $D = \{0, 1, 2, 5\}$, and only $(0, 5)$ is allowed, with saliency $0.5$. After it, $x' = (1, 0, 0, 1, 1, 1)$ with logits $(0.5, 1.5, -2)$, and the label is $1$.

JSMA changed four features, $C = (3, 4, 0, 5)$, so $\lVert x' - x \rVert_0 = 4$ and $\lVert x' - x \rVert_\infty = 0.8$, from feature $0$. With $\gamma = 0.5$ the budget is $3$, only one pair fits, and the attack fails after the first pair.

The greedy choice is not minimal here. Setting only $x_0 = 1$ gives logits $(0.5, 1.1, -0.1)$, already class $1$. The pair $(0, 4)$ has the largest $\alpha$, but its $\beta$ is weak, and the product prefers $(3, 4)$.

## Correctness

**Theorem 1.** JSMA stops after at most $\lfloor G / 2 \rfloor$ full passes of the loop. It returns $x' \in [0,1]^d$ with $x' \ge x$ in every coordinate, $\lVert x' - x \rVert_0 = |C| \le G$, and a success flag that is true exactly when the label of $x'$ is $t$.

The proof is a loop invariant: $C$ has no repeated feature, its size is even and at most $G$, the domain is the first domain minus $C$, and $x'_i = \min(x_i + \theta, 1)$ for $i \in C$ while $x'_i = x_i$ otherwise. Each full pass adds two new features and keeps all of this. A lemma shows that line L5 returns the allowed pair with the largest saliency. The full proof is in `proofs/correctness.md`.

So every reported success is a valid targeted adversarial example for the model, inside the budget. The theorem says nothing about the smallest set: JSMA is greedy, and a failure does not prove that no set of $G$ features works. On the 500 seeded random affine models of the tests, JSMA succeeds in 94 cases, and an exhaustive search finds a smaller set in 82 of them (a measurement).

## Complexity

- **Time.** Each pass costs one Jacobian, $g$, which is $K$ backward passes in general, $O(K d)$ to sum the rows, and $O(d^2)$ to score the pairs. There are at most $G/2$ passes, so the total is $O(G (g + K d + d^2))$.
- **Space.** $\Theta(K d)$ for the Jacobian, plus $\Theta(d)$ for $x'$, $D$ and $C$.
- **Model.** These counts are in the real-ram model, with one Jacobian as a unit of work. On large inputs the $d^2$ pair search is the main cost, which is one reason later $\ell_0$ attacks score features in other ways.

## Properties

- **Deterministic.** No randomness. Ties go to the first pair.
- **Targeted and $\ell_0$.** It controls the number of changed features, not their size.
- **Monotone.** This version only raises features. A second version only lowers them.
- **Not minimal.** Greedy, as the example shows.
- **Valid output.** Every success is in the box and in the budget (Theorem 1).

## Variants and improvements

- **Single features.** The paper first defines the map for one feature: the score is $\frac{\partial z_t}{\partial x_i}\,\lvert \sum_{j \ne t} \frac{\partial z_j}{\partial x_i} \rvert$ when the first factor is positive and the sum is negative. The condition is rarely met for one feature alone, which is why the attack uses pairs.
- **Softmax or logits.** The map can use the Jacobian of the softmax outputs or of the logits. Carlini and Wagner (2017) call the two versions JSMA-F and JSMA-Z.
- **Lowering features.** Swap the signs of the conditions and lower features toward $0$.
- **Untargeted.** Pick the target as the class that is easiest to reach, or score the pairs against the true class only.
- **The C&W $\ell_0$ attack.** Carlini and Wagner run their $\ell_2$ attack many times and fix the features that matter least, which gives smaller $\ell_0$ changes than JSMA on their models.

## When to use it

Use JSMA on small models to study $\ell_0$ threat models, in which an attacker can change a few features by any amount, such as a few pixels or a few fields of a record. For $\ell_\infty$ or $\ell_2$ threat models, use the [PGD attack](/pgd-attack/), [DeepFool](/deepfool/) or the [Carlini-Wagner attack](/carlini-wagner-attack/). For a strong $\ell_0$ evaluation, run more than one attack, because a greedy failure is weak evidence.

## Pitfalls

- **Read failures with care.** A failure of a greedy search is not a proof of robustness. Report JSMA results as an upper bound on robust accuracy for the $\ell_0$ budget.
- **Softmax saturation.** On the softmax version, outputs near $0$ or $1$ have tiny gradients, and the map can be empty. This is how [defensive distillation](/defensive-distillation/) seemed to stop JSMA. Attacks that work on the logits are not stopped in this way.
- **Features at the top.** A feature already at $1$ is not in the domain. Inputs that are mostly at $1$ leave few choices.
- **Cost on large inputs.** The $d^2$ pair search is slow for large $d$. Restrict it to the top features, or use another method.
- **Even counts.** The attack changes features in pairs, so it cannot report a set of odd size, even when one feature is enough, as in the example.

## Implementations

The code of this page is an abstract model on synthetic data. The attack runs only on models that the tests build from a fixed seed: affine models with given or seeded weights, or two-layer ReLU networks from `mlkit.tiny_relu_net`, on seeded random inputs. It never reads real data or touches a real system. The tests check the example of the page, edge cases, the pair choice against a brute-force search on 500 random Jacobians, the output on 500 random affine models against an exhaustive search over feature sets, and the box, the budget and the success flag on seeded networks.

## History

Before JSMA, Szegedy et al. (2014) and Goodfellow, Shlens and Szegedy (2015) studied small changes in $\ell_2$ and $\ell_\infty$. Papernot, McDaniel, Jha, Fredrikson, Celik and Swami posted JSMA in November 2015 and published it at IEEE EuroS&P 2016. They named the Jacobian of the model the forward derivative, in contrast to the gradient of the loss used by FGSM, and they also gave a taxonomy of goals and knowledge of the adversary. The same group used JSMA to evaluate [defensive distillation](/defensive-distillation/) (2016) and to study [transferability](/adversarial-transferability/). Carlini and Wagner (2016, 2017) showed that attacks that work on the logits break distilled models, and gave an $\ell_0$ attack with smaller changes.

## References
