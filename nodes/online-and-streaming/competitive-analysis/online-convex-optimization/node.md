---
tag: XHH8FE
kind: problem
slug: online-convex-optimization
name: Online convex optimization
aliases:
- OCO
- online convex programming
area: online-and-streaming/competitive-analysis
level: advanced
summary: In each round, choose a point of a convex set, then pay a convex loss chosen by an adversary. The goal is low regret against the best fixed point; the optimal rate is Θ(GD sqrt(T)).
prereqs: [convex-set, convex-function, subgradient, regret]
see_also: [online-gradient-descent, expert-problem, multiplicative-weights-update, follow-the-leader, mirror-descent, stochastic-gradient-descent, adagrad, strong-convexity]
sources:
  - paper: "Martin Zinkevich, Online convex programming and generalized infinitesimal gradient ascent, Proceedings of the 20th International Conference on Machine Learning (ICML), 2003, 928-936"
    locator: the definition of online convex programming, the greedy projection algorithm and Theorem 1 (regret at most D^2 sqrt(T)/2 + (sqrt(T) - 1/2) G^2)
  - paper: doi:10.1561/2400000013
    title: "Elad Hazan, Introduction to online convex optimization, Foundations and Trends in Optimization 2(3-4) (2016), 157-325"
    locator: Chapter 1 (the model and examples), Chapter 3 (online gradient descent, the lower bound of order GD sqrt(T), strongly convex losses, and online-to-batch conversion), Chapter 4 (exp-concave losses and online Newton step) and Chapter 5 (follow the regularized leader)
  - paper: doi:10.1007/s10994-007-5016-8
    title: "Elad Hazan, Amit Agarwal and Satyen Kale, Logarithmic regret algorithms for online convex optimization, Machine Learning 69(2-3) (2007), 169-192"
    locator: regret O((G^2 / lambda) log T) for lambda-strongly convex losses and O(d log T) for exp-concave losses
  - paper: doi:10.1561/2200000018
    title: "Shai Shalev-Shwartz, Online learning and online convex optimization, Foundations and Trends in Machine Learning 4(2) (2012), 107-194"
    locator: Chapters 2 and 3 (follow the regularized leader and online mirror descent as unified algorithms for OCO)
---

Online convex optimization (OCO) is the online learning problem in which a learner picks a point $x_t$ of a convex set $K$ in each round, after which an adversary reveals a convex loss function $f_t$ and the learner pays $f_t(x_t)$. The goal is small [regret](/regret/) against the best fixed point of $K$ in hindsight. Zinkevich (2003) defined the problem and showed that [online gradient descent](/online-gradient-descent/) has regret $O(GD\sqrt{T})$ for losses with gradients bounded by $G$ on a set of diameter $D$; this rate is optimal, and strongly convex losses allow $O(\log T)$. The [expert problem](/expert-problem/), online regression and online portfolio selection are special cases.

## In plain words

Each round you must choose a point in some region, such as a mix of investments or the settings of a model. After you choose, you learn a cost for every possible point, and you pay the cost of your point. The costs can change in any way from round to round, but each cost is bowl shaped: it has no separate dips, so going downhill always leads to the bottom.

You want your total cost to be not much more than the total cost of the single best point, chosen with hindsight. This is possible. A simple plan is to move a small step downhill on each new cost and to stay inside the region. Then the extra cost grows only like the square root of the number of rounds, so the average extra cost per round goes to zero.

## Definition

Let $K \subset \mathbb{R}^d$ be a nonempty, closed, bounded, [convex set](/convex-set/) with diameter $D = \max_{x, y \in K}\|x - y\|_2$. In each round $t = 1, \ldots, T$:

1. the learner chooses $x_t \in K$;
2. the adversary chooses a [convex function](/convex-function/) $f_t : K \to \mathbb{R}$;
3. the learner pays $f_t(x_t)$ and observes $f_t$, or at least a [subgradient](/subgradient/) $g_t \in \partial f_t(x_t)$.

The regret is

$$R_T = \sum_{t=1}^{T} f_t(x_t) - \min_{x \in K} \sum_{t=1}^{T} f_t(x).$$

The standard assumption is that every subgradient has norm at most $G$, so each $f_t$ is $G$-Lipschitz on $K$. The adversary may choose $f_t$ after it sees $x_1, \ldots, x_t$, so it is adaptive; a deterministic learner suffices here, because the losses are convex and the learner can play a mean in place of a random point. A learner is good if $\sup R_T = o(T)$, and the problem asks for the best rate in terms of $T$, $D$ and $G$, and of the curvature of the losses.

## Variants

