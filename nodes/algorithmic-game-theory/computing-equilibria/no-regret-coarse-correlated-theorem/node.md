---
tag: DXJ0WG
kind: theorem
slug: no-regret-coarse-correlated-theorem
name: No-regret convergence to coarse correlated equilibria
aliases:
- Hannan consistency theorem
area: algorithmic-game-theory/computing-equilibria
level: core
summary: "When all players have external regret o(T), the empirical distribution of play converges to the set of coarse correlated equilibria."
prereqs: [coarse-correlated-equilibrium, regret, no-regret-dynamics]
see_also: [multiplicative-weights-update, smoothness-framework, price-of-anarchy, no-regret-zero-sum-theorem, correlated-equilibrium, blum-mansour-reduction, optimistic-hedge, nash-equilibrium]
sources:
  - book: isbn:9781316624791
    title: "Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016"
    locator: "Lecture 13 (the hierarchy of equilibrium concepts, coarse correlated equilibria) and Lecture 17 (no-regret dynamics converge to coarse correlated equilibria)"
  - book: isbn:9780521841085
    title: "Nicolo Cesa-Bianchi and Gabor Lugosi, Prediction, Learning, and Games, Cambridge University Press, 2006"
    locator: "Chapter 7 (prediction and playing games, regret and equilibria of repeated games)"
---

This theorem connects online learning with equilibria. If every player of a repeated game chooses its moves so that its [external regret](/regret/) grows more slowly than the number of rounds $T$, then the time average of the joint play is an approximate [coarse correlated equilibrium](/coarse-correlated-equilibrium/), and the error goes to 0. The proof is a few lines: the regret condition and the equilibrium condition are the same inequality, written once for a sequence and once for its average. With [multiplicative weights](/multiplicative-weights-update/), the average is an $\varepsilon$-coarse correlated equilibrium after $O(\log k / \varepsilon^2)$ rounds, so coarse correlated equilibria are easy to compute and to reach by simple behavior, unlike [Nash equilibria](/nash-equilibrium/). The theorem gives the convergence of [no-regret dynamics](/no-regret-dynamics/), and together with the [smoothness framework](/smoothness-framework/) it gives price of anarchy bounds for the outcomes of learning.

## Statement

A finite game has players $1, \ldots, n$, finite strategy sets $S_1, \ldots, S_n$, and utilities $u_i : S_1 \times \cdots \times S_n \to [-1, 1]$, which the players maximize. In rounds $t = 1, \ldots, T$, the play is a distribution $\pi^t$ on the set of profiles. The usual cases are the product $\pi^t = \sigma_1^t \times \cdots \times \sigma_n^t$ of the mixed strategies that the players choose, or the point mass on the profile $s^t$ that is actually played. The *external regret* of player $i$ is

$$R_i(T) = \max_{a \in S_i} \sum_{t=1}^{T} \mathbb{E}_{s \sim \pi^t}\, u_i(a, s_{-i}) - \sum_{t=1}^{T} \mathbb{E}_{s \sim \pi^t}\, u_i(s),$$

the gain that the best fixed strategy would have had over the actual play, against the same moves of the others. The *empirical distribution* is $\bar\pi_T = \frac{1}{T} \sum_{t=1}^T \pi^t$. A distribution $\pi$ on profiles is an *$\varepsilon$-coarse correlated equilibrium* if $\mathbb{E}_{s \sim \pi}\, u_i(s) \ge \mathbb{E}_{s \sim \pi}\, u_i(a, s_{-i}) - \varepsilon$ for every player $i$ and every $a \in S_i$; for $\varepsilon = 0$ it is a coarse correlated equilibrium.

**Theorem.**
1. If $R_i(T) \le \varepsilon T$ for every player $i$, then $\bar\pi_T$ is an $\varepsilon$-coarse correlated equilibrium.
2. If $R_i(T)/T \to 0$ for every player $i$ as $T \to \infty$, then the distance from $\bar\pi_T$ to the set of coarse correlated equilibria tends to 0.

The theorem does not need the players to be independent, to know the game, or to use the same algorithm. Each player needs only its own regret to be small.

## In plain words

A player has no regret when, looking back, no single fixed move would have done clearly better than what it did. Now take the history of all the rounds and pick a round at random. This random round is a joint plan for all the players. Suppose a referee proposes this plan, and a player is allowed to reject it in advance and use one fixed move instead. Rejecting is the same as playing that fixed move in every round of the history. No regret says that this is not much better. So no player wants to reject the plan, which is what a coarse correlated equilibrium means.

## Proof

**Part 1.** Fix a player $i$ and a strategy $a \in S_i$. By linearity of expectation, $\mathbb{E}_{s \sim \bar\pi_T}\, f(s) = \frac{1}{T} \sum_t \mathbb{E}_{s \sim \pi^t}\, f(s)$ for every function $f$ of profiles. Apply this to $f(s) = u_i(a, s_{-i}) - u_i(s)$:

$$\mathbb{E}_{s \sim \bar\pi_T}\, u_i(a, s_{-i}) - \mathbb{E}_{s \sim \bar\pi_T}\, u_i(s) = \frac{1}{T} \Big( \sum_t \mathbb{E}_{\pi^t}\, u_i(a, s_{-i}) - \sum_t \mathbb{E}_{\pi^t}\, u_i(s) \Big) \le \frac{R_i(T)}{T} \le \varepsilon.$$

