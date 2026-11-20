---
tag: 259HJ8
kind: algorithm
slug: optimistic-hedge
name: Optimistic hedge
aliases:
- optimistic multiplicative weights
- OMWU
area: algorithmic-game-theory/computing-equilibria
level: research
summary: Multiplicative weights that count the last loss twice as a prediction of the next. In games it reaches regret polylog(T) for every player.
model: real-ram
complexity:
  vars: {k: the number of actions, T: the number of rounds}
  time: {worst: O(k T)}
  space: {extra: O(k)}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2015
  people: [Vasilis Syrgkanis, Alekh Agarwal, Haipeng Luo, Robert E. Schapire, Constantinos Daskalakis, Maxwell Fishelson, Noah Golowich]
  note: "Rakhlin and Sridharan (2013) studied optimistic online learning with predictable sequences. Syrgkanis, Agarwal, Luo and Schapire (2015) proved the RVU bound and individual regret O(T^(1/4)) in games, and Daskalakis, Fishelson and Golowich (2021) proved regret O(n log k log^4 T) for every player."
prereqs: [multiplicative-weights-update, regret, no-regret-dynamics]
see_also: [no-regret-coarse-correlated-theorem, no-regret-zero-sum-theorem, mirror-descent, online-convex-optimization, blum-mansour-reduction, coarse-correlated-equilibrium, expert-problem, regret-matching]
sources:
  - paper: "Vasilis Syrgkanis, Alekh Agarwal, Haipeng Luo and Robert E. Schapire, Fast convergence of regularized learning in games, Advances in Neural Information Processing Systems 28 (2015)"
    title: Fast convergence of regularized learning in games
    locator: "the RVU property, its proof for optimistic follow the regularized leader and optimistic Hedge, the bound on the sum of regrets, and individual regret O(T^(1/4))"
  - paper: "Constantinos Daskalakis, Maxwell Fishelson and Noah Golowich, Near-optimal no-regret learning in general games, Advances in Neural Information Processing Systems 34 (2021), 27604-27616, arXiv:2108.06924"
    title: Near-optimal no-regret learning in general games
    locator: "Theorem 3.1 (with step size 1/(C m log^4 T), each of m players has regret O(m log n_i log^4 T))"
  - paper: "Alexander Rakhlin and Karthik Sridharan, Optimization, learning, and games with predictable sequences, Advances in Neural Information Processing Systems 26 (2013)"
    title: "Optimization, learning, and games with predictable sequences"
    locator: "optimistic mirror descent with the last loss as the prediction, and its use in zero-sum games"
  - book: isbn:9781316624791
    title: "Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016"
    locator: "Lecture 17 (no-regret dynamics and multiplicative weights, the baseline that this method improves)"
---

Optimistic Hedge is a variant of [multiplicative weights](/multiplicative-weights-update/) for the [expert problem](/expert-problem/). Plain Hedge weights each action by $e^{-\eta L(a)}$, where $L(a)$ is the total past loss. Optimistic Hedge adds the last loss once more, as a guess that the next loss will look like the last one. Against an arbitrary adversary it keeps the $O(\sqrt{T \log k})$ [regret](/regret/) of Hedge. When the losses change slowly, its regret is much smaller, and in a game where every player uses it, the losses of each player change slowly because the others' strategies do. Daskalakis, Fishelson and Golowich (2021) proved that each of $n$ players then has regret $O(n \log k \log^4 T)$, against $\Theta(\sqrt{T})$ for plain Hedge. By [no-regret convergence to coarse correlated equilibria](/no-regret-coarse-correlated-theorem/), the empirical distribution of play is then an $\tilde{O}(1/T)$ coarse correlated equilibrium. The general framework is [no-regret dynamics](/no-regret-dynamics/); for two-player zero-sum games see [no-regret convergence in zero-sum games](/no-regret-zero-sum-theorem/).

## In plain words

A learner picks among several actions every day and then learns what each action would have cost. The usual method keeps a score for each action and favours the actions that have cost little so far. The optimistic method also bets that tomorrow will look like today: it counts today's cost twice when it sets tomorrow's chances. If the costs really change slowly, this bet pays off, and the learner reacts a step earlier. If the bet fails, the extra term only costs a bounded amount per round. In a game where every player learns this way, each player's choices change slowly, so the costs that the others see also change slowly, and the bet is almost always right.

## The problem

There are $k$ actions and $T$ rounds. In round $t$ the learner chooses a distribution $x_t$ on the actions, an adversary who may know $x_t$ chooses a loss vector $\ell_t \in [0, 1]^k$, and the learner pays $x_t \cdot \ell_t$. The regret is

$$\text{Reg}_T = \sum_{t=1}^{T} x_t \cdot \ell_t - \min_{a} \sum_{t=1}^{T} \ell_t(a).$$

The goal is small regret against every adversary, and much smaller regret when the loss vectors change slowly, as they do in a game in which all players learn.