- **Online linear optimization.** $f_t(x) = g_t \cdot x$. Every OCO problem reduces to it, since convexity gives $f_t(x_t) - f_t(x) \le g_t \cdot (x_t - x)$ for $g_t \in \partial f_t(x_t)$; most algorithms use only this linear bound.
- **Strongly convex losses.** If each $f_t$ is $\lambda$-[strongly convex](/strong-convexity/), the optimal regret is $\Theta((G^2/\lambda)\log T)$ (Hazan, Agarwal and Kale 2007).
- **Exp-concave losses.** If $e^{-\alpha f_t}$ is concave, as for the log loss of portfolio selection, the online Newton step has regret $O((1/\alpha + GD)\, d \log T)$.
- **Bandit convex optimization.** The learner sees only the number $f_t(x_t)$. Flaxman, Kalai and McMahan (2005) estimate a gradient from one value and get regret $O(T^{3/4})$; better rates need more complex methods.
- **Dynamic regret.** The comparator is a sequence $u_1, \ldots, u_T$ with path length $P = \sum_t \|u_{t+1} - u_t\|$; online gradient descent gets $O(\sqrt{T}(1 + P))$, and better with more care.
- **Unknown horizon and adaptive rates.** The step size $\eta_t \propto 1/\sqrt{t}$, the [doubling trick](/doubling-trick/), or [AdaGrad](/adagrad/) remove the need to know $T$, $G$ or the geometry in advance.

## Examples

- **Experts.** $K = \Delta_n$, the probability simplex, and $f_t(p) = p \cdot \ell_t$ with $\ell_t \in [0, 1]^n$. Here $D = \sqrt 2$ and $G = \sqrt n$; online gradient descent gets $O(\sqrt{nT})$, and [Hedge](/multiplicative-weights-update/), which is mirror descent with the entropy, gets $O(\sqrt{T \ln n})$ by using the right geometry.
- **Online regression.** $K$ is a ball of weight vectors and $f_t(w) = (w \cdot a_t - b_t)^2$ for a data point $(a_t, b_t)$ revealed after the prediction. This is the online form of [linear regression](/linear-regression/) and of training by [stochastic gradient descent](/stochastic-gradient-descent/).
- **Online classification.** $f_t(w) = \max(0, 1 - b_t\, w \cdot a_t)$, the hinge loss, or the logistic loss of [logistic regression](/logistic-regression/).
- **Portfolio selection.** $K = \Delta_n$ and $f_t(p) = -\ln(p \cdot r_t)$, where $r_t$ is the vector of price ratios of the assets in round $t$. Low regret means that the wealth is close to that of the best constant rebalanced portfolio; see [portfolio optimization](/portfolio-optimization/).
- **A one-dimensional example.** $K = [0, 1]$ and $f_t(x) = |x - z_t|$ for points $z_t$. The best fixed point is a [median](/median/) of the $z_t$, and online gradient descent moves $x_t$ toward $z_t$ by a step $\eta_t$; the [online gradient descent](/online-gradient-descent/) page works it out.

A non-example: if the losses may be non-convex, a deterministic learner has linear regret. The adversary gives loss $1$ on a small ball around $x_t$ and $0$ elsewhere; the learner pays $T$, and a point outside all $T$ balls pays $0$.

## Known algorithms

- [Online gradient descent](/online-gradient-descent/) (Zinkevich 2003): $x_{t+1} = \Pi_K(x_t - \eta_t g_t)$. Regret at most $\frac32 GD\sqrt{T}$ with $\eta_t = D/(G\sqrt t)$, and $\frac{G^2}{2\lambda}(1 + \ln T)$ for $\lambda$-strongly convex losses with $\eta_t = 1/(\lambda t)$.
- [Follow the regularized leader](/follow-the-leader/): $x_t = \arg\min_{x \in K} \{\sum_{s<t} g_s \cdot x + R(x)/\eta\}$. With a 1-strongly convex regularizer $R$ of range $B$ on $K$, regret $O(G\sqrt{BT})$ in the dual norm.
- [Mirror descent](/mirror-descent/): the same family in its update form. With the entropy on the simplex it is [Hedge](/multiplicative-weights-update/).
- [AdaGrad](/adagrad/): per-coordinate step sizes from the past gradients, with regret that adapts to sparse gradients.
- Online Newton step (Hazan, Agarwal and Kale 2007): a second-order method for exp-concave losses with regret $O(d \log T)$.
- [Follow the perturbed leader](/follow-the-leader/) (Kalai and Vempala 2005): for linear losses over a set with an offline optimizer.

## Bounds

