---
tag: 2WWJMG
kind: algorithm
slug: interval-bound-propagation
name: Interval bound propagation
aliases:
- IBP
area: security-and-privacy/adversarial-machine-learning
level: advanced
summary: "Pushes an input box through the network layer by layer with interval arithmetic, to certify robustness and to train certifiably robust models."
model: real-ram
complexity:
  vars: {N: the number of weights of the network, n: the width of the widest layer, d: the input dimension}
  time: {worst: Θ(N + d)}
  space: {extra: Θ(n + d)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2018
  people: [Matthew Mirman, Timon Gehr, Martin Vechev, Sven Gowal, Krishnamurthy Dvijotham, Robert Stanforth]
  note: Mirman, Gehr and Vechev trained networks through the box domain of abstract interpretation at ICML 2018, and Gowal et al. showed later in 2018 that plain interval bounds with a careful schedule train strongly verifiable networks.
prereqs: [relu, interval-arithmetic, adversarial-example]
see_also: [neural-network-verification-problem, linear-bound-propagation, reluplex, randomized-smoothing, abstract-interpretation, interval-domain, adversarial-training, pgd-attack]
sources:
  - url: https://arxiv.org/abs/1810.12715
    title: Sven Gowal, Krishnamurthy Dvijotham, Robert Stanforth, Rudy Bunel, Chongli Qin, Jonathan Uesato, Relja Arandjelovic, Timothy Mann and Pushmeet Kohli, On the effectiveness of interval bound propagation for training verifiably robust models, arXiv 2018 (a later version appeared at ICCV 2019 as Scalable verified training for provably robust image classification)
    locator: the interval bounds in center and radius form, the margin specification folded into the last layer, and the training loss with the schedules for epsilon and kappa
  - url: https://proceedings.mlr.press/v80/mirman18b.html
    title: Matthew Mirman, Timon Gehr and Martin Vechev, Differentiable abstract interpretation for provably robust neural networks, ICML 2018, PMLR 80, pages 3578 to 3586
    locator: training through the box domain and the zonotope domain of abstract interpretation
  - url: https://proceedings.mlr.press/v80/wong18a.html
    title: Eric Wong and J. Zico Kolter, Provable defenses against adversarial examples via the convex outer adversarial polytope, ICML 2018, PMLR 80, pages 5286 to 5295
    locator: the linear relaxation that gives tighter bounds than intervals, for comparison
  - url: https://arxiv.org/abs/1902.06705
    title: Nicholas Carlini, Anish Athalye, Nicolas Papernot, Wieland Brendel, Jonas Rauber, Dimitris Tsipras, Ian Goodfellow, Aleksander Madry and Alexey Kurakin, On evaluating adversarial robustness, arXiv 2019
    locator: the difference between a certified lower bound and an attack upper bound on robust accuracy
  - paper: "Battista Biggio and Fabio Roli, Wild patterns: Ten years after the rise of adversarial machine learning, Pattern Recognition 84, pages 317 to 331, 2018"
    locator: the threat model in three parts used on this page
---

Interval bound propagation (IBP) computes, for every output of a ReLU network, a lower and an upper bound that hold for every input in a box. It pushes the box through the network one layer at a time. An affine layer maps a box with center $\mu$ and radius $r$ into the box with center $W\mu + b$ and radius $|W| r$, and a ReLU maps an interval $[l, u]$ to $[\max(l, 0), \max(u, 0)]$. To certify that a classifier keeps the label $y$ on $B_\infty(x, \epsilon) \cap [0,1]^d$, IBP bounds the margins $z_y - z_j$ from below; if every lower bound is positive, no input of the box changes the label. The method is sound and incomplete: a positive answer is a proof, a negative answer proves nothing. It costs about two forward passes, so Gowal et al. (2018) could use it inside the training loss of large networks.

**Threat model.** IBP is a defense, so the threat model is the one that the certificate covers. The goal can be untargeted or targeted, since a certificate for all labels $j \ne y$ covers both. The knowledge is unlimited: the certificate holds against a white-box attacker who knows the weights. The capability is a change at test time within $B_\infty(x, \epsilon) \cap [0,1]^d$.

## In plain words

Suppose each input number may move a little, inside a known range. IBP asks how far each number in the next layer can move as a result, and it answers with a range again: the smallest and the largest value that the number can take.

For a weighted sum the answer is simple. The middle of the range is the weighted sum of the middles, and the width grows by the size of each weight, whatever its sign. For a ReLU, which sets negative numbers to zero, the range is cut at zero.

At the end the method has a range for each output score. If the lowest possible score of the right class is above the highest possible score of every other class, no allowed change can make the model wrong. If not, the method cannot tell, because its ranges are often too wide.

## The problem

Take a network with logits $z(x) = W_K\, \mathrm{relu}(\cdots \mathrm{relu}(W_1 x + b_1) \cdots) + b_K$ in $\mathbb{R}^k$, an input $x \in [0,1]^d$ with label $y$ and a radius $\epsilon \ge 0$. Let $S = B_\infty(x, \epsilon) \cap [0,1]^d$. The verification question of the [neural network verification problem](/neural-network-verification-problem/) is whether $z_y(x') - z_j(x') > 0$ for every $x' \in S$ and every $j \ne y$. IBP answers a weaker question: it computes numbers $\underline m_j$ with $\underline m_j \le \min_{x' \in S} (z_y(x') - z_j(x'))$, and it reports "certified" when every $\underline m_j > 0$.

