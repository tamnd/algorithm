---
tag: FJGSGJ
kind: algorithm
slug: regret-matching
name: Regret matching
aliases:
- Hart-Mas-Colell regret matching
area: algorithmic-game-theory/computing-equilibria
level: core
summary: Switches from the last action to each other action with probability proportional to its positive conditional regret. The empirical play converges to the correlated equilibria.
model: real-ram
complexity:
  vars: {n: the number of players, k: the largest number of pure strategies of a player, T: the number of rounds}
  time: {worst: O(n k T)}
  space: {extra: "O(n k^2)"}
properties: {deterministic: false, exact: false, online: true, recursive: false}
history:
  year: 2000
  people: [Sergiu Hart, Andreu Mas-Colell]
  note: "Hart and Mas-Colell defined the conditional procedure and proved that its empirical distribution converges almost surely to the set of correlated equilibria; their unconditional version gives Hannan's no external regret property."
prereqs: [correlated-equilibrium, regret]
see_also: [no-regret-dynamics, counterfactual-regret-minimization, blum-mansour-reduction, blackwell-approachability, coarse-correlated-equilibrium, multiplicative-weights-update, correlated-equilibrium-linear-program, no-regret-coarse-correlated-theorem]
sources:
  - paper: doi:10.1111/1468-0262.00153
    title: "Sergiu Hart and Andreu Mas-Colell, A simple adaptive procedure leading to correlated equilibrium, Econometrica 68(5) (2000), 1127-1150"
    locator: "Section 2, the procedure (2.2) with the inertia condition of footnote 5 and the Main Theorem (proof in Appendix 1); Section 3, the Proposition linking regrets and correlated epsilon-equilibria; Section 4(c), the unconditional procedure (4.2) and Theorem B; Section 4(d), the procedure (2.2) is not universally calibrated"
  - paper: doi:10.2140/pjm.1956.6.1
    title: "David Blackwell, An analog of the minimax theorem for vector payoffs, Pacific Journal of Mathematics 6(1) (1956), 1-8"
    locator: the approachability theorem that Hart and Mas-Colell use in Section 3
  - book: isbn:9780521841085
    title: "Nicolo Cesa-Bianchi and Gabor Lugosi, Prediction, Learning, and Games, Cambridge University Press, 2006"
    locator: "Chapter 2 (the polynomially weighted average forecaster, of which unconditional regret matching is the quadratic case) and Chapter 7 (internal regret and correlated equilibria)"
  - book: isbn:9781316624791
    title: "Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016"
    locator: Lecture 18 (swap regret and correlated equilibria)
---

Regret matching is a learning rule for a repeated finite game. A player who played $j$ in the last round switches to another strategy $l$ with probability proportional to the positive part of the *conditional regret* $D(j, l)$: how much more the player would have earned so far by playing $l$ in every round in which it played $j$. Hart and Mas-Colell (2000) proved that if every player uses it, the empirical distribution of play converges almost surely to the set of [correlated equilibria](/correlated-equilibrium/). The rule is simpler than the [Blum-Mansour reduction](/blum-mansour-reduction/), which reaches the same set through no swap regret with a stationary distribution in each round. Its unconditional version, which plays each action with probability proportional to its positive external [regret](/regret/), only reaches [coarse correlated equilibria](/coarse-correlated-equilibrium/); it is the learner inside [counterfactual regret minimization](/counterfactual-regret-minimization/). The general scheme behind both is [no-regret dynamics](/no-regret-dynamics/), and the proof uses [Blackwell approachability](/blackwell-approachability/).

## In plain words

A game is played again and again. After each round, a player looks back at the rounds in which it made its last choice. For every other choice, it asks: had I made that other choice in all those rounds, how much more would I have earned? These amounts are regrets. The player then switches to another choice with a chance that grows with its regret, and stays with the last choice otherwise. Choices that would not have helped get no chance. A fixed constant keeps the total chance of switching below one. When everybody plays this way, the record of how often each combination of choices appeared settles into a pattern that a mediator could recommend and nobody would want to disobey.

