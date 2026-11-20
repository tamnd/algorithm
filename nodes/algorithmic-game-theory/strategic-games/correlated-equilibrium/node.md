---
tag: GK1DHP
kind: definition
slug: correlated-equilibrium
name: Correlated equilibrium
aliases:
- Aumann correlated equilibrium
area: algorithmic-game-theory/strategic-games
level: core
summary: A distribution over action profiles such that no player, told only their own recommended action, gains by deviating from it.
prereqs: [mixed-strategy, nash-equilibrium, best-response]
see_also: [nash-equilibrium, coarse-correlated-equilibrium, correlated-equilibrium-linear-program, ellipsoid-against-hope, blum-mansour-reduction, regret-matching, no-regret-dynamics, pure-nash-equilibrium]
sources:
  - paper: doi:10.1016/0304-4068(74)90037-8
    title: "Robert J. Aumann, Subjectivity and correlation in randomized strategies, Journal of Mathematical Economics 1(1) (1974), 67-96"
    locator: the definition of correlated equilibrium and the examples in which it gives more than every Nash equilibrium
  - paper: "Robert J. Aumann, Correlated equilibrium as an expression of Bayesian rationality, Econometrica 55(1) (1987), 1-18"
    title: Correlated equilibrium as an expression of Bayesian rationality
    locator: correlated equilibrium as the outcome of common knowledge of rationality with a common prior
  - paper: "Sergiu Hart and David Schmeidler, Existence of correlated equilibria, Mathematics of Operations Research 14(1) (1989), 18-25"
    title: Existence of correlated equilibria
    locator: the existence proof by linear programming duality, without a fixed point theorem
  - paper: "Itzhak Gilboa and Eitan Zemel, Nash and correlated equilibria, some complexity considerations, Games and Economic Behavior 1(1) (1989), 80-93"
    title: "Nash and correlated equilibria: some complexity considerations"
    locator: NP-hardness of decision questions about Nash equilibria and polynomial time for the same questions about correlated equilibria
  - paper: "Christos H. Papadimitriou and Tim Roughgarden, Computing correlated equilibria in multi-player games, Journal of the ACM 55(3) (2008), article 14"
    title: Computing correlated equilibria in multi-player games
    locator: the polynomial algorithm for succinct games with the polynomial expectation property
  - paper: "Sergiu Hart and Andreu Mas-Colell, A simple adaptive procedure leading to correlated equilibrium, Econometrica 68(5) (2000), 1127-1150"
    title: A simple adaptive procedure leading to correlated equilibrium
    locator: regret matching, whose empirical distribution of play converges to the set of correlated equilibria
---

A correlated equilibrium is a probability distribution over the profiles of a game such that, if a mediator draws a profile and tells each player only their own part of it, no player can gain by playing something other than the recommendation. Robert Aumann defined it in 1974. Every [Nash equilibrium](/nash-equilibrium/) is a correlated equilibrium, but the set of correlated equilibria is a polytope given by linear inequalities, so it is easy to compute, and it can contain outcomes that are better for all players than every Nash equilibrium.

## Definition

Let $G = (N, (S_i), (u_i))$ be a finite [normal-form game](/normal-form-game/) whose players maximize, and let $S = S_1 \times \cdots \times S_n$. A distribution $p$ on $S$ is a *correlated equilibrium* if, for every player $i$ and every pair $a, b \in S_i$,

$$\sum_{s \in S:\ s_i = a} p(s)\, \big(u_i(s) - u_i(b, s_{-i})\big) \ge 0.$$

The inequality says: a player told to play $a$ does not gain by playing $b$ instead. When $p$ gives positive probability to $a$, divide by that probability; then the left side is the expected gain of following the recommendation, under the conditional distribution of $s_{-i}$ given $s_i = a$. So the condition is that every recommendation with positive probability is a [best response](/best-response/) to the conditional distribution of the others' play.

**Swap form.** Equivalently, for every player $i$ and every map $\varphi: S_i \to S_i$, $\mathbb{E}_{s \sim p}[u_i(s)] \ge \mathbb{E}_{s \sim p}[u_i(\varphi(s_i), s_{-i})]$. Taking $\varphi$ that sends $a$ to $b$ and fixes the rest gives the pairwise inequality; summing pairwise inequalities over $a$ gives any $\varphi$. This is the form that swap regret measures.

**A polytope.** The conditions are $\sum_i |S_i|(|S_i| - 1)$ linear inequalities in the $|S|$ unknowns $p(s)$, together with $p \ge 0$ and $\sum_s p(s) = 1$. So the set of correlated equilibria is a convex polytope, and a correlated equilibrium that maximizes any linear function, such as the sum of the payoffs, is found by a [linear program](/correlated-equilibrium-linear-program/) of size polynomial in the size of the payoff table.

**The best-response support fact.** For a product distribution $p(s) = \prod_i \sigma_i(s_i)$, the conditional distribution of $s_{-i}$ given $s_i = a$ is $\sigma_{-i}$ whatever $a$ is. So $p$ is a correlated equilibrium if and only if every $a$ in the support of $\sigma_i$ is a best response to $\sigma_{-i}$. A mixed strategy is a best response if and only if its support is inside the set of pure best responses, so this holds if and only if $\sigma$ is a Nash equilibrium. The product correlated equilibria are exactly the mixed Nash equilibria.

**The hierarchy.** Identify a pure profile with the point mass on it and a mixed profile with its product distribution. Then

$$\text{pure Nash} \subseteq \text{mixed Nash} \subseteq \text{correlated equilibria} \subseteq \text{coarse correlated equilibria}.$$

