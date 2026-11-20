---
tag: XW8JM5
kind: definition
slug: pure-nash-equilibrium
name: Pure Nash equilibrium
aliases:
- pure-strategy Nash equilibrium
- PNE
area: algorithmic-game-theory/strategic-games
level: intro
summary: A profile of pure strategies, one per player, in which no player can raise their payoff by switching alone to another pure strategy.
prereqs: [normal-form-game, best-response, nash-equilibrium]
see_also: [nash-equilibrium, correlated-equilibrium, coarse-correlated-equilibrium, potential-game, best-response-dynamics, pls-completeness-of-congestion-games, subgame-perfect-equilibrium, dominant-strategy]
sources:
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994
    locator: Chapter 2 (Nash equilibrium of a strategic game, in pure actions, with the standard examples)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 3 (pure-strategy Nash equilibria and examples)
  - url: https://timroughgarden.org/f13/l/l13.pdf
    title: "Tim Roughgarden, CS364A Algorithmic Game Theory, Lecture 13, Potential games and a hierarchy of equilibria, Stanford University, November 2013 (revised as Lecture 13 of Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016)"
    locator: the definitions of pure Nash, mixed Nash, correlated and coarse correlated equilibria and the inclusions among them
  - paper: "Melvin Dresher, Probability of a pure equilibrium point in n-person games, Journal of Combinatorial Theory 8(1) (1970), 134-145"
    title: Probability of a pure equilibrium point in n-person games
    locator: the probability that a random game has a pure equilibrium, and its limit 1 - 1/e
  - paper: "Robert W. Rosenthal, A class of games possessing pure-strategy Nash equilibria, International Journal of Game Theory 2 (1973), 65-67"
    title: A class of games possessing pure-strategy Nash equilibria
    locator: congestion games and their potential function
---

A pure Nash equilibrium is a profile in which each player chooses one strategy with certainty and no player can gain by switching alone to another strategy. It is the special case of a [Nash equilibrium](/nash-equilibrium/) in which nobody randomizes, and it is the smallest of the four standard equilibrium sets: pure Nash, mixed Nash, [correlated](/correlated-equilibrium/) and [coarse correlated](/coarse-correlated-equilibrium/) equilibria. Unlike a mixed equilibrium, a pure one need not exist, as matching pennies shows.

## Definition

Let $G = (N, (S_i), (u_i))$ be a [normal-form game](/normal-form-game/) whose players maximize their payoffs. A profile $s = (s_1, \ldots, s_n) \in S$ is a *pure Nash equilibrium* if

