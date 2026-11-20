---
tag: 71AA39
kind: definition
slug: coarse-correlated-equilibrium
name: Coarse correlated equilibrium
aliases:
- CCE
- Hannan consistent distribution
area: algorithmic-game-theory/strategic-games
level: core
summary: A distribution over action profiles such that no player gains by committing in advance to one fixed action instead of following the draw.
prereqs: [correlated-equilibrium]
see_also: [correlated-equilibrium, no-regret-coarse-correlated-theorem, no-regret-dynamics, regret, smoothness-framework, price-of-anarchy, no-regret-zero-sum-theorem, multiplicative-weights-update]
sources:
  - paper: doi:10.1007/BF01769190
    title: "Herve Moulin and Jean-Philippe Vial, Strategically zero-sum games, the class of games whose completely mixed equilibria cannot be improved upon, International Journal of Game Theory 7(3-4) (1978), 201-221"
    locator: the definition of the correlation scheme in which players commit before the draw, now called coarse correlated equilibrium
  - paper: "James Hannan, Approximation to Bayes risk in repeated play, in Contributions to the Theory of Games III, Annals of Mathematics Studies 39, Princeton University Press (1957), 97-139"
    title: Approximation to Bayes risk in repeated play
    locator: the first strategy for repeated play whose average payoff approaches that of the best fixed action in hindsight
  - book: isbn:9781316624791
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 13 (the hierarchy of equilibria), Lecture 14 (robust price of anarchy bounds for coarse correlated equilibria) and Lecture 17 (no-regret dynamics converge to coarse correlated equilibria)
---

A coarse correlated equilibrium is a probability distribution over the profiles of a game such that no player gains by committing in advance to one fixed strategy, instead of agreeing to play their part of the drawn profile. It is the largest of the four standard equilibrium sets, and it is exactly the set that players with no external regret reach together, so it is the equilibrium notion behind many bounds on the [price of anarchy](/price-of-anarchy/) of learning players. Moulin and Vial defined it in 1978; the regret idea goes back to Hannan in 1957.

## Definition

Let $G = (N, (S_i), (u_i))$ be a finite [normal-form game](/normal-form-game/) whose players maximize. A distribution $p$ on $S = S_1 \times \cdots \times S_n$ is a *coarse correlated equilibrium* if, for every player $i$ and every $b \in S_i$,

$$\mathbb{E}_{s \sim p}\big[u_i(s)\big] \ge \mathbb{E}_{s \sim p}\big[u_i(b, s_{-i})\big].$$

The right side depends on $p$ only through the marginal distribution of $s_{-i}$. So the condition says: following the draw is at least as good as ignoring it and playing $b$ against the others' marginal play. A player decides before seeing the recommendation, unlike in a [correlated equilibrium](/correlated-equilibrium/), where the player decides after seeing it.

**A polytope.** These are $\sum_i |S_i|$ linear inequalities in the unknowns $p(s)$, together with $p \ge 0$ and $\sum_s p(s) = 1$, so the set is a convex polytope and a linear program finds an element that maximizes any linear function.

**The best-response support fact.** For a product distribution $p = \sigma_1 \times \cdots \times \sigma_n$, the condition is $u_i(\sigma) \ge u_i(b, \sigma_{-i})$ for every pure $b$, which is the Nash condition, since no mixed deviation does better than the best pure one. So the product coarse correlated equilibria are exactly the mixed Nash equilibria, and in a Nash equilibrium every strategy in the support of $\sigma_i$ is a pure [best response](/best-response/) to $\sigma_{-i}$.

**The hierarchy.** With pure profiles as point masses and mixed profiles as product distributions,

$$\text{pure Nash} \subseteq \text{mixed Nash} \subseteq \text{correlated equilibria} \subseteq \text{coarse correlated equilibria}.$$

The last inclusion holds because, for fixed $b$, the sum over $a \in S_i$ of the correlated inequalities "told $a$, do not switch to $b$" is the coarse inequality for $b$. Each inclusion can be strict: matching pennies has a mixed equilibrium and no pure one; in chicken, with (D, D) = (0, 0), (D, C) = (7, 2), (C, D) = (2, 7) and (C, C) = (6, 6), the uniform distribution on (D, C), (C, D) and (C, C) is a correlated equilibrium and not a product; and the rock-paper-scissors example below is a coarse correlated equilibrium that is not correlated.