The second inclusion is the support fact above. The third holds because, for a fixed $b$, summing the inequality over all $a \in S_i$ gives $\mathbb{E}_p[u_i(s)] \ge \mathbb{E}_p[u_i(b, s_{-i})]$, which is the condition of a [coarse correlated equilibrium](/coarse-correlated-equilibrium/). Each inclusion can be strict: matching pennies has a mixed equilibrium and no pure one; the chicken example below is a correlated equilibrium that is not a product; and the rock-paper-scissors example below is a coarse correlated equilibrium that is not a correlated one. Since a Nash equilibrium exists ([Nash's theorem](/nash-existence-theorem/)), so does a correlated equilibrium; Hart and Schmeidler (1989) gave a direct proof by linear programming duality, with no fixed point theorem.

## Examples and non-examples

Each table lists the payoff of the row player first.

**Chicken.** Each driver can dare (D) or chicken out (C).

| | D | C |
| --- | --- | --- |
| D | 0, 0 | 7, 2 |
| C | 2, 7 | 6, 6 |

The Nash equilibria are (D, C) and (C, D), with payoff sums 9, and the mixed equilibrium in which each player plays C with probability $2/3$, which gives each player $14/3$ and a sum of $28/3$.

- *The traffic light.* Let $p$ be uniform on (D, C), (C, D) and (C, C). A row player told D knows the column player plays C, and D gets $7 > 6$. A row player told C knows the column player plays D or C with probability $1/2$ each; C gets $(2 + 6)/2 = 4$ and D gets $(0 + 7)/2 = 7/2$. The column player is symmetric. So $p$ is a correlated equilibrium, with payoff 5 to each player, which is more than the $14/3$ of the symmetric Nash equilibrium. It is not a product distribution: it gives probability 0 to (D, D) but positive probability to (D, C) and (C, D).
- *The best for the sum.* Let $p$ give $1/4$ to (D, C), $1/4$ to (C, D) and $1/2$ to (C, C). A row player told C sees D with probability $1/3$ and C with $2/3$; C gets $2/3 + 4 = 14/3$ and D gets $14/3$, so the constraint is tight. A row player told D again gets $7 > 6$. Each player gets $7/4 + 2/4 + 3 = 21/4$, a sum of $21/2$. Enumerating the vertices of the polytope shows that this is the largest sum of any correlated equilibrium, and it is larger than the sum $28/3$ of the best Nash equilibrium.

**Prisoner's dilemma.** Defection is strictly dominant, so (D, D) is the only correlated equilibrium ([prisoner's dilemma](/prisoners-dilemma/)). In general, a strategy $a$ that is strictly dominated by a pure strategy $b$ has probability 0 in every correlated equilibrium, because the inequality for $a$ and $b$ fails as soon as $a$ has positive probability.

**Non-example: rock-paper-scissors.** Let the winner get 1, the loser $-1$, and a tie 0, and let $p$ be uniform on the 6 profiles where the players differ. A player told Rock knows the other plays Paper or Scissors with probability $1/2$ each. Rock gets $(-1 + 1)/2 = 0$, but Scissors gets $(1 + 0)/2 = 1/2$, so the swap from Rock to Scissors gains $1/2$ given the recommendation, and $1/6$ overall. So $p$ is not a correlated equilibrium. It is a coarse correlated equilibrium: every fixed strategy gets 0 against the uniform marginal of the other player, which equals the payoff 0 of $p$. The only correlated equilibrium of the game is the uniform product, the unique Nash equilibrium.

**Public and private signals.** Mixing two Nash equilibria with a public coin, as $1/2$ on (D, C) and $1/2$ on (C, D) in chicken, gives a correlated equilibrium, and every convex combination of Nash equilibria is one. The traffic light above is not of this form, since it puts weight on (C, C), which is not a Nash equilibrium; the private part of the signal is what lets correlated equilibria leave the convex hull of the Nash equilibria.

## Related definitions

- **Coarse correlated equilibrium.** Compare only with fixed deviations chosen before the draw ([coarse correlated equilibrium](/coarse-correlated-equilibrium/)). When every player has two strategies the two sets are equal: for $S_i = \{a, b\}$, the coarse inequality for the deviation $b$ is the correlated inequality for $a$ and $b$, because the terms with $s_i = b$ are 0.
- **Computation.** For a game given by its payoff table, a correlated equilibrium, and one that maximizes the welfare, is found in polynomial time by linear programming ([correlated equilibrium linear program](/correlated-equilibrium-linear-program/)); Gilboa and Zemel (1989) showed that questions such as "is there an equilibrium with payoff at least $k$" are NP-hard for Nash equilibria and polynomial for correlated equilibria. For succinct games with many players, where the table is too large, Papadimitriou and Roughgarden (2008) found a correlated equilibrium in polynomial time by the [ellipsoid against hope](/ellipsoid-against-hope/) method.
- **Learning.** If every player uses an algorithm with swap regret $o(T)$, the empirical distribution of play over $T$ rounds converges to the set of correlated equilibria. Regret matching (Hart and Mas-Colell 2000, [regret matching](/regret-matching/)) is one such procedure, and the [Blum-Mansour reduction](/blum-mansour-reduction/) turns any no-external-regret algorithm into a no-swap-regret one ([no-regret dynamics](/no-regret-dynamics/)).
- **Bayesian view.** Aumann (1987) showed that a correlated equilibrium is the outcome when players are Bayesian rational with a common prior about the state of the world, which makes it a natural solution concept and not only a relaxation.
- **Approximate version.** An $\varepsilon$-correlated equilibrium allows each inequality to fail by $\varepsilon$ ([epsilon-Nash equilibrium](/epsilon-nash-equilibrium/) is the same relaxation of the Nash conditions).

## References