$$u_i(s) \ge u_i(s_i', s_{-i}) \quad \text{for every player } i \in N \text{ and every } s_i' \in S_i.$$

Equivalently, every $s_i$ is a pure [best response](/best-response/) to $s_{-i}$: $s_i \in \mathrm{BR}_i(s_{-i})$. The equilibrium is *strict* if every inequality with $s_i' \ne s_i$ is strict, that is, each $s_i$ is the unique best response.

**Checking pure deviations is enough.** No mixed deviation can do better either: $u_i(\sigma_i', s_{-i}) = \sum_{t} \sigma_i'(t)\, u_i(t, s_{-i})$ is an average of pure payoffs, so it is at most the largest of them. In general, a mixed strategy is a best response if and only if its support is inside the set of pure best responses. So a pure Nash equilibrium is a mixed Nash equilibrium in which every $\sigma_i$ puts probability 1 on $s_i$.

**Checking cost.** Testing one profile takes $\sum_i |S_i|$ payoff lookups. A game with $n$ players and $k$ strategies each, given as a table, has $k^n$ profiles; testing all of them takes $O(n k \cdot k^n)$ lookups, which is polynomial in the size $n k^n$ of the table. So finding all pure equilibria of a game in normal form is easy; the hard cases are succinct games, whose input is much smaller than the table.

**The hierarchy.** Identify a pure profile $s$ with the distribution on $S$ that puts probability 1 on $s$, and a mixed profile with the product distribution it defines. Then

$$\text{pure Nash} \subseteq \text{mixed Nash} \subseteq \text{correlated equilibria} \subseteq \text{coarse correlated equilibria},$$

and each inclusion can be strict:

- *Matching pennies* has a mixed equilibrium, both players uniform, but no pure one.
- In *chicken*, with (D, D) = (0, 0), (D, C) = (7, 2), (C, D) = (2, 7) and (C, C) = (6, 6), the uniform distribution on (D, C), (C, D) and (C, C) is a correlated equilibrium with payoff 5 to each player. It is not a product of two mixed strategies, since it gives probability 0 to (D, D) and positive probability to both (D, C) and (C, D).
- In *rock-paper-scissors*, the uniform distribution on the 6 profiles where the two players differ is a coarse correlated equilibrium: against the uniform marginal of the other player, every fixed strategy gets 0, the payoff of the distribution. It is not a correlated equilibrium: a player told Rock knows that the other plays Paper or Scissors with probability $1/2$ each, and Scissors would get $1/2$ instead of 0.

Each larger set is easier to compute: for an explicit game, a pure equilibrium may not exist, finding a mixed one is PPAD-complete already for two players, and correlated and coarse correlated equilibria are solutions of linear programs.

## Examples and non-examples

Each table lists the payoff of the row player first.

**Prisoner's dilemma.** With (C, C) = (3, 3), (C, D) = (0, 5), (D, C) = (5, 0) and (D, D) = (1, 1), the only pure equilibrium is (D, D). It is strict: each player loses 1 by switching to C. At (C, C), each player gains 2 by switching to D.

**Battle of the sexes.**

| | O | F |
| --- | --- | --- |
| O | 2, 1 | 0, 0 |
| F | 0, 0 | 1, 2 |

(O, O) and (F, F) are strict pure equilibria; at (O, F) and (F, O) both players get 0 and each gains by a switch. The game also has a mixed equilibrium, with payoff $2/3$ to each player, which is not pure.

**Matching pennies.** In each of the four profiles, the player who loses gains 2 by switching, so there is no pure equilibrium. [Nash's theorem](/nash-existence-theorem/) needs mixed strategies.

**An equilibrium with a weakly dominated strategy.** In the normal form of the entry game, Out gives $(0, 2)$ against both Fight and Accommodate, In gives $(-1, -1)$ against Fight and $(1, 1)$ against Accommodate. Both (In, Accommodate) and (Out, Fight) are pure equilibria. The second one is not strict, because the column player gets 2 with either column, and it uses Fight, which Accommodate weakly dominates. It is not [subgame perfect](/subgame-perfect-equilibrium/).

**Non-example: one player at a best response.** In chicken, at (D, D) both players get 0, and each would gain 2 by chickening out. At (C, C) each gets 6 and would gain 1 by daring. Neither profile is an equilibrium; the pure equilibria are (D, C) and (C, D).

## Related definitions

- **Classes with pure equilibria.** Games with a [dominant strategy](/dominant-strategy/) for every player; finite [potential games](/potential-game/), where every sequence of strict improvements ends at a pure equilibrium ([finite improvement property](/finite-improvement-property/)); [atomic congestion games](/atomic-congestion-game/), which are potential games (Rosenthal 1973, [Rosenthal's theorem](/rosenthal-potential-theorem/)); and finite games of [perfect information](/perfect-information-game/), by backward induction.
- **Complexity in succinct games.** In congestion games a pure equilibrium always exists, but finding one is PLS-complete ([PLS-completeness of congestion games](/pls-completeness-of-congestion-games/)), and [best-response dynamics](/best-response-dynamics/) can take exponentially many steps.
- **Random games.** If all payoffs are drawn independently from a continuous distribution, each profile is a pure equilibrium with probability $k^{-n}$ in a game with $n$ players and $k$ strategies each, so the expected number of pure equilibria is $k^n \cdot k^{-n} = 1$. The probability that at least one exists tends to $1 - 1/e \approx 0.632$ as the numbers of strategies grow (Dresher 1970, after a two-player result of Goldberg, Goldman and Newman in 1968).
- **Mixed Nash equilibrium.** The general case, which always exists in finite games ([Nash equilibrium](/nash-equilibrium/)).
- **Approximate pure equilibria.** A pure profile where no player gains more than $\varepsilon$ ([epsilon-Nash equilibrium](/epsilon-nash-equilibrium/)).

## References