**Upper bound.** Online gradient descent has $R_T \le \frac32 GD\sqrt T$ for every sequence of convex $G$-Lipschitz losses, and $R_T \le \frac{G^2}{2\lambda}(1 + \ln T)$ when every loss is $\lambda$-strongly convex. The [online gradient descent](/online-gradient-descent/) page proves both.

**Lower bound $\Omega(GD\sqrt T)$.** For every learner, even one that knows $T$, there are linear $G$-Lipschitz losses on an interval of length $D$ with $R_T \ge \frac{GD}{2}\sqrt{T/3}$.

*Proof.* Let $K = [-D/2, D/2]$ and $f_t(x) = \varepsilon_t G x$, where $\varepsilon_1, \ldots, \varepsilon_T$ are independent uniform signs in $\{-1, +1\}$, drawn after the learner fixes its rule. The learner's point $x_t$ depends only on $\varepsilon_1, \ldots, \varepsilon_{t-1}$, so $\mathbb{E}[\varepsilon_t G x_t] = 0$, and the learner's expected total loss is $0$. With $S = \sum_t \varepsilon_t$, the best fixed point has total loss $\min_{x \in K} G S x = -\frac{GD}{2}|S|$. So $\mathbb{E}[R_T] = \frac{GD}{2}\mathbb{E}|S|$. Now $\mathbb{E}[S^2] = T$ and $\mathbb{E}[S^4] = 3T^2 - 2T \le 3T^2$. By Hölder's inequality with exponents $3/2$ and $3$, $\mathbb{E}[S^2] = \mathbb{E}[|S|^{2/3}|S|^{4/3}] \le (\mathbb{E}|S|)^{2/3}(\mathbb{E}S^4)^{1/3}$, so $\mathbb{E}|S| \ge T^{3/2}/\sqrt{3T^2} = \sqrt{T/3}$. Some fixed sign sequence has regret at least the mean, which gives the claim. $\square$

The same argument in $d$ dimensions on a cube gives $\Omega(GD\sqrt T)$ for every $d$. With the central limit theorem, $\mathbb{E}|S| \sim \sqrt{2T/\pi}$, so the constant $\frac{1}{2\sqrt3} \approx 0.29$ in front of $GD\sqrt T$ improves to about $0.40$; online gradient descent has $1.5$.

**Strongly convex losses.** For $\lambda$-strongly convex losses, regret $\Omega((G^2/\lambda)\log T)$ is necessary in the worst case, already for quadratic losses in one dimension, so the bound of online gradient descent is tight up to a constant (Abernethy, Bartlett, Rakhlin and Tewari, COLT 2008).

## Reductions

- **From convex to linear losses.** Replace $f_t$ by the linear function $x \mapsto g_t \cdot x$ with $g_t \in \partial f_t(x_t)$. Since $f_t(x_t) - f_t(x) \le g_t \cdot (x_t - x)$, any regret bound for the linear losses holds for the convex ones.
- **Online to batch.** If $f_1, f_2, \ldots$ are i.i.d. draws of a random convex function with mean $F(x) = \mathbb{E}[f(x)]$, then the average point $\bar x_T = \frac1T \sum_t x_t$ has $\mathbb{E}[F(\bar x_T)] - \min_K F \le \mathbb{E}[R_T]/T$. *Proof:* $x_t$ depends only on $f_1, \ldots, f_{t-1}$, so $\mathbb{E}[f_t(x_t)] = \mathbb{E}[F(x_t)]$; by [Jensen's inequality](/jensens-inequality/), $F(\bar x_T) \le \frac1T\sum_t F(x_t)$; and $\mathbb{E}[\min_x \sum_t f_t(x)] \le \min_x \sum_t F(x)$. Combine the three. So an online algorithm with regret $O(GD\sqrt T)$ is a stochastic optimizer with error $O(GD/\sqrt T)$, which is the rate of [stochastic gradient descent](/stochastic-gradient-descent/).
- **To games.** In a convex-concave game, two OCO learners that play against each other have average iterates that form an approximate equilibrium, with error $(R_T + R'_T)/T$. This gives a proof of the [minimax theorem](/minimax-theorem/) for [zero-sum games](/zero-sum-game/).
- **To the expert problem.** Experts are OCO on the simplex with linear losses, as in the examples.

## Applications

- **Training models on streams.** Online and stochastic gradient methods for regression, classification and recommendation, where the data arrive one example at a time and may change over time.
- **Online advertising and pricing.** Bidding and pricing problems where the payoff of a decision is a convex function revealed after the decision.
- **Portfolio management.** Universal portfolios and online Newton step for wealth close to the best constant rebalanced portfolio.
- **Optimization and games.** Online learning algorithms used offline to solve convex programs, saddle-point problems and zero-sum games approximately, through the online-to-batch and game reductions.

## References