**Regret form.** Let players play a repeated game for $T$ rounds, with profiles $s^1, \ldots, s^T$. The *external [regret](/regret/)* of player $i$ is $\max_{b} \sum_t u_i(b, s^t_{-i}) - \sum_t u_i(s^t)$. The empirical distribution, uniform on $s^1, \ldots, s^T$, is an $\varepsilon$-coarse correlated equilibrium, with each inequality allowed to fail by $\varepsilon$, if and only if every player's external regret is at most $\varepsilon T$. This identity is the [no-regret coarse correlated theorem](/no-regret-coarse-correlated-theorem/); a distribution that is a limit of such empirical distributions is what the alias "Hannan consistent" refers to.

## Examples and non-examples

Each table lists the payoff of the row player first.

**Rock-paper-scissors.** Let the winner get 1, the loser $-1$, and a tie 0, and let $p$ be uniform on the 6 profiles where the two players differ. Each player wins in 3 of them and loses in 3, so each gets 0. The marginal of each player is uniform, and every fixed strategy gets 0 against the uniform marginal, so no coarse inequality fails: $p$ is a coarse correlated equilibrium. It is not a correlated equilibrium. A player told Rock knows the other plays Paper or Scissors with probability $1/2$ each; Rock gets $(-1 + 1)/2 = 0$ and Scissors gets $(1 + 0)/2 = 1/2$. So the swap from Rock to Scissors gains $1/2$ given the recommendation, and $1/6$ overall. The only correlated equilibrium of this game is the uniform product.

**A strictly dominated strategy with positive weight.** Take

| | L | R |
| --- | --- | --- |
| T | 0, 0 | 3, 1 |
| M | 3, 0 | 0, 0 |
| B | 2, 1 | -1, 0 |

Row M strictly dominates row B, since $3 > 2$ and $0 > -1$. Let $p$ give $1/2$ to (B, L) and $1/2$ to (T, R). The row player gets $(2 + 3)/2 = 5/2$; against the column marginal $(1/2, 1/2)$, T and M get $3/2$ and B gets $1/2$. The column player gets $(1 + 1)/2 = 1$; against the row marginal, which is $1/2$ on T and $1/2$ on B, L and R both get $1/2$. So $p$ is a coarse correlated equilibrium that plays the dominated B with probability $1/2$. It is not a correlated equilibrium, because a row player told B gains $3 - 2 = 1$ by playing M. A fixed deviation to M would give up the good outcome (T, R), which is why the coarse inequalities hold.

**Two strategies per player.** When every $S_i$ has two elements $a$ and $b$, the coarse inequality for $b$ equals the correlated inequality for the pair $a, b$, because the terms with $s_i = b$ are 0. So in such games, chicken and the [prisoner's dilemma](/prisoners-dilemma/) among them, the coarse correlated equilibria are exactly the correlated equilibria. In the prisoner's dilemma the only one is (D, D).

**Two-player zero-sum games.** Let $v$ be the value of a zero-sum game in which the row player gets $u(s)$ and the column player $-u(s)$, let $p$ be a coarse correlated equilibrium, and let $x$ and $y$ be its row and column marginals. The row inequalities give $\mathbb{E}_p[u] \ge \max_a u(a, y) \ge v$, and the column inequalities give $\mathbb{E}_p[u] \le \min_c u(x, c) \le v$, by the [minimax theorem](/minimax-theorem/). So every coarse correlated equilibrium pays the value $v$, and both marginals are optimal strategies. This is why no-regret play solves zero-sum games ([no-regret zero-sum theorem](/no-regret-zero-sum-theorem/)).

## Related definitions

- **Learning.** If every player runs an algorithm with external regret $o(T)$, such as [multiplicative weights](/multiplicative-weights-update/), the empirical distribution of play converges to the set of coarse correlated equilibria; with payoffs in $[0, 1]$ and $k$ strategies each, $O(\log k/\varepsilon^2)$ rounds of multiplicative weights give an $\varepsilon$-coarse correlated equilibrium ([no-regret dynamics](/no-regret-dynamics/)). The play itself need not converge to anything.
- **Price of anarchy.** A price of anarchy bound proved by the [smoothness framework](/smoothness-framework/) holds for coarse correlated equilibria, and so for the average welfare of no-regret players, not only for Nash equilibria.
- **Correlated equilibrium.** The finer notion, with one inequality per pair of strategies and a decision after the recommendation ([correlated equilibrium](/correlated-equilibrium/)); swap regret plays the role of external regret.
- **Hannan's procedure.** Hannan (1957) gave the first strategy for repeated play whose average payoff approaches that of the best fixed strategy in hindsight; its joint play reaches the coarse correlated equilibria.

## References
