---
tag: X8NYQC
kind: algorithm
slug: online-gradient-descent
name: Online gradient descent
aliases:
- projected online gradient descent
- OGD
- greedy projection
area: online-and-streaming/competitive-analysis
level: advanced
summary: Take a projected gradient step on each revealed convex loss. With step D/(G sqrt t) the regret is at most (3/2)GD sqrt(T); strongly convex losses give O(log T).
solves: [online-convex-optimization]
model: real-ram
complexity:
  vars: {d: the dimension of the decision set, T: the number of rounds}
  time: {worst: Θ(d·T)}
  space: {extra: Θ(d)}
properties: {online: true, deterministic: true, comparison: false, recursive: false}
history:
  year: 2003
  people: [Martin Zinkevich]
  note: Zinkevich (2003) defined online convex programming and proved the O(sqrt(T)) regret of greedy projection; Hazan, Agarwal and Kale (2007) proved O(log T) for strongly convex losses with step 1/(lambda t).
prereqs: [online-convex-optimization, subgradient, projected-gradient-descent, regret]
see_also: [gradient-descent, stochastic-gradient-descent, mirror-descent, adagrad, follow-the-leader, doubling-trick, strong-convexity, multiplicative-weights-update]
sources:
  - paper: "Martin Zinkevich, Online convex programming and generalized infinitesimal gradient ascent, Proceedings of the 20th International Conference on Machine Learning (ICML), 2003, 928-936"
    locator: Section 2 (the greedy projection algorithm, Theorem 1 with step 1/sqrt(t), and the dynamic regret bound)
  - paper: doi:10.1007/s10994-007-5016-8
    title: "Elad Hazan, Amit Agarwal and Satyen Kale, Logarithmic regret algorithms for online convex optimization, Machine Learning 69(2-3) (2007), 169-192"
    locator: Theorem 1 (online gradient descent with step 1/(H t) has regret at most (G^2 / (2H)) (1 + log T) for H-strongly convex losses)
  - paper: doi:10.1561/2400000013
    title: "Elad Hazan, Introduction to online convex optimization, Foundations and Trends in Optimization 2(3-4) (2016), 157-325"
    locator: Section 3.1 (Theorem 3.1, the bound (3/2) G D sqrt(T)), Section 3.2 (the lower bound) and Section 3.3 (logarithmic regret for strongly convex losses)
  - paper: doi:10.1561/2200000018
    title: "Shai Shalev-Shwartz, Online learning and online convex optimization, Foundations and Trends in Machine Learning 4(2) (2012), 107-194"
    locator: Section 2.4 (online gradient descent as linearized follow the regularized leader) and Chapter 3
---

Online gradient descent (OGD) is the basic algorithm for [online convex optimization](/online-convex-optimization/): after each round it takes one step against a [subgradient](/subgradient/) of the loss it just paid, and projects the result back onto the convex decision set. Zinkevich (2003) showed that with steps $\eta_t = D/(G\sqrt t)$ its [regret](/regret/) is at most $\frac32 GD\sqrt T$ against every adversary, which is optimal up to a constant; for $\lambda$-strongly convex losses, steps $1/(\lambda t)$ give $\frac{G^2}{2\lambda}(1 + \ln T)$. This page is the online-learning view; the same update with a fixed objective is [projected gradient descent](/projected-gradient-descent/), and with random samples of one objective it is [stochastic gradient descent](/stochastic-gradient-descent/).

## In plain words

Each round you choose a point, and then you learn a bowl-shaped cost and pay its value at your point. Before the next round you move a little in the downhill direction of that cost, and if the move takes you out of the allowed region, you go back to the nearest allowed point.

The costs can change in any way, so no single move is safe. But each move brings you closer to the best fixed point, or the cost of that round was small. The steps get smaller over time, so you do not jump too far after one bad round. Your total cost then exceeds that of the best fixed point by an amount that grows only like the square root of the number of rounds.

## The problem

A closed convex set $K \subset \mathbb{R}^d$ of diameter $D$ is given. In each round $t = 1, \ldots, T$ the learner plays $x_t \in K$, then the adversary reveals a convex loss $f_t$, and the learner pays $f_t(x_t)$. The adversary may see $x_1, \ldots, x_t$ before it chooses $f_t$. The learner needs only one subgradient $g_t \in \partial f_t(x_t)$, with $\|g_t\| \le G$. The goal is to make the regret $\sum_t f_t(x_t) - \min_{x \in K}\sum_t f_t(x)$ small.

## The algorithm

