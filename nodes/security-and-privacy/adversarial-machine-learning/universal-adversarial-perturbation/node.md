---
tag: NQDGS5
kind: algorithm
slug: universal-adversarial-perturbation
name: Universal adversarial perturbation
aliases:
- image-agnostic perturbation
area: security-and-privacy/adversarial-machine-learning
level: advanced
summary: "Builds one small perturbation that changes the label of many inputs at once, by adding DeepFool steps over a data set and projecting the sum back onto a norm ball."
model: real-ram
complexity:
  vars: {n: the number of data points, P: the number of passes, T: the DeepFool iterations per point, d: the input dimension, K: the number of classes, g: the cost of the logits and their Jacobian}
  time: {worst: O(P n T (g + K d))}
  space: {extra: Θ(K d)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2016
  people: [Seyed-Mohsen Moosavi-Dezfooli, Alhussein Fawzi, Omar Fawzi, Pascal Frossard]
  note: Moosavi-Dezfooli, Fawzi, Fawzi and Frossard posted the algorithm in October 2016 (CVPR 2017) and showed that one perturbation fools ImageNet networks on most images.
prereqs: [deepfool, adversarial-example]
see_also: [deepfool, adversarial-transferability, fast-gradient-sign-method, pgd-attack, evasion-attack, adversarial-training, randomized-smoothing]
sources:
  - url: https://arxiv.org/abs/1610.08401
    title: Seyed-Mohsen Moosavi-Dezfooli, Alhussein Fawzi, Omar Fawzi and Pascal Frossard, Universal adversarial perturbations, CVPR 2017, pages 1765 to 1773
    locator: the definition of a universal perturbation and of the fooling rate, the algorithm with DeepFool steps and the projection, the ImageNet experiments and the study of transfer across networks
  - url: https://arxiv.org/abs/1511.04599
    title: Seyed-Mohsen Moosavi-Dezfooli, Alhussein Fawzi and Pascal Frossard, DeepFool, a simple and accurate method to fool deep neural networks, CVPR 2016, pages 2574 to 2582
    locator: the inner step of the algorithm
  - paper: "Battista Biggio and Fabio Roli, Wild patterns: Ten years after the rise of adversarial machine learning, Pattern Recognition 84, pages 317 to 331, 2018"
    locator: the threat model in three parts used on this page
---

A universal adversarial perturbation is one vector $v$, small in a norm, such that adding it to most inputs changes their label. It does not depend on the input. Moosavi-Dezfooli, Fawzi, Fawzi and Frossard (2017) gave an algorithm to build it: go through a data set, and each time $x + v$ still has the label of $x$, add the [DeepFool](/deepfool/) step that pushes $x + v$ across the nearest boundary, then project $v$ back onto the ball of radius $\epsilon$. Repeat until the fooling rate, the fraction of inputs whose label changes, is high enough. On ImageNet networks the paper found such vectors that fool most images and also fool other networks. That result shows that the decision boundaries of a network share directions across many inputs.

**Threat model.** The goal is untargeted, on a whole input distribution at once. The knowledge is white box: the attacker computes the logits and their Jacobian, and has samples of the inputs. The capability is one fixed change $v$ with $\lVert v \rVert_p \le \epsilon$, $p \in \{2, \infty\}$, added at test time to every input and clipped to $[0,1]^d$. The attacker does not need to see the input that the change is added to.

## In plain words

A normal adversarial example is made for one input. A universal one is made once and used on every input.

The algorithm starts with $v = 0$ and looks at the training inputs one at a time. If $v$ already changes the label of an input, it moves on. If not, it computes the smallest extra push that changes the label of $x + v$, adds that push to $v$, and shrinks $v$ back to the allowed size if it is too large.

The pushes for different inputs often point in similar directions, because the borders of the classes tend to have shared directions. So the sum does not cancel out, and one vector of the allowed size can change many labels.

## The problem

Given logits $z$ on $[0,1]^d$ with label $k(u) = \arg\max_j z_j(u)$, data $x^1, \dots, x^n$, a radius $\epsilon$ and a norm $p$, find $v$ with $\lVert v \rVert_p \le \epsilon$ that makes the fooling rate
$$R(v) = \frac{1}{n}\,\big|\{i : k(\operatorname{clip}(x^i + v)) \ne k(x^i)\}\big|$$
large. The paper asks for $R(v) \ge 1 - \delta$ on the data distribution for a given $\delta$. Maximizing $R$ is a hard combinatorial problem in general. The algorithm is a heuristic for it.

## The algorithm

```pseudo id=main
UNIVERSAL(z, x^1..x^n, epsilon, p, target, P)
L1  v ← 0
L2  for pass ← 1 to P do
L3      for i ← 1 to n do
L4          if k(clip(x^i + v)) = k(x^i) then
L5              r ← DEEPFOOL step at clip(x^i + v), away from the class k(x^i)
L6              v ← the projection of v + r onto the ball ||v||_p ≤ epsilon
L7      rate ← R(v)
L8      if rate ≥ target then stop the loop
L9  return (v, rate)
```

Line L5 runs the iterations of [DeepFool](/deepfool/) from the point $\operatorname{clip}(x^i + v)$, with an overshoot of $0.02$ and at most 10 iterations in the code. It returns the total step. Line L6 projects onto the ball: for $p = 2$ it scales $v$ down to length $\epsilon$, and for $p = \infty$ it clips each coordinate to $[-\epsilon, \epsilon]$. The paper visits the data in a new random order on each pass. The code uses the order of the data, so it is deterministic.

## Example

**A linear model.** Take two classes in the plane with logits $(0, f(u))$, $f(u) = u_1 + u_2 - 0.6$, so $w = (1, 1)$. Take five points, all of label 1:

| point | $(0.5, 0.3)$ | $(0.4, 0.5)$ | $(0.6, 0.5)$ | $(0.7, 0.6)$ | $(0.5, 0.6)$ |
|---|---|---|---|---|---|
| $f(x)$ | 0.2 | 0.3 | 0.5 | 0.7 | 0.5 |

Let $\epsilon = 0.3$ and $p = 2$. The first pass goes as follows. At $(0.5, 0.3)$, $f = 0.2$, the step is $1.02 \cdot 0.1 \cdot (-1, -1)$, and $v = (-0.102, -0.102)$. At $(0.4, 0.5)$, $f(x + v) = 0.096$, the step is $(-0.04896, -0.04896)$, and $v = (-0.15096, -0.15096)$. At $(0.6, 0.5)$, $f(x + v) = 0.1981$, the step makes $v + r = (-0.25198, -0.25198)$ of length $0.3564$, and line L6 scales it to $v = (-0.21213, -0.21213)$, of length $0.3$. At the last two points $v$ is at the edge of the ball in the direction of $-w$, so the steps add to it and the projection gives the same $v$ again. The fooling rate is $2/5 = 0.4$, and the second pass changes nothing.

This is the best rate for the $\ell_2$ ball: any $v$ moves $f$ by at least $-\epsilon \lVert w \rVert_2 = -0.4243$, so only the two points with $f(x) \le 0.4243$ can change label. For $p = \infty$ the bound uses $\lVert w \rVert_1 = 2$, so the best $v$ moves $f$ by $-0.6$. The algorithm ends the first pass at $v = (-0.3, -0.3)$ and fools four of the five points, a rate of $0.8$. Only $(0.7, 0.6)$, with $f = 0.7$, keeps its label.

**A small network.** Take the network of `mlkit.tiny_relu_net` with seed 26, $d = 4$, $h = 8$ and $K = 3$. Draw 40 training points and 200 new points, uniform in $[0,1]^4$, from the same seeded generator. With $\epsilon = 0.3$ in $\ell_2$, the algorithm stops changing $v$ after the first pass. The vector $v = (-0.098, -0.144, -0.021, 0.243)$ has length $0.3$ and fools 22 of the 40 training points (rate $0.55$) and 116 of the 200 new points (rate $0.58$). For comparison, 100 random directions of length $0.3$ fool on average $31.7$ percent of the new points, and a separate DeepFool run on each new point changes the label within $0.3$ for 91 percent of them. So the universal vector is between the two: much better than a random direction, and worse than one attack per input.

## Correctness

**Theorem 1 (a valid output).** The returned $v$ satisfies $\lVert v \rVert_p \le \epsilon$, and the returned rate is $R(v)$ on the data.

**Theorem 2 (an upper bound).** For a binary affine model $f(u) = w^\top u + b$, with all points of label 1 and no clip active, every $v$ in the ball has $R(v) \le R^\star = |\{i : f(x^i) \le \epsilon \lVert w \rVert_q\}| / n$, with $q = 2$ for $p = 2$ and $q = 1$ for $p = \infty$.

**Theorem 3 (optimal in $\ell_2$ on binary affine models).** Under the conditions of Theorem 2 with $p = 2$, and with no $f(x^i)$ equal to $\epsilon \lVert w \rVert_2$, one pass gives $R(v) = R^\star$.

Theorem 1 holds because $v$ starts at $0$ and changes only by a projection onto the ball. Theorem 2 is Hölder's inequality: $w^\top v \ge -\lVert w \rVert_q \lVert v \rVert_p$. For Theorem 3, every DeepFool step is a positive multiple of $-w$, so $v$ stays on the ray of $-w$ and its length only grows, up to $\epsilon$; once a point is fooled it stays fooled, and each point that the full ball can fool is fooled when the pass reaches it. The proofs are in `proofs/correctness.md`. For $p = \infty$ the result can be below $R^\star$ when the box clips some coordinates and not others, and for a network there is no optimality claim.

## Complexity

- **Time.** Each pass checks $n$ labels and runs DeepFool on at most $n$ points, each at most $T$ iterations of cost $g + O(K d)$, and line L7 costs $n$ more pairs of label calls. The total for $P$ passes is $O(P n T (g + K d))$.
- **Space.** $\Theta(K d)$ for one Jacobian, $\Theta(d)$ for $v$ and the step. The data is read, not copied.
- **Model.** These counts are in the real-ram model, with one call of the logits and Jacobian as a unit of work. The paper reports that a small part of the training set, much smaller than the full set, is enough on ImageNet (a measurement).

## Properties

- **Input-agnostic.** One $v$ for all inputs. It can be computed offline and applied without knowing the input.
- **Deterministic in this code.** The paper shuffles the data on each pass, which makes it random.
- **In the ball.** The output always satisfies the norm bound (Theorem 1).
- **Generalizes.** A vector built on some inputs often fools new inputs at a similar rate, as in the network example. This is a measurement, not a guarantee.
- **Transfers.** The paper reports that a vector built for one network also fools other networks at a lower rate (see [adversarial transferability](/adversarial-transferability/)).

## Variants and improvements

- **Other inner steps.** Replace DeepFool by an FGSM or PGD step on the loss of the current batch. This gives a stochastic gradient method on the average loss over the data, projected onto the ball.
- **Data-free versions.** Later work builds universal vectors without training data, by maximizing the activations of inner layers.
- **Generative models.** A network can be trained to output universal perturbations, which gives many different ones quickly.
- **Universal adversarial training.** Train the model against the current universal vector, which costs much less than [adversarial training](/adversarial-training/) per input, and protects only against universal changes.
- **Patches.** Replace the norm ball by a small region of the input, where any value is allowed.

## When to use it

Use the algorithm on small models to study how much the boundaries of a model share directions, or to compare the risk of one fixed change with the risk of attacks per input. It is also a cheap test of a defense: if one fixed vector fools a defended model on many inputs, the defense is weak. Use [PGD](/pgd-attack/) per input to measure robust accuracy, since a universal vector gives a weaker attack than one made for each input.

## Pitfalls

- **Rate on the training points only.** Report the rate on new points, as in the network example. A rate measured on the points used to build $v$ overstates the effect.
- **A universal vector is weaker than one attack per input.** In the example, 58 percent against 91 percent at the same radius. Do not use the universal rate as a robust accuracy.
- **The clip.** Inputs at the edge of the box absorb part of $v$. The fooling rate uses $\operatorname{clip}(x + v)$, so compute it in the same way as the algorithm.
- **Order of the data.** On a network the result depends on the order of visits. Shuffle with a fixed seed and report it.
- **Compare with random noise.** A fair report gives the rate of random vectors of the same size, which can be large on a small model, as the 31.7 percent in the example shows.

## Implementations

The code of this page is an abstract model on synthetic data. The algorithm runs only on models and data that the tests build from a fixed seed: affine models with given or seeded weights, and two-layer ReLU networks from `mlkit.tiny_relu_net`, on seeded random points. It never reads real data or touches a real system. The tests check the two examples of the page, edge cases, the projection, that on 500 random binary affine models the rate never passes the Hölder bound and equals it in $\ell_2$, and that on seeded networks the output stays in the ball and the reported rate is correct.

## History

Szegedy et al. (2014) found that adversarial examples made for one network often fool another, and Goodfellow, Shlens and Szegedy (2015) related this to directions in which models are close to linear. Moosavi-Dezfooli, Fawzi, Fawzi and Frossard posted universal perturbations in October 2016 and published them at CVPR 2017. They built them with [DeepFool](/deepfool/) steps on a part of the ImageNet training set, reported high fooling rates on validation images for several networks, and showed that the vectors transfer across networks. They related the effect to shared directions of large curvature of the decision boundaries. Later work found data-free and generative methods.

## References