## The problem

The input is a finite game with players $N = \{1, \ldots, n\}$, pure strategy sets $S_i$ with $k_i = |S_i| \le k$, and utilities $u_i : S \to \mathbb{Q}$, maximized. Let $\Delta_i = \max_s u_i(s) - \min_s u_i(s)$ be the payoff range of player $i$. The game is played for $T$ rounds; $s^t \in S$ is the profile of round $t$. The empirical distribution is $z_T(s) = |\{t \le T : s^t = s\}| / T$.

For player $i$ and strategies $j \ne l$ in $S_i$, the cumulative conditional regret after round $t$ is

$$D^t_i(j, l) = \sum_{\tau \le t,\ s^\tau_i = j} \big[u_i(l, s^\tau_{-i}) - u_i(s^\tau)\big].$$

A distribution $z$ on $S$ is a correlated $\varepsilon$-equilibrium if $\sum_{s : s_i = j} z(s)\,[u_i(l, s_{-i}) - u_i(s)] \le \varepsilon$ for all $i$ and $j \ne l$. The goal is a sequence of play whose empirical distribution $z_T$ is a correlated $\varepsilon_T$-equilibrium with $\varepsilon_T \to 0$. Each player sees the past profiles and knows its own utility; it does not need the utilities of the others.

## The algorithm

Each player $i$ uses an inertia constant $\mu > (k_i - 1)\Delta_i$; one $\mu$ above all these bounds serves every player.

```pseudo id=main
REGRET-MATCHING(G, mu, T)       ▷ every player i uses the same rule
L1  D_i(j, l) ← 0 for every player i and every pair j ≠ l in S_i
L2  draw s^1, each s^1_i uniform in S_i
L3  for t = 1, 2, ..., T
L4      for each player i
L5          j ← s^t_i                                   ▷ the strategy just played
L6          for each l ≠ j: D_i(j, l) ← D_i(j, l) + u_i(l, s^t_-i) - u_i(s^t)
L7          for each l ≠ j: p_i(l) ← max(D_i(j, l), 0) / (t mu)
L8          p_i(j) ← 1 - Σ_{l ≠ j} p_i(l)              ▷ inertia: stay with j
L9      draw s^{t+1}, each s^{t+1}_i from p_i, independently
L10 return z_T, the uniform distribution on s^1, ..., s^T, and D
```

Line L6 updates only the row $j$ of the regret matrix of player $i$, the row of the strategy just played, so after round $t$ the entry $D_i(j, l)$ equals $D^t_i(j, l)$. Line L7 is the switching probability $R_t(j, l) / \mu$ of Hart and Mas-Colell, where $R_t = \max(D^t / t, 0)$ is the average positive regret. Each $D^t_i(j, l)/t$ is at most $\Delta_i$, so the sum in line L8 is at most $(k_i - 1)\Delta_i / \mu < 1$, and $p_i$ is a probability distribution with $p_i(j) > 0$. The constant $\mu$ is what makes the rule conditional: the probability of $j$ is not a regret but the remainder, so a player with small regrets mostly repeats itself.

The unconditional version keeps one cumulative external regret $R_i(l) = \sum_{\tau \le t} [u_i(l, s^\tau_{-i}) - u_i(s^\tau)]$ per strategy and plays $p_i(l) = R_i(l)^+ / \sum_{l'} R_i(l')^+$, or any distribution when all regrets are at most 0. It needs no $\mu$ and does not depend on the last strategy.

## Example

Take chicken with strategies D (dare) and C (chicken) and payoffs (D, D) = (0, 0), (D, C) = (7, 2), (C, D) = (2, 7) and (C, C) = (6, 6). Here $k_i = 2$ and $\Delta_i = 7$, so $\mu = 8$ works. Suppose the first profile is (C, C) and the first draw sends the row player to D.