## The algorithm

```pseudo id=main
IBP(layers (W_1, b_1) .. (W_K, b_K), l, u)    ▷ the box l <= x <= u
L1  l, u ← the input box
L2  for k ← 1 to K do
L3      mu ← (u + l)/2, r ← (u - l)/2           ▷ center and radius
L4      mu ← W_k mu + b_k
L5      r ← |W_k| r                             ▷ |W_k| takes the absolute value of each entry
L6      l ← mu - r, u ← mu + r
L7      if k < K then                           ▷ a ReLU follows every layer but the last
L8          l ← max(l, 0), u ← max(u, 0)
L9  return (l, u)
CERTIFY-IBP(layers, x, y, epsilon)
L10 l ← max(x - epsilon, 0), u ← min(x + epsilon, 1)
L11 replace (W_K, b_K) by the rows W_K[y] - W_K[j] and the entries b_K[y] - b_K[j], for j != y
L12 (l', u') ← IBP(layers, l, u)
L13 return min_j l'_j > 0
```

Line L1 starts from the input box. Line L3 writes the current box in center and radius form. Lines L4 and L5 apply the affine layer: the center moves like a point, and the radius grows by the absolute weights, because the term $W(v - \mu)$ is largest in coordinate $i$ when each $v_t - \mu_t$ has the sign of $W_{it}$. Line L8 applies the ReLU to both ends, which is exact for one monotone function of one variable.

Line L10 builds the box of the threat model, cut to the valid range. Line L11 folds the margins $z_y - z_j$ into the last layer, so that line L12 bounds each margin directly and not the two logits on their own. Line L13 needs a strictly positive lower bound, so a tie counts as not certified.

## Example

Take $d = 2$, two hidden ReLUs and two logits, with
$W_1 = \begin{pmatrix} 2 & -1 \\ 1 & -2 \end{pmatrix}$, $b_1 = (0, 0.5)$, $W_2 = \begin{pmatrix} 1 & -1 \\ -2 & 2 \end{pmatrix}$, $b_2 = (1, 0)$.
At $x = (0.5, 0.5)$ the hidden layer is $(0.5, 0)$ and the logits are $z(x) = (1.5, -1)$, so $y = 0$. Line L11 gives the margin $m = z_0 - z_1 = 3 h_1 - 3 h_2 + 1$, where $h = \mathrm{relu}(W_1 x + b_1)$. Take $\epsilon = 0.25$, so the box of line L10 is $[0.25, 0.75]^2$.