The first inequality is the definition of $R_i(T)$ as a maximum over $a$. This is the condition of an $\varepsilon$-coarse correlated equilibrium for $i$ and $a$.

**Part 2.** The distributions on the finite set of profiles form a compact simplex $\Delta$. For $\varepsilon \ge 0$, let $C_\varepsilon \subseteq \Delta$ be the set of $\varepsilon$-coarse correlated equilibria. It is closed, because each of its constraints is a non-strict linear inequality in $\pi$, and $C_0 = \bigcap_{\varepsilon > 0} C_\varepsilon$. Let $\varepsilon_T = \max_i \max(R_i(T), 0)/T$, so that $\varepsilon_T \to 0$ and $\bar\pi_T \in C_{\varepsilon_T}$ by Part 1. Suppose that the distance from $\bar\pi_T$ to $C_0$ does not tend to 0. Then for some $\delta > 0$ there are infinitely many $T$ with distance at least $\delta$. By compactness, a subsequence of these $\bar\pi_T$ converges to some $\pi^* \in \Delta$, and $\pi^*$ also has distance at least $\delta$ from $C_0$, since the distance to a set is continuous. For every fixed $\varepsilon > 0$, all but finitely many terms of the subsequence lie in $C_\varepsilon$, which is closed, so $\pi^* \in C_\varepsilon$. Hence $\pi^* \in C_0$, a contradiction. (The set $C_0$ is not empty: it contains every Nash equilibrium.) $\blacksquare$

## Consequences

- **Fast approximate equilibria.** [Multiplicative weights](/multiplicative-weights-update/), with utilities in $[-1, 1]$, has external regret $O(\sqrt{T \log k})$ against any sequence, where $k = \max_i |S_i|$. If every player uses it, the empirical distribution is an $\varepsilon$-coarse correlated equilibrium after $T = O(\log k / \varepsilon^2)$ rounds. Each round costs one expected payoff vector per player. This is in contrast with Nash equilibria, which are PPAD-hard to compute even in two-player games.
- **Faster in self-play.** The bound of Part 1 holds for any opponents. When all players use the same smooth algorithm, the regrets are much smaller: [optimistic Hedge](/optimistic-hedge/) has regret polylogarithmic in $T$ in self-play, so the empirical distribution is an $\varepsilon$-coarse correlated equilibrium after roughly $1/\varepsilon$ rounds, up to logarithmic factors.
- **Price of anarchy of learning.** A robust price of anarchy bound proved by the [smoothness framework](/smoothness-framework/) holds for every coarse correlated equilibrium, so by the theorem it holds, up to a vanishing error, for the time-averaged welfare of any no-regret dynamics. For example, in atomic congestion games with affine costs the average cost of no-regret dynamics tends to at most $5/2$ times the optimum ([price of anarchy](/price-of-anarchy/)).
- **Zero-sum games.** In a two-player zero-sum game, the marginals of every coarse correlated equilibrium are optimal strategies. With the theorem, this gives the [convergence of no-regret dynamics in zero-sum games](/no-regret-zero-sum-theorem/) and a proof of the minimax theorem.
- **Correlated equilibria need more.** The same proof with swap regret in place of external regret gives a [correlated equilibrium](/correlated-equilibrium/). Algorithms with small swap regret exist, for example by the [Blum-Mansour reduction](/blum-mansour-reduction/) or [regret matching](/regret-matching/).

## Tightness

- **Not a correlated equilibrium.** External regret is not enough for a correlated equilibrium. In rock-paper-scissors, with payoff 1 for a win, $-1$ for a loss and 0 for a tie, let the players cycle through the six profiles in which they play different moves. Each player wins three of six rounds and loses three, so its average payoff is 0. Every fixed move also gets 0 on average against the uniform moves of the opponent. So the regret stays bounded, and the empirical distribution, uniform on the six profiles, is a coarse correlated equilibrium. It is not a correlated equilibrium: when player 1 is told to play rock, player 2 plays paper or scissors with equal chance, and scissors would gain $1/2$ on average.
- **Not a Nash equilibrium, and no convergence of the play itself.** The theorem is about the time average of the joint play. The average of the product distributions is in general correlated, so it is not a mixed profile, and the day-to-day strategies $\sigma^t$ need not converge at all. In matching pennies, multiplicative weights moves away from the equilibrium, while the empirical distribution still converges to the set of coarse correlated equilibria.
- **Convergence to a set.** Part 2 says that $\bar\pi_T$ approaches the set of coarse correlated equilibria. It need not converge to one point, because the set can be large and the dynamics can drift inside it.
- **The rate is the regret.** Part 1 converts regret into equilibrium error one for one. Against adversarial opponents no algorithm has external regret $o(\sqrt{T \log k})$ in the worst case, so a bound for all no-regret dynamics cannot be better than the order $\sqrt{\log k / T}$.

## History

Hannan (1957) gave the first procedure for a repeated game whose average regret against the best fixed strategy goes to 0. Moulin and Vial (1978) defined the equilibrium notion that is now called a coarse correlated equilibrium. The link between the two is a direct consequence of the definitions, and it is a standard part of the theory of learning in games. Cesa-Bianchi and Lugosi (2006) treat it in their chapter on prediction and games, and Roughgarden (2016) presents it as the convergence of no-regret dynamics. The use of the theorem for the price of anarchy of learning comes from the work on robust bounds and smooth games by Blum, Hajiaghayi, Ligett and Roth (2008) and Roughgarden (2009).

## References