```pseudo id=main
ONLINE-GRADIENT-DESCENT(K, x_1, η_1, η_2, …)
L1  x ← x_1, a point of K
L2  for t ← 1 to T do
L3      play x_t ← x
L4      receive f_t and pay f_t(x_t)
L5      g_t ← a subgradient of f_t at x_t
L6      y ← x_t − η_t g_t
L7      x ← Π_K(y)                  ▷ the point of K nearest to y
```

Steps for the two main cases:

- **Convex, $G$-Lipschitz losses:** $\eta_t = D/(G\sqrt t)$. Regret at most $\frac32 GD\sqrt T$. If $T$ is known, the fixed step $D/(G\sqrt T)$ gives $GD\sqrt T$.
- **$\lambda$-strongly convex losses:** $\eta_t = 1/(\lambda t)$. Regret at most $\frac{G^2}{2\lambda}(1 + \ln T)$.

For a box, $\Pi_K$ clips each coordinate to its interval; for a Euclidean ball of radius $r$ it scales $y$ by $\min(1, r/\|y\|)$; for the simplex it takes $O(d \log d)$ time by sorting.

## Example

Take $K = [0, 1]$, $D = 1$, and the losses $f_t(x) = (x - z_t)^2$ with $z = (2, -1, 2, 2)$. Each loss is $2$-strongly convex, so use $\eta_t = 1/(2t)$ and start at $x_1 = 1/2$. The gradient is $g_t = 2(x_t - z_t)$, so $y = x_t - (x_t - z_t)/t$.

| $t$ | $x_t$ | $z_t$ | $f_t(x_t)$ | $g_t$ | $y$ | $x_{t+1}$ |
|---|---|---|---|---|---|---|
| 1 | $1/2$ | $2$ | $9/4$ | $-3$ | $2$ | $1$ |
| 2 | $1$ | $-1$ | $4$ | $4$ | $0$ | $0$ |
| 3 | $0$ | $2$ | $4$ | $-4$ | $2/3$ | $2/3$ |
| 4 | $2/3$ | $2$ | $16/9$ | $-8/3$ | $1$ | $1$ |

OGD pays $433/36 \approx 12.03$. The best fixed point is the mean $5/4$ clipped to $1$, which pays $1 + 4 + 1 + 1 = 7$. So the regret is $181/36 \approx 5.03$. The bound of Theorem 2 in the proof, $\sum_t g_t^2/(4t) = 9/4 + 2 + 4/3 + 4/9 = 217/36 \approx 6.03$, holds. The projections in rounds 1 and 2 matter: without them the point would leave $[0, 1]$.

## Correctness

The proof uses one potential, the squared distance $a_t = \|x_t - x^*\|^2$ to a fixed comparator $x^* \in K$. Projection onto a convex set does not increase the distance to any point of the set, so a step gives $a_{t+1} \le a_t - 2\eta_t\langle g_t, x_t - x^*\rangle + \eta_t^2\|g_t\|^2$. Convexity says that the regret of round $t$ is at most $\langle g_t, x_t - x^*\rangle$. Divide by $2\eta_t$ and sum: the distance terms telescope to at most $D^2/(2\eta_T)$ when the steps do not increase, and the rest is $\frac12\sum_t\eta_t\|g_t\|^2$. With $\eta_t = D/(G\sqrt t)$ and $\sum_t 1/\sqrt t \le 2\sqrt T - 1$, this is $\frac32 GD\sqrt T - \frac12 GD$. For $\lambda$-strongly convex losses, the extra term $-\frac\lambda2 a_t$ in the convexity bound cancels the distance terms exactly when $\eta_t = 1/(\lambda t)$, and only $\sum_t\|g_t\|^2/(2\lambda t)$ is left. The full proofs are in the proof file.

## Complexity

- **Time.** Each round needs one subgradient of $f_t$, $O(d)$ arithmetic for the step, and one projection. For a box or a ball the projection takes $O(d)$ time, so the total is $\Theta(d \cdot T)$ plus the cost of the subgradients. For a general $K$ the projection is a convex quadratic program, and it can be the most costly part.
- **Space.** $\Theta(d)$: the current point and one gradient. OGD keeps no history.

## Properties