| step | center $\mu$ | radius $r$ | lower $l$ | upper $u$ |
|---|---|---|---|---|
| input (L1, L3) | $(0.5, 0.5)$ | $(0.25, 0.25)$ | $(0.25, 0.25)$ | $(0.75, 0.75)$ |
| layer 1 (L4 to L6) | $(0.5, 0)$ | $(0.75, 0.75)$ | $(-0.25, -0.75)$ | $(1.25, 0.75)$ |
| ReLU (L8) | | | $(0, 0)$ | $(1.25, 0.75)$ |
| margin layer (L3 to L6) | $1.75$ | $3$ | $-1.25$ | $4.75$ |

The lower bound $-1.25$ is negative, so IBP does not certify the point at $\epsilon = 0.25$. The point is robust all the same: the true minimum of $m$ over the box is $1$, which [Reluplex](/reluplex/) proves exactly and [linear bound propagation](/linear-bound-propagation/) bounds from below by $0.25$. The loss comes from line L5 in the margin layer: the radius $3 \cdot 0.625 + 3 \cdot 0.375$ treats $h_1$ and $h_2$ as free to move in opposite directions, while both depend on the same two inputs.

At $\epsilon = 0.1$ both hidden bounds are $[0.2, 0.8]$ and $[-0.3, 0.3]$, and the margin bound is $2.05 - 1.35 = 0.7 > 0$, so IBP certifies. For $\epsilon \le 1/6$ the first hidden unit stays positive on the box, and the bound is $2.5 - 18\epsilon$. It is positive exactly when $\epsilon < 5/36 \approx 0.139$, so that is the radius that IBP certifies. The exact robust radius of this point is $5/12 \approx 0.417$.

## Correctness

**Theorem (soundness).** If $l \le u$ on input, then for every $v$ with $l \le v \le u$, the output $f(v)$ of the layers satisfies $l' \le f(v) \le u'$ for the pair $(l', u')$ of line L9. So if CERTIFY-IBP returns true, then $z_y(x') > z_j(x')$ for every $x' \in B_\infty(x, \epsilon) \cap [0,1]^d$ and every $j \ne y$.

The proof is an induction on the layers. If $|v_t - \mu_t| \le r_t$ for every $t$, then $|(Wv + b)_i - (W\mu + b)_i| = |\sum_t W_{it}(v_t - \mu_t)| \le \sum_t |W_{it}| r_t$, which is lines L4 to L6. The ReLU is nondecreasing, so $l \le a \le u$ gives $\max(l, 0) \le \max(a, 0) \le \max(u, 0)$, which is line L8. After line L11 the outputs of the last layer are exactly the margins, so positive lower bounds rule out every label change. The bound of one affine layer is also tight: each end is reached at a corner of the box. The full proof is in `proofs/correctness.md`.

The theorem is about exact arithmetic. With floating point numbers, the bounds can be off by rounding; a verifier that must be sound on floats rounds every lower bound down and every upper bound up, as in [interval arithmetic](/interval-arithmetic/).

## Complexity

- **Time.** Each layer costs one product with $W_k$ (line L4) and one with $|W_k|$ (line L5), so the total is $\Theta(N + d)$ for $N$ weights, about twice a forward pass. Line L11 costs $O(k h)$ for the last layer with $h$ inputs.
- **Space.** $\Theta(n + d)$ besides the weights, for the center and the radius of the current layer.
- **Training.** In IBP training the bounds are part of the loss, so a training step costs about as much as a step of normal training with two extra passes.

## Properties

- **Sound, not complete.** A certificate is a proof (a theorem). A failure says nothing, as in the example.
- **A lower bound on robust accuracy.** The fraction of test points that IBP certifies is a lower bound on the robust accuracy, and an attack such as the [PGD attack](/pgd-attack/) gives an upper bound.
- **Exact for one layer.** For one affine layer, or a network whose hidden units are all stable on the box, the bound of each output alone is tight.
- **Monotone in the box.** A smaller input box gives smaller or equal output boxes, so the certified radius is well defined and can be found by bisection.
- **Loose for deep networks.** The width grows by a factor of about $\lVert |W_k| \rVert$ per layer and ignores all correlations between units, so for a network trained without IBP the bounds are often useless after a few layers (a measurement in the papers below).