## The algorithm

```pseudo id=main
OPTIMISTIC-HEDGE(k, eta, T)     ▷ eta > 0 is the step size
L1  x ← the uniform distribution on the k actions
L2  m ← the zero vector         ▷ the loss vector of the previous round
L3  for t ← 1 to T
L4      play x and observe the loss vector l
L5      for each action a
L6          x(a) ← x(a) · exp(-eta (2 l(a) - m(a)))
L7      divide each x(a) by the sum of all x(a)
L8      m ← l
```

After line L8 of round $t$, the distribution is

$$x_{t+1}(a) \propto \exp\big(-\eta\,(L_t(a) + \ell_t(a))\big), \qquad L_t = \ell_1 + \cdots + \ell_t,$$

because the factors of line L6 telescope: the sum of $2\ell_s - \ell_{s-1}$ over $s \le t$ is $L_t + \ell_t$. Plain Hedge uses $L_t$ alone. So optimistic Hedge is Hedge run on the cumulative loss plus a prediction $\ell_t$ of the next loss. It is the entropy case of optimistic [mirror descent](/mirror-descent/) and of optimistic follow the regularized leader, in the frame of [online convex optimization](/online-convex-optimization/). In code, the weights are better kept as logarithms, so that they do not underflow.

## Example

Take $k = 2$ actions, $\eta = 1$, and the losses $(1, 0)$, $(1, 0)$, $(0, 1)$, $(0, 1)$. The table shows the distribution of optimistic Hedge, the exponent $-(L_{t-1} + \ell_{t-1})$ that defines it, and the distribution of plain Hedge, rounded to four places.

| round | loss | exponent | optimistic $x_t$ | it pays | Hedge $x_t$ | it pays |
|---|---|---|---|---|---|---|
| 1 | (1, 0) | (0, 0) | (0.5, 0.5) | 0.5 | (0.5, 0.5) | 0.5 |
| 2 | (1, 0) | (-2, 0) | (0.1192, 0.8808) | 0.1192 | (0.2689, 0.7311) | 0.2689 |
| 3 | (0, 1) | (-3, 0) | (0.0474, 0.9526) | 0.9526 | (0.1192, 0.8808) | 0.8808 |
| 4 | (0, 1) | (-2, -2) | (0.5, 0.5) | 0.5 | (0.2689, 0.7311) | 0.7311 |

Each fixed action loses 2 in total. Optimistic Hedge loses 2.0718 and plain Hedge loses 2.3808. The optimistic learner moves away from action 1 faster in round 2, loses more in round 3 when the losses switch, and then returns to the middle in round 4, while Hedge is still behind.

## Correctness

**RVU bound.** With $\ell_0 = 0$, for every $T$ and every adversary,

$$\text{Reg}_T \le \frac{\ln k}{\eta} + \eta \sum_{t=1}^{T} \|\ell_t - \ell_{t-1}\|_\infty^2 - \frac{1}{8\eta} \sum_{t=2}^{T} \|x_t - x_{t-1}\|_1^2 .$$

