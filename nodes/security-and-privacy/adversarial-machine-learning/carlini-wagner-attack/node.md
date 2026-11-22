---
tag: 2XQ46N
kind: algorithm
slug: carlini-wagner-attack
name: Carlini-Wagner attack
aliases:
- CW attack
- C&W attack
area: security-and-privacy/adversarial-machine-learning
level: core
summary: "Finds a small l2 perturbation by minimizing the squared distance plus c times a margin loss on the logits, with a tanh change of variables for the box and a binary search on c."
model: real-ram
complexity:
  vars: {d: the input dimension, T: the number of optimizer steps in one round, s: the number of rounds of the binary search, g: the cost of the logits and two rows of their Jacobian}
  time: {worst: O(s T (g + d))}
  space: {extra: Θ(d)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2016
  people: [Nicholas Carlini, David Wagner]
  note: Carlini and Wagner posted the attacks in August 2016 (IEEE S&P 2017). They compared seven loss functions and three ways to keep the box, and broke defensive distillation.
prereqs: [adversarial-example, logistic-regression]
see_also: [deepfool, pgd-attack, defensive-distillation, jacobian-saliency-map-attack, zeroth-order-optimization-attack, adversarial-transferability, evasion-attack, adam]
sources:
  - url: https://arxiv.org/abs/1608.04644
    title: Nicholas Carlini and David Wagner, Towards evaluating the robustness of neural networks, IEEE Symposium on Security and Privacy 2017, pages 39 to 57
    locator: the seven objective functions and the choice of the margin loss on the logits, the three ways to handle the box (projected gradient, clipped gradient, change of variables), the binary search on c, the l2, l0 and l_infinity attacks, and the evaluation on defensively distilled networks
  - url: https://arxiv.org/abs/1607.04311
    title: Nicholas Carlini and David Wagner, Defensive distillation is not robust to adversarial examples, arXiv 2016
    locator: the first report that distilled networks fall to attacks on the logits
  - url: https://arxiv.org/abs/1312.6199
    title: Christian Szegedy, Wojciech Zaremba, Ilya Sutskever, Joan Bruna, Dumitru Erhan, Ian Goodfellow and Rob Fergus, Intriguing properties of neural networks, ICLR 2014
    locator: Section 4.1 (the box-constrained L-BFGS search for the minimal perturbation, the form that the C&W attack refines)
  - url: https://arxiv.org/abs/1705.07263
    title: Nicholas Carlini and David Wagner, Adversarial examples are not easily detected, bypassing ten detection methods, ACM AISec 2017
    locator: the C&W loss adapted to a classifier joined with a detector
  - url: https://arxiv.org/abs/1709.04114
    title: Pin-Yu Chen, Yash Sharma, Huan Zhang, Jinfeng Yi and Cho-Jui Hsieh, EAD, elastic-net attacks to deep neural networks via adversarial examples, AAAI 2018
    locator: the C&W objective with an added l1 term
  - paper: "Battista Biggio and Fabio Roli, Wild patterns: Ten years after the rise of adversarial machine learning, Pattern Recognition 84, pages 317 to 331, 2018"
    locator: the threat model in three parts used on this page
---

The Carlini-Wagner attack (C&W attack) looks for the smallest change $\eta$ in $\ell_2$ that gives an input a wrong label. It replaces the hard constraint "the label is wrong" by a penalty: it minimizes $\lVert \eta \rVert_2^2 + c \cdot \ell(x + \eta)$, where $\ell$ is a margin loss on the logits that becomes negative once another class wins. It removes the box constraint $x + \eta \in [0,1]^d$ with the change of variables $x' = \tfrac12(\tanh w + 1)$, runs the [Adam](/adam/) optimizer on $w$, and sets the weight $c$ by binary search. Carlini and Wagner (2017) built it to measure how robust a network really is, and with it they broke [defensive distillation](/defensive-distillation/), which had stopped the earlier attacks. With [DeepFool](/deepfool/) it is the standard minimal-distance attack, and it is slower and more precise.

**Threat model.** The goal is untargeted on this page (the paper uses mostly targeted attacks; the change is one line). The knowledge is white box: the attacker computes the logits and their gradients. The capability is a change at test time anywhere in $[0,1]^d$; the attack reports the $\ell_2$ size of the smallest change it found, so the radius $\epsilon$ is an output, not an input.

## In plain words

A fixed-radius attack asks "is there a wrong label within distance $\epsilon$?". The C&W attack asks "how close is the nearest wrong label?".

It sets up a trade. One term wants the change to be small. The other term wants the logit of some wrong class to beat the logit of the true class. A weight $c$ says how much the second term counts. With a small $c$ the change stays tiny but the label may not flip. With a large $c$ the label flips but the change may be bigger than needed. So the attack tries a value of $c$, checks the label, and halves the range of $c$, as in a binary search.

The pixels must stay between $0$ and $1$. The attack writes each pixel as a smooth function of a free number, so that every value of that number gives a valid pixel.

## The problem

Given logits $z(v) \in \mathbb{R}^K$ on $v \in [0,1]^d$ and an input $x$ with $f(x) = y$, the attack approximates
$$\rho_2(x) = \min \{\lVert x' - x \rVert_2 : x' \in [0,1]^d,\ f(x') \ne y\}.$$
It solves, for a weight $c > 0$ and a confidence $\kappa \ge 0$,
$$\min_{w \in \mathbb{R}^d} \lVert x'(w) - x \rVert_2^2 + c\, \ell(x'(w)), \qquad x'(w) = \tfrac12(\tanh w + 1), \qquad \ell(v) = \max\big(z_y(v) - \max_{i \ne y} z_i(v),\ -\kappa\big).$$
The loss $\ell$ is positive while class $y$ wins, and it stops at $-\kappa$ once another class wins by $\kappa$, so the attack does not push further than it needs. For a target class $t$, use $\max(\max_{i \ne t} z_i - z_t, -\kappa)$ instead; this is the function the paper calls $f_6$, the best of the seven it tried.

## The algorithm

```pseudo id=main
CW-L2(z, x, y, c, kappa, T, s)              ▷ x in [0, 1]^d with f(x) = y
L1  lo ← 0; hi ← ∞; best ← none
L2  repeat s times                          ▷ rounds of the binary search on c
L3      w ← artanh(2x - 1)                  ▷ start at x itself
L4      for t ← 1 to T do
L5          x' ← (tanh(w) + 1) / 2          ▷ always in (0, 1)^d
L6          if max_{i≠y} z_i(x') - z_y(x') ≥ kappa and f(x') ≠ y and x' is closer to x than best then best ← x'
L7          w ← Adam step on ∇_w (||x' - x||_2^2 + c · ℓ(x'))
L8      if this round recorded an adversarial x' then hi ← c else lo ← c
L9      c ← (lo + hi) / 2 if hi < ∞ else 10 c
L10 return best
```

Line L3 starts each round at $w$ with $x'(w) = x$; the code keeps $2x_i - 1$ inside $(-1, 1)$ by a margin of $10^{-9}$, so that $\operatorname{artanh}$ stays finite. Line L6 records every adversarial iterate that is closer than the best so far, in every round. Line L7 uses the gradient
$$\frac{\partial}{\partial w_i} = \Big(2(x'_i - x_i) + c\,\big(\partial_i z_y(x') - \partial_i z_j(x')\big)\Big)\cdot \tfrac12\big(1 - \tanh^2 w_i\big),$$
where $j$ is the best other class, and the term in $c$ drops out where $\ell = -\kappa$. Lines L8 and L9 are the binary search: a success means $c$ was large enough, so $c$ goes down; a failure means $c$ goes up, by a factor of $10$ until the first success.

## Example

Take the linear model of the page [adversarial example](/adversarial-example/): $K = 3$, $z(v) = Wv$ with rows $(1, 0)$, $(0, 1)$ and $(-1, -1)$, and $x = (0.6, 0.4)$ with $y = 0$. The nearest wrong label is class $1$, across the line $v_1 = v_2$, at $\rho_2(x) = 0.2/\sqrt2 = 0.141421$. Run the attack with $c = 0.1$, $\kappa = 0$, $T = 100$ Adam steps of rate $0.01$ and $s = 8$ rounds.

Along the direction $(-1, 1)/\sqrt2$ the objective is $\tau^2 + c\,\max(0.2 - \sqrt2\,\tau, 0)$, with its minimum at $\tau = c/\sqrt2$. This crosses the boundary only when $c/\sqrt2 \ge 0.141421$, that is $c \ge 0.2$. The rounds show it:

| round | $c$ | adversarial point found? | closest distance in the round |
|---|---|---|---|
| 1 | 0.1 | no | none |
| 2 | 1 | yes | 0.14151 |
| 3 | 0.55 | yes | 0.14168 |
| 4 | 0.325 | yes | 0.14143 |
| 5 | 0.2125 | yes | 0.14156 |
| 6 | 0.15625 | no | none |
| 7 | 0.184375 | yes | 0.14159 |
| 8 | 0.1703125 | no | none |

The first round fails, so line L9 multiplies $c$ by $10$. Then the search halves the interval each round. Round 7 has $c < 0.2$ and still records an adversarial point: the momentum of Adam carries one iterate just across the line before it comes back, and line L6 records it. This is allowed, because line L6 checks the label of the actual point.

The output is $x^\star = (0.499997, 0.500003)$ from round 4, at distance $0.141426$, which is $1.00003$ times $\rho_2(x)$. The run cost $8 \cdot 100 = 800$ gradients. With $\kappa = 0.1$, the attack must reach $z_1 - z_0 \ge 0.1$, which is at least $0.3/\sqrt2 = 0.212132$ away, and it returns $(0.44998, 0.55002)$ at distance $0.212161$.

## Correctness

**Theorem 1 (a valid output).** If the attack returns a point $x^\star$, then $x^\star \in [0,1]^d$, $f(x^\star) \ne y$, the best other logit is at least $\kappa$ above $z_y(x^\star)$, and $\lVert x^\star - x \rVert_2 \ge \rho_2(x)$.

**Theorem 2.** The output is the closest point to $x$ among all adversarial iterates of all rounds.

**Lemma (the search).** Before the first success, $c$ grows by a factor of $10$ in each round. After it, $lo < c < hi$, and each round halves $hi - lo$.

The change of variables maps $\mathbb{R}^d$ onto $(0,1)^d$ one to one, so every iterate is a valid input (Lemma 1 of the proof page). Line L6 records only points that pass the test, so the output is a real adversarial example, and its distance is an upper bound on $\rho_2(x)$. The full proofs are in `proofs/correctness.md`.

For two classes and an affine model, the objective is convex in $x'$, and the attack gets close to $\rho_2(x)$, as in the example. For a network the objective is not convex, Adam can stop at a local minimum, and success need not be monotone in $c$. So the distance found is an upper bound on $\rho_2(x)$, never a lower bound.

## Complexity

- **Time.** Each step costs one evaluation of the logits and of the gradient of $z_y - z_j$, which is $g$ (one forward and one backward pass), plus $O(d)$ for the distance term, the change of variables and the Adam update. The total is $O(s\, T\, (g + d))$. With the large step counts used on image models, the attack costs thousands of gradients, against one for FGSM and a few for DeepFool.
- **Space.** $\Theta(d)$ for $w$, the two Adam moment vectors and the best point.
- **Model.** These counts are in the real-ram model, with one gradient as a unit of work.

## Properties

- **Deterministic.** The start is $x$, and Adam has no randomness.
- **Minimal, not fixed-radius.** The output distance estimates $\rho_2(x)$ from above. To get robust accuracy at a radius $\epsilon$, count the points whose distance is above $\epsilon$; this is an upper bound on robust accuracy.
- **Uses logits, not probabilities.** The margin on logits does not saturate. A loss on softmax outputs has gradients near $0$ when one class has probability near $1$, which is what made distillation look robust.
- **Confidence.** A larger $\kappa$ gives larger changes that the model labels wrong by a wide margin. Such points [transfer](/adversarial-transferability/) better to other models.

## Variants and improvements

- **Targeted attack.** Use $\ell(v) = \max(\max_{i \ne t} z_i(v) - z_t(v), -\kappa)$.
- **The $\ell_0$ attack.** Run the $\ell_2$ attack, find the coordinate that contributes least, fix it to its value in $x$, and repeat while the attack still succeeds. The coordinates that stay free form a small set, as in the [Jacobian saliency map attack](/jacobian-saliency-map-attack/).
- **The $\ell_\infty$ attack.** Replace $\lVert \eta \rVert_2^2$ by $\sum_i \max(|\eta_i| - \tau, 0)$ and lower $\tau$ after each success.
- **Elastic net (EAD).** Chen et al. (2018) add an $\ell_1$ term to the objective.
- **Black box.** The [ZOO attack](/zeroth-order-optimization-attack/) runs the same objective with gradients estimated from score queries.
- **Detectors.** Carlini and Wagner (2017, AISec) treat a detector and a classifier as one model with one more class, and run the attack on it. They bypassed ten detection methods in this way.

## When to use it

Use the C&W attack to estimate the minimal $\ell_2$ distance to the decision boundary, to evaluate a defense with an attack on the logits, and as a check after FGSM and PGD. It is slow, so it is not used inside training. For a quick estimate use [DeepFool](/deepfool/); for a fixed radius use the [PGD attack](/pgd-attack/), which can run on the C&W margin loss too. To prove that no smaller change exists, use a verifier or a certificate such as [randomized smoothing](/randomized-smoothing/).

## Pitfalls

- **Clipping instead of the change of variables.** Projected or clipped gradient steps work, but Carlini and Wagner found them worse with Adam: clipped coordinates get stuck at $0$ or $1$.
- **A loss on probabilities.** On a network with a saturated softmax, such as a distilled network at temperature $1$, the gradient of the loss on probabilities is almost $0$, and the attack fails. Use the logits.
- **One value of $c$.** A fixed $c$ is either too small (no success) or too large (a bigger change than needed). The binary search matters.
- **Only the last iterate.** The last iterate can be on the wrong side of the boundary. Record the closest adversarial iterate, as line L6 does.
- **Calling a failure robustness.** If all rounds fail, nothing is proved. Increase $T$, $s$ and the start value of $c$ before drawing a conclusion.
- **Ties.** With $\kappa = 0$, a point exactly on the boundary may count as class $y$. A small $\kappa$ avoids points that rounding can flip back.

## Implementations

The code of this page is an abstract model on synthetic data. The attack runs only on models that the tests build from a fixed seed: linear models with given or seeded weights, or two-layer ReLU networks from `mlkit.tiny_relu_net`, on seeded random inputs. It never reads real data or touches a real system. The tests check the example of the page with $\kappa = 0$ and $\kappa = 0.1$, the change of variables and the margin, the gradient of line L7 against central finite differences, the distance against the closed form on 300 random two-class linear models, the lower bound $\rho_2(x)$ on 500 random multiclass linear models, and that every output on random networks is adversarial and inside the box.

## History

Szegedy et al. (2014) found the first adversarial examples of deep networks by a box-constrained L-BFGS search on $c \lVert \eta \rVert + \text{loss}$, with a line search on $c$. Papernot et al. (2016) proposed defensive distillation and reported that it stopped the known attacks. Carlini and Wagner posted a short note in July 2016 that distillation is not robust, and in August 2016 the full paper (IEEE S&P 2017). They compared seven loss functions and three ways to keep the box, chose the margin on logits and the tanh change of variables, and gave attacks for $\ell_0$, $\ell_2$ and $\ell_\infty$. Their attacks succeeded on all the test points of both distilled and undistilled networks on MNIST and CIFAR10 (a measurement in the paper). The attack became the reference for evaluating defenses, and its margin loss is now common in PGD too.

## References