## Variants and improvements

- **IBP training.** Gowal et al. (2018) minimize $\kappa\, L(z(x), y) + (1 - \kappa)\, L(\hat z, y)$, where $\hat z$ is the worst-case logit vector built from the lower bounds of the margins. Training ramps $\epsilon$ up from 0 and $\kappa$ down from 1, so the network learns to keep its bounds tight. Networks trained this way are often certified by IBP itself.
- **Abstract domains.** IBP is [abstract interpretation](/abstract-interpretation/) with the [interval domain](/interval-domain/). Mirman, Gehr and Vechev (2018) also train with zonotopes, which keep linear correlations.
- **Linear bounds.** [Linear bound propagation](/linear-bound-propagation/) (CROWN and its relatives) bounds each unit by linear functions of the input. It is usually tighter and costs more. CROWN-IBP uses IBP for the hidden layers and a linear bound for the last layer, as a cheaper middle ground.
- **Complete verification.** IBP bounds are the first step of branch-and-bound verifiers and the bound tightening step of [Reluplex](/reluplex/) and of [mixed integer programming](/mixed-integer-programming/) encodings: a unit whose interval does not contain 0 needs no case split.

## When to use it

Use IBP as the cheapest sound check, to decide quickly that many points are safe, to tighten bounds before an exact verifier, and above all to train networks that are certifiable. Do not use it to verify a network trained without it: the bounds are usually too loose, and a linear bound or an exact method is needed. For large $\ell_2$ radii on large models, [randomized smoothing](/randomized-smoothing/) gives a different, probabilistic certificate.

## Pitfalls

- **Bounds from the ends instead of the center.** Computing $W l + b$ and $W u + b$ at lines L4 and L5 is wrong as soon as $W$ has a negative entry: the "lower" bound can be above the "upper" bound, and the result is not sound. Use the center and radius form, or split $W$ into its positive and negative parts.
- **Bounding the logits apart.** Without line L11, the check $\underline z_y > \overline z_j$ ignores that $z_y$ and $z_j$ depend on the same hidden units. It is still sound but looser than the margin bound. Fold the margins into the last layer.
- **Floating point.** Lines L4 to L6 in floats can round a bound inward. A certificate meant as a proof must round outward, or use exact rational arithmetic. The code of this page uses plain floats, so its tests compare with a small tolerance.
- **The box outside the valid range.** If line L10 does not cut the box to $[0,1]^d$, the certificate covers more points than the threat model asks for and fails more often. It is not wrong, only weaker.
- **A ReLU after the last layer.** If line L7 also applies a ReLU after layer $K$, the margin bounds are cut at 0 and lose their meaning as logits.

## Implementations

The code of this page is an abstract model on synthetic data. The verifier runs only on small ReLU networks that the tests build from a fixed seed, either with random weights or from `mlkit.tiny_relu_net`, on seeded random inputs. It never reads real data or touches a real system. The tests check the example table and the radius $5/36$, that a point box gives the forward pass, that one affine layer is tight at the corners, and soundness on 500 random networks against the exact range from an enumeration of all activation patterns and against dense sampling. They also check that nested boxes give nested bounds and that no sampled input breaks a certified point.

## History

Interval arithmetic is old, and abstract interpretation with intervals goes back to Cousot and Cousot in 1977. Its use for neural networks came with the search for certificates after adversarial examples were found. Gehr et al. (2018) verified networks with abstract interpretation in the AI2 system, and Mirman, Gehr and Vechev (ICML 2018) made the abstract domains differentiable, so that a network could be trained to make its own bounds tight. Gowal et al. posted "On the effectiveness of interval bound propagation for training verifiably robust models" in October 2018. They showed that the simplest domain, intervals, gives strong verified accuracy when the training schedule is chosen with care, at a small cost per step. IBP training then became a common baseline for certified training, and later work such as CROWN-IBP mixed it with linear bounds.

## References