| $t$ | $s^t$ | $D_1(\text{C}, \text{D})$ | $D_1(\text{D}, \text{C})$ | $D_2(\text{C}, \text{D})$ | row player at $t + 1$ | column player at $t + 1$ |
|---|---|---|---|---|---|---|
| 1 | (C, C) | 7 - 6 = 1 | 0 | 1 | D with prob. 1/8 (drawn) | D with prob. 1/8 (not drawn) |
| 2 | (D, C) | 1 | 6 - 7 = -1 | 1 + (0 - 2) = -1 | C with prob. 0 | D with prob. 0 |
| 3 | (D, C) | 1 | -2 | -3 | C with prob. 0 | D with prob. 0 |
| 4 | (D, C) | 1 | -3 | -5 | C with prob. 0 | D with prob. 0 |

From round 2 on, both regrets of the strategies being played are negative, so nobody switches, and (D, C), a pure Nash equilibrium, repeats for ever. After $T$ rounds, $z_T$ puts $1/T$ on (C, C) and $(T - 1)/T$ on (D, C). The only positive regret is $D_1(\text{C}, \text{D}) = 1$, and indeed $z_T$ is a correlated $\varepsilon$-equilibrium exactly for $\varepsilon \ge 1/T$: the row player, told C, gains $z_T(\text{C}, \text{C}) \cdot (7 - 6) = 1/T$ by playing D. Other draws give longer runs, and in general the limit points of $z_T$ need not be products. The uniform distribution on (D, C), (C, D) and (C, C), with payoff 5 each, is a correlated equilibrium of this game that no product distribution gives.

## Correctness

The proof has an exact part and a probabilistic part.

The exact part is an identity. For every $i$ and $j \ne l$,

$$\sum_{s : s_i = j} z_T(s)\,\big[u_i(l, s_{-i}) - u_i(s)\big] = \frac{D^T_i(j, l)}{T},$$

because both sides add the same terms, one for each round $t$ with $s^t_i = j$, divided by $T$. So $z_T$ is a correlated $\varepsilon$-equilibrium if and only if $\max_{i, j, l} D^T_i(j, l) \le \varepsilon T$, and the algorithm knows its own exact error. The same identity with the external regrets says that the empirical distribution is a coarse correlated $\varepsilon$-equilibrium if and only if every external regret is at most $\varepsilon T$.

The probabilistic part is the theorem of Hart and Mas-Colell: if every player uses lines L5 to L9 with $\mu > (k_i - 1)\Delta_i$, then $\max(D^T_i(j, l), 0)/T \to 0$ almost surely for all $i$, $j$ and $l$, so $z_T$ converges almost surely to the set of correlated equilibria. Their proof follows the squared distance of the average regret vector to the negative orthant and shows that it falls in expectation, with an extra argument for the inertia. For the unconditional version there is a short deterministic bound, proved in the proof file: if the regret is updated with the expected payoff of $p_i$, then the external regret after $t$ rounds is at most $\Delta_i \sqrt{k_i t}$ against any opponents. The proof file has the identity, the bound and the well-definedness of line L8.

## Complexity

In each round, line L6 costs $k_i - 1$ payoff lookups and additions for player $i$, lines L7 and L8 cost $O(k_i)$, and line L9 costs $O(k_i)$ to draw. So a round costs $O(n k)$ and $T$ rounds cost $O(n k T)$, plus the cost of recording the profiles. The regret matrices take $O(n k^2)$ space; the empirical distribution takes space for its support, at most $\min(T, |S|)$ profiles.

The speed is slow. For their stationary-distribution variant, Hart and Mas-Colell note that the expected regrets are of order $1/\sqrt{t}$, so an $\varepsilon$-equilibrium takes on the order of $1/\varepsilon^2$ rounds, with constants that depend on $k$ and the payoffs, and no procedure can do better in general when the others play fixed mixed strategies. In the unconditional version, the bound $\Delta \sqrt{k T}$ gives an $\varepsilon$-coarse correlated equilibrium, for payoffs in $[0, 1]$, after $T = k / \varepsilon^2$ rounds; [multiplicative weights](/multiplicative-weights-update/) needs only $O(\log k / \varepsilon^2)$ rounds, but regret matching has no step size to tune.

## Properties

