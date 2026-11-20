---
tag: GW377H
kind: theorem
slug: no-regret-zero-sum-theorem
name: No-regret convergence in zero-sum games
aliases:
- Freund-Schapire theorem
area: algorithmic-game-theory/computing-equilibria
level: core
summary: "When both players of a zero-sum game run no-regret algorithms, their average strategies are approximately optimal and the average payoff tends to the value."
prereqs: [zero-sum-game, minimax-theorem, regret, multiplicative-weights-update]
see_also: [no-regret-coarse-correlated-theorem, no-regret-dynamics, zero-sum-game-linear-programming, yao-minimax-principle, robinson-fictitious-play-theorem, optimistic-hedge, boosting, adaboost]
sources:
  - paper: doi:10.1006/game.1999.0738
    title: "Yoav Freund and Robert E. Schapire, Adaptive game playing using multiplicative weights, Games and Economic Behavior 29(1-2) (1999), 79-103"
    locator: "the multiplicative weights algorithm for repeated play of a matrix game, the bound on its regret, and the corollaries that the average strategies are approximately optimal and that the minimax theorem follows"
  - book: isbn:9781316624791
    title: "Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016"
    locator: Lecture 17 (no-regret dynamics) and Lecture 18 (the minimax theorem proved with no-regret dynamics)
  - book: isbn:9780521841085
    title: "Nicolo Cesa-Bianchi and Gabor Lugosi, Prediction, Learning, and Games, Cambridge University Press, 2006"
    locator: "Chapter 7 (prediction and playing games, the minimax theorem from regret bounds)"
---

In a two-player [zero-sum game](/zero-sum-game/), simple learning finds optimal play. If both players choose their mixed strategies round by round with algorithms whose [regret](/regret/) grows more slowly than the number of rounds $T$, then the average of each player's strategies is an approximately optimal strategy, and the average payoff tends to the value of the game. The error is the sum of the two average regrets. With [multiplicative weights](/multiplicative-weights-update/) on both sides, this gives $\varepsilon$-optimal strategies after $O(\log(m + n)/\varepsilon^2)$ rounds, and the argument also proves the [minimax theorem](/minimax-theorem/) again, with no use of LP duality or fixed points. The result is due to Freund and Schapire (1999). It is the special case for two-player zero-sum games of the [convergence to coarse correlated equilibria](/no-regret-coarse-correlated-theorem/), and it is the reason why [no-regret dynamics](/no-regret-dynamics/) can replace the [linear program](/zero-sum-game-linear-programming/) for large games.

## Statement

The game is a real $m \times n$ matrix $M$ with entries in $[-1, 1]$. The row player picks $x \in \Delta_m$ and gets $x^\top M y$; the column player picks $y \in \Delta_n$ and pays it. In rounds $t = 1, \ldots, T$ the players choose $x^t$ and $y^t$, and each may see the past choices of the other. The regrets are

$$R_{\text{row}}(T) = \max_{i} \sum_{t=1}^T (M y^t)_i - \sum_{t=1}^T x^{t\top} M y^t, \qquad R_{\text{col}}(T) = \sum_{t=1}^T x^{t\top} M y^t - \min_{j} \sum_{t=1}^T (x^{t\top} M)_j.$$

Let $\bar x = \frac1T \sum_t x^t$, $\bar y = \frac1T \sum_t y^t$, $\bar v = \frac1T \sum_t x^{t\top} M y^t$, and let $v$ be the value of the game.

**Theorem (Freund and Schapire 1999).** Let $\varepsilon_r = R_{\text{row}}(T)/T$ and $\varepsilon_c = R_{\text{col}}(T)/T$. Then

1. $\min_j (\bar x^\top M)_j \ge v - \varepsilon_r - \varepsilon_c$ and $\max_i (M \bar y)_i \le v + \varepsilon_r + \varepsilon_c$, so $\bar x$ and $\bar y$ are $(\varepsilon_r + \varepsilon_c)$-optimal strategies;
2. $v - \varepsilon_r \le \bar v \le v + \varepsilon_c$.

So if both regrets are $o(T)$, the average strategies become optimal and the average payoff tends to $v$.

## In plain words

Two players play the same zero-sum game many times, and each adjusts its mix of moves from what has happened so far. Neither knows the game in advance or solves anything. Each only makes sure that, looking back, no single fixed move would have done clearly better. Then the overall mix that each player has used, counted over all the rounds, is almost an optimal strategy of the game. The reason is short: the row player's lack of regret means the column player's overall mix gives nothing away, and the other way around.

## Proof

By the definition of the regrets and linearity,

$$\max_i (M \bar y)_i = \frac1T \max_i \sum_t (M y^t)_i = \bar v + \varepsilon_r, \qquad \min_j (\bar x^\top M)_j = \frac1T \min_j \sum_t (x^{t\top} M)_j = \bar v - \varepsilon_c.$$

For every $x$ and $y$, $\min_j (x^\top M)_j \le x^\top M y \le \max_i (M y)_i$, so

