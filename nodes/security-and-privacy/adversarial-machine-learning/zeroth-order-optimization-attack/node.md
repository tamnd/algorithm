---
tag: 7Y1PKM
kind: algorithm
slug: zeroth-order-optimization-attack
name: Zeroth order optimization attack
aliases:
- ZOO attack
area: security-and-privacy/adversarial-machine-learning
level: advanced
summary: "A black-box attack that sees only the output probabilities. It minimizes the Carlini-Wagner loss by coordinate descent, with each partial derivative estimated by a symmetric difference of two queries."
model: real-ram
complexity:
  vars: {T: the number of steps, d: the input dimension, K: the number of classes, q: the cost of one query}
  time: {worst: O(T (q + d + K))}
  space: {extra: Θ(d)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2017
  people: [Pin-Yu Chen, Huan Zhang, Yash Sharma, Jinfeng Yi, Cho-Jui Hsieh]
  note: Chen, Zhang, Sharma, Yi and Hsieh posted ZOO in August 2017 (AISec 2017), to attack a model through its scores without training a substitute model.
prereqs: [carlini-wagner-attack, finite-differences]
see_also: [boundary-attack, coordinate-descent, adam, adversarial-transferability, evasion-attack, pgd-attack, stochastic-gradient-descent]
sources:
  - url: https://arxiv.org/abs/1708.03999
    title: Pin-Yu Chen, Huan Zhang, Yash Sharma, Jinfeng Yi and Cho-Jui Hsieh, ZOO, zeroth order optimization based black-box attacks to deep neural networks without training substitute models, Proceedings of the 10th ACM Workshop on Artificial Intelligence and Security (AISec 2017), pages 15 to 26
    locator: the loss on log probabilities, the symmetric difference estimate, the coordinate Adam and Newton methods, and the reduction of the attack space for large inputs
  - url: https://arxiv.org/abs/1608.04644
    title: Nicholas Carlini and David Wagner, Towards evaluating the robustness of neural networks, IEEE Symposium on Security and Privacy 2017, pages 39 to 57
    locator: the margin loss with confidence kappa that ZOO adapts
  - url: https://arxiv.org/abs/1712.04248
    title: Wieland Brendel, Jonas Rauber and Matthias Bethge, Decision-based adversarial attacks, reliable attacks against black-box machine learning models, ICLR 2018
    locator: the attack with labels only, for comparison
  - paper: "Battista Biggio and Fabio Roli, Wild patterns: Ten years after the rise of adversarial machine learning, Pattern Recognition 84, pages 317 to 331, 2018"
    locator: the threat model in three parts used on this page
---

The zeroth order optimization attack (ZOO) runs the [Carlini-Wagner attack](/carlini-wagner-attack/) without gradients. It sees only the probabilities that the model returns for a query. It picks one input coordinate at a time, estimates the partial derivative of the attack loss from two queries, at the point moved a little up and a little down along that coordinate, and takes an [Adam](/adam/) step on that coordinate. Chen, Zhang, Sharma, Yi and Hsieh (2017) introduced it. On their MNIST and CIFAR10 models it reached success rates and distances close to the white-box C&W attack, with no substitute model, at the cost of many queries. For large inputs they reduce the number of coordinates and sample the important ones first.

**Threat model.** The goal is untargeted here; the paper also gives the targeted form. The knowledge is black box with scores: a query of $u$ returns the probability vector $p(u)$, and nothing about the weights or gradients. The capability is a change at test time in $[0,1]^d$. The attack reports the $\ell_2$ distance it found after $T$ steps, with exactly $3T$ queries.

## In plain words

The C&W attack needs the slope of its loss, which comes from the gradient of the model. Without the model, you can still measure the slope along one direction: query the input moved a little up and a little down, and divide the difference of the two losses by the distance between them.

Doing this for all $d$ coordinates costs $2d$ queries for one gradient. ZOO does not wait for a full gradient. It picks one coordinate at random, measures its slope, and moves only that coordinate. This is coordinate descent, and each step is cheap.

The loss uses the logarithm of the probabilities. The differences of these logarithms are the differences of the logits, so the loss is the same as the C&W loss.

## The problem

Given probabilities $p(u) = \operatorname{softmax}(z(u))$ on $[0,1]^d$, an input $x$ with label $y$, a constant $c > 0$ and a confidence $\kappa \ge 0$, minimize
$$F(u) = \lVert u - x \rVert_2^2 + c\, \ell(u), \qquad \ell(u) = \max\Big(\ln p_y(u) - \max_{i \ne y} \ln p_i(u),\ -\kappa\Big),$$
over $u \in [0,1]^d$, using only values of $p$. Since $\ln p_y - \ln p_i = z_y - z_i$, the loss $\ell$ is the C&W margin of the logits. The goal is a point of another label that is close to $x$. The best value is the distance $\rho_2(x)$ to the nearest point of another label.

## The algorithm

```pseudo id=main
ZOO(p, x, y, c, kappa, T, lr, h)
L1  u ← x; best ← none
L2  for t ← 1 to T do
L3      i ← a coordinate drawn uniformly from 1..d
L4      g ← (F(u + h e_i) - F(u - h e_i)) / (2h)                 ▷ two queries
L5      update the Adam moments of coordinate i with g (beta1 = 0.9, beta2 = 0.999, with bias correction)
L6      u_i ← clip_[0,1](u_i - lr · m_i / (sqrt(v_i) + 1e-8))
L7      query p(u); if its label is not y and u is closer to x than best then best ← u
L8  return (best, 3T)
```

Line L4 is the symmetric difference along the unit vector $e_i$, with $h = 10^{-4}$, the value of the paper. Line L5 keeps separate Adam moments and step counts for each coordinate, as in ZOO-ADAM. Line L7 keeps the closest adversarial iterate seen so far, not the last iterate. This code uses one fixed $c$, and one coordinate per step. On a GPU the paper estimates a batch of coordinates at once.

## Example

Take the linear model of the page [adversarial example](/adversarial-example/): $K = 3$, logits $z(u) = Wu$ with rows $(1, 0)$, $(0, 1)$ and $(-1, -1)$, and $x = (0.6, 0.4)$ with label $0$. The model returns $p(x) = (0.4949, 0.4052, 0.0999)$. The nearest point of another label is $(0.5, 0.5)$, at $\rho_2 = 0.2/\sqrt2 = 0.14142$. Run ZOO with $c = 1$, $\kappa = 0.05$, $T = 400$, $\mathrm{lr} = 0.005$, $h = 10^{-4}$ and `random.Random(1)`:

| step | coordinate | estimate $g$ | $u$ | $z_1 - z_0$ | distance |
|---|---|---|---|---|---|
| 1 | 0 | 1.0 | (0.595, 0.4) | -0.195 | 0.005 |
| 3 | 1 | -1.0 | (0.59, 0.405) | -0.185 | 0.01118 |
| 20 | 1 | -0.9003 | (0.55513, 0.45477) | -0.10036 | 0.0708 |
| 40 | 0 | 0.8027 | (0.49654, 0.49385) | -0.00269 | 0.13969 |
| 41 | 0 | 0.7931 | (0.49176, 0.49385) | 0.00209 | 0.14326 |
| 400 | 1 | -0.6954 | (0.50283, 0.55339) | 0.05056 | 0.18158 |

At the start the margin term is active, and the estimates are close to the true partial derivatives $\pm 1$ of $c(z_0 - z_1)$, plus the small term $2(u - x)$. Adam then moves each coordinate by about $\mathrm{lr}$ per step. At step 41, after 123 queries, the iterate crosses the boundary at distance $0.14326$, which is $1.013$ times $\rho_2$. After that the iterate goes on to the minimizer of $F$, where the margin reaches $\kappa$, near distance $(0.2 + 0.05)/\sqrt2 = 0.17678$. It never finds a closer adversarial point, so the run returns $(0.49176, 0.49385)$ after 1200 queries. This is the ZOO row in the table of the page [evasion attack](/evasion-attack/).

## Correctness

**Lemma 1.** If no probability is below the floor of the code, $\ell(u) = \max(z_y(u) - \max_{i \ne y} z_i(u), -\kappa)$. So the attack minimizes the C&W loss, and the label from the scores is the label from the logits.

**Lemma 2.** If $\phi(s) = F(u + s e_i)$ is three times differentiable on $[-h, h]$ with $|\phi'''| \le M$, the estimate of line L4 is within $M h^2 / 6$ of $\partial_i F(u)$.

**Theorem 1.** For $T$ steps the attack makes exactly $3T$ queries, every iterate is in $[0,1]^d$, and a returned point is in the box, has a label other than $y$, and is the closest to $x$ of all adversarial iterates. So its distance is at least $\rho_2(x)$ in the box.

Lemma 1 holds because the log of the softmax is $z_i$ minus a term common to all classes. Lemma 2 is Taylor's theorem with the remainder. Near a kink of the max in $\ell$ it does not apply, and rounding adds an error of about $\varepsilon_{\text{mach}} |F| / h$. Theorem 1 follows from the count of queries per step, the clip of line L6, and the rule of line L7. The full proofs are in `proofs/correctness.md`. There is no claim of convergence to a minimum of $F$, and a run can return none.

## Complexity

- **Time.** Each step makes three queries of cost $q$ and computes a distance in $O(d)$ and a margin in $O(K)$. The total is $O(T (q + d + K))$. The distance can be kept up to date in $O(1)$, since only one coordinate changes.
- **Queries.** Exactly $3T$. A full gradient by differences would cost $2d$ queries, so ZOO with $T$ steps touches each coordinate about $T/d$ times. For large $d$ the number of queries is the main cost, which is why the paper reduces the attack space and samples important coordinates.
- **Space.** $\Theta(d)$ for the iterate, the best point and the Adam moments.

## Properties

- **Scores only.** It needs the probabilities, not the gradients. With labels only, use the [boundary attack](/boundary-attack/).
- **The same loss as C&W.** By Lemma 1.
- **Valid output.** A returned point is in the box and has another label (Theorem 1).
- **Randomized.** The coordinate order depends on the seed.
- **Upper bound.** Like every attack, a success gives an upper bound on $\rho_2(x)$, and a failure proves nothing.

## Variants and improvements

- **ZOO-Newton.** Estimate also the second derivative along the coordinate, $(F(u + h e_i) - 2F(u) + F(u - h e_i))/h^2$, and take a Newton step. The paper gives both versions.
- **Search over $c$.** Run the attack for several values of $c$ and keep the smallest success, as in C&W.
- **Attack-space reduction.** Optimize over a smaller grid of coordinates and resize, then refine.
- **Random directions.** Estimate the derivative along random vectors instead of coordinates. Methods of this kind, for example with natural evolution strategies, need fewer queries on image models.
- **Targeted version.** Swap the roles: $\ell(u) = \max(\max_{i \ne t} \ln p_i - \ln p_t, -\kappa)$.

## When to use it

Use ZOO on small models to study the threat model in which only scores are visible, or to compare an evaluation with and without gradients. If a model resists gradient attacks but not ZOO, its gradients were masked. For a white-box evaluation, the [Carlini-Wagner attack](/carlini-wagner-attack/) gives the same loss with exact gradients and far less work.

## Pitfalls

- **The step $h$.** A large $h$ biases the estimate, and a tiny $h$ is lost in rounding. Also, scores rounded by the model make small differences zero.
- **Kinks.** Near a change of the active class in the max, or of a ReLU, the estimate mixes two slopes.
- **Keep the best iterate.** The iterate moves past the boundary toward the minimizer of $F$, as in the example. The last iterate is often farther than the best one.
- **A fixed $c$.** Too small a $c$ never crosses the boundary, too large a $c$ gives large distances. Search over $c$ or report it.
- **Query cost grows with $d$.** Results on small models do not carry over to high dimensions without the reductions of the paper.

## Implementations

The code of this page is an abstract model on synthetic data. The attack runs only on score functions that the tests build from a fixed seed: softmax outputs of affine models with given or seeded weights, and of two-layer ReLU networks from `mlkit.tiny_relu_net`, on seeded random inputs, with the coordinates drawn from `random.Random` seeded in the test. It never reads real data or touches a real system. The tests check the example of the page, edge cases, Lemma 1 on 500 random logit vectors, the estimate of line L4 against the exact derivative on 500 random affine models, the query count, the box and the lower bound on seeded binary linear models, and that results on seeded networks are adversarial.

## History

Black-box attacks before ZOO trained a substitute model and relied on [transferability](/adversarial-transferability/), as in Papernot et al. (2017). Chen, Zhang, Sharma, Yi and Hsieh posted ZOO in August 2017 and published it at AISec 2017. They used the C&W loss on log probabilities, coordinate Adam and Newton steps with symmetric differences, and reductions of the attack space for ImageNet models. Later score-based attacks estimated gradients along random directions or searched with fewer queries, and the [boundary attack](/boundary-attack/) (2018) removed the need for scores.

## References