Syrgkanis, Agarwal, Luo and Schapire (2015) called a bound of this form, regret bounded by variation in utilities, the RVU property. The proof compares $x_t$ with the iterate $y_t \propto e^{-\eta L_{t-1}}$ of plain Hedge and uses that the negative entropy is 1-strongly convex in the $\ell_1$ norm (Pinsker's inequality). Since $\|\ell_t - \ell_{t-1}\|_\infty \le 1$, the regret is at most $\ln k/\eta + \eta T$ against any adversary, which is $2\sqrt{T \ln k}$ for $\eta = \sqrt{\ln k / T}$.

**Games.** Let $n$ players each run optimistic Hedge with the same $\eta \le 1/(\sqrt{8}(n-1))$ on their expected losses, scaled to $[0, 1]$. A change of one opponent's distribution by $d$ in the $\ell_1$ norm changes a player's loss vector by at most $d$ in the $\infty$ norm, so $\|\ell^i_t - \ell^i_{t-1}\|_\infty^2 \le (n-1)\sum_{j \ne i}\|x^j_t - x^j_{t-1}\|_1^2$. Summing the RVU bounds over the players, the variation terms are cancelled by the movement terms, and

$$\sum_{i=1}^{n} \text{Reg}^i_T \le \frac{n \ln k}{\eta} + n\eta$$

for every $T$. In a two-player zero-sum game the sum of the two regrets is $T$ times the duality gap of the average strategies, so the averages are an $O(\log k / T)$ equilibrium. The full proofs are in the proof file.

The bound on the sum does not bound each regret in a general game. Syrgkanis et al. (2015) showed that each regret is $O(T^{1/4})$ with a suitable step size, and Daskalakis, Fishelson and Golowich (2021, Theorem 3.1) showed that with $\eta = 1/(C n \log^4 T)$, for a suitable constant $C$, each player has regret $O(n \log k \log^4 T)$. Their proof is long; it bounds the higher-order differences of the loss sequence and is not reproduced here.

## Complexity

Each round of lines L5 to L8 takes $O(k)$ time, so $T$ rounds take $O(k T)$, the same as plain Hedge. The memory is $O(k)$: the distribution and the last loss vector. In a game, computing the expected loss vectors usually dominates, at $O(n k^n)$ per round for a game in normal form. For an $\varepsilon$-coarse correlated equilibrium, the number of rounds drops from $O(\log k / \varepsilon^2)$ for plain Hedge to $\tilde{O}(n \log k / \varepsilon)$, where the tilde hides factors polylogarithmic in $1/\varepsilon$.

## Properties

- **Robust.** Against an arbitrary adversary the regret is $O(\sqrt{T \log k})$, the same order as Hedge.
- **Adaptive to slow change.** The regret depends on the total squared variation of the losses, not on $T$. For a constant loss sequence it is at most $\ln k / \eta + \eta$.
- **Uncoupled.** Each player uses only its own loss vectors; it does not need the payoffs of the others.
- **Last iterate.** In two-player zero-sum games with a unique equilibrium, the distributions themselves converge to it for a small enough step size (Daskalakis and Panageas, 2019), while those of Hedge spiral away. In general games the last iterate need not converge.

## Variants and improvements

- **Optimistic mirror descent and follow the regularized leader.** Any strongly convex regularizer gives an RVU bound; the entropy gives Hedge, and the Euclidean norm gives optimistic [online gradient descent](/online-gradient-descent/).
- **Swap regret.** Optimistic Hedge inside the copies of the [Blum-Mansour reduction](/blum-mansour-reduction/) gives polylogarithmic swap regret in games, and so fast convergence to correlated equilibria (Anagnostides, Daskalakis, Farina, Fishelson, Golowich and Sandholm, 2022).
- **Other predictions.** Line L6 uses $\ell_{t-1}$ as the guess of $\ell_t$. Any other predictable guess fits the same analysis, with $\|\ell_t - m_t\|$ in place of $\|\ell_t - \ell_{t-1}\|$.
- **Bandit feedback.** With only the loss of the chosen action, as in the [multi-armed bandit](/multi-armed-bandit/) and [Exp3](/exp3/), the variation of the losses cannot be observed directly, and these fast rates do not carry over in the same form.

## When to use it

Use it in place of Hedge when all players of a game run the same kind of learner, for example to compute approximate coarse correlated equilibria, or zero-sum equilibria with an $O(1/T)$ rate, by self-play. It costs nothing extra per round and keeps the worst-case guarantee. When the losses come from an adversary with no structure, it gives no gain over Hedge.

## Pitfalls

- **Factor 2 in line L6.** Using $\exp(-\eta\,\ell(a))$ gives plain Hedge, and using $\exp(-2\eta\,\ell(a))$ without the $+\eta\,m(a)$ gives Hedge with step $2\eta$. The prediction must be added for the next round and removed in the round after, which is what $2\ell - m$ does.
- **Forgetting line L8.** If $m$ stays zero, the exponents grow by $2\eta\,\ell$, again plain Hedge with step $2\eta$.
- **Step size too large in games.** The cancellation in the sum of regrets needs $\eta \le 1/(\sqrt{8}(n-1))$ in the form proved here. With a larger step, the variation terms of line L6 may not be absorbed, and the dynamics can oscillate.
- **Underflow in lines L6 and L7.** After many rounds the weights $x(a)$ become tiny and can underflow to 0, after which line L6 can never raise them again. Keep the logarithms of the weights and normalize against the largest one.

## Implementations

The Python code keeps the logarithms of the weights and implements lines L1 to L8 in floating point. The tests check the closed form $x_{t+1} \propto e^{-\eta(L_t + \ell_t)}$, the RVU bound and the simpler bound $\ln k/\eta + (\eta/2)\sum_t \|\ell_t - \ell_{t-1}\|_\infty^2$ after many prefixes against random, adaptive, alternating and slowly drifting adversaries, the bound $n \ln k / \eta + n\eta$ on the sum of regrets in self-play in chicken, rock-paper-scissors and a random three-player game, the identity between the sum of regrets and the duality gap in random zero-sum games, and that in matching pennies the last iterate approaches the equilibrium while that of Hedge moves away.

## History

Optimism in online learning goes back to Rakhlin and Sridharan (2013), who used the last loss as a prediction in mirror descent and showed fast convergence in zero-sum games; Daskalakis, Deckelbaum and Kim had earlier given uncoupled dynamics for zero-sum games that converge at a rate close to $1/T$. Syrgkanis, Agarwal, Luo and Schapire (2015) defined the RVU property and extended the fast rates to general games. Daskalakis, Fishelson and Golowich (2021) brought the individual regret of optimistic Hedge down to polylogarithmic in $T$.

## References