- **Uncoupled and simple.** A player needs only its own payoffs and the past play; there is no step size and no stationary distribution to compute.
- **Not universal.** The conditional rule (lines L5 to L9) does not guarantee small regrets against arbitrary opponents; Hart and Mas-Colell give adversaries that keep its regrets positive. The guarantee needs all players to use it. The unconditional version and the stationary-distribution variant are universal.
- **Time averages, not play.** Only the empirical distribution converges, and it converges to a set, not to a point. In the example it settles on a pure Nash equilibrium, but in general it can keep moving inside the set of correlated equilibria.
- **Zero probability for bad replies.** A strategy with no positive regret gets probability 0, unlike smooth fictitious play, which plays every strategy with positive probability.

## Variants and improvements

- **Unconditional regret matching.** Probabilities proportional to the positive external regrets give no external regret (Hart and Mas-Colell, Theorem B), so the empirical distribution converges to the coarse correlated equilibria, a larger set. With expected payoffs the bound is deterministic.
- **Regret matching plus.** Clip the cumulative regrets at 0 after each round, and average the strategies with weights that grow with $t$. This variant, used in counterfactual regret minimization for poker, converges much faster in practice in zero-sum games.
- **Stationary-distribution version.** Play the invariant distribution of the matrix of positive regrets (Hart and Mas-Colell, Theorem A). It has no swap regret against any opponents, like the Blum-Mansour reduction.
- **Counterfactual regret minimization.** In an extensive-form game, run unconditional regret matching at every information set, on counterfactual values; in two-player zero-sum games the average strategies converge to a Nash equilibrium.

## When to use it

Use it when players should learn a correlated equilibrium with no knowledge of the others' payoffs and no step size, or as a simple model of adaptive behavior. To compute a correlated equilibrium of a game given in normal form, the [linear program](/correlated-equilibrium-linear-program/) is exact and faster. For guarantees against arbitrary opponents, use the unconditional version (for external regret) or the Blum-Mansour reduction (for swap regret). In large zero-sum games, use regret matching plus inside counterfactual regret minimization.

## Pitfalls

- **A too small inertia.** With $\mu \le (k_i - 1)\Delta_i$ in line L7, the sum in line L8 can exceed 1, and $p_i(j)$ becomes negative. Choose $\mu$ above the bound.
- **Dividing by the wrong count.** Line L7 divides by $t$, the number of rounds, not by the number of rounds in which $j$ was played; with the latter the procedure is a different one, and the theorem does not cover it.
- **Updating the wrong row.** Line L6 changes only the row of the strategy just played. Adding the round to every row turns every row into the external regrets, the theorem no longer applies, and small external regrets certify only a coarse correlated equilibrium.
- **Expecting the play to converge.** The mixed strategies of line L8 can cycle for ever; only the empirical distribution of line L10 approaches the set of correlated equilibria.
- **Using it alone against an adversary.** The conditional rule has no guarantee for one player against arbitrary opponents (Section 4(d) of Hart and Mas-Colell).

## Implementations

The Python code runs lines L1 to L10 for all players with exact rational regrets, so the correlated equilibrium gap of the empirical distribution is exact. It also has a class for the unconditional version in floating point, and a deterministic self-play with expected payoffs. The tests check the exact identity between the regrets and the correlated equilibrium inequalities of $z_T$ on random games, the trace of the example, convergence on chicken and on the prisoner's dilemma with fixed seeds, the bound $\Delta \sqrt{k t}$ against random adversaries at every round, and the coarse correlated equilibrium inequalities of the averaged self-play.

## History

Hannan (1957) and Blackwell (1956) gave the first procedures with no external regret. Foster and Vohra (1997) showed that players who best-respond to calibrated forecasts reach correlated equilibria. Hart and Mas-Colell (2000) found the simple regret matching rule, proved its convergence to correlated equilibria with Blackwell's approachability theorem as a guide, and gave the unconditional version. Zinkevich and coauthors (2007) used unconditional regret matching at each information set in counterfactual regret minimization, which became the basis of poker programs.

## References
