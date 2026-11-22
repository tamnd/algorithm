---
tag: 0K6SWG
kind: algorithm
slug: boundary-attack
name: Boundary attack
aliases:
- decision-based attack
area: security-and-privacy/adversarial-machine-learning
level: advanced
summary: "A black-box attack that sees only labels. It starts from an input of another class and takes random steps along the decision boundary, keeping those that stay wrong and get closer."
model: real-ram
complexity:
  vars: {T: the number of steps, d: the input dimension, q: the cost of one label query}
  time: {worst: O(T (d + q))}
  space: {extra: Θ(d)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2017
  people: [Wieland Brendel, Jonas Rauber, Matthias Bethge]
  note: Brendel, Rauber and Bethge posted the attack in December 2017 (ICLR 2018), as an attack that needs only the final label of the model.
prereqs: [adversarial-example, evasion-attack]
see_also: [zeroth-order-optimization-attack, carlini-wagner-attack, deepfool, adversarial-transferability, evasion-attack, pgd-attack, randomized-smoothing]
sources:
  - url: https://arxiv.org/abs/1712.04248
    title: Wieland Brendel, Jonas Rauber and Matthias Bethge, Decision-based adversarial attacks, reliable attacks against black-box machine learning models, ICLR 2018
    locator: the description of the attack, with the proposal on the sphere, the step toward the original input and the adaptation of the two step sizes, and the comparison with gradient attacks on MNIST, CIFAR10 and ImageNet models
  - url: https://arxiv.org/abs/1904.02144
    title: Jianbo Chen, Michael I. Jordan and Martin J. Wainwright, HopSkipJumpAttack, a query-efficient decision-based attack, IEEE Symposium on Security and Privacy 2020
    locator: the estimate of the gradient direction at the boundary from labels, as a faster successor
  - url: https://arxiv.org/abs/1608.04644
    title: Nicholas Carlini and David Wagner, Towards evaluating the robustness of neural networks, IEEE Symposium on Security and Privacy 2017, pages 39 to 57
    locator: the white-box l2 attack used as the reference in the comparison
  - paper: "Battista Biggio and Fabio Roli, Wild patterns: Ten years after the rise of adversarial machine learning, Pattern Recognition 84, pages 317 to 331, 2018"
    locator: the threat model in three parts used on this page
---

The boundary attack finds an adversarial example while it sees only the label that a model returns for a query, with no gradients and no scores. It starts from a point that already has another label, for example random noise, and walks toward the original input $x$. Each step tries a random move along a sphere around $x$ and then a small move toward $x$, and keeps the new point only if its label is still wrong. So the point always stays adversarial and never moves away from $x$, and it slides along the decision boundary toward the nearest part of it. Brendel, Rauber and Bethge (2018) introduced it and showed that, with enough queries, it finds distances close to those of white-box gradient attacks. Because it needs no gradients, it is not fooled by defenses that only hide or break the gradient.

**Threat model.** The goal is untargeted. The knowledge is black box with labels only: a query returns $k(u) = \arg\max_j z_j(u)$ and nothing else. The attacker needs a starting point $a^0$ with $k(a^0) \ne y$. The capability is a change at test time in $[0,1]^d$; the attack reports the $\ell_2$ distance it reaches after $T$ steps, with at most $2T$ queries.

## In plain words

Think of a room with a wall that splits it into two parts, and you are on the wrong side. You want to stand on the wrong side as close as you can to a point $x$ on the right side, but you are blind: you can only ask whether you are on the wrong side.

Start anywhere on the wrong side. Take a random step around $x$ at the same distance, and ask. If you are still on the wrong side, step a little toward $x$ and ask again. If you are still on the wrong side, stay there. If either answer is no, go back.

Over time you end up at the wall, at the place closest to $x$. If most tries fail, make the steps smaller. If most succeed, make them larger.

## The problem

Given a label oracle $k$ on $[0,1]^d$, an input $x$ with label $y = k(x)$, and a start $a^0$ with $k(a^0) \ne y$, find $a$ with $k(a) \ne y$ and $\lVert a - x \rVert_2$ as small as possible, with a budget of queries. The best value is $\rho_2(x)$, the distance from $x$ to the nearest input of another label. Any output gives an upper bound on it.

## The algorithm

```pseudo id=main
BOUNDARY(k, x, y, a0, T, alpha, beta)
L1  a ← a0
L2  for t ← 1 to T do                       ▷ stop early if a = x
L3      eta ← a vector of d draws from N(0, 1)
L4      D ← ||a - x||_2; m ← a + alpha D eta / ||eta||_2; o ← clip(x + D (m - x) / ||m - x||_2); c ← clip(o + beta (x - o))
L5      if k(o) ≠ y then                     ▷ the move on the sphere is still adversarial
L6          if k(c) ≠ y then a ← c           ▷ the move toward x too
L7      every 10 steps: alpha ← alpha · 1.5 if more than 5 of 10 o were adversarial, else alpha / 1.5; beta ← min(beta · 1.5, 0.9) if more than 2 of 10 c were accepted, else beta / 1.5
L8  return (a, the number of queries)
```

Line L4 builds two candidates. The orthogonal candidate $o$ is a random move of relative size $\alpha$ projected back onto the sphere of radius $D$ around $x$. The full candidate $c$ then moves a fraction $\beta$ of the way to $x$. Line L7 is a simple form of the rule of the paper, which tunes $\alpha$ so that about half of the moves on the sphere stay adversarial, and shrinks $\beta$ when moves toward $x$ fail. The paper also clips and rescales the proposal so that it stays in the box and has the required size.

## Example

**A straight boundary.** Take two classes in the plane with $k(u) = 1$ when $u_1 + u_2 > 0.8$ and $k(u) = 0$ otherwise. Let $x = (0.5, 0.5)$, with label $1$. The nearest point of label $0$ is on the line at $(0.4, 0.4)$, so $\rho_2 = 0.2 / \sqrt2 = 0.14142$. Start at $a^0 = (0.1, 0.1)$, at distance $0.56569$, with $\alpha = \beta = 0.1$ and the generator `random.Random(1)`:

| steps | queries | $\alpha$ for the next 10 | $\beta$ for the next 10 | distance | ratio to $\rho_2$ |
|---|---|---|---|---|---|
| 0 | 0 | 0.1 | 0.1 | 0.56569 | 4.0 |
| 10 | 20 | 0.15 | 0.15 | 0.19724 | 1.395 |
| 20 | 39 | 0.225 | 0.1 | 0.14251 | 1.008 |
| 50 | 82 | 0.15 | 0.0296 | 0.14251 | 1.008 |
| 100 | 157 | 0.225 | 0.0039 | 0.14167 | 1.002 |
| 200 | 295 | 0.0198 | 0.0001 | 0.14144 | 1.0001 |

In the first 10 steps all 10 full candidates are accepted, since the point is far from the boundary, and the distance drops fast. At step 20 the point $(0.4106, 0.3891)$ is close to the line, and most moves toward $x$ cross it, so $\beta$ shrinks. From step 20 to step 90 no full candidate is accepted. The point only gets closer when the move on the sphere slides it along the line toward $(0.4, 0.4)$. At step 200 the point is $(0.4009, 0.3991)$.

**Three classes.** On the linear model of the page [adversarial example](/adversarial-example/), with rows $(1, 0)$, $(0, 1)$ and $(-1, -1)$, $x = (0.6, 0.4)$, label $0$, start $(0, 1)$ and `random.Random(1)`, 200 steps use 297 queries and reach the distance $0.14146$, which is $1.0002$ times $\rho_2 = 0.14142$. This is the row of the boundary attack in the table of the page [evasion attack](/evasion-attack/).

## Correctness

**Theorem 1 (the invariant).** With $\alpha > 0$ and $0 < \beta < 1$ at the start, after every step the point $a$ is in $[0,1]^d$, its label is not $y$, and its distance to $x$ does not grow. When a full candidate is accepted, the distance shrinks by a factor of at least $1 - \beta$. The attack uses at most $2T$ queries.

**Corollary (a bound from below on linear models).** If $k(u) = 1$ exactly when $w^\top u + b > 0$, the distance of every iterate is at least $|w^\top x + b| / \lVert w \rVert_2 = \rho_2(x)$.

The proof rests on two facts. Before the clip, $o$ is at distance $D$ from $x$ and $c - x = (1 - \beta)(o - x)$. The clip to the box can only move a point toward $x$, because $x$ is in the box. A point is accepted only after a query shows its label is not $y$. The full proofs are in `proofs/correctness.md`.

The theorem does not say that the distance reaches $\rho_2(x)$, or how fast. That depends on the step sizes, the dimension and the shape of the boundary. On the 500 seeded random linear models of the tests, in one to four dimensions, 120 steps gave at most $1.066$ times the minimum (a measurement).

## Complexity

- **Time.** Each step draws $d$ numbers, builds two candidates in $O(d)$, and makes at most two queries of cost $q$. The total is $O(T (d + q))$.
- **Queries.** At most $2T$. This is the real cost in practice. In high dimensions the walk needs many steps, since a random direction is almost orthogonal to the useful one. The paper reports many thousands of queries per input on image models (a measurement).
- **Space.** $\Theta(d)$ for the point, the noise and the two candidates.

## Properties

- **Label only.** No gradients or scores.
- **Always adversarial.** The current point never loses the wrong label (Theorem 1). So it can stop at any time and return a valid result.
- **Monotone.** The distance never grows.
- **Randomized.** The result depends on the seed.
- **Robust to gradient masking.** It does not use gradients, so it is a useful check on defenses that make gradients useless.

## Variants and improvements

- **Targeted version.** Start from an input of the target class and keep only points of that class.
- **Better starts.** Start from a point of another label found by a [transfer attack](/adversarial-transferability/), or from the result of a line search between noise and $x$.
- **HopSkipJumpAttack.** Chen, Jordan and Wainwright (2020) estimate the direction of the gradient at the boundary from the labels of random points near it, then take a step and do a binary search back to the boundary. It needs far fewer queries.
- **Other norms.** The same walk works in $\ell_\infty$ with a different proposal.
- **Scores.** If the model returns scores, use a score-based method such as the [ZOO attack](/zeroth-order-optimization-attack/), which needs fewer queries.

## When to use it

Use the boundary attack on small models to study the threat model in which only labels are visible, or to check a defense that might hide gradients. If a defended model is robust against gradient attacks and the boundary attack finds much smaller distances, the gradients were not useful, and the defense needs a stronger evaluation. For white-box evaluation, use the [Carlini-Wagner attack](/carlini-wagner-attack/) or the [PGD attack](/pgd-attack/), which are faster and more precise.

## Pitfalls

- **Few queries, large distances.** Early in the walk the distance can be far above $\rho_2$. A result with a small query budget is a weak upper bound.
- **Stalls.** Near the boundary, $\beta$ shrinks fast, and the distance can stop moving for many steps, as in the example from step 20 to step 90. Restart with larger steps if this lasts.
- **The start matters.** A start far from the boundary or in a bad region costs queries. On a model with several regions of other labels, the walk can stay near a boundary that is not the nearest one.
- **Randomness.** Report the seed and run several seeds, since the result changes with the noise.
- **Rounding.** On a real system, inputs are rounded before the model sees them. The abstract model of this page has no such step.

## Implementations

The code of this page is an abstract model on synthetic data. The attack runs only on label functions that the tests build from a fixed seed: linear rules with given or seeded weights, and two-layer ReLU networks from `mlkit.tiny_relu_net`, on seeded random inputs, with the noise from `random.Random` seeded in the test. It never reads real data or touches a real system. The tests check the two examples of the page, edge cases, that on 500 random inputs the two candidates never move away from $x$, that on 500 random linear models the result stays adversarial, within the query budget, and between $\rho_2$ and the start distance, and that on seeded networks the result stays adversarial.

## History

Earlier black-box attacks used scores, as in [ZOO](/zeroth-order-optimization-attack/) (2017), or trained a substitute model for a [transfer attack](/adversarial-transferability/), as in Papernot et al. (2017). Brendel, Rauber and Bethge posted the boundary attack in December 2017 and published it at ICLR 2018. They showed that a walk with only labels reaches distances close to those of the [Carlini-Wagner attack](/carlini-wagner-attack/) on MNIST, CIFAR10 and ImageNet models, with many more queries, and that it works on models whose gradients are masked, such as distilled networks. Later methods, such as HopSkipJumpAttack (2020), reduced the number of queries by estimating the direction of the gradient at the boundary.

## References
