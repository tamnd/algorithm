---
tag: M591DH
kind: algorithm
slug: adagrad
name: AdaGrad
aliases:
- adaptive gradient
- adaptive gradient algorithm
- diagonal AdaGrad
area: optimization/gradient-methods
level: core
summary: Scales each coordinate's step by the inverse root of its accumulated squared gradients.
solves: [stochastic-optimization]
model: real-ram
complexity:
  vars: {d: the dimension, k: the number of rounds, g: the cost of one stochastic gradient, D: the largest side of the box, G: the bound on the largest gradient coordinate, ε: the target expected gap of the averaged point}
  time: {worst: O(k (g + d))}
  space: {extra: Θ(d)}
  steps: {expected: "⌈2 D^2 d^2 G^2 / ε^2⌉"}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2011
  people: [John Duchi, Elad Hazan, Yoram Singer]
  note: Duchi, Hazan and Singer (2011) introduced AdaGrad with regret bounds that adapt to the observed gradients; McMahan and Streeter (2010) gave closely related adaptive bounds at the same time.
prereqs: [online-convex-optimization, regret, stochastic-gradient-descent, projected-gradient-descent]
see_also: [rmsprop, adadelta, adam, stochastic-gradient-descent, online-convex-optimization, mirror-descent, regret, stochastic-optimization]
sources:
  - paper: "John Duchi, Elad Hazan and Yoram Singer, Adaptive subgradient methods for online learning and stochastic optimization, Journal of Machine Learning Research 12, 2011, pages 2121 to 2159"
    locator: Section 1.3 and Figure 1 for the diagonal and full-matrix updates, Theorem 5 for the diagonal regret bound, Corollary 6 for the bound with the step D_∞ / √2
  - url: https://arxiv.org/abs/1002.4908
    title: H. Brendan McMahan and Matthew Streeter, Adaptive bound optimization for online convex optimization, COLT 2010
    locator: Sections 3 and 4, per-coordinate adaptive regularization and its regret bound on a box
  - url: https://arxiv.org/abs/1806.01811
    title: Rachel Ward, Xiaoxia Wu and Léon Bottou, AdaGrad stepsizes, Sharp convergence over nonconvex landscapes, Journal of Machine Learning Research 21(219), 2020
    locator: Theorems 2.1 and 2.2, AdaGrad-Norm on smooth nonconvex functions with the rate O(log k / √k) without knowledge of the Lipschitz constant
  - paper: doi:10.1109/TIT.2004.833339
    title: Nicolò Cesa-Bianchi, Alex Conconi and Claudio Gentile, On the generalization ability of on-line learning algorithms, IEEE Transactions on Information Theory 50(9), 2004
    locator: pages 2050 to 2057, the online to batch conversion used for the stochastic corollary
  - paper: doi:10.3115/v1/D14-1162
    title: Jeffrey Pennington, Richard Socher and Christopher D. Manning, GloVe, Global vectors for word representation, EMNLP 2014
    locator: Section 4.2, training of word vectors with AdaGrad
---

AdaGrad is an [online](/online-convex-optimization/) and stochastic gradient method that gives each coordinate its own step size, $\eta$ divided by the square root of the sum of the squares of all past gradients in that coordinate. Coordinates with large or frequent gradients get small steps, and rare coordinates keep large steps. On a box of side $D$, diagonal AdaGrad has [regret](/regret/) at most $\sqrt{2}D\sum_i\lVert g_{1:T,i}\rVert_2$ with no tuning to the gradient sizes, which is much smaller than the bound of plain [stochastic gradient descent](/stochastic-gradient-descent/) when the gradients are sparse. Duchi, Hazan and Singer introduced it in 2011, and it led to [RMSProp](/rmsprop/) and [Adam](/adam/).

## In plain words

Plain gradient descent uses one step size for every direction. If some features of the data are rare, their directions get few useful updates, and a step small enough for the common features is far too small for the rare ones.

AdaGrad keeps a running total of how much each direction has moved. Directions that have seen a lot of gradient take smaller and smaller steps; directions that have seen little keep taking big steps. Nobody has to tune a separate step for each direction, and the method never needs to know how large the gradients will be.

## The problem