$$\bar v - \varepsilon_c = \min_j (\bar x^\top M)_j \;\le\; \max_x \min_j (x^\top M)_j \;\le\; \min_y \max_i (M y)_i \;\le\; \max_i (M \bar y)_i = \bar v + \varepsilon_r. \tag{1}$$

The middle inequality is the easy half of the minimax theorem. By the minimax theorem, both middle terms are $v$, and (1) gives $\bar v - \varepsilon_c \le v \le \bar v + \varepsilon_r$, which is part 2. Then $\min_j (\bar x^\top M)_j = \bar v - \varepsilon_c \ge v - \varepsilon_r - \varepsilon_c$ and $\max_i (M \bar y)_i = \bar v + \varepsilon_r \le v + \varepsilon_r + \varepsilon_c$, which is part 1. $\blacksquare$

**The minimax theorem from regret.** The proof uses the minimax theorem only to name $v$. Without it, (1) says that the gap between $\min_y \max_x$ and $\max_x \min_y$ is at most $\varepsilon_r + \varepsilon_c$. Multiplicative weights with step $\eta$ has regret at most $\ln k/\eta + \eta T$ for payoffs in $[-1, 1]$ and $k$ actions, against every sequence, so with $\eta = \sqrt{\ln k / T}$ both average regrets are at most $2\sqrt{\ln \max(m, n) / T}$. Let $T \to \infty$: the gap is 0, which is the minimax theorem.

## Consequences

- **Fast approximate solutions.** With multiplicative weights on both sides, $\bar x$ and $\bar y$ are $\varepsilon$-optimal after $T = O(\log(m + n)/\varepsilon^2)$ rounds. Each round costs one product $M y^t$ and one product $x^{t\top} M$, so the total time is $O(m n \log(m + n)/\varepsilon^2)$. For large games this is faster than the exact [linear program](/zero-sum-game-linear-programming/), and it only needs the two products, so it also works when $M$ is given implicitly.
- **One player can best respond.** If the column player plays a best response $y^t$ to $x^t$ in each round, then $\sum_t x^{t\top} M y^t = \sum_t \min_j (x^{t\top} M)_j \le \min_j \sum_t (x^{t\top} M)_j$, so $R_{\text{col}}(T) \le 0$. The theorem then holds with $\varepsilon_c = 0$, and $\bar y$ is supported on at most $T$ columns. So every game has an $\varepsilon$-optimal strategy of the column player with support $O(\log m / \varepsilon^2)$.
- **Boosting.** Freund and Schapire describe [boosting](/boosting/) as this game: the rows are the training examples, the columns are the weak hypotheses, the booster runs multiplicative weights over the examples, and the weak learner best responds. [AdaBoost](/adaboost/) is close to this scheme, and the theorem explains why a weak learner that beats one half on every distribution gives a strong learner.
- **Faster in self-play.** If both players use [optimistic Hedge](/optimistic-hedge/), the sum $R_{\text{row}}(T) + R_{\text{col}}(T)$ stays bounded by $O(\log(m + n))$ for all $T$, so the error $\varepsilon_r + \varepsilon_c$ falls like $1/T$ instead of $1/\sqrt{T}$.
- **Lower bounds.** [Yao's minimax principle](/yao-minimax-principle/) uses the minimax theorem for matrices of costs of algorithms on inputs, and the regret proof gives an approximate version of it with explicit, small supports.

## Tightness

- **Averages, not the last iterate.** The theorem is about $\bar x$ and $\bar y$. The strategies $x^t$, $y^t$ themselves need not converge. In matching pennies, multiplicative weights on both sides moves away from the equilibrium $(1/2, 1/2)$ toward the boundary, while the averages converge to it. Optimistic Hedge and related methods do converge in the last iterate in such games.
- **The rate.** The error equals the sum of the average regrets, and against an adversary no algorithm has regret $o(\sqrt{T \log k})$ in the worst case. In a game the opponent is not an adversary, which is why self-play can do better, as for optimistic Hedge.
- **Learning without regret guarantees.** Fictitious play, in which each player best responds to the empirical mix of the other, has linear regret against some sequences, but in zero-sum games its averages still converge to optimal strategies, by [Robinson's theorem](/robinson-fictitious-play-theorem/). Its rate can be much slower.
- **Zero sum matters.** In general-sum games, small regrets give only a coarse correlated equilibrium, and the averages $\bar x$ and $\bar y$ need not form a Nash equilibrium. In the game where both players get 2 at (A, A), 1 at (B, B) and 0 otherwise, alternating between (A, A) and (B, B) gives both players negative regret, but $\bar x = \bar y = (1/2, 1/2)$ is not an equilibrium: against it, A gives 1 and B gives $1/2$.

## History

Hannan (1957) and Blackwell (1956) studied repeated play against an unknown opponent and the guarantees that a player can secure in the long run. Brown (1951) proposed fictitious play as a way to compute the value, and Robinson (1951) proved that it converges in zero-sum games. Freund and Schapire (1999) gave the multiplicative weights algorithm for repeated matrix games, the bound on the error of the average strategies, and the proof of the minimax theorem from it, and they used the same game view to explain boosting. Later work made the convergence faster in self-play, starting with the optimistic methods of Rakhlin and Sridharan (2013).

## References