- **Optimal for convex Lipschitz losses.** No algorithm has regret $o(GD\sqrt T)$ on all sequences; the [online convex optimization](/online-convex-optimization/) page proves a lower bound of $\frac{GD}{2}\sqrt{T/3}$ with random linear losses.
- **Optimal for strongly convex losses.** The $O((G^2/\lambda)\log T)$ bound is tight up to a constant.
- **Anytime.** With $\eta_t = D/(G\sqrt t)$ it needs no knowledge of $T$, and it pays only a factor $3/2$ over the best fixed step for a known $T$. The [doubling trick](/doubling-trick/) is the other way to remove $T$; it costs a factor $\sqrt2/(\sqrt2 - 1) \approx 3.41$.
- **Deterministic and works against adaptive adversaries.** The proof does not use any assumption on how $f_t$ is chosen.
- **Data-dependent bound.** The bound $\frac{D^2}{2\eta_T} + \frac12\sum_t\eta_t\|g_t\|^2$ uses the real gradients, so small gradients give small regret; AdaGrad chooses the steps to make this bound small.
- **Equal to follow the leader for squared loss.** For $f_t(x) = (x - z_t)^2$ on $[0, 1]$ with $z_t \in [0, 1]$ and $\eta_t = 1/(2t)$, the point $x_{t+1}$ is the mean of $z_1, \ldots, z_t$, which is the choice of [follow the leader](/follow-the-leader/).

## Variants and improvements

- **Lazy projection (dual averaging).** Keep the sum of all gradients and play $\Pi_K(x_1 - \eta\sum_{s<t} g_s)$. This is follow the regularized leader with the regularizer $\frac12\|x\|^2$, and it has the same $O(GD\sqrt T)$ bound.
- **Mirror descent.** Replace the squared Euclidean distance by a Bregman divergence. With the entropy on the simplex it is [Hedge](/multiplicative-weights-update/), with regret $O(\sqrt{T \ln n})$ for experts, in place of $O(\sqrt{nT})$ for OGD; see [mirror descent](/mirror-descent/).
- **AdaGrad.** Per-coordinate steps $\eta_{t,j} \propto 1/\sqrt{\sum_{s \le t} g_{s,j}^2}$; see [AdaGrad](/adagrad/).
- **Online Newton step.** A second-order variant for exp-concave losses, with regret $O(d \log T)$ (Hazan, Agarwal and Kale 2007).
- **Bandit feedback.** Estimate the gradient from one loss value at a random nearby point (Flaxman, Kalai and McMahan 2005), with regret $O(T^{3/4})$.
- **Dynamic regret.** With a fixed step, OGD also competes with slowly moving comparators, with regret $O(\sqrt T(1 + P))$ for path length $P$ (Zinkevich 2003).

## When to use it

Use OGD when the decisions form a convex set with a cheap projection and the losses are convex, such as online regression, online classification with the hinge or logistic loss, or online resource allocation. It is the default first choice because it is simple, needs only gradients, and keeps no history. Prefer [Hedge](/multiplicative-weights-update/) on the simplex with many experts, since its bound depends on $\ln n$ and not on $\sqrt n$. Prefer AdaGrad when the gradients are sparse or of very different sizes in different coordinates. Use the step $1/(\lambda t)$ only when every loss is surely $\lambda$-strongly convex.

## Pitfalls

- **Wrong step size.** A fixed step that is too large gives regret of order $\eta G^2 T$, and one that is too small gives $D^2/\eta$. With $\eta_t = 1/(\lambda t)$ for losses that are not strongly convex, the first term of the bound grows like $D^2\lambda T$, which is linear.
- **Wrong scale of $G$ or $D$.** The tuned step needs the right bounds. If $G$ is unknown, use adaptive steps of the form $D/\sqrt{\sum_{s \le t}\|g_s\|^2}$, which adapt to the real gradients.
- **No projection.** Without line L7 the points can leave $K$, the comparator bound fails, and the iterates can drift without limit on linear losses.
- **Projection onto a non-convex set.** Lemma 1 of the proof needs $K$ convex. For a non-convex $K$, the nearest point can be farther from $x^*$ than $y$ is.
- **Last iterate versus average.** The regret bound is about the points played. For a fixed stochastic objective the guarantee is for the average point (online-to-batch conversion), not for the last point.

## Implementations

## History

Zinkevich (2003) introduced online convex programming and analyzed greedy projection, now called online gradient descent, with steps $1/\sqrt t$; he also applied it to repeated games through generalized infinitesimal gradient ascent. Gradient methods for online prediction were older: Cesa-Bianchi, Long and Warmuth (1996) analyzed gradient descent for online linear regression, and Kivinen and Warmuth (1997) compared additive and multiplicative updates. Hazan, Agarwal and Kale (2007) proved the logarithmic regret for strongly convex losses and introduced the online Newton step for exp-concave losses. The constant $\frac32$ in the bound with $\eta_t = D/(G\sqrt t)$ is the one in Hazan's 2016 survey.

## References