In online convex optimization, the method plays $x_t$ in a closed convex set $X$, a convex loss $f_t$ is revealed, and the method receives a subgradient $g_t \in \partial f_t(x_t)$. The goal is small regret $R_T(u) = \sum_t(f_t(x_t) - f_t(u))$ for every $u \in X$. In [stochastic optimization](/stochastic-optimization/), $f_t = f(\cdot, \xi_t)$ with independent samples, and the averaged iterate solves $\min_X\mathbb{E}f(x, \xi)$. The theorem below takes $X = \prod_i[l_i, h_i]$, a box with sides $D_i \le D_\infty$.

## The algorithm

```pseudo id=main
ADAGRAD(∇f, x₁, η, T, box [l, h])
L1  x ← x₁;  s ← 0 ∈ ℝ^d
L2  for t ← 1 to T do
L3      g ← ∇fₜ(x)                         ▷ (sub)gradient of the loss of round t
L4      sᵢ ← sᵢ + gᵢ² for every i
L5      xᵢ ← xᵢ − η gᵢ / √sᵢ for every i with sᵢ > 0
L6      xᵢ ← min(max(xᵢ, lᵢ), hᵢ)           ▷ projection onto the box
L7  return x₁, …, x_{T+1}
```

Line L5 uses $\sqrt{s_i}$, which includes the current gradient. Many codes write $\eta g_i/(\sqrt{s_i} + \epsilon)$ with a small $\epsilon$ to avoid a division by zero; the regret proof uses $\epsilon = 0$ and skips coordinates whose gradients have all been zero. For a general convex set, line L6 is the projection in the norm $\sum_i\sqrt{s_i}\,z_i^2$, which for a box is the clip.

## Example

Take the box $[-1, 1]^2$, $x_1 = (0, 0)$, $\eta = 1$ and linear losses $f_t(x) = \langle g_t, x\rangle$. Coordinate 1 gets a gradient in every round, and coordinate 2 gets one gradient, in round 3.

| $t$ | $x_t$ | $g_t$ | $\sqrt{s_1}$ | $\sqrt{s_2}$ |
|---|---|---|---|---|
| 1 | (0, 0) | (1, 0) | 1 | 0 |
| 2 | (−1, 0) | (−1, 0) | 1.41421 | 0 |
| 3 | (−0.29289, 0) | (1, 2) | 1.73205 | 2 |
| 4 | (−0.87024, −1) | (1, 0) | 2 | 2 |
| 5 | (−1, −1) | (1, 0) | 2.23607 | 2 |
| 6 | (−1, −1) | (0.5, 0) | 2.29129 | 2 |

The single gradient in coordinate 2 moves it by $\eta \cdot 2/2 = 1$, straight to the boundary, while coordinate 1 takes steps that shrink like $1/\sqrt{t}$. The total loss is $-1.66314$; the best fixed point is the vertex $(-1, -1)$ with loss $-5.5$, so the regret is $3.83686$. The bound $(D^2/(2\eta) + \eta)\sum_i\lVert g_{1:6,i}\rVert_2$ with $D = 2$ is $3 \cdot (2.29129 + 2) = 12.874$.

## Correctness

The proof below works one coordinate at a time, because the box and the diagonal metric are separable.

- **One coordinate.** Clipping does not increase the distance to any $u_i$ in the interval, so $g_{t,i}(x_{t,i} - u_i) \le \frac{G_{t,i}}{2\eta}\big((x_{t,i} - u_i)^2 - (x_{t+1,i} - u_i)^2\big) + \frac{\eta}{2}g_{t,i}^2/G_{t,i}$, where $G_{t,i} = \sqrt{s_i}$ after round $t$.
- **Telescoping.** Since $G_{t,i}$ only grows and each squared distance is at most $D_i^2$, the first terms add up to at most $D_i^2G_{T,i}/(2\eta)$.
- **The sum lemma.** $\sum_ta_t/\sqrt{a_1 + \dots + a_t} \le 2\sqrt{a_1 + \dots + a_T}$, so the second terms add up to at most $\eta G_{T,i}$.
- **Regret.** By convexity, $R_T(u) \le \sum_i\big(\frac{D_i^2}{2\eta} + \eta\big)\lVert g_{1:T,i}\rVert_2$, which is $\sqrt{2}D_\infty\sum_i\lVert g_{1:T,i}\rVert_2$ for $\eta = D_\infty/\sqrt{2}$.

The regret bound holds for every sequence of convex losses. With independent samples, the online to batch conversion gives $\mathbb{E}F(\bar{x}_T) - F^* \le \mathbb{E}R_T(x^*)/T$.

## Complexity

Each round costs one gradient and $O(d)$ arithmetic, with $\Theta(d)$ extra memory for the sums. If every gradient coordinate is at most $G$ in absolute value, then $\sum_i\lVert g_{1:T,i}\rVert_2 \le dG\sqrt{T}$, so $\mathbb{E}F(\bar{x}_T) - F^* \le \sqrt{2}DdG/\sqrt{T}$, and $\lceil2D^2d^2G^2/\varepsilon^2\rceil$ rounds give accuracy $\varepsilon$. This worst case is about the same as for SGD on the box; the gain comes when coordinate $i$ is nonzero in only $T_i$ rounds, and the sum drops to at most $G\sum_i\sqrt{T_i}$.

## Properties

- **Adaptive without tuning to scale.** The bound holds for every $\eta > 0$ and does not need a bound on the gradients; only $\eta$ trades off the two terms.
- **Steps never increase.** $\eta/\sqrt{s_i}$ is nonincreasing in each coordinate, which is what the proof uses and also what makes the method slow in long nonconvex runs.
- **Scale invariance per coordinate.** Multiplying the gradients in one coordinate by $c > 0$ does not change the steps in that coordinate.
- **Deterministic** given the loss sequence. With sampled gradients, the randomness comes only from the oracle.
- **Nonconvex.** The scalar version AdaGrad-Norm, with one step $\eta/\sqrt{\sum_s\lVert g_s\rVert^2}$, finds a point with a small gradient on smooth nonconvex functions at the rate $O(\log k/\sqrt{k})$ without knowing the Lipschitz constant (Ward, Wu and Bottou 2020).

## Variants and improvements

- **Full-matrix AdaGrad.** Use $H_t = (\sum_sg_sg_s^\top)^{1/2}$, which adapts to correlated directions at a cost of $O(d^2)$ to $O(d^3)$ per step.
- **AdaGrad with dual averaging or composite terms.** Add a regularizer such as $\lambda\lVert x\rVert_1$ and solve the per-coordinate step in closed form, which gives sparse solutions (Duchi, Hazan and Singer 2011).
- **[RMSProp](/rmsprop/).** Replace the sum by an exponential moving average, so old gradients are forgotten and the steps do not shrink to zero.
- **[Adadelta](/adadelta/) and [Adam](/adam/).** Add a unit correction or momentum to the RMSProp idea.
- **AdaGrad-Norm.** One adaptive scalar step for all coordinates.

## When to use it

Use AdaGrad for convex problems with sparse features, such as linear models on text or click data and word embeddings, where rare features need large steps. It also suits online learning, where the regret bound holds for any sequence. For deep networks trained for many steps, its steps shrink too much, and RMSProp or Adam are the usual choices.

## Pitfalls

- **Vanishing steps.** The sums grow without bound, so after many steps learning nearly stops, even when the problem changes.
- **First large gradient.** A single large gradient early in training makes that coordinate's step small for the rest of the run.
- **The $\epsilon$ term.** A large $\epsilon$ changes the method into SGD with a fixed step for small gradients; a tiny one can give huge first steps.
- **Comparing bounds.** The regret bound is in terms of $D_\infty$, the side of a box; on a Euclidean ball the right comparison uses a different diameter, and AdaGrad need not be better.

## Implementations

## History

Duchi, Hazan and Singer (2011) introduced AdaGrad, motivated by sparse features in online learning, and proved regret bounds that adapt to the gradients seen. McMahan and Streeter (2010) proved closely related per-coordinate bounds in the same period. The method became a standard tool for training word embeddings (Pennington, Socher and Manning 2014) and large linear models, and its accumulated sums were replaced by moving averages in RMSProp and Adam. Ward, Wu and Bottou (2020) analysed its scalar form on nonconvex problems.

## References
